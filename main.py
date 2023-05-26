import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logs import setup_logging
from routes.api import router
from src.models import all_models
from src.models.database import engine

load_dotenv()

all_models.Base.metadata.create_all(engine)


app = FastAPI()

origins = ["http://localhost:3000", "http://16.170.249.16"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


setup_logging()
logging.info("Starting the application")
app.include_router(router)
