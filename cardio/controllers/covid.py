from cardio.db import models
from cardio.db.enums import For
from cardio.controllers import errors
from sklearn.base import ClassifierMixin
from joblib import dump, load
from loguru import logger
from uuid import uuid4


_current_model_id: str = None
_current_model: ClassifierMixin = None


def get(id: str):
    try:
        model = models.get(id, For.COVID)
    except Exception as e:
        logger.error(f'Database layer error: {e}')
        raise errors.InternalError(e)
    
    if not model:
        logger.info(f'Model {id} not found')
        raise errors.NotFoundError(f'Model with id {id} not found')
    return model


def get_list():
    try:
        return models.get_list()
    except Exception as e:
        raise errors.InternalError(e)


def get_current():
    return get(_current_model_id)


def predict(id: str, params: dict):
    model = get(id)

    if 'file_path' not in model:
        logger.error(f'Field "file_path" does not exist in the model {id}')
        raise errors.FieldNotExistError(f'Field "file_path" does not exist in the model {id}')

    try:
        model = load(model['file_path'])
    except Exception as e:
        logger.error(f'Failed to load the model {id}: {e}')
        raise errors.InternalError(e)

    return str(type(model))


def create(model):
    try:
        model = load(model)
    except Exception as e:
        logger.error(f'Failed to load the model: {e}')
        raise errors.InternalError(e)
    
    file_path = f'models/{uuid4()}.joblib'

    try:
        dump(model, filename=file_path)
        logger.info(f'Save the model along the path {file_path}')
    
    except Exception as e:
        logger.error(f'Failed to save the model: {e}')
        raise errors.InternalError(e)

    try:
        _id = models.create({
            'python_type': str(type(model)),
            'file_path': file_path
        }, For.COVID)
    
    except Exception as e:
        logger.error(f'Database layer error: {e}')
        raise errors.InternalError(e)

    return get(_id)
