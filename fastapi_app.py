from enum import Enum
from typing import Union

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    id: int
    category: Category


fake_db = {
    0: Item(name="Hammer", price=9.99, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, id=2, category=Category.CONSUMABLES),
}



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def get_items() -> dict[str, list[Item]]:
    return {"items": list(fake_db.values())}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.post("/items")
def add_item(item: Item) -> dict[str, Item]:
    if fake_db.get(item.id) is not None:
        raise HTTPException(
            status_code=400, detail=f"Item with {item.id=} already exists."
        )
    # Inserting data into the database
    # INSERT INTO Table name Values (id, name, title )
    fake_db[item.id] = item
    return {"added": item}
