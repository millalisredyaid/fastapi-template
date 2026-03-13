import logging
from fastapi import FastAPI
from pydantic import BaseModel

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Pydantic
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: str | None = None

@app.get("/health")
def health():
    logger.info("health endpoint called")
    return {"status": "ok"}

# POST エンドポイント
@app.post("/items")
def create_item(item: Item):
    return {"message": "item received", "item": item}