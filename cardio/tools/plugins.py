from cardio.tools.base_plugin import Plugin
from os import walk
from os.path import splitext, join
from loguru import logger


_plugins: dict[Plugin] = {}


def get(name: str) -> Plugin:
    return _plugins.get(name)


def gelt_list(skip: int = None, limit: int = None) -> list[Plugin]:
    plugins = list(sorted([i for i in _plugins.values()], key=lambda x: x.__name__))

    if skip:
        plugins = plugins[skip:]
    if limit:
        plugins = plugins[:limit]
    
    return plugins, len(_plugins)


def init(directory: str) -> None:
    try:
        if directory[:2] == './' or directory[:2] == '.\\':
            directory = directory[2:]
        
        plugin_files = []
        
        for path, _, files in walk(directory):
            for file in files:
                plugin_file = splitext(file)
                
                if plugin_file[1] == '.py':
                    plugin_files.append(join(path, plugin_file[0]).replace('\\', '.').replace('/', '.'))

        if not plugin_files:
            logger.warning(f'There are no .py files in the directory {directory}')

        for plugin_file in plugin_files:
                __import__(plugin_file)

        if not Plugin.__subclasses__():
            logger.warning(f'No plugins found in directory {directory}')

        for plugin in Plugin.__subclasses__():
            if plugin.__name__ in _plugins:
                logger.warning(f'There is already a plugin named {plugin.__name__}')
                continue

            # ТУТ проверять, что схема валидна

            _plugins[plugin.__name__] = plugin
            plugin.on_load()
            
            logger.info(f'Plugin {plugin.__name__} loaded')
    
    except Exception as e:
        logger.error(f'Error: {e}')
