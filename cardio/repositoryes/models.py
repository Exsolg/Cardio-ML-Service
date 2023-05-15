from cardio.repositoryes.repositoryes import get_models_repository
from uuid import uuid4
from datetime import datetime
from loguru import logger
from math import ceil


def create(model: dict) -> str:
    try:
        model['_id'] = str(uuid4())
        model['created_at'] = datetime.utcnow()

        return get_models_repository().insert_one(model).inserted_id
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def delete(id: str):
    try:
        _filters = {'_id': id, 'deleted_at': None}
    
        _update = {'$set': {'deleted_at': datetime.utcnow()}}

        return True if get_models_repository().update_one(_filters, _update).modified_count else None
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get(id: str) -> dict:
    try:
        _filters = {'_id': id, 'deleted_at': None}

        return get_models_repository().find_one(_filters)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get_list(filters: dict) -> list:
    _filters = {'deleted_at': None}
    
    limit = _relu(filters['limit']) if filters.get('limit') else 0
    skip = _relu(filters['page'] - 1) * filters['limit'] if filters.get('limit') and filters.get('page') else 0

    try:
        total = get_total_count()
        return {
            'contents': list(get_models_repository().find(_filters, limit=limit, skip=skip)),
            'page': filters['page'] if filters.get('page') and filters['page'] >= 1 else 1,
            'limit': limit if limit > 0 else None,
            'totalPages': ceil(total / limit) if limit > 0 else 1,
            'totalElements': total
        } 
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get_total_count() -> int:
    filters = {'deleted_at': None}
    
    return len(list(get_models_repository().find(filters)))


def _relu(input):
    return input if input > 0 else 0

'''
        if limit is None and skip is None:
            return list(get_models_repository().find(_filters))
        
        elif limit and skip is None:
            return list(get_models_repository().find(_filters, limit=limit))
'''