from cardio.tools.base_plugin import Plugin
from cardio.tools.errors import NotDirectoryError

from os.path import exists, isdir, abspath
from os import makedirs
from loguru import logger


_directory: str = ''


def directory() -> str:
    global _directory
    return _directory


def init(path: str) -> None:
    try:
        path = abspath(path)

        if not exists(path):
            makedirs(path)
        
        if not isdir(path):
            raise NotDirectoryError(f'{path} is not a directory')
        
        global _directory
        _directory = path

    except Exception as e:
        logger.error(f'Error: {e}')
        raise e
