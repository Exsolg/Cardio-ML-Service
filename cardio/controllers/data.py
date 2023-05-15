from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from loguru import logger

from cardio.services.errors import NotFoundError, ValidationError
from cardio.services import data as data_service
from cardio.controllers.reqparsers import base as base_reqparsers
from cardio.controllers.reqparsers import data as data_reqparsers
from cardio.controllers.schemes import data as data_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/datasets')
api.add_model(data_schemes.data.name, data_schemes.data)
api.add_model(data_schemes.data_list.name, data_schemes.data_list)
api.add_model(data_reqparsers.data.name, data_reqparsers.data)
api.add_model(base_schemes.error.name, base_schemes.error)


@api.route('/<uuid:id>/data')
class Dataset(Resource):
    @api.doc(description='Get data list from dataset', id='get_data_list', params={'id': {'format': 'uuid'}})
    @api.expect(base_reqparsers.get_list, validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=data_schemes.data_list)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(data_service.get_list(str(id), args),
                           data_schemes.data_list,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


    @api.doc(description='Add data in dataset', id='create_data', params={'id': {'format': 'uuid'}})
    @api.expect([data_reqparsers.data], validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=data_schemes.data_list)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def post(self, id):
        try:
            # ТУТ Убрать этот ужас. Тут из json удаляются поля с None
            data = [{
                'sample': {k: v for k, v in data['sample'].items() if v is not None},
                'prediction': {k: v for k, v in data['prediction'].items() if v is not None},
                } for data in api.payload]

            return marshal(data_service.create_list(str(id), data),
                           data_schemes.data_list,
                           skip_none=True), HTTPStatus.OK
        
        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/data/<uuid:dataId>')
class Dataset(Resource):
    @api.doc(description='Get data from dataset', id='get_data', params={'id': {'format': 'uuid'}, 'dataId': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=data_schemes.data)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id, dataId):
        try:
            return marshal(data_service.get(str(id), str(dataId)),
                           data_schemes.data,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Delete data from dataset', id='delete_data', params={'id': {'format': 'uuid'}, 'dataId': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def delete(self, id, dataId):
        try:
            data_service.delete(str(id), str(dataId))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
