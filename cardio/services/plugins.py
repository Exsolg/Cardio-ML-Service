from cardio.services import errors
from plugins.base_plugin import Plugin
from math import ceil
from os import walk
from os.path import splitext, join
from loguru import logger


_plugins: dict[Plugin] = {}


def get_list(filter: dict) -> list[dict]:
    try:

        filter['page'] =  filter['page']  if filter['page']  >= 1 else 1
        filter['limit'] = filter['limit'] if filter['limit'] >= 1  else 10

        return {
            'contents': sorted([
                {
                    'name': v.__name__,
                    'description': v.description,
                } for v in _plugins.values()
            ], key=lambda x: x['name'])[(filter['page'] - 1) * filter['limit']: filter['page'] * filter['limit']],
            'page':          filter['page'],
            'limit':         filter['limit'],
            'totalPages':    ceil(len(_plugins) / filter['limit']),
            'totalElements': len(_plugins),
        }
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def get(name: str) -> dict:
    try:
        plugin = _plugins.get(name)

        if not plugin:
            raise errors.NotFoundError(f'Plugin {name} not found')

        if plugin:
            return {
                'name':              plugin.__name__,
                'description':       plugin.description,
                'shchemaPrediction': plugin.scheme_prediction,
                'shchemaSample':     plugin.scheme_sample,
            }

    except errors.NotFoundError as e:
        logger.debug(f'NotFoundError: {e}')
        raise e
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def get_plugin(name: str) -> Plugin:
    try:

        plugin = _plugins.get(name)

        if not plugin:
            raise errors.NotFoundError(f'Plugin {name} not found')

        return plugin

    except errors.NotFoundError as e:
        logger.debug(f'NotFoundError: {e}')
        raise e
    
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)
    

def _load_plugins():
    try:
        plugin_files = []
        
        for path, _, files in walk('plugins'):
            for file in files:
                plugin_file = splitext(file)
                
                if plugin_file[1] == '.py' and plugin_file[0] != 'base_plugin':
                    plugin_files.append(join(path, plugin_file[0]).replace('\\', '.').replace('/', '.'))

        for plugin_file in plugin_files:
                __import__(plugin_file)

        for plugin in Plugin.__subclasses__():
            if plugin.__name__ in _plugins:
                logger.warning(f'There is already a plugin named {plugin.__name__}')
                continue

            _plugins[plugin.__name__] = plugin
            plugin.on_load()
            
            logger.info(f'Plugin {plugin.__name__} loaded')
    
    except Exception as e:
        logger.error(f'Error: {e}')


_load_plugins()
