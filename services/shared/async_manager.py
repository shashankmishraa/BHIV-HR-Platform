"""
Production-Grade Async Processing Manager
Handles async operations, connection pooling, and resource management
"""

import asyncio
import logging
import time
import weakref
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional, List, Callable
import threading
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

try:
    import aiohttp
    import aiofiles
except ImportError:
    aiohttp = None
    aiofiles = None

try:
    import asyncpg
    import psycopg2.pool
except ImportError:
    asyncpg = None
    psycopg2 = None

logger = logging.getLogger(__name__)

class AsyncConnectionPool:
    """Production-grade async connection pool manager"""
    
    def __init__(self, database_url: str, min_size: int = 5, max_size: int = 20):
        self.database_url = database_url
        self.min_size = min_size
        self.max_size = max_size
        self.pool = None
        self._lock = asyncio.Lock()
        self._closed = False
        
    async def initialize(self):
        """Initialize the connection pool"""
        if self.pool is not None:
            return
            
        async with self._lock:
            if self.pool is not None:
                return
                
            try:
                if asyncpg:
                    self.pool = await asyncpg.create_pool(
                        self.database_url,
                        min_size=self.min_size,
                        max_size=self.max_size,
                        command_timeout=30,
                        server_settings={
                            'application_name': 'bhiv_hr_agent',
                            'jit': 'off'
                        }
                    )
                    logger.info(f"AsyncPG pool initialized: {self.min_size}-{self.max_size} connections")
                else:
                    logger.warning("AsyncPG not available, using fallback connection management")
                    
            except Exception as e:
                logger.error(f"Failed to initialize connection pool: {e}")
                raise
    
    @asynccontextmanager
    async def acquire(self):
        """Acquire a connection from the pool"""
        if self._closed:
            raise RuntimeError("Connection pool is closed")
            
        if self.pool is None:
            await self.initialize()
            
        if asyncpg and self.pool:
            async with self.pool.acquire() as connection:
                yield connection
        else:
            # Fallback for when asyncpg is not available
            yield None
    
    async def close(self):
        """Close the connection pool"""
        if self._closed:
            return
            
        async with self._lock:
            if self.pool and asyncpg:
                await self.pool.close()
                logger.info("Connection pool closed")
            self._closed = True

