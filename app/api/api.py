from fastapi import APIRouter
from app.api.endpoints import health, items, analyze

# 「API全体の親ルーター」
api_router = APIRouter()

# 各エンドポイント
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
