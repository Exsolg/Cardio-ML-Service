from cardio.tools import plugins as plugin_tools
from cardio.repositories import models as models_repository
from cardio.repositories import datasets as datasets_repository
from cardio.services.errors import NotFoundError, InternalError

from loguru import logger
from math import ceil


def get(dataset_id: int, id: str) -> dict:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')

        model = models_repository.get(id)
        
        if not model:
            raise NotFoundError(f'Model {id} not found in dataset {dataset_id}')
        
        plugin = plugin_tools.get(model['plugin'])
        
        if plugin:
            model['plugin'] = {
            'name':              plugin.__name__,
            'description':       plugin.description,
            'shchemaPrediction': plugin.scheme_prediction,
            'shchemaSample':     plugin.scheme_sample,
            }
        
        else:
            logger.warning(f'Plugin {model["plugin"]} was not found when processing the model {id}')
            model['plugin'] = None
        
        return model
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get_list(dataset_id: int, filter: dict) -> dict:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')

        page =  filter.pop('page')
        limit = filter.pop('limit')

        page =  page  if page  >= 1 else 1
        limit = limit if limit >= 1 else 10

        skip = (page - 1) * limit

        models, total = models_repository.get_list(skip, limit, filter)

        for model in models:
            plugin = plugin_tools.get(model['plugin'])

            if not plugin:
                logger.warning(f'Plugin {model["plugin"]} was not found when processing the model {model["_id"]}')
                model['plugin'] = None

        return {
            'contents':      models,
            'page':          page,
            'limit':         limit,
            'totalPages':    ceil(total / limit),
            'totalElements': total
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def delete(dataset_id: int, id: str):
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Model {id} not found in dataset {dataset_id}')

        model = models_repository.get(id)
        
        if not model:
            raise NotFoundError(f'Model {id} not found')

        models_repository.delete(id)
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)
