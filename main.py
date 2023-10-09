from fastapi import FastAPI, HTTPException
from helper import Helper
from models import Item
import uuid

items: list[Item] = []

app = FastAPI()

@app.get("/items")
def get_items():
    return items

@app.get("/item/{itemid}")
def get_item(itemid):
    return Helper.find_item(itemid)

@app.put("/item")
def put_item(item: Item):
    item.total_price = (item.price * (item.tax / 100)) + item.price
    item.id = str(uuid.uuid4())
    items.append(item)
    return item

@app.patch("/item")
def patch_item(item: Item):
    if(Helper.replace_item(item)):
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/item/{itemid}")
def delete_item(itemid):
    item_to_delete = Helper.find_item(itemid)
    if(item_to_delete):
        items.remove(item_to_delete)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)