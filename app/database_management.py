import logging

from flask_pymongo import PyMongo

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
database_session = None


def init_database_connection(app):
    global database_session
    app.config["MONGO_URI"] = "mongodb+srv://cosmin0123:cosmin0123@cluster0.yalgy.mongodb.net/app?retryWrites=true&w=majority"
    database_session = PyMongo(app).db
    logger.info('Successful initiated the database')


def get_database_session():
    return database_session
