from flask_restx import Resource, Namespace, marshal
from flask_restx._http import HTTPStatus

from cardio.services.errors import NotFoundError
from cardio.services import plugins as plugins_service
from cardio.controllers.reqparsers import base as base_reqparse
from cardio.controllers.schemes import base as base_schemes
from cardio.controllers.schemes import plugins as plugin_schemes


api = Namespace('/plugins')
api.models[base_schemes.error_schema.name] = base_schemes.error_schema
api.models[plugin_schemes.plugins_schema.name] = plugin_schemes.plugins_schema
api.models[plugin_schemes.plugin_schema.name] = plugin_schemes.plugin_schema
api.models[plugin_schemes.simple_plugin_schema.name] = plugin_schemes.simple_plugin_schema
api.models[plugin_schemes.schema_schema.name] = plugin_schemes.schema_schema


@api.route('/')
class Plugin(Resource):
    @api.doc(description='Gets plugins list', id='get_list')
    @api.expect(base_reqparse.get_list_parser)
    @api.response(HTTPStatus.OK, 'Success', model=plugin_schemes.plugins_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def get(self):
        try:
            args = base_reqparse.get_list_parser.parse_args()

            x = plugins_service.get_list(args)

            return marshal(x,
                plugin_schemes.plugins_schema,
                skip_none=True), HTTPStatus.OK
        
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/<name>')
class Plugin(Resource):
    @api.doc(description='Get plugin', id='get')
    @api.response(HTTPStatus.OK, 'Success', model=plugin_schemes.plugin_schema)
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found', model=base_schemes.error_schema)
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', model=base_schemes.error_schema)
    def get(self, name):
        try:
            return marshal(plugins_service.get(name),
                plugin_schemes.plugin_schema,
                skip_none=True), HTTPStatus.OK
        
        except NotFoundError:
            return {'message': f'Plugin {name} not found'}, HTTPStatus.NOT_FOUND

        except Exception:
            return {'message': 'Internal Server Error'}, HTTPStatus.INTERNAL_SERVER_ERROR
