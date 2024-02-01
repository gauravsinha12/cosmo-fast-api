from fastapi import FastAPI
from products import router as product_router
from orders import router as order_router
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from faker import Faker

app = FastAPI()
fake = Faker()
async def generate_fake_product():
    return {
        "_id": str(ObjectId()),
        "name": fake.word(),
        "price": fake.pyfloat(min_value=10, max_value=1000, right_digits=2),
        "quantity": fake.random_int(min=1, max=100),
    }


@app.post("/fake/{num}")
async def add_fake_products(num: int):
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017/")
        db = client["ecommerce"]
        products_collection = db["products"]

        fake_products = [await generate_fake_product() for _ in range(num)]
        await products_collection.insert_many(fake_products)

        return JSONResponse(content={"message": f"{num} fake products added to the database."})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        client.close()

app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(order_router, prefix="/orders", tags=["orders"])