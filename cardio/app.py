from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api

from cardio.api.cabs import cabs_api
from cardio.api.covid import covid_api

api = Api(prefix='/v1')
db = PyMongo()

def create_app(config):
    app = Flask(__name__)
    
    app.config['MONGO_URI'] = f'mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}/{config.MONGO_DB_NAME}'
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG

    api.add_namespace(cabs_api, '/cabs')
    api.add_namespace(covid_api, '/covid')

    api.init_app(app)
    db.init_app(app)
    
    return app
