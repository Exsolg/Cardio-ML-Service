from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api

from cardio.controllers.models import api as models_api

from cardio.repositoryes.repositoryes import init_repositories


def create_app(config):
    app = Flask(__name__)
    db = PyMongo()
    api = Api(prefix='/v1',
              version='2.0.0',
              title='Cardio ML API',
              description='The ML API for the Cardio Center project')
    
    app.config['MONGO_URI'] = f'mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}/?authMechanism=DEFAULT'
    app.config['SECRET_KEY'] = config.SECRET_KEY

    db.init_app(app)
    db.db = db.cx[config.MONGO_DB_NAME]
    init_repositories(db.db)
    
    api.add_namespace(models_api, '/models')
    api.init_app(app)
    
    return app
