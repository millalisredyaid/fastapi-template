import logging

from fastapi import APIRouter, HTTPException

from app.schemas.item import Item, ItemCreate

logger = logging.getLogger(__name__)

router = APIRouter()

items_db: list[Item] = [
    Item(id=1, name="Иви", price=100, in_stock=True),
    Item(id=2, name="Амбреон", price=77, in_stock=False),
]


@router.get("", response_model=list[Item])
async def read_items():
    logger.info("Read all items")
    return items_db


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            logger.info("Read item id=%s", item_id)
            return item

    logger.warning("Item not found id=%s", item_id)
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("", status_code=201, response_model=Item)
async def create_item(item_in: ItemCreate):
    new_id = len(items_db) + 1
    new_item = Item(id=new_id, **item_in.model_dump())
    items_db.append(new_item)
    logger.info("Created item id=%s", new_id)
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_in: ItemCreate):
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item_in.model_dump())
            items_db[index] = updated_item
            logger.info("Updated item id=%s", item_id)
            return updated_item

    logger.warning("Item not found id=%s", item_id)
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            deleted_item = items_db.pop(index)
            logger.info("Deleted item id=%s", item_id)
            return deleted_item

    logger.warning("Item not found id=%s", item_id)
    raise HTTPException(status_code=404, detail="Item not found")
