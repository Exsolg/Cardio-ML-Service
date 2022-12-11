from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from flask import request
from cardio.controllers import covid, errors
from cardio.api import reqparsers
from cardio.api import schemes
from loguru import logger


covid_api = Namespace('covid')
covid_api.models[schemes.predict_schema.name] = schemes.predict_schema
covid_api.models[schemes.model_schema.name] = schemes.model_schema
covid_api.models[schemes.models_schema.name] = schemes.models_schema
covid_api.models[schemes.error_schema.name] = schemes.error_schema
covid_api.models[schemes.score_schema.name] = schemes.score_schema


@covid_api.route('/')
class Model(Resource):
    @covid_api.response(HTTPStatus.OK, '', model=schemes.models_schema)
    @covid_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, '', model=schemes.error_schema)
    def get(self):
        try:
            return marshal({'models': covid.get_list()}, schemes.models_schema, skip_none=True), 200
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500
    
    @covid_api.expect(reqparsers.covid_model_create_parser)
    @covid_api.response(HTTPStatus.OK, '', model=schemes.models_schema)
    @covid_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, '', model=schemes.error_schema)
    def post(self):
        args = reqparsers.covid_model_create_parser.parse_args()
        try:
            return marshal(covid.create(args['model']), schemes.model_schema, skip_none=True), 200
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500


@covid_api.route('/<id>')
class Model(Resource):
    @covid_api.response(HTTPStatus.OK, '', model=schemes.model_schema)
    @covid_api.response(HTTPStatus.NOT_FOUND, '', model=schemes.error_schema)
    @covid_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, '', model=schemes.error_schema)
    def get(self, id):
        try:
            return marshal(covid.get(id), schemes.model_schema, skip_none=True), 200
        except errors.NotFoundError:
            return {'message': f'Model {id} not found'}, 404
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500


@covid_api.route('/<id>/predict')
class Model(Resource):
    @covid_api.expect(reqparsers.covid_predict_parser)
    @covid_api.response(HTTPStatus.OK, '', model=schemes.predict_schema)
    @covid_api.response(HTTPStatus.NOT_FOUND, '', model=schemes.error_schema)
    @covid_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, '', model=schemes.error_schema)
    def post(self, id):
        args = reqparsers.covid_predict_parser.parse_args()
        try:
            return covid.predict(id, args)
        except errors.NotFoundError:
            return {'message': f'Model {id} not found'}, 404
        except Exception as e:
            logger.error(f'Error: {e}')
            return {'message': 'Internal Server Error'}, 500
