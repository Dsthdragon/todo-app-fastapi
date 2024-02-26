from fastapi import FastAPI, Request, Depends, Form

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.database import engine, Base


templates: Jinja2Templates = Jinja2Templates(directory="templates")



def create_app() -> FastAPI:

    app = FastAPI()
    
    Base.metadata.create_all(bind=engine)
    from app.routes import router
    
    app.include_router(router)
    
    return app
