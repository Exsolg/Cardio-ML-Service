from cardio.tools import plugins as plugin_tools
from cardio.tools import datasets as dataset_tools
from cardio.tools.base_plugin import Plugin
from cardio.tools.helpers import сompare_models_quality
from cardio.repositories import data as data_repository
from cardio.repositories import models as models_repository
from cardio.repositories import datasets as datasets_repository
from cardio.services.errors import NotFoundError, InternalError, ValidationError

from loguru import logger
from math import ceil
from jsonschema import validate, ValidationError as _ValidationError


def get(dataset_id: int, id: str) -> dict:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')

        data = data_repository.get(id)

        if not data or data['datasetId'] != dataset_id:
            raise NotFoundError(f'Data {id} not found in dataset {dataset_id}')

        return data
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get_list(dataset_id: int, filter: dict):
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')
        
        page =  filter.pop('page')
        limit = filter.pop('limit')

        page =  page  if page  >= 1 else 1
        limit = limit if limit >= 1 else 10

        skip = (page - 1) * limit

        datasets, total = data_repository.get_list(skip, limit, {'datasetId': dataset_id, **filter})

        return {
            'contents':      datasets,
            'page':          page,
            'limit':         limit,
            'totalPages':    ceil(total / limit),
            'totalElements': total
        }
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def delete(dataset_id: int, id: int) -> None:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')

        data = data_repository.get(id)

        if not data or data['datasetId'] != dataset_id:
            raise NotFoundError(f'Data {id} not found in dataset {dataset_id}')
        
        data_repository.delete(id)
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def create(dataset_id: int, data: dict) -> dict:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')
    
        for name in dataset['plugins']:
            plugin = plugin_tools.get(name)
            
            if not plugin:
                logger.warning(f'Plugin {name} was not found when processing the dataset {dataset_id}')
                continue
                
            validate(data['sample'], plugin.scheme_sample)
            validate(data['prediction'], plugin.scheme_prediction)

        return data_repository.get(data_repository.create({'datasetId': dataset_id, **data}))
    
    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e

    except _ValidationError as e:
        logger.info(f'ValidationError: {e}')
        raise ValidationError(e)

    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def create_list(dataset_id: int, data: list[dict]) -> dict:
    try:
        dataset = datasets_repository.get(dataset_id)

        if not dataset:
            raise NotFoundError(f'Dataset {dataset_id} not found')

        for name in dataset['plugins']:
            plugin = plugin_tools.get(name)
            
            if not plugin:
                logger.warning(f'Plugin {name} was not found when processing the dataset {dataset_id}')
                continue

            for d in data:
                validate(d['sample'], plugin.scheme_sample)
                validate(d['prediction'], plugin.scheme_prediction)

        for d in data:
            data_repository.create({'datasetId': dataset_id, **d})

        new_data, total = data_repository.get_list(
            skip=dataset['dataCount'],
            limit=len(data),
            filter={'datasetId': dataset_id})
        
        if len(data) + dataset['newData'] >= dataset['trainingSteps']:
            datasets_repository.update(dataset_id, {'newData': 0})

            data_for_training, _ = data_repository.get_list(
                skip=0,
                limit=total,
                filter={'datasetId': dataset_id})

            dataset_tools.add_to_training_queue(dataset_id, dataset['plugins'], data_for_training, _save_model)
        
        else:
            datasets_repository.update(dataset_id, {'newData': len(data) + dataset['newData']})

        return {
            'contents':      new_data,
            'page':          1,
            'limit':         len(data),
            'totalPages':    1,
            'totalElements': len(data),
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


def _save_model(dataset_id: str, plugin: Plugin) -> None:

    dataset = datasets_repository.get(dataset_id)

    if not dataset:
        raise NotFoundError(f'Dataset {id} not found')

    if not dataset.get('bestModelId'):
        id = models_repository.create({
            'score': plugin.get_score(),
            'params': plugin.get_params(),
            'filePath': plugin.save_in_file(),
            'plugin': plugin.__class__.__name__,
            'datasetId': dataset_id
        })

        datasets_repository.update(dataset_id, {'bestModelId': id})

        return
    
    old_model = models_repository.get(dataset['bestModelId'])
    
    if best_model_index := сompare_models_quality([old_model['score'], plugin.get_score()]) >= 0:
        if best_model_index == 1:
            id = models_repository.create({
            'score': plugin.get_score(),
            'params': plugin.get_params(),
            'filePath': plugin.save_in_file(),
            'plugin': plugin.__class__.__name__,
            'datasetId': dataset_id
            })

            datasets_repository.update(dataset_id, {'bestModelId': id})
    
    else:
        logger.warning(f'Failed to determine the best model for dataset {dataset_id}')
