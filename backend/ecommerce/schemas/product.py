"""Product related schemas"""

# base libraries
from typing import Optional, List
from uuid import UUID, uuid4
import random
import time

# external libraries
from sqlmodel import SQLModel, Field, Relationship

__all__ = (
    "Category",
    "CategoryCreate",
    "CategoryRead",
    "CategoryReadWithProducts",
    "Product", 
    "ProductCreate",
    "ProductRead",
    "ProductReadWithAttributes",
    "ProductReadWithItems",
    "ProductUpdate",
    "Attribute",
    "AttributeCreate",
    "AttributeRead",
    "AttributeValue",
    "AttributeValueCreate",
    "AttributeValueRead",
    "Item",
    "ItemCreate",
    "ItemRead",
    "ItemUpdate",
    "Image",
    "ImageRead"
)

# Categories
class CategoryBase(SQLModel):
    """Base model for Category"""
    name: str = Field(index=True, unique=True)
    description: str = ""

class Category(CategoryBase, table = True):
    """Main Table model for Category"""
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(
        back_populates="category", sa_relationship_kwargs={'cascade': 'all, delete'})
    images: List["Image"] = Relationship(back_populates="category")

# Products
class ProductBase(SQLModel):
    """Base Product model"""
    name: str = Field(index=True, unique=True)
    description: str
    # image_url: Optional[str] = None
    category_id: int = Field(default=None, foreign_key="category.id")

class Product(ProductBase, table=True):
    """Main table model for Product"""
    id: Optional[int] = Field(primary_key=True)
    category: Category = Relationship(back_populates="products")
    images: List["Image"] = Relationship(back_populates="product")
    product_items: List["Item"] = Relationship(
        back_populates="product", sa_relationship_kwargs={'cascade': 'all, delete'})
    attributes: List["Attribute"] = Relationship(
        back_populates="product", sa_relationship_kwargs={'cascade': 'all, delete'})

# Product Attributes
class AttributeBase(SQLModel):
    """Base class for product attributes,
product attributes are key, value pair tables.
This class will contain the key, and a one-to-many relationship to 
the list of possible values"""
    name: str

class Attribute(AttributeBase, table = True):
    """Main Attribute table"""
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="attributes")
    values: List["AttributeValue"] = Relationship(back_populates="attribute")

# Attribute Values
class AttributeValueBase(SQLModel):
    """Base attribute value"""
    value: str  # This could be 'Small', 'Red', 'Cotton', etc.
    attribute_id: int = Field(foreign_key="attribute.id")

class AttributeValue(AttributeValueBase, table=True):
    """Main table for attribute values. for item variations"""
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    item: Optional["Item"] = Relationship(back_populates="attribute_values")
    attribute: Optional[Attribute] = Relationship(back_populates="values")


# Items
class ItemBase(SQLModel):
    """Base Item class"""
    name: str = Field(index=True, unique=True)
    description: str = ""
    stock_quantity: int
    sku: str | None = None # will be autogenerated
    product_id: int = Field(foreign_key="product.id")
    price: float

class Item(ItemBase, table=True):
    """Item table"""
    id: int = Field(primary_key=True)
    product: "Product" = Relationship(back_populates="product_items")
    images: List["Image"] = Relationship(back_populates="item")
    attribute_values: List["AttributeValue"] = Relationship(
        back_populates="item", sa_relationship_kwargs={'cascade': 'all, delete'})

# Images

class ImageBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_url: str
class Image(ImageBase, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    item_id: Optional[int] = Field(default=None, foreign_key="item.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    product: Optional[Product] = Relationship(back_populates="images")
    item: Optional[Item] = Relationship(back_populates="images")
    category: Optional[Category] = Relationship(back_populates="images")

# pydantic models

class CategoryCreate(CategoryBase):
    """Create model for category"""

class CategoryRead(CategoryBase):
    """Read model for category"""
    id: int
    images: List[Image]

class AttributeCreate(AttributeBase):
    """Used by API to add extra attributes to product"""

class ProductCreate(ProductBase):
    """Used by api to create products.
    extra attributes are appeneded by create_product function in db"""
    attributes: Optional[List[AttributeCreate]] = None

class ProductRead(ProductBase):
    """Product Read model"""
    id: int
    images: List[Image]

class ProductUpdate(SQLModel):
    """Used by api to update products.
    extra attributes are appeneded by create_product function in db"""
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class AttributeRead(AttributeBase):
    """Product Attribute Read model"""
    id: int

class AttributeValueCreate(AttributeValueBase):
    """AttributeValue Create Model"""

class AttributeValueRead(AttributeValueBase):
    """AttributeValue Read Model"""
    id: int
    attribute: AttributeRead  # Nested read model to include attribute details

class ItemCreate(ItemBase):
    """For creating items, include a list of AttributeValueCreate instances"""
    attribute_values: Optional[List[AttributeValueCreate]] = None

class ItemRead(ItemBase):
    """Reading items back, include detailed attribute value information"""
    id: int
    product: ProductRead
    attribute_values: List[AttributeValueRead] = []
    images: List[Image]

class ItemUpdate(SQLModel):
    """Used by api to update products.
    extra attributes are appeneded by create_product function in db"""
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = None
    price: Optional[int] = None

class CategoryReadWithProducts(CategoryRead):
    """Inherits from CategoryRead, used to display products from category"""
    products: Optional[List[ProductRead]] = None

class ProductReadWithItems(ProductRead):
    """Update the Product models to include items with attributes in the read model"""
    items: List[ItemRead] = []

class ProductReadWithAttributes(ProductRead):
    """Inherits from CategoryRead, used to display products from category"""
    attributes: Optional[List[AttributeRead]] = []

class ImageRead(ImageBase):
    pass
