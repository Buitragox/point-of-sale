from utils.db import db
from sqlalchemy.types import Text, Integer, Float

class Product(db.Model):
    __tablename__ = "product"
    __table_args__ = { 'schema': 'inventory' }
    product_id = db.Column("product_id", Integer, primary_key=True, autoincrement=True)
    product_name = db.Column("product_name", Text)
    product_amount = db.Column("product_amount", Integer)
    product_price = db.Column("product_price", Float)

    def __init__(self, name, amount, price):
        self.product_name = name
        self.product_amount = amount
        self.product_price = price
