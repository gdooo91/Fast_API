from operator import index

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
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
    parts_orderd = Column(Boolean, default= False)
    start_build = Column(Boolean, default= False)
    ship_date = Column(String, default = str(dtDate.today().year) + "/" + str(dtDate.today().month) + "/" + str(dtDate.today().day))
    install_date = Column(String, default = str(dtDate.today().year) + "/" + str(dtDate.today().month) + "/" + str(dtDate.today().day))
    

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Projects(Base):
    __tablename__ = "projects"
    
    projectid = Column(Integer, primary_key=True, index=True)
    companyid = Column(Integer)     ## ForeignKey("company.id")
    contactid = Column(Float, default = 0.0)
    shiptoenduser = Column(Boolean, default= False)
    enduser = Column(Integer, default = 0 )
    endusecontactid = Column(Float, default = 0.0)
    employeeid = Column(Integer, default = 0 )
    purchaseordernumber = Column(String, default = "")
    saleid = Column(Float, default = 0.0)
    projecttotalbillingestimate = Column(Float, default = 0.0)
    projectname = Column(String, default = "")
    projecttypeid = Column(Integer, default = 0 )
    projectmodel = Column(String, default = "")
    projectdescription = Column(String, default = "")
    numberofaxis = Column(Float, default = 0.0)
    projectscanning = Column(Boolean, default= False)
    projectscanwidth = Column(String, default = "")
    projectserialnumber = Column(String, default = "")
    projectbegindate = Column(String, default = "")
    projectenddate = Column(String, default = "")
    projectduedate = Column(String, default = "")
    probeorderdate = Column(String, default = "")
    partsorderdate = Column(String, default = "")
    projectshipdate = Column(String, default = "")
    projectinstalldate = Column(String, default = "")
    projectclosed = Column(Boolean, default= False)
    projectstatus = Column(String, default = "")
    hand = Column(String, default = "")
    valvemodel = Column(String, default = "")
    touchscreen = Column(String, default = "")
    numberofprobes = Column(Float, default = 0.0)
    projectreference = Column(String, default = "")