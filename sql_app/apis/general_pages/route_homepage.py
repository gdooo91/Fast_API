from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from . import crud, models, schemas


templates = Jinja2Templates(directory="sql_app/templates")
general_pages_router = APIRouter()


@general_pages_router.get("/")
async def home(request: Request):
	
	return templates.TemplateResponse("homepage.html",{"request":request})


