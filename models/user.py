from utils.db import db
from sqlalchemy.types import Text, Integer, UUID
from uuid import uuid4



class UserAccount(db.Model):
    __tablename__ = "user_account"
    __table_args__ = { 'schema': 'account' }
    UUID_User = db.Column("user_id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_name = db.Column("user_name", Text)
    user_password = db.Column("user_password", Text)
    user_role = db.Column("user_role", Integer)

    def __init__(self, user, password, rol):

        self.user_name = user
        self.user_password = password
        self.user_role = rol

