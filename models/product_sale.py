from utils.db import db
from sqlalchemy.types import Integer, UUID
from sqlalchemy import Column, ForeignKey
from uuid import uuid4

class ProductSale(db.Model):
    Column()
    __tablename__ = "product_sale"
    __table_args__ = { 'schema': 'sales' }
    sale_id = Column("sale_id", UUID, ForeignKey("sales.sale.sale_id"), primary_key=True)
    product_id = Column("product_id", Integer, ForeignKey("inventory.product.product_id"), primary_key=True)
    amount = Column("amount", Integer)
