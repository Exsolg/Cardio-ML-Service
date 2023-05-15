from cardio.repositoryes import data as data_repository
from cardio.services.errors import NotFoundError, InternalError
from loguru import logger


def get(id: str) -> dict:
    try:
        dataset = data_repository.get(id)

        if not dataset:
            raise NotFoundError(f'Data {id} not found')

        return dataset
    
    except NotFoundError as e:
        logger.debug(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)

def get_list(filter: dict):
    try:
        return data_repository.get_list(filter)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)
