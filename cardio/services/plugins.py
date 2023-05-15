from cardio.services.errors import NotFoundError
from plugins.base_plugin import Plugin
from os import walk
from os.path import splitext, join


_plugins: list[Plugin] = []


def get_list() -> list[dict]:
    return [{
        'name': i.__name__,
        'description': i.description,
        'scheme_response': i.scheme_response,
        'scheme_training': i.scheme_training,
        } for i in _plugins]


def get(name: str) -> Plugin:
    for i in _plugins:
        if i.__name__ == name:
            return i
    raise NotFoundError('Plugin {name} not found')


def _load_plugins():
    plugin_files = []
    
    for path, _, files in walk('plugins'):
        for file in files:
            plugin_file = splitext(file)
            
            if plugin_file[1] == '.py' and plugin_file[0] != 'base_plugin':
                plugin_files.append(join(path, plugin_file[0]).replace('\\', '.').replace('/', '.'))

    for plugin_file in plugin_files:
            __import__(plugin_file)

    for plugin in Plugin.__subclasses__():
        if plugin.__name__ in [type(i).__name__ for i in _plugins]:
            print(f'There is already a plugin named {plugin.__name__}')
            continue

        _plugins.append(plugin)
        _plugins[-1].on_load()
        print(f'Plugin {plugin.__name__} loaded')


_load_plugins()
