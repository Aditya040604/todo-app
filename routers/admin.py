from fastapi import APIRouter, HTTPException, Path
from starlette import status
from models.models import Todos
from dependecies.auth_dependency import user_dependency, db_dependency

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    print(user)
    if user is None or user.role != "admin":
        raise HTTPException(status_code=401, detail="Access denied. Admin privileges are required to perform this action.")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)
):
    if user is None or user.role != "admin":
        raise HTTPException(status_code=401, detail="Authenticaiton Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
