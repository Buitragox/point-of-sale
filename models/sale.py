from utils.db import db
from sqlalchemy.types import Text, UUID, Float
from sqlalchemy import Column, ForeignKey
from uuid import uuid4

class Sale(db.Model):
    __tablename__ = "sale"
    __table_args__ = { 'schema': 'sales' }
    sale_id = Column("sale_id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    sale_price = Column("sale_price", Float)
    seller_id = Column("seller_id", UUID(as_uuid=True), ForeignKey('account.user_account.user_id'), nullable=False)
    client_id = Column("client_id", Text)

    def __init__(self, sale_id, sale_price, seller_id, client_id):
        self.sale_id = sale_id
        self.sale_price = sale_price
        self.seller_id = seller_id
        self.client_id = client_id
