from cardio.repositoryes import models
from cardio.services import errors
from loguru import logger
from cardio.services import plugins as plugins_service
from jsonschema import validate


def get(id: str) -> dict:
    try:
        model = models.get(id)
        
        if not model:
            raise errors.NotFoundError(f'Model {id} not found')
        
        return model
    
    except errors.NotFoundError as e:
        logger.debug(f'NotFoundError: {e}')
        raise e
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def get_list(filter: dict) -> dict:
    try:
        return models.get_list(filter)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def delete(id: str) -> bool:
    get(id)

    try:
        return models.delete(id)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def predict(id: str, params: dict) -> float:
    model = get(id)
    plugin = plugins_service.get(model['plugin'])

    validate(params, plugin.scheme)

    try:
        if 'file_path' not in model:
            raise errors.FieldNotExistError(f'Field "file_path" does not exist in the model {id}')

        p = plugin()
        p.load_from_file(model['file_path'])

        return p.predict(params)

    except errors.FieldNotExistError as e:
        logger.error(f'FieldNotExistError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)
