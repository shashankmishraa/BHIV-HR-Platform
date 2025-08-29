"""
Scalable Queue-Based Processing System
Handles async candidate processing and batch operations
"""
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    RESUME_PROCESSING = "resume_processing"
    CANDIDATE_ANALYSIS = "candidate_analysis"
    BULK_UPLOAD = "bulk_upload"
    AI_MATCHING = "ai_matching"
    REPORT_GENERATION = "report_generation"

@dataclass
class ProcessingTask:
    """Task for queue processing"""
    id: str
    type: TaskType
    status: TaskStatus
    data: Dict[str, Any]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    priority: int = 1  # 1=low, 5=high
    retry_count: int = 0
    max_retries: int = 3

class QueueProcessor:
    """Scalable queue processor for HR platform tasks"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.tasks: Dict[str, ProcessingTask] = {}
        self.workers: List[asyncio.Task] = []
        self.running = False
        
    async def start(self):
        """Start the queue processor with worker tasks"""
        if self.running:
            return
            
        self.running = True
        logger.info(f"Starting queue processor with {self.max_workers} workers")
        
        # Start worker tasks
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
        
        logger.info("Queue processor started successfully")
    
    async def stop(self):
        """Stop the queue processor gracefully"""
        if not self.running:
            return
            
        logger.info("Stopping queue processor...")
        self.running = False
        
        # Cancel all workers
        for worker in self.workers:
            worker.cancel()
        
        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        
        logger.info("Queue processor stopped")
    
    async def submit_task(self, task_type: TaskType, data: Dict[str, Any], priority: int = 1) -> str:
        """Submit a new task to the queue"""
        task_id = str(uuid.uuid4())
        
        task = ProcessingTask(
            id=task_id,
            type=task_type,
            status=TaskStatus.PENDING,
            data=data,
            created_at=datetime.now(),
            priority=priority
        )
        
        self.tasks[task_id] = task
        await self.task_queue.put(task)
        
        logger.info(f"Task submitted: {task_id} ({task_type.value})")
        return task_id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        return {
            "id": task.id,
            "type": task.type.value,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "result": task.result,
            "error": task.error,
            "retry_count": task.retry_count
        }
    
    async def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue processing statistics"""
        pending_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.PENDING)
        processing_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.PROCESSING)
        completed_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for task in self.tasks.values() if task.status == TaskStatus.FAILED)
        
        return {
            "queue_size": self.task_queue.qsize(),
            "total_tasks": len(self.tasks),
            "pending_tasks": pending_tasks,
            "processing_tasks": processing_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "workers": len(self.workers),
            "running": self.running
        }
    
    async def _worker(self, worker_name: str):
        """Worker task that processes items from the queue"""
        logger.info(f"Worker {worker_name} started")
        
        while self.running:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Update task status
                task.status = TaskStatus.PROCESSING
                task.started_at = datetime.now()
                
                logger.info(f"Worker {worker_name} processing task {task.id} ({task.type.value})")
                
                try:
                    # Process the task based on type
                    result = await self._process_task(task)
                    
                    # Mark as completed
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                    task.result = result
                    
                    logger.info(f"Task {task.id} completed successfully")
                    
                except Exception as e:
                    logger.error(f"Task {task.id} failed: {str(e)}")
                    
                    # Handle retry logic
                    task.retry_count += 1
                    if task.retry_count <= task.max_retries:
                        task.status = TaskStatus.PENDING
                        task.started_at = None
                        await self.task_queue.put(task)  # Re-queue for retry
                        logger.info(f"Task {task.id} re-queued for retry ({task.retry_count}/{task.max_retries})")
                    else:
                        task.status = TaskStatus.FAILED
                        task.completed_at = datetime.now()
                        task.error = str(e)
                        logger.error(f"Task {task.id} failed permanently after {task.max_retries} retries")
                
                # Mark task as done in queue
                self.task_queue.task_done()
                
            except asyncio.TimeoutError:
                # No tasks in queue, continue
                continue
            except asyncio.CancelledError:
                logger.info(f"Worker {worker_name} cancelled")
                break
            except Exception as e:
                logger.error(f"Worker {worker_name} error: {str(e)}")
                await asyncio.sleep(1)  # Brief pause before continuing
        
        logger.info(f"Worker {worker_name} stopped")
    
    async def _process_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process a task based on its type"""
        if task.type == TaskType.RESUME_PROCESSING:
            return await self._process_resume_task(task)
        elif task.type == TaskType.CANDIDATE_ANALYSIS:
            return await self._process_candidate_analysis_task(task)
        elif task.type == TaskType.BULK_UPLOAD:
            return await self._process_bulk_upload_task(task)
        elif task.type == TaskType.AI_MATCHING:
            return await self._process_ai_matching_task(task)
        elif task.type == TaskType.REPORT_GENERATION:
            return await self._process_report_generation_task(task)
        else:
            raise ValueError(f"Unknown task type: {task.type}")
    
    async def _process_resume_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process resume parsing task"""
        data = task.data
        resume_url = data.get('resume_url')
        candidate_id = data.get('candidate_id')
        
        # Simulate resume processing
        await asyncio.sleep(2)  # Simulate processing time
        
        # Mock AI analysis results
        analysis_result = {
            "candidate_id": candidate_id,
            "resume_url": resume_url,
            "extracted_skills": ["Python", "JavaScript", "React", "SQL"],
            "experience_years": 3,
            "education_level": "Masters",
            "seniority_level": "Mid-level",
            "technical_score": 85,
            "confidence": 0.92,
            "processing_time": "2.1 seconds"
        }
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "processed_at": datetime.now().isoformat()
        }
    
    async def _process_candidate_analysis_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process candidate AI analysis task"""
        data = task.data
        candidate_id = data.get('candidate_id')
        
        # Simulate AI analysis
        await asyncio.sleep(1.5)
        
        analysis_result = {
            "candidate_id": candidate_id,
            "overall_score": 87.5,
            "technical_match": 85,
            "values_alignment": 4.3,
            "cultural_fit": 89,
            "recommendation": "Recommend",
            "ai_insights": [
                "Strong technical background",
                "Good cultural fit indicators",
                "Excellent growth potential"
            ]
        }
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "processed_at": datetime.now().isoformat()
        }
    
    async def _process_bulk_upload_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process bulk candidate upload task"""
        data = task.data
        candidates = data.get('candidates', [])
        job_id = data.get('job_id')
        
        # Simulate bulk processing
        processed_count = 0
        failed_count = 0
        
        for candidate in candidates:
            await asyncio.sleep(0.1)  # Simulate per-candidate processing
            
            # Simulate some failures
            if processed_count % 10 == 9:  # Every 10th candidate fails
                failed_count += 1
            else:
                processed_count += 1
        
        return {
            "status": "success",
            "job_id": job_id,
            "total_candidates": len(candidates),
            "processed_count": processed_count,
            "failed_count": failed_count,
            "processing_time": f"{len(candidates) * 0.1:.1f} seconds"
        }
    
    async def _process_ai_matching_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process AI candidate matching task"""
        data = task.data
        job_id = data.get('job_id')
        candidate_count = data.get('candidate_count', 0)
        
        # Simulate AI matching processing
        await asyncio.sleep(3)  # More intensive processing
        
        # Generate mock top candidates
        top_candidates = []
        for i in range(min(5, candidate_count)):
            top_candidates.append({
                "id": i + 1,
                "name": f"Candidate {i + 1}",
                "score": 95 - (i * 2),
                "values_alignment": 4.8 - (i * 0.1),
                "skills_match": 92 - (i * 1.5)
            })
        
        return {
            "status": "success",
            "job_id": job_id,
            "top_candidates": top_candidates,
            "total_analyzed": candidate_count,
            "algorithm_version": "v3.0.0-queue",
            "processing_time": "3.2 seconds"
        }
    
    async def _process_report_generation_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process report generation task"""
        data = task.data
        report_type = data.get('report_type')
        job_id = data.get('job_id')
        
        # Simulate report generation
        await asyncio.sleep(4)  # Report generation takes time
        
        report_data = {
            "report_type": report_type,
            "job_id": job_id,
            "generated_at": datetime.now().isoformat(),
            "total_candidates": 28,
            "report_url": f"https://example.com/reports/{job_id}_{report_type}.csv",
            "file_size": "2.3 MB",
            "columns": ["candidate_id", "name", "ai_score", "values_scores", "recommendation"]
        }
        
        return {
            "status": "success",
            "report": report_data,
            "processing_time": "4.1 seconds"
        }

# Global queue processor instance
queue_processor = QueueProcessor(max_workers=3)

async def start_queue_processor():
    """Start the global queue processor"""
    await queue_processor.start()

async def stop_queue_processor():
    """Stop the global queue processor"""
    await queue_processor.stop()

async def submit_task(task_type: TaskType, data: Dict[str, Any], priority: int = 1) -> str:
    """Submit a task to the global queue processor"""
    return await queue_processor.submit_task(task_type, data, priority)

async def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Get task status from the global queue processor"""
    return await queue_processor.get_task_status(task_id)

async def get_queue_stats() -> Dict[str, Any]:
    """Get queue statistics from the global queue processor"""
    return await queue_processor.get_queue_stats()