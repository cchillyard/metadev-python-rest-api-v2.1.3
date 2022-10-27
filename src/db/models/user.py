from email.policy import default
import enum
from sqlalchemy import Column, String, Enum

from ..db_setup import Base

class Role(enum.Enum):
    admin = 'admin'
    user = 'user'

class User(Base):
    __tablename__ = 'user'

    id = Column(String(100), primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)

    def __repr__(self):
        return f'<User {self.name}>'