from cardio.tools import plugins as plugin_tools
from cardio.tools.base_plugin import Plugin
from cardio.repositories import datasets as datasets_repository
from cardio.repositories import models as models_repository
from cardio.services.errors import NotFoundError, InternalError, ValidationError

from jsonschema import validate, ValidationError as _ValidationError
from loguru import logger
from math import ceil
from datetime import datetime


def get(id: str) -> dict:
    try:
        dataset = datasets_repository.get(id)

        if not dataset:
            raise NotFoundError(f'Dataset {id} not found')

        plugins = []
        for name in dataset['plugins']:
            plugin = plugin_tools.get(name)

            if not plugin:
                logger.warning(f'Plugin {name} was not found when processing the dataset {id}')
                continue
            
            plugins.append({
                'name': plugin.__name__,
                'description': plugin.description,
            })
            
        dataset['plugins'] = plugins

        return dataset
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get_list(filter: dict) -> dict:
    try:
        page =  filter.pop('page')
        limit = filter.pop('limit')

        page =  page  if page  >= 1 else 1
        limit = limit if limit >= 1 else 10

        skip = (page - 1) * limit

        datasets, total = datasets_repository.get_list(skip, limit, filter)

        for dataset in datasets:
            plugins = []
            for name in dataset['plugins']:
                plugin = plugin_tools.get(name)

                if not plugin:
                    logger.warning(f'Plugin {name} was not found when processing the dataset {dataset["_id"]}')
                    continue
                
                plugins.append(plugin.__name__)
            
            dataset['plugins'] = plugins

        return {
            'contents':      datasets,
            'page':          page,
            'limit':         limit,
            'totalPages':    ceil(total / limit),
            'totalElements': total
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def delete(id: str) -> None:
    try:
        dataset = datasets_repository.get(id)

        if not dataset:
            raise NotFoundError(f'Dataset {id} not found')

        datasets_repository.delete(id)
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def create(dataset: dict) -> dict:
    try:
        for name in dataset['plugins']:
            if not plugin_tools.get(name):
                raise NotFoundError(f'Plugin {name} not found')
            
        dataset = datasets_repository.get(datasets_repository.create(dataset))

        plugins = []
        for name in dataset['plugins']:
            plugin = plugin_tools.get(name)
            
            plugins.append({
                'name': plugin.__name__,
                'description': plugin.description,
            })
            
        dataset['plugins'] = plugins
        
        return dataset

    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def update(id: str, dataset: dict) -> dict:     # ТУТ если меняем плагины, нужно валижировать вю дату
    try:
        _dataset = datasets_repository.get(id)

        if not _dataset:
            raise NotFoundError(f'Dataset {id} not found')

        for name in dataset['plugins']:
            if not plugin_tools.get(name):
                raise NotFoundError(f'Plugin {name} not found')

        datasets_repository.update(id, dataset)
        
        return datasets_repository.get(id)
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def training_status(id: str) -> dict:
    try:
        _dataset = datasets_repository.get(id)

        if not _dataset:
            raise NotFoundError(f'Dataset {id} not found')
        
        return {
            'plugin':            'None',
            'progress':          0,
            'trainingStartDate': datetime.now(),
        }
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def predict(dataset_id: int, samples: list[dict]) -> list[dict]:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')

        if not dataset.get('bestModel'):
            raise NotFoundError(f'Models not found in dataset {dataset_id}')

        model = models_repository.get(dataset['bestModel'])

        plugin = plugin_tools.get(model['plugin'])

        if not plugin:
            raise NotFoundError(f'Plugin {model["plugin"]} not found')

        for samle in samples:
            validate(samle, plugin.scheme_sample)
        
        plugin: Plugin = plugin()
        plugin.load_from_file(model['filePath'])

        predictions = plugin.predict([i['sample'] for i in samples])

        return {
            'contents':      predictions,
            'page':          1,
            'limit':         len(predictions),
            'totalPages':    1,
            'totalElements': len(predictions),
        }
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e
    
    except _ValidationError as e:
        logger.info(f'ValidationError: {e}')
        raise ValidationError(e)

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)