class AsyncTaskManager:
    """Manages async tasks with proper lifecycle and error handling"""
    
    def __init__(self, max_concurrent_tasks: int = 100):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.task_semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self._shutdown_event = asyncio.Event()
        self._task_counter = 0
        
    async def submit_task(self, coro, task_name: Optional[str] = None) -> str:
        """Submit an async task for execution"""
        if task_name is None:
            self._task_counter += 1
            task_name = f"task_{self._task_counter}"
            
        async def _wrapped_task():
            async with self.task_semaphore:
                try:
                    return await coro
                except Exception as e:
                    logger.error(f"Task {task_name} failed: {e}")
                    raise
                finally:
                    self.active_tasks.pop(task_name, None)
        
        task = asyncio.create_task(_wrapped_task())
        self.active_tasks[task_name] = task
        return task_name
    
    async def wait_for_task(self, task_name: str, timeout: Optional[float] = None):
        """Wait for a specific task to complete"""
        task = self.active_tasks.get(task_name)
        if task is None:
            return None
            
        try:
            return await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning(f"Task {task_name} timed out")
            task.cancel()
            raise
    
    async def shutdown(self, timeout: float = 30.0):
        """Gracefully shutdown all tasks"""
        self._shutdown_event.set()
        
        if not self.active_tasks:
            return
            
        logger.info(f"Shutting down {len(self.active_tasks)} active tasks")
        
        # Cancel all tasks
        for task_name, task in self.active_tasks.items():
            if not task.done():
                task.cancel()
                logger.debug(f"Cancelled task: {task_name}")
        
        # Wait for tasks to complete or timeout
        try:
            await asyncio.wait_for(
                asyncio.gather(*self.active_tasks.values(), return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.warning("Some tasks did not complete within shutdown timeout")
        
        self.active_tasks.clear()

class AsyncHTTPManager:
    """Manages HTTP sessions with connection pooling and retry logic"""
    
    def __init__(self, timeout: int = 30, max_connections: int = 100):
        self.timeout = timeout
        self.max_connections = max_connections
        self.session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()
        
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None or self.session.closed:
            async with self._lock:
                if self.session is None or self.session.closed:
                    if aiohttp is None:
                        raise RuntimeError("aiohttp not available")
                        
                    connector = aiohttp.TCPConnector(
                        limit=self.max_connections,
                        limit_per_host=20,
                        ttl_dns_cache=300,
                        use_dns_cache=True,
                        keepalive_timeout=30,
                        enable_cleanup_closed=True
                    )
                    
                    timeout_config = aiohttp.ClientTimeout(total=self.timeout)
                    
                    self.session = aiohttp.ClientSession(
                        connector=connector,
                        timeout=timeout_config,
                        headers={'User-Agent': 'BHIV-HR-Agent/3.2.0'}
                    )
                    
        return self.session
    
    async def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        """Make HTTP request with retry logic"""
        session = await self.get_session()
        
        max_retries = kwargs.pop('max_retries', 3)
        retry_delay = kwargs.pop('retry_delay', 1.0)
        
        for attempt in range(max_retries + 1):
            try:
                async with session.request(method, url, **kwargs) as response:
                    # Read response to ensure connection is properly closed
                    await response.read()
                    return response
                    
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == max_retries:
                    logger.error(f"HTTP request failed after {max_retries} retries: {e}")
                    raise
                    
                logger.warning(f"HTTP request attempt {attempt + 1} failed: {e}, retrying...")
                await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
    
    async def close(self):
        """Close HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()
            # Wait for underlying connections to close
            await asyncio.sleep(0.1)

class AsyncResourceManager:
    """Centralized async resource management"""
    
    def __init__(self):
        self.resources: Dict[str, Any] = {}
        self.cleanup_callbacks: List[Callable] = []
        self._shutdown_complete = asyncio.Event()
        
    def register_resource(self, name: str, resource: Any, cleanup_callback: Optional[Callable] = None):
        """Register a resource for management"""
        self.resources[name] = resource
        if cleanup_callback:
            self.cleanup_callbacks.append(cleanup_callback)
            
    def get_resource(self, name: str) -> Any:
        """Get a managed resource"""
        return self.resources.get(name)
    
    async def cleanup_all(self):
        """Cleanup all managed resources"""
        logger.info("Starting resource cleanup")
        
        for callback in self.cleanup_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
            except Exception as e:
                logger.error(f"Error during resource cleanup: {e}")
        
        self.resources.clear()
        self.cleanup_callbacks.clear()
        self._shutdown_complete.set()
        logger.info("Resource cleanup complete")

class AsyncProcessingEngine:
    """Main async processing engine with comprehensive management"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection_pool = AsyncConnectionPool(database_url)
        self.task_manager = AsyncTaskManager()
        self.http_manager = AsyncHTTPManager()
        self.resource_manager = AsyncResourceManager()
        
        # Register resources
        self.resource_manager.register_resource("db_pool", self.connection_pool, self.connection_pool.close)
        self.resource_manager.register_resource("http_manager", self.http_manager, self.http_manager.close)
        self.resource_manager.register_resource("task_manager", self.task_manager, self.task_manager.shutdown)
        
        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown")
            asyncio.create_task(self.shutdown())
            
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    async def initialize(self):
        """Initialize the processing engine"""
        try:
            await self.connection_pool.initialize()
            logger.info("Async processing engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize async processing engine: {e}")
            raise
    
    async def process_batch(self, items: List[Any], processor_func: Callable, batch_size: int = 10) -> List[Any]:
        """Process items in batches with async optimization"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # Create tasks for batch processing
            tasks = []
            for item in batch:
                task_name = await self.task_manager.submit_task(processor_func(item))
                tasks.append(task_name)
            
            # Wait for batch completion
            batch_results = []
            for task_name in tasks:
                try:
                    result = await self.task_manager.wait_for_task(task_name, timeout=30.0)
                    batch_results.append(result)
                except Exception as e:
                    logger.error(f"Batch processing error: {e}")
                    batch_results.append(None)
            
            results.extend(batch_results)
            
            # Small delay between batches to prevent overwhelming
            await asyncio.sleep(0.01)
        
        return results
    
    async def shutdown(self):
        """Graceful shutdown of the processing engine"""
        logger.info("Initiating async processing engine shutdown")
        await self.resource_manager.cleanup_all()
        logger.info("Async processing engine shutdown complete")

# Global instance
_async_engine: Optional[AsyncProcessingEngine] = None

def get_async_engine(database_url: Optional[str] = None) -> AsyncProcessingEngine:
    """Get or create the global async processing engine"""
    global _async_engine
    
    if _async_engine is None:
        if database_url is None:
            raise ValueError("Database URL required for first initialization")
        _async_engine = AsyncProcessingEngine(database_url)
    
    return _async_engine

async def initialize_async_engine(database_url: str):
    """Initialize the global async processing engine"""
    engine = get_async_engine(database_url)
    await engine.initialize()
    return engine

async def shutdown_async_engine():
    """Shutdown the global async processing engine"""
    global _async_engine
    if _async_engine:
        await _async_engine.shutdown()
        _async_engine = None