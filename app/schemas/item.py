from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(..., example="Иви")
    price: float = Field(..., gt=0, example=100.0)
    in_stock: bool = Field(default=True)


class ItemCreate(ItemBase):
    """Validation model used for create and update operations."""
    pass


class Item(ItemBase):
    """Response model including the item identifier."""
    id: int

    model_config = ConfigDict(from_attributes=True)
