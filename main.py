from fastapi import FastAPI
from db.database import engine
from models import models
from routers import auth, todos, admin, users

app = FastAPI(title="Todo Application", description="Arrange your tasks efficiently")

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
