from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api
from loguru import logger

from cardio.controllers.models import api as models_api
from cardio.controllers.plugins import api as plugins_api
from cardio.controllers.datasets import api as datasets_api
from cardio.repositoryes.repositoryes import init as init_repositoryes

from config import Config


def create_app(config: Config):
    app = Flask(__name__)
    db = PyMongo()
    api = Api(prefix='/v1',
              version='2.1.0',
              title='Cardio ML API',
              description='The ML API for the Cardio Center project')
    
    app.config['MONGO_URI'] = f'mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}/?authMechanism=DEFAULT'
    app.config['SECRET_KEY'] = config.SECRET_KEY

    logger.info('Repositories initialization...')

    db.init_app(app)
    db.db = db.cx[config.MONGO_DB_NAME]
    init_repositoryes(db.db)
    
    logger.info('API initialization...')

    api.add_namespace(models_api, models_api.name)
    api.add_namespace(plugins_api, plugins_api.name)
    api.add_namespace(datasets_api, datasets_api.name)

    api.init_app(app)
    
    return app
