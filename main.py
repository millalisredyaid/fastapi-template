import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Pydantic model
class Item(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True
    description: str | None = None


# Sample data（Pydantic model list）
items: list[Item] = [
    Item(id=1, name="Иви", price=100, in_stock=True),
    Item(id=2, name="Амбреон", price=77, in_stock=False),
]


# Input model (without id)
class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: str | None = None


# health
@app.get("/health")
def health():
    logger.info("health endpoint called")
    return {"status": "ok"}


# GET all items
@app.get("/items")
def read_items():
    logger.info("Read all items")
    return items


# GET item detail
@app.get("/items/{item_id}")
def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            logger.info("Read item id=%s", item_id)
            return item

    logger.info("Item not found id=%s", item_id)
    raise HTTPException(status_code=404, detail="Item not found")


# POST (Create)
@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    new_id = len(items) + 1
    new_item = Item(id=new_id, **item.model_dump())
    items.append(new_item)
    logger.info("Created item id=%s", new_id)
    return new_item


# PUT (Update item)
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.model_dump())
            items[index] = updated_item
            logger.info("Updated item id=%s", item_id)
            return updated_item

    logger.info("Item not found id=%s", item_id)
    raise HTTPException(status_code=404, detail="Item not found")


# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            deleted_item = items.pop(index)
            logger.info("Deleted item id=%s", item_id)
            return deleted_item

    logger.info("Item not found id=%s", item_id)
    raise HTTPException(status_code=404, detail="Item not found")
