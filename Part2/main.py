from fastapi import FastAPI, HTTPException, Depends, status  # type: ignore
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session
import uuid

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class ProductInfo(BaseModel):
    """
    Model for product details to be used in requests and responses.
    """

    productId: str
    productName: str
    productDesc: str
    price: float
    stockQuantity: int


class ProductUpdate(BaseModel):
    """
    Model for updating product details. Fields are optional.
    """

    productName: str = None
    productDesc: str = None
    price: float = None
    stockQuantity: int = None


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


dp_dependency = Annotated[Session, Depends(get_db)]


@app.post("/api/products/createProduct", status_code=status.HTTP_201_CREATED)
async def createProduct(productInfo: ProductInfo, db: dp_dependency, status_code=201):
    """
    Create a new product in the inventory.

    - **productInfo**: A `ProductInfo` object containing product details.
    - Returns a success message along with the created product's details.

    **Example request:**
    ```json
    {
        "productId": "12345",
        "productName": "Laptop",
        "productDesc": "A high-end laptop",
        "price": 1500.00,
        "stockQuantity": 10
    }
    ```

    **Example response:**
    ```json
    {
        "message": "Product created successfully",
        "product": {
            "productId": "12345",
            "productName": "Laptop",
            "productDesc": "A high-end laptop",
            "price": 1500.00,
            "stockQuantity": 10
        }
    }
    ```
    """
    product = (
        db.query(models.Product)
        .filter(models.Product.productId == productInfo.productId)
        .first()
    )
    if product:
        raise HTTPException(status_code=409, detail="Product already exists")

    productName, productDesc, price, stockQuantity = (
        productInfo.productName,
        productInfo.productDesc,
        productInfo.price,
        productInfo.stockQuantity,
    )
    newProduct = models.Product(
        productName=productName,
        productDesc=productDesc,
        price=price,
        stockQuantity=stockQuantity,
    )
    db.add(newProduct)
    db.commit()

    return {
        "message": "Product created successfully",
        "product": ProductInfo(
            productId=newProduct.productId,
            productName=productName,
            productDesc=productDesc,
            price=price,
            stockQuantity=stockQuantity,
        ),
    }


@app.patch("/api/updateProduct/{productId}")
async def updateProduct(
    productId: str, productUpdate: ProductUpdate, db: dp_dependency
):
    """
    Update an existing product by its `productId`.

    - **productId**: The unique ID of the product to update.
    - **productUpdate**: A `ProductUpdate` object containing fields to update.

    **Example request:**
    ```json
    {
        "productName": "Updated Laptop",
        "price": 1400.00
    }
    ```

    **Example response:**
    ```json
    {
        "message": "Product updated successfully"
        "updatedField": {
            "productName": "Updated Laptop",
            "price": 1400.00
        }
    }
    ```
    """
    product = (
        db.query(models.Product).filter(models.Product.productId == productId).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updateInfo = productUpdate.dict(exclude_unset=True)
    for key, value in updateInfo.items():
        if hasattr(product, key):
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return {"message": "Product updated successfully", "updatedField": updateInfo}


@app.delete("/api/deleteProduct/{productId}")
async def deleteProduct(productId: str, db: dp_dependency):
    """
    Delete a product by its `productId`.

    - **productId**: The unique ID of the product to delete.

    **Example response:**
    ```json
    {
        "message": "Product deleted successfully"
        "deletedProduct": {
            "productId": "12345",
            "productName": "Laptop",
            "productDesc": "A high-end laptop",
            "price": 1500.00,
            "stockQuantity": 10
        }
    }
    ```
    """
    product = (
        db.query(models.Product).filter(models.Product.productId == productId).first()
    )
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully", "deletedProduct": product}
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/api/products/getProduct/{productId}", response_model=ProductInfo)
async def getProduct(productId: str, db: dp_dependency):
    """
    Get the details of a product by its `productId`.

    - **productId**: The unique ID of the product to retrieve.

    **Example response:**
    ```json
    {
        "productId": "12345",
        "productName": "Laptop",
        "productDesc": "A high-end laptop",
        "price": 1500.00,
        "stockQuantity": 10
    }
    ```
    """
    product = (
        db.query(models.Product).filter(models.Product.productId == productId).first()
    )
    if product:
        return ProductInfo(
            productId=product.productId,
            productName=product.productName,
            productDesc=product.productDesc,
            price=product.price,
            stockQuantity=product.stockQuantity,
        )
    raise HTTPException(status_code=404, detail="Product not found")
