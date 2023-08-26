from cardio.services.errors import NotFoundError, InternalError
from cardio.services.models.plugins import Plugin, PluginsPage, PluginsFilter, SimplePlugin
from cardio.tools import plugins as plugin_tools

from math import ceil
from loguru import logger


def get_list(filter: PluginsFilter) -> PluginsPage:
    try:
        skip = (filter.page - 1) * filter.limit

        plugins, total = plugin_tools.gelt_list(skip, filter.limit, filter.name)

        return PluginsPage(
            page=filter.page,
            limit=filter.limit,
            total_pages=ceil(total / filter.limit),
            total_elements=total,
            elements=[
                SimplePlugin(
                    name=plugin.__name__,
                    description=plugin.description,
                )
                for plugin in plugins
            ]
        )
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)


def get(name: str) -> Plugin:
    try:
        plugin = plugin_tools.get(name)

        if not plugin:
            raise NotFoundError(f'Plugin {name} not found')
        
        return Plugin(
            name=plugin.__name_,
            description=plugin.description,
            shchema_sample=plugin.scheme_sample,
            shchema_prediction=plugin.scheme_prediction,
        )

    except NotFoundError as e:
        logger.info(f'NotFoundError: {e}')
        raise e
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise InternalError(e)
