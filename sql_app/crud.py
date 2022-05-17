from sqlalchemy.orm import Session
from . import models, schemas


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_name(db: Session, project_name: str):
    return db.query(models.Project).filter(models.Project.project_name == project_name).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.Project):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, project_id: int):
    db_item = models.Item(**item.dict(), owner_id=project_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
