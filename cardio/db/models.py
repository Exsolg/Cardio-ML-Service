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


def get_list(page: int = None, limit: int = None, _for: enums.For = None) -> list:
    filters = {'deleted_at': None}
    if _for:
        filters['for'] = _for
    
    skip = None if page is None or limit is None else page * limit

    try:
        if limit is None and skip is None:
            return list(get_models_repository().find(filters))
        elif limit and skip is None:
            return list(get_models_repository().find(filters, limit=limit))
        return list(get_models_repository().find(filters, limit=limit, skip=skip))
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e

def get_total_count(_for: enums.For = None) -> int:
    filters = {'deleted_at': None}
    if _for:
        filters['for'] = _for
    
    return len(list(get_models_repository().find(filters)))
