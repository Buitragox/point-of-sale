from utils.db import db
from sqlalchemy.types import Text, Integer, Double, UUID
from uuid import uuid4

class Sale(db.Model):
    __tablename__ = "sale"
    __table_args__ = { 'schema': 'sales' }
    sale_id = db.Column("sale_id", UUID, primary_key=True, default=uuid4)
    sale_price = db.Column("sale_price", Double)
    seller_id = db.Column("seller_id", UUID)
    client_id = db.Column("client_id", Text)

    def __init__(self, sale_id, sale_price, seller_id, client_id):
        self.sale_id = sale_id
        self.sale_price = sale_price
        self.seller_id = seller_id
        self.client_id = client_id
