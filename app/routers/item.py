from fastapi import APIRouter

# Create a router object
router = APIRouter()

# Define a route within the router
@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# You can define more routes as needed
