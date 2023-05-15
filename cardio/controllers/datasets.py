from jsonschema.exceptions import ValidationError

from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from flask import request

from cardio.services.errors import NotFoundError
from cardio.services import datasets as datasets_service
from cardio.controllers.reqparsers import base as base_reqparse
from cardio.controllers.reqparsers import datasets as dataset_reqparse
from cardio.controllers.schemes import datasets as dataset_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/datasets')
api.models[base_schemes.error_schema.name] = base_schemes.error_schema


@api.route('/')
class Dataset(Resource):
    @api.doc(description='Gets datasets list', id='get_list')
    @api.expect(base_reqparse.get_list_parser)
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.datasets_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def get(self):
        try:
            args = base_reqparse.get_list_parser.parse_args()

            return marshal(datasets_service.get_list(args),
                           dataset_schemes.datasets_schema,
                           skip_none=True), HTTPStatus.OK
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(description='Create dataset', id='create')
    @api.expect(dataset_reqparse.create_parser)
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.dataset_schema)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def post(self):
        try:
            args = dataset_reqparse.create_parser.parse_args()
            return marshal(datasets_service.create(args),
                           dataset_schemes.dataset_schema,
                           skip_none=True), HTTPStatus.OK

        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>')
class Dataset(Resource):
    @api.doc(description='Get dataset', id='get', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.dataset_schema)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def get(self, id):
        try:
            return marshal(datasets_service.get(str(id)),
                           dataset_schemes.dataset_schema,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError:
            return {'message': f'Dataset {id} not found'}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc(description='Delete dataset', id='delete', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def delete(self, id):
        try:
            datasets_service.delete(str(id))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError:
            return {'message': f'Dataset {id} not found'}, HTTPStatus.NOT_FOUND
        
        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
