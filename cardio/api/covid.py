from flask_restx import Resource, Namespace
from flask import request
from cardio.controllers import covid, errors
from cardio.api.reqparsers import covid_predict_parser
from cardio.api import schemes
from loguru import logger


covid_api = Namespace('covid')
covid_api.models[schemes.predict_schema.name] = schemes.predict_schema
covid_api.models[schemes.model_schema.name] = schemes.model_schema
covid_api.models[schemes.models_schema.name] = schemes.models_schema


@covid_api.route('/')
class Model(Resource):
    def get(self):
        try:
            return covid.get_list(), 200
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500
    
    def post(self):
        try:
            return covid.create(request.files['model']), 200
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500


@covid_api.route('/<id>',)
class Model(Resource):
    def get(self, id):
        try:
            return covid.get(id), 200
        except errors.NotFoundError:
            return {'message': f'Model {id} not found'}, 404
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500


@covid_api.route('/<id>/predict')
class Model(Resource):
    def post(self, id):
        args = covid_predict_parser.parse_args()
        try:
            return covid.predict(id, args)
        except errors.NotFoundError:
            return {'message': f'Model {id} not found'}, 404
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500
