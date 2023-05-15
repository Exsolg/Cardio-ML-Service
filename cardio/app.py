from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api

from cardio.api.cabs import cabs_api
from cardio.api.covid import covid_api

from cardio.db.repositoryes import init_repositories


def create_app(config):
    app = Flask(__name__)
    db = PyMongo()
    api = Api(prefix='/v1')
    
    app.config['MONGO_URI'] = f'mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}/?authMechanism=DEFAULT'
    app.config['SECRET_KEY'] = config.SECRET_KEY

    print(app.config['MONGO_URI'])

    db.init_app(app)
    db.db = db.cx[config.MONGO_DB_NAME]
    init_repositories(db.db)

    api.add_namespace(cabs_api, '/cabs')
    api.add_namespace(covid_api, '/covid')
    api.init_app(app)
    
    return app
