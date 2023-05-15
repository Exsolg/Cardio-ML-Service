from cardio.repositoryes import datasets as datasets_repository
from cardio.repositoryes import data as data_repository
from cardio.services import plugins as plugins_service
from cardio.services import data as data_service
from cardio.services.errors import NotFoundError, InternalError

from jsonschema.exceptions import ValidationError
from loguru import logger
from jsonschema import validate


def get(id: str) -> dict:
    try:
        dataset = datasets_repository.get(id)

        if not dataset:
            raise NotFoundError(f'Dataset {id} not found')

        plugins = []
        for p in dataset['plugins']:
            try:
                plugins.append(plugins_service.get(p))

            except NotFoundError as e:
                logger.error(f'NotFoundError: {e}')
            
        dataset['plugins'] = plugins

        return dataset
    
    except NotFoundError as e:
        logger.debug(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get_list(filter: dict) -> dict:
    try:
        return datasets_repository.get_list(filter)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def delete(id: str) -> bool:
    get(id)

    try:
        return datasets_repository.delete(id)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def create(dataset: dict) -> dict:
    for plugin_name in dataset['plugins']:
        plugins_service.get_plugin(plugin_name)

    try:
        return datasets_repository.get(datasets_repository.create(dataset))

    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def update(id: str, dataset: dict) -> dict:
    get(id)

    if dataset.get('plugins'):
        for plugin_name in dataset['plugins']:
            plugins_service.get_plugin(plugin_name)

    try:
        datasets_repository.update(id, dataset)
        return get(id)
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def add_data(id: str, data_list: dict) -> dict:
    dataset = get(id)

    for data in data_list['data']:
        for p in dataset['plugins']:
            try:
                plugin = plugins_service.get_plugin(p['name'])
                validate(data['sample'], plugin.scheme_sample)
                validate(data['target'], plugin.scheme_prediction)
            
            except ValidationError as e:
                logger.info(f'ValidationError when checking the plugin {p}: {e}')
                raise ValidationError(f'Error when checking the plugin {p}: {e}')
            
            except Exception as e:
                logger.error(f'Error: {e}')
                raise InternalError(e)
    
    try:
        for data in data_list['data']:                 # Поменять на подачу всего списка
            data['datasetId'] = dataset['_id']
            
            id = data_repository.create(data)
            
            data['_id'] = id

        return {
            'page':          1,
            'limit':         len(data_list['data']),
            'totalPages':    1,
            'totalElements': len(data_list['data']),
            'contents':      data_list['data'],
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get_data_list(id: str, filter: dict) -> dict:
    dataset = get(id)

    filter['datasetId'] = dataset['_id']

    return data_service.get_list(filter)
