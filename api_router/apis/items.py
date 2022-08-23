from fastapi import APIRouter

router = APIRouter()


fake_items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items[skip : skip + limit]
