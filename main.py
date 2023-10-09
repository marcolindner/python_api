from fastapi import FastAPI, HTTPException, Request
from helper import Helper
from models import Item
import uuid, logging, time, string, random

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__) 

items: list[Item] = []

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response


@app.get("/items")
def get_items():
    logger.info("GET /items")
    return items

@app.get("/item/{itemid}")
def get_item(itemid):
    logger.info("GET /item/{itemid}")
    return Helper.find_item(itemid, items)

@app.put("/item")
def put_item(item: Item):
    item.total_price = (item.price * (item.tax / 100)) + item.price
    item.id = str(uuid.uuid4())
    items.append(item)
    return item

@app.patch("/item")
def patch_item(item: Item):
    if(Helper.replace_item(item, items)):
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/item/{itemid}")
def delete_item(itemid):
    item_to_delete = Helper.find_item(itemid, items)
    if(item_to_delete):
        items.remove(item_to_delete)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)