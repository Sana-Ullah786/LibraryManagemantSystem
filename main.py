from fastapi import FastAPI

from src.models import all_models
from src.models.database import engine

app = FastAPI()

all_models.Base.metadata.create_all(engine)
