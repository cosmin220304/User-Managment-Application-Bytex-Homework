import logging
import os

from flask_pymongo import PyMongo
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
database_session = None


def init_database_connection(app):
    global database_session
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    database_session = PyMongo(app).db
    logger.info('Successful initiated the database')


def get_database_session():
    return database_session
