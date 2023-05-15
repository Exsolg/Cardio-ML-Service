from jsonschema.exceptions import ValidationError
from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from flask import request

from cardio.services.errors import NotFoundError
from cardio.services import datasets as datasets_service
from cardio.controllers.reqparsers import base as base_reqparsers
from cardio.controllers.reqparsers import datasets as dataset_reqparsers
from cardio.controllers.reqparsers import data as data_reqparsers
from cardio.controllers.schemes import datasets as dataset_schemes
from cardio.controllers.schemes import data as data_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/datasets')
api.models[dataset_schemes.simple_dataset.name] = dataset_schemes.simple_dataset
api.models[dataset_schemes.datasets.name] = dataset_schemes.datasets
api.models[dataset_schemes.dataset.name] = dataset_schemes.dataset
api.models[data_schemes.data.name] = data_schemes.data
api.models[data_schemes.simple_data.name] = data_schemes.simple_data
api.models[data_schemes.data_list.name] = data_schemes.data_list
api.models[dataset_reqparsers.create.name] = dataset_reqparsers.create
api.models[dataset_reqparsers.update.name] = dataset_reqparsers.update
api.models[data_reqparsers.data.name] = data_reqparsers.data
api.models[data_reqparsers.data_list.name] = data_reqparsers.data_list
api.models[base_schemes.error.name] = base_schemes.error


@api.route('/')
class Dataset(Resource):
    @api.doc(description='Gets datasets list', id='get_list')
    @api.expect(base_reqparsers.get_list)
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.datasets)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(datasets_service.get_list(args),
                           dataset_schemes.datasets,
                           skip_none=True), HTTPStatus.OK
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(description='Create dataset', id='create')
    @api.expect(dataset_reqparsers.create, validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.dataset)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def post(self):
        try:
            return marshal(datasets_service.create(api.payload),
                           dataset_schemes.dataset,
                           skip_none=True), HTTPStatus.OK

        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>')
class Dataset(Resource):
    @api.doc(description='Get dataset', id='get', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.dataset)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id):
        try:
            return marshal(datasets_service.get(str(id)),
                           dataset_schemes.dataset,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Delete dataset', id='delete', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def delete(self, id):
        try:
            datasets_service.delete(str(id))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Update dataset', id='update', params={'id': {'format': 'uuid'}})
    @api.expect(dataset_reqparsers.update, validate=True)
    @api.response(HTTPStatus.NO_CONTENT, 'Success', model=dataset_schemes.dataset)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def patch(self, id):
        try:
            return marshal(datasets_service.update(str(id), api.payload),
                           dataset_schemes.dataset,
                           skip_none=True), HTTPStatus.OK

        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/data')
class Dataset(Resource):
    @api.doc(description='Get data from dataset', id='get_data', params={'id': {'format': 'uuid'}})
    @api.expect(base_reqparsers.get_list, validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=data_schemes.data_list)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(datasets_service.get_data_list(str(id), args),
                           data_schemes.data_list,
                           skip_none=True), HTTPStatus.OK
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(description='Add data in dataset', id='add_data', params={'id': {'format': 'uuid'}})
    @api.expect(data_reqparsers.data_list, validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=data_schemes.data_list)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def post(self, id):
        try:
            return marshal(datasets_service.add_data(str(id), api.payload),
                           data_schemes.data_list,
                           skip_none=True), HTTPStatus.OK
        
        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
