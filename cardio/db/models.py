from cardio.db.repositoryes import get_models_repository
from cardio.db import enums
from uuid import uuid4
from datetime import datetime
from loguru import logger


def create(model: dict, _for: enums.For) -> str:
    try:
        model['_id'] = str(uuid4())
        model['for'] = _for
        model['created_at'] = datetime.utcnow()

        return get_models_repository().insert_one(model).inserted_id
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def delete(id: str, _for: enums.For = None):
    try:
        filters = {'_id': id, 'deleted_at': None}
        if _for:
            filters['for'] = _for
    
        update = {'$set': {'deleted_at': datetime.utcnow()}}

        return True if get_models_repository().update_one(filters, update).modified_count else None
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get(id: str, _for: enums.For = None) -> dict:
    filters = {'_id': id, 'deleted_at': None}
    if _for:
        filters['for'] = _for

    try:
        return get_models_repository().find_one(filters)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get_list(_for: enums.For = None) -> list:
    filters = {'deleted_at': None}
    if _for:
        filters['for'] = _for

    try:
        return list(get_models_repository().find(filters))
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e
