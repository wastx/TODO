from fastapi import Request, Depends, Form, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from starlette.templating import Jinja2Templates

from todo.config import settings
from todo.database.base import get_db
from todo.models import ToDo

router = APIRouter()

templates = Jinja2Templates(directory='todo/templates')


@router.get('/')
def home(request: Request, db_session: Session = Depends(get_db)):
    todos = db_session.query(ToDo).all()
    return templates.TemplateResponse('todo/index.html',
                                      {'request': request,
                                       'app_name': settings.app_name,
                                       'todo_list': todos}
                                      )


@router.post('/add')
def add(title: str = Form(...), db_session: Session = Depends(get_db)):
    new_todo = ToDo(title=title)
    db_session.add(new_todo)
    db_session.commit()

    url = router.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@router.put('/update/{todo_id}')
def update(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(ToDo).filter(ToDo.id == todo_id).first()
    todo.is_complete = not todo.is_complete
    db_session.commit()

    url = router.url_path_for('home')

    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@router.delete('/delete/{todo_id}')
def delete(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(ToDo).filter_by(id=todo_id).first()
    db_session.delete(todo)
    db_session.commit()

    url = router.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
