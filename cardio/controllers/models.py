from jsonschema.exceptions import ValidationError

from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from flask import request

from cardio.services.errors import NotFoundError
from cardio.services import models as models_service
from cardio.controllers.reqparsers import base as base_reqparse
from cardio.controllers.schemes import models as model_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/models')
api.models[model_schemes.predict_schema.name] = model_schemes.predict_schema
api.models[model_schemes.simple_model_schema.name] = model_schemes.simple_model_schema
api.models[model_schemes.models_schema.name] = model_schemes.models_schema
api.models[base_schemes.error_schema.name] = base_schemes.error_schema
api.models[model_schemes.score_schema.name] = model_schemes.score_schema
api.models[model_schemes.model_schema.name] = model_schemes.model_schema


@api.route('/')
class Model(Resource):
    @api.doc(description='Gets models list', id='get_list')
    @api.expect(base_reqparse.get_list_parser)
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.models_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def get(self):
        try:
            args = base_reqparse.get_list_parser.parse_args()

            return marshal(models_service.get_list(args),
                           model_schemes.models_schema,
                           skip_none=True), HTTPStatus.OK
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>')
class Model(Resource):
    @api.doc(description='Get model', id='get', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.model_schema)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def get(self, id):
        try:
            return marshal(models_service.get(str(id)),
                           model_schemes.model_schema,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError:
            return {'message': f'Model {id} not found'}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Delete model', id='delete', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def delete(self, id):
        try:
            models_service.delete(str(id))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError:
            return {'message': f'Model {id} not found'}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/predict')
class Model(Resource):
    @api.doc(description='Model prediction', id='predict', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.predict_schema)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', base_schemes.error_schema)
    def post(self, id):
        try:
            args = request.json
            return marshal(models_service.predict(str(id), args),
                           model_schemes.predict_schema,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError:
            return {'message': f'Model {id} not found'}, HTTPStatus.NOT_FOUND
    
        except ValidationError as e:
            return {'message': e.message}, HTTPStatus.BAD_REQUEST
        
        except Exception:
            return {'message': f'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
