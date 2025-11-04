from fastapi import APIRouter, HTTPException, Path
from starlette import status
from models.models import Todos
from dependecies.auth_dependency import user_dependency, db_dependency
from schemas.todos_schemas import TodoRequest

router = APIRouter(prefix="/todos", tags=["todos"])








@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        return HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user.id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)
):
    if user is None:
        return HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.id)
        .first()
    )
    # since id are different no need to check every record in db once the record with the matching id is found and this happens if we use fist() method
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        return HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.id)
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(ge=1),
):
    if user is None:
        return HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)
):
    if user is None:
        return HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.id
    ).delete()
    db.commit()
