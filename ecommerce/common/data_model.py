from sqlalchemy import Column, Integer, String
from ecommerce.common.db_client import Base

class User(Base):  # Assuming we have a User model
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)