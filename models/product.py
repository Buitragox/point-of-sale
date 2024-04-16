from utils.db import db
from sqlalchemy.types import Text, Integer, Float
from sqlalchemy import Column

class Product(db.Model):
    __tablename__ = "product"
    __table_args__ = { 'schema': 'inventory' }
    product_id = Column("product_id", Integer, primary_key=True, autoincrement=True)
    product_name = Column("product_name", Text)
    product_amount = Column("product_amount", Integer)
    product_price = Column("product_price", Float)

    def __init__(self, name, amount, price):
        self.product_name = name
        self.product_amount = amount
        self.product_price = price
