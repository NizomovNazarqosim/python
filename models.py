from database import Base
from sqlalchemy import Column, Integer, String, UUID


class User(Base):
    __tablename__ = 'users'
    
    id=Column(Integer,primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    class Config:
        from_attributes = True
        