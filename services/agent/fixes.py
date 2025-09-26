"""
AI Agent Production Fixes
Addresses: DB timeouts, HTTP leaks, queue backpressure, JSON errors, circuit breaker, logging
"""

import asyncio
import json
import logging
import time
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any

import aiohttp
import psycopg2
from psycopg2 import pool


class CircuitBreaker:
    """Simple circuit breaker for external service calls"""
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e


class DatabaseManager:
    """Database connection manager with pooling and retry logic"""
    def __init__(self):
        self.pool = None
        self.max_retries = 3
        self.retry_delay = 1

    def init_pool(self, database_url: str):
        try:
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                1, 10,  # min=1, max=10
                database_url,
                connect_timeout=10
            )
            logging.info("Database pool initialized")
        except Exception as e:
            logging.error(f"Failed to init DB pool: {e}")

    @asynccontextmanager
    async def get_connection(self):
        if not self.pool:
            raise Exception("Database pool not initialized")
        
        conn = None
        for attempt in range(self.max_retries):
            try:
                conn = self.pool.getconn()
                yield conn
                return
            except psycopg2.OperationalError:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                raise
            finally:
                if conn:
                    self.pool.putconn(conn)


class HTTPSessionManager:
    """Manages HTTP sessions to prevent leaks"""
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


class TaskQueue:
    """Async task queue with backpressure handling"""
    def __init__(self, max_size=100):
        self.queue = asyncio.Queue(maxsize=max_size)
        self.workers = []
        self.running = False

    async def put(self, task):
        try:
            self.queue.put_nowait(task)
        except asyncio.QueueFull:
            logging.warning("Task queue full, dropping task")
            raise Exception("Queue full")

    async def start_workers(self, num_workers=3):
        self.running = True
        for i in range(num_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)

    async def _worker(self, name):
        while self.running:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                await task()
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logging.error(f"Worker {name} error: {e}")

    async def stop(self):
        self.running = False
        for worker in self.workers:
            worker.cancel()


def safe_json_parse(data: str) -> Dict[Any, Any]:
    """Safe JSON parsing with error handling"""
    try:
        if not data or not data.strip():
            return {}
        return json.loads(data)
    except json.JSONDecodeError as e:
        logging.warning(f"JSON decode error: {e}, data: {data[:100]}...")
        return {}


def setup_production_logging():
    """Configure production-appropriate logging"""
    logging.basicConfig(
        level=logging.INFO,  # Changed from DEBUG
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("agent.log", mode="a")
        ]
    )
    
    # Reduce verbosity for specific loggers
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


# Global instances
db_manager = DatabaseManager()
http_manager = HTTPSessionManager()
task_queue = TaskQueue()
circuit_breaker = CircuitBreaker()