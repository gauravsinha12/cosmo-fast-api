## Cosmo Fast API

### 1. Problem Statement
You need to create a sample backend application in FastAPI, Python and MongoDB. The challenge assumes you have basic knowledge of Python and some knowledge of Flask / Django / FastAPI as well as MongoDB.

### 2 Database Schema
#### 2.1 Orders
```json
{
    "createdOn": "Optional[datetime]",
    "orderItems": "List[OrderItem]",
    "userAddress": "userAddress",
    "totalPrice": "Optional[float]"
}
```
#### 2.2 OrderItem
```json
{
    "productId": "string",
    "boughtQuantity": "int"
}
```
#### 2.3 UserAddress
```json
{
    "City": "string",
    "Country": "string",
    "ZipCode": "string"
}
```
#### 2.4 Products
```json
{
    "name": "string",
    "price": "float",
    "quantity": "int"
}
```

### 3. How to run the application

#### 3.1. Clone the repository
```bash
git clone https://github.com/gauravsinha12/cosmo-fast-api.git
```

#### 3.2. Install the dependencies
```bash
pip install -r requirements.txt
```

#### 3.3 Run the application
```bash
uvicorn main:app --host 0.0.0.0 --port 5050
```

#### 3.4 Open the application in browser
```bash
http://127.0.0.1:5050
```
#### 3.5 To use Swagger
```bash
http://127.0.0.1:5050/docs/
```

### 4. API Documentation

#### 4.1.
![Data Creation](./SS/fake.png)

- POST
  `/fake/11`


#### 4.2. `/products`
![Products](./SS/products.png)

- GET
    - `/all/`
    Get list of all products
    - `/all?limit=10`
    Get list of all products with limit of 10
    - `/all?limit=10&offset=5`
    Get list of all products with limit of 10 and offset of 5
    - `/all?min_price=100&max_price=1000`
    Get list of all products filetered by price between 100 and 1000
    - `/all?min_price=100&max_price=1000&limit=10&offset=5`
    Get list of all products filetered by price between 100 and 1000 with limit of 10 and offset of 5
    - `/{product_id}/`
    Get a product
- POST
    - `/create/`
    Create a new product
- PUT
    - `/{product_id}/`
    Update a product
- DELETE
    - `/{product_id}/`
    Delete a product

#### 4.3. `/orders` 
![order](./SS/orders.png)

- GET
    - `/all/`
    Get list of all orders
    - `/all?limit=10`
    Get list of all orders with limit of 10
    - `/all?limit=10&offset=5`
    Get list of all orders with limit of 10 and offset of 5
- POST
    - `/create/`
    Create a new order
- PUT
    - `/{order_id}/`
    Update an order
- DELETE
    - `/{order_id}/`
    Delete an order

