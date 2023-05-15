from cardio.repositoryes.repositoryes import datasets
from cardio.repositoryes.pipelines import datasets as dataset_pipelines
from uuid import uuid4
from datetime import datetime
from loguru import logger
from math import ceil


def create(dataset: dict) -> str:
    try:
        dataset['_id'] = str(uuid4())
        dataset['created_at'] = datetime.utcnow()

        return datasets().insert_one(dataset).inserted_id
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def delete(id: str) -> bool:
    try:
        _filters = {'_id': id, 'deleted_at': None}
    
        _update = {'$set': {'deleted_at': datetime.utcnow()}}

        return True if datasets().update_one(_filters, _update).modified_count else None
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def update(id: str, dataset: dict) -> bool:
    try:
        _filters = {'_id': id, 'deleted_at': None}
    
        _update = {'$set': dataset}

        return True if datasets().update_one(_filters, _update).modified_count else None
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get(id: str) -> dict:
    try:
        result = list(datasets().aggregate(dataset_pipelines.get(id)))
        
        return result[0] if result else None
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get_list(filters: dict) -> list:
    filters['page'] =  filters['page']  if filters.get('page')  and filters['page'] >= 1  else 1
    filters['limit'] = filters['limit'] if filters.get('limit') and filters['limit'] >= 1 else 10

    skip = (filters['page'] - 1) * filters['limit']

    try:
        total = _get_total_count()
        return {
            'contents': list(datasets().aggregate(dataset_pipelines.get_list(skip, filters['limit']))),
            'page': filters['page'],
            'limit': filters['limit'],
            'totalPages': ceil(total / filters['limit']),
            'totalElements': total
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def _get_total_count() -> int:
    filters = {'deleted_at': None}
    
    return len(list(datasets().find(filters)))
