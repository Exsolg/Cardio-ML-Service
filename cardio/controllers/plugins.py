from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus
from loguru import logger

from cardio.services.errors import NotFoundError
from cardio.services import plugins as plugins_service
from cardio.controllers.reqparsers import base as base_reqparsers
from cardio.controllers.schemes import base as base_schemes
from cardio.controllers.schemes import plugins as plugin_schemes


api = Namespace('/plugins')
api.add_model(base_schemes.error.name, base_schemes.error)
api.add_model(plugin_schemes.schema.name, plugin_schemes.schema)
api.add_model(plugin_schemes.plugin.name, plugin_schemes.plugin)
api.add_model(plugin_schemes.plugins.name, plugin_schemes.plugins)
api.add_model(plugin_schemes.simple_plugin.name, plugin_schemes.simple_plugin)


@api.route('/')
class Plugin(Resource):
    @api.doc(description='Gets plugins list', id='get_list')
    @api.expect(base_reqparsers.get_list, validate=True)
    @api.response(HTTPStatus.OK, 'Success', model=plugin_schemes.plugins)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self):
        try:
            args = base_reqparsers.get_list.parse_args()

            return marshal(plugins_service.get_list(args),
                           plugin_schemes.plugins,
                           skip_none=True), HTTPStatus.OK
        
        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/<name>')
class Plugin(Resource):
    @api.doc(description='Get plugin', id='get')
    @api.response(HTTPStatus.OK, 'Success', model=plugin_schemes.plugin)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error)
    def get(self, name):
        try:
            return marshal(plugins_service.get(name),
                           plugin_schemes.plugin,
                           skip_none=True), HTTPStatus.OK
        
        except NotFoundError as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND

        except Exception as e:
            logger.debug(f'Error: {e}')
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
