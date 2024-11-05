from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String
from app.model.base import Base

class Login(Base):
    __tablename__ = "login"
    Id = Column(String(26),primary_key=True)
    Pass = Column(String(255))
    