from cardio.repositoryes.repositoryes import data
from uuid import uuid4
from datetime import datetime
from loguru import logger
from math import ceil


def create(sample: dict) -> str:
    try:
        sample['_id'] = str(uuid4())
        sample['created_at'] = datetime.utcnow()

        return data().insert_one(sample).inserted_id
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def delete(id: str) -> bool:
    try:
        _filters = {'_id': id, 'deleted_at': None}
    
        _update = {'$set': {'deleted_at': datetime.utcnow()}}

        return True if data().update_one(_filters, _update).modified_count else None
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get(id: str) -> dict:
    try:
        _filters = {'_id': id, 'deleted_at': None}

        return data().find_one(_filters)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get_list(filters: dict) -> list:
    filters['deleted_at'] = None
    
    page =  filters.pop('page')  if filters.get('page')  and filters['page']  >= 1 else 1
    limit = filters.pop('limit') if filters.get('limit') and filters['limit'] >= 1 else 10

    skip = (page - 1) * limit

    try:
        total = _get_total_count(filters)
        return {
            'contents':      list(data().find(filters, skip=skip, limit=limit)),
            'page':          page,
            'limit':         limit,
            'totalPages':    ceil(total / limit),
            'totalElements': total
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def _get_total_count(filters: dict) -> int:
    return len(list(data().find(filters)))
