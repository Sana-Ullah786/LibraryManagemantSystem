import logging

from fastapi import FastAPI

from logs import setup_logging
from routes.api import router
from src.models import all_models
from src.models.database import engine

all_models.Base.metadata.create_all(engine)


app = FastAPI()
setup_logging()
logging.info("Starting the application")
app.include_router(router)
