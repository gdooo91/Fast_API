from operator import index

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from .database import Base
from datetime import date as dtDate

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Project(Base):
    __tablename__ = "project"
    
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    paid = Column(Boolean, index=True)
    parts_orderd = Column(Boolean, default=False)
    start_build = Column(Boolean, default=False)
    ship_date = Column(String, default = str(dtDate.today().year) + "/" + str(dtDate.today().month) + "/" + str(dtDate.today().day))
    install_date = Column(String, default = str(dtDate.today().year) + "/" + str(dtDate.today().month) + "/" + str(dtDate.today().day))
    

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
