from utils.db import db
from sqlalchemy.types import Text, Integer, UUID
from uuid import uuid4



class UserAccount(db.Model):
    __tablename__ = "user_account"
    __table_args__ = { 'schema': 'account' }
    UUID_user = db.Column("user_id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_name = db.Column("user_name", Text)
    user_password = db.Column("user_password", Text)
    user_role = db.Column("user_role", Integer)
    user_status = db.Column("user_state")

    def __init__(self, user, password, role, status):
        self.user_name = user
        self.user_password = password
        self.user_role = role
        self.user_status = status