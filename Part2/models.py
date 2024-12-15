import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, Integer, String, Double
from database import Base


class Product(Base):
    """
    Product model for representing a product in the database.

    This model is used to store product details in the "products" table. Each product has a unique ID,
    a name, description, price, and stock quantity. The `productId` is auto-generated using UUID.

    Attributes:
        productId (str): The unique identifier for the product (UUID).
        productName (str): The name of the product (max length 255 characters).
        productDesc (str): A brief description of the product (max length 255 characters).
        price (float): The price of the product.
        stockQuantity (int): The number of units of the product in stock.

    Example usage:
    ```python
    # Create a new product
    new_product = Product(
        productName="Laptop",
        productDesc="A high-end gaming laptop",
        price=1500.00,
        stockQuantity=25
    )
    ```
    """

    __tablename__ = "products"

    # The unique product identifier (UUID). This field is auto-generated using `uuid.uuid4()`
    # and is used as the primary key.
    productId = Column(
        String(36), primary_key=True, default=uuid.uuid4(), nullable=False
    )  # Auto-generate UUID

    # The name of the product. This field is mandatory.
    productName = Column(String(255), nullable=False)

    # A description of the product. This field is optional.
    productDesc = Column(String(255))

    # The price of the product. This field is mandatory.
    price = Column(Double, nullable=False)

    # The quantity of the product in stock. This field is mandatory.
    stockQuantity = Column(Integer, nullable=False)
