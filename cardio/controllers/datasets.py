from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from flask import request
from loguru import logger

from cardio.services.errors import NotFoundError, ValidationError, BadRequestError
from cardio.services import datasets as datasets_service
from cardio.controllers.reqparsers import base as base_reqparsers
from cardio.controllers.reqparsers import datasets as dataset_reqparsers
from cardio.controllers.reqparsers import models as model_reqparsers
from cardio.controllers.schemes import datasets as dataset_schemes
from cardio.controllers.schemes import models as model_schemes
from cardio.controllers.schemes import base as base_schemes


api = Namespace('/datasets')
api.add_model(dataset_schemes.simple_dataset.name, dataset_schemes.simple_dataset)
api.add_model(dataset_schemes.datasets.name, dataset_schemes.datasets)
api.add_model(dataset_schemes.dataset.name, dataset_schemes.dataset)
api.add_model(dataset_schemes.training_status.name, dataset_schemes.training_status)
api.add_model(dataset_reqparsers.create.name, dataset_reqparsers.create)
api.add_model(dataset_reqparsers.update.name, dataset_reqparsers.update)
api.add_model(model_reqparsers.sample.name, model_reqparsers.sample)
api.add_model(model_schemes.predictions_list.name, model_schemes.predictions_list)
api.add_model(base_schemes.error.name, base_schemes.error)


@api.route('/')
class Dataset(Resource):
    @api.doc(description='Gets datasets list', id='get_list')
    @api.expect(base_reqparsers.get_list, validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.datasets)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(datasets_service.get_list(args),
                           dataset_schemes.datasets,
                           skip_none=True), HTTPStatus.OK
        
        except Exception as e:
            logger.debug(f'Error: {e}')
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
        
        except BadRequestError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

        except Exception as e:
            logger.debug(f'Error: {e}')
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
        
        except Exception as e:
            logger.debug(f'Error: {e}')
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
        
        except Exception as e:
            logger.debug(f'Error: {e}')
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

        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/training-status')
class Dataset(Resource):
    @api.doc(description='Get training status for dataset', id='get_training_status', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.OK, 'Success', model=dataset_schemes.training_status)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, id):
        try:
            return marshal(datasets_service.training_status(str(id)),
                           dataset_schemes.training_status,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/predict')
class Model(Resource):
    @api.doc(description='Best model prediction', id='predict_model', params={'id': {'format': 'uuid'}})
    @api.expect(list(model_reqparsers.sample), validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=model_schemes.predictions_list)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', base_schemes.error)
    def post(self, id):
        try:
            return marshal(datasets_service.predict(str(id), api.payload),
                           model_schemes.predictions_list,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
    
        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<uuid:id>/train')
class Model(Resource):
    @api.doc(description='Start training', id='train_model', params={'id': {'format': 'uuid'}})
    @api.response(HTTPStatus.NO_CONTENT, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', base_schemes.error)
    def post(self, id):
        try:
            datasets_service.train(str(id))
            return None, HTTPStatus.NO_CONTENT
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
    
        except ValidationError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
