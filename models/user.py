from utils.db import db
from sqlalchemy.types import Text, Integer, UUID
from sqlalchemy import ForeignKey, Column
from uuid import uuid4
from hashlib import md5


class RoleAccount(db.Model):
    __tablename__ = "role_account"
    __table_args__ = { 'schema': 'account' }
    role_id = Column('role_id', Integer, primary_key=True)
    role_name = Column('role_name', Text, nullable=False)

    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name


class UserAccount(db.Model):
    __tablename__ = "user_account"
    __table_args__ = { 'schema': 'account' }
    user_id = Column("user_id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_name = Column("user_name", Text, nullable=False)
    user_password = Column("user_password", Text, nullable=False)
    user_role = Column("user_role", Integer, ForeignKey("account.role_account.role_id"), nullable=False)
    user_state = Column("user_state", Integer, nullable=False, default=1)

    def __init__(self, username: str, password: str, role: int, state: int):
        self.user_name = username
        self.user_password = md5(password.encode()).hexdigest()
        self.user_role = role
        self.user_state = state

    def __repr__(self) -> str:
        return f"<UserAccount: {self.user_id}, {self.user_name}, {self.user_role}, {self.user_state}>"
