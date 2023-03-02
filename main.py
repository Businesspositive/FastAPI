from fastapi import FastAPI
from model import  models
from setup.database import engine
from routers import users, customers


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(customers.router)

