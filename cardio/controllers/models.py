from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from loguru import logger

from cardio.services.errors import NotFoundError, ValidationError
from cardio.services import models as models_service
from cardio.controllers.reqparsers import base as base_reqparsers
from cardio.controllers.reqparsers import models as model_reqparsers
from cardio.controllers.schemes import models as model_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/datasets')
api.add_model(model_schemes.predictions_list.name, model_schemes.predictions_list)
api.add_model(model_schemes.simple_model.name, model_schemes.simple_model)
api.add_model(model_schemes.models.name, model_schemes.models)
api.add_model(base_schemes.error.name, base_schemes.error)
api.add_model(model_schemes.model.name, model_schemes.model)
api.add_model(model_reqparsers.sample.name, model_reqparsers.sample)


@api.route('/<uuid:id>/models')
class Model(Resource):
    @api.doc(description='Gets models list', id='get_models_list')
    @api.expect(base_reqparsers.get_list)
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.models)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(models_service.get_list(str(id), args),
                           model_schemes.models,
                           skip_none=True), HTTPStatus.OK
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/models/<uuid:modelId>')
class Model(Resource):
    @api.doc(description='Get model', id='get_model', params={'id': {'format': 'uuid'}, 'modelId': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.model)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id, modelId):
        try:
            return marshal(models_service.get(str(id), str(modelId)),
                           model_schemes.model,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Delete model', id='delete_model', params={'id': {'format': 'uuid'}, 'modelId': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def delete(self, id, modelId):
        try:
            models_service.delete(str(id), str(modelId))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/models/<uuid:modelId>/predict')
class Model(Resource):
    @api.doc(description='Model prediction', id='predict_model', params={'id': {'format': 'uuid'}, 'modelId': {'format': 'uuid'}})
    @api.expect(list(model_reqparsers.sample), validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.predictions_list)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', base_schemes.error)
    def post(self, id, modelId):
        try:
            # ТУТ Убрать этот ужас. Тут из json удаляются поля с None
            data = [{
                'sample': {k: v for k, v in data['sample'].items() if v is not None},
                } for data in api.payload]

            return marshal(models_service.predict(str(id), str(modelId), data),
                           model_schemes.predictions_list,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
    
        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': f'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
