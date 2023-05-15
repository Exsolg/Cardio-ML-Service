from cardio.repositories.repositories import models
from uuid import uuid4
from datetime import datetime
from loguru import logger


def create(model: dict) -> str:
    try:
        return models().insert_one({
            '_id': str(uuid4()),
            'createdAt': datetime.utcnow(),
            **model,
        }).inserted_id
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def delete(id: str) -> bool:
    try:
        return True if models().update_one({'_id': id, 'deletedAt': None},
                                           {'$set': {'deletedAt': datetime.utcnow()}}).modified_count else False
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get(id: str) -> dict:
    try:
        return models().find_one({'_id': id, 'deletedAt': None})
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def get_list(skip: int = None, limit: int = None, filter: dict = {}) -> list:
    try:
        kwargs = {}

        if limit is not None:
            kwargs['limit'] = limit
        if skip is not None:
            kwargs['skip'] = skip

        return (list(models().find({'deletedAt': None, **filter}, **kwargs).sort('createdAt')),
                _get_total_count(filter))
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def _get_total_count(filter: dict = {}) -> int:
    return len(list(models().find({'deletedAt': None, **filter})))

