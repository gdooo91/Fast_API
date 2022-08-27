from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#START APP: uvicorn sql_app.main:app --reload

# from core.config import settings
# from sql_app.apis.general_pages.route_homepage import general_pages_router
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="sql_app/templates")
general_pages_router = APIRouter()

# Dependency
def get_db():
    # TODO: Use python-dotenv to save the database info. (Like .env in JS)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def include_router(app):
	app.include_router(general_pages_router)


def start_application():
	# app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	app = FastAPI(title="Projects Display",version="V0.1")
	include_router(app)
	return app 

#app = FastAPI()
app = start_application()

# PROJECT FUNTIONS 


@app.get("/", response_model=list[schemas.Project_read])
def read_projects(request: Request ,db: Session = Depends(get_db)):
    # retrun the last/first 10 Projects 
    # TODO: Test if this is looking for the last or first. 
    users = crud.get_projects(db, skip=0, limit=10)
    return templates.TemplateResponse("homepage.html",{"request":request, "projects": users})
    # return users
    # return templates.TemplateResponse("homepage.html",{"projects": users})


@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.Project, db: Session = Depends(get_db)):
    db_project = crud.get_project_by_name(db, project_name=project.project_name)
    if db_project:
        raise HTTPException(status_code=400, detail="Project already Made!")
    return crud.create_project(db=db, project=project)

# incorprated to the home page.
# @app.get("/projects/", response_model=list[schemas.Project_read])
# def read_project(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_projects(db, skip=skip, limit=limit)
#     return users

@app.get("/Aprojects/") #, response_model=schemas.AProjects)
def get_Access_Projects(request: Request, db: Session = Depends(get_db)):
    Aprojects = crud.get_Aproject(db=db)
    projects = list()

    for Aproj in Aprojects:
        proj = schemas.Project(project_name=str(Aproj.projectname), \
            paid= True, \
            parts_orderd= False, \
            start_build= False, \
            ship_date= str(Aproj.partsorderdate), \
            install_date=str(Aproj.partsorderdate))
        projects.append(proj)
    
    return templates.TemplateResponse("homepage.html",{"request":request, "projects": projects})

@app.get("/projects/{name}", response_model=schemas.Project_read)
def get_project_using_name(
    request: Request, name: str, db: Session = Depends(get_db)
):
    # return crud.get_project_by_name(db=db, project_name=name)
    project = crud.get_project_by_name(db=db, project_name=name)
    return templates.TemplateResponse("projectInfo.html",{"request":request, "project": project })

@app.get("/createproject")
def get_project_create_page(
    request: Request
):
    return templates.TemplateResponse("createproject.html",{"request":request})
    
@app.post("/createproject")
async def create_project(
    request: Request,
    # new_project: schemas.Project,
    db: Session = Depends(get_db)
    ):
    form = await request.form()
    # new_project  = models.Project() 
    # new_project(**dict(form.items))
    new_project = models.Project()
    new_project.project_name =  form.get("project_name")
    new_project.paid =  form.get("paid")
    new_project.parts_orderd =  form.get("parts_orderd")
    new_project.start_build =  form.get("start_build")
    new_project.ship_date =  form.get("ship_date")
    new_project.install_date =  form.get("install_date")

    db_project = crud.get_project_by_name(db, project_name = new_project.project_name)
    if db_project:
        raise HTTPException(status_code = 400, detail = "Project Exist!")

    if new_project.paid == None:
        new_project.paid = False
    else:
        new_project.paid = True
    
    if new_project.parts_orderd == None:
        new_project.parts_orderd = False
    else:
        new_project.parts_orderd = True

    if new_project.start_build == None:
        new_project.start_build = False
    else:
        new_project.start_build = True
    
    project = schemas.Project(
        project_name = new_project.project_name,
        paid = new_project.paid,
        parts_orderd = new_project.parts_orderd,
        start_build = new_project.start_build,
        ship_date = new_project.ship_date,
        install_date = new_project.install_date
    )
    try:
        crud.create_project(db = db, project = project)
        users = crud.get_projects(db, skip=0, limit=10)
        return templates.TemplateResponse("homepage.html",{"request":request, "projects": users})
    except:
        raise HTTPException(status_code = 400, detail = "DataBase is down!")
    

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
