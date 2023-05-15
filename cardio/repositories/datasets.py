from cardio.repositories.repositories import datasets
from cardio.repositories.pipelines import datasets as dataset_pipelines
from uuid import uuid4
from datetime import datetime
from loguru import logger


def create(dataset: dict) -> str:
    try:
        return datasets().insert_one({
            '_id': str(uuid4()),
            'createdAt': datetime.utcnow(),
            **dataset,
        }).inserted_id
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def delete(id: str) -> bool:
    try:
        return True if datasets().update_one({'_id': id, 'deletedAt': None},
                                           {'$set': {'deletedAt': datetime.utcnow()}}).modified_count else False
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def update(id: str, dataset: dict) -> bool:
    try:
        return True if datasets().update_one({'_id': id, 'deletedAt': None},
                                             {'$set': dataset}).modified_count else False
    
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


def get_list(skip: int = None, limit: int = None, filter: dict = {}) -> list:
    try:
        return (list(datasets().aggregate(dataset_pipelines.get_list(skip, limit, {'deletedAt': None, **filter}))),
                _get_total_count())
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def _get_total_count(filter: dict = {}) -> int:
    return len(list(datasets().find({'deletedAt': None, **filter})))
