from cardio.services.errors import NotFoundError, InternalError
from cardio.tools import plugins as plugin_tools

from math import ceil
from loguru import logger


def get_list(filter: dict) -> list[dict]:
    try:
        page =  filter.pop('page')
        limit = filter.pop('limit')

        page =  page  if page  >= 1 else 1
        limit = limit if limit >= 1 else 10

        skip = (page - 1) * limit

        plugins, total = plugin_tools.gelt_list(skip, limit)

        return {
            'contents': [{
                'name': p.__name__,
                'description': p.description,
            } for p in plugins],
            'page':          page,
            'limit':         limit,
            'totalPages':    ceil(total / limit),
            'totalElements': total
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get(name: str) -> dict:
    try:
        plugin = plugin_tools.get(name)

        if not plugin:
            raise NotFoundError(f'Plugin {name} not found')

        if plugin:
            return {
                'name':              plugin.__name__,
                'description':       plugin.description,
                'shchemaPrediction': plugin.scheme_prediction,
                'shchemaSample':     plugin.scheme_sample,
            }

    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)
