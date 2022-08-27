from typing import Union
from pydantic import BaseModel

#ADDED
from datetime import datetime, time, timedelta


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class Project(BaseModel):
    # id : int
    project_name : str
    paid : bool
    parts_orderd : bool
    start_build : bool
    ship_date : str
    install_date : str

    class Config:
        orm_mode = True

class Project_read(Project):
    id = int

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

class AProjects(BaseModel):
    projectid : int
    companyid : int
    contactid : float
    shiptoenduser : bool
    enduser : int
    endusecontactid : float
    employeeid : int
    purchaseordernumber : str
    saleid : float
    projecttotalbillingestimate : float
    projectname : str
    projecttypeid : int
    projectmodel : str
    projectdescription : str
    numberofaxis : float
    projectscanning : bool
    projectscanwidth : str
    projectserialnumber : str
    projectbegindate : str
    projectenddate : str
    projectduedate : str
    probeorderdate : str
    partsorderdate : str
    projectshipdate : str
    projectinstalldate : str
    projectclosed : bool
    projectstatus : str
    hand : str
    valvemodel : str
    touchscreen : str
    numberofprobes : float
    projectreference : str