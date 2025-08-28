import httpx
from ..core.config import settings

async def get_top_candidates(job_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.agent_service_url}/match", json={"job_id": job_id})
        response.raise_for_status()
        return response.json()
