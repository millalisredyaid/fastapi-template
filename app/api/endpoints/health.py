import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def health_check():
    logger.info("Health check endpoint called")
    return {
        "status": "ok",
        "service": "security-agent-api",
        "version": "0.1.0",
    }
