from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from app import templates
from app.models import Todo
from app.database import get_db
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="", tags=["SETUP APPS"])


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "todo_list": todos
        }
    )


@router.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = Todo(title=title)
    db.add(new_todo)
    db.commit()

    url = router.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()

    url = router.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = router.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
