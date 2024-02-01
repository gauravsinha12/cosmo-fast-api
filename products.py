from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

router = APIRouter()

class Product(BaseModel):
    name: str
    price: float
    quantity: int

async def get_products_collection():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["ecommerce"]
    return db["products"]

@router.get("/all", response_model=dict)
async def list_products(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    filters = {}
    
    if min_price is not None:
        filters["price"] = {"$gte": min_price}
        
    if max_price is not None:
        filters["price"] = {"$lte": max_price}
        
    if min_price is not None and max_price is not None:
        filters["price"] = {"$gte": min_price, "$lte": max_price}
        
    if min_price is not None and max_price is not None and min_price >= max_price:
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot be greater than or equal to the maximum price",)
   
    products_collection = await get_products_collection()
    products = products_collection.find(filters).skip(offset).limit(limit)
    product_list = []
    async for product in products:
        product_list.append(
            {
                "id": str(product["_id"]),
                "name": product["name"],
                "price": product["price"],
                "quantity": product["quantity"],
            }
        )
    total_records = await products_collection.count_documents(filters)
    next_offset = offset + limit if total_records > offset + limit else None
    prev_offset = offset - limit if offset - limit >= 0 else None
    return {
        "data": product_list,
        "page": {
            "limit": limit,
            "nextOffset": next_offset,
            "prevOffset": prev_offset,
            "total": total_records,
        },
    }


@router.post("/create", response_model=dict)
async def create_product(product: Product):
    products_collection = await get_products_collection()
    result = await products_collection.insert_one(product.model_dump())
    product_id = str(result.inserted_id)
    return {"productId": product_id, **product.model_dump()}

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: str):
    products_collection = await get_products_collection()
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "productId": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "quantity": product["quantity"],
    }

@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: str, updated_product: Product):
    products_collection = await get_products_collection()
    product_id_obj = ObjectId(product_id)
    existing_product = await products_collection.find_one({"_id": product_id_obj})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await products_collection.update_one({"_id": product_id_obj}, {"$set": updated_product.model_dump()})

    return {"message": "Product updated successfully"}

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    products_collection = await get_products_collection()
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
