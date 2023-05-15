from jsonschema.exceptions import ValidationError
from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from flask import request

from cardio.services.errors import NotFoundError
from cardio.services import models as models_service
from cardio.controllers.reqparsers import base as base_reqparsers
from cardio.controllers.schemes import models as model_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/models')
api.models[model_schemes.prediction.name] = model_schemes.prediction
api.models[model_schemes.simple_model.name] = model_schemes.simple_model
api.models[model_schemes.models.name] = model_schemes.models
api.models[base_schemes.error.name] = base_schemes.error
api.models[model_schemes.score.name] = model_schemes.score
api.models[model_schemes.model.name] = model_schemes.model


@api.route('/')
class Model(Resource):
    @api.doc(description='Gets models list', id='get_list')
    @api.expect(base_reqparsers.get_list)
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.models)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(models_service.get_list(args),
                           model_schemes.models,
                           skip_none=True), HTTPStatus.OK
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>')
class Model(Resource):
    @api.doc(description='Get model', id='get', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.model)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id):
        try:
            return marshal(models_service.get(str(id)),
                           model_schemes.model,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Delete model', id='delete', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def delete(self, id):
        try:
            models_service.delete(str(id))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/predict')
class Model(Resource):
    @api.doc(description='Model prediction', id='predict', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.prediction)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', base_schemes.error)
    def post(self, id):
        try:
            args = request.json
            return marshal(models_service.predict(str(id), args),
                           model_schemes.prediction,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
    
        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST
        
        except Exception:
            return {'message': f'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
