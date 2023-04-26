from fastapi import FastAPI

from routes.api import router
from src.models import all_models
from src.models.database import engine

all_models.Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(router)
