from cardio.db.repositoryes import init_repositories
from cardio.db import models
from cardio.db.enums import For
from cardio.tests.config import Config
from pymongo import MongoClient


db = MongoClient(f'mongodb://{Config.MONGO_USER}:{Config.MONGO_PASSWORD}@{Config.MONGO_HOST}:{Config.MONGO_PORT}/?authMechanism=DEFAULT')
db.drop_database(Config.MONGO_TEST_DB_NAME)
init_repositories(db[Config.MONGO_TEST_DB_NAME])


def test_create():
    model = {}
    _for = For.COVID

    _id = models.create(model, _for)

    return None


def test_get():
    print('ichbeuibciebvie')
    model = models.get('1')
    print(models)
