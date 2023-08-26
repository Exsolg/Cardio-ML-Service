# from pymongo import MongoClient
from fastapi import FastAPI
from loguru import logger

from cardio.controllers.utils.responses import INTERNAL_SERVER_ERROR
from cardio.controllers.utils.exception_handlers import not_found_handler, bad_request_handler, internal_server_error_handler
from cardio.controllers.plugins import plugins_api
from cardio.services.errors import NotFoundError, BadRequestError, InternalError
# from cardio.repositories.repositories import init as init_repositories
from cardio.tools.plugins import init as init_plugins
# from cardio.tools.model_files import init as init_model_files

from config import Config


def create_app(config: Config) -> FastAPI:
    # db = MongoClient()

    global_api = FastAPI(
        debug=config.DEBUG,
        docs_url=None,
        redoc_url=None,
    )

    _init_routes(global_api, config)
    
    # app.config['MONGO_URI'] = f'mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}/?authMechanism=DEFAULT'
    # app.config['SECRET_KEY'] = config.SECRET_KEY

    logger.info('Repositories initialization...')

    # init_repositories(db.db)

    logger.info('Plugins initialization...')

    init_plugins(config.PLUGINS_DIR)

    logger.info('Models initialization...')

    # init_model_files(config.MODELS_DIR)
    
    return global_api


def _init_routes(global_api: FastAPI, config: Config):
    logger.info('Routes initialization...')

    api_v1 = FastAPI(
        debug=config.DEBUG,
        version=config.VERSION,
        title=f'{config.TITLE} V1',
        summary=config.SUMMARY,
        description=config.DESCRIPTION,
        docs_url='/openapi' if config.OPENAPI_IS_VISIBLE else None,
        redoc_url=None,
        responses=INTERNAL_SERVER_ERROR,
    )

    api_v1.add_exception_handler(NotFoundError, not_found_handler)
    api_v1.add_exception_handler(BadRequestError, bad_request_handler)
    api_v1.add_exception_handler(InternalError, internal_server_error_handler)

    api_v1.include_router(plugins_api)
    
    global_api.mount(f'{config.PREFIX}/v1', api_v1)



