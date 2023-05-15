from os import getenv
from dotenv import load_dotenv
from  distutils.util import strtobool


load_dotenv()


class Config(object):
    MONGO_PORT =        int(getenv('CARDIO_MONGO_PORT',         default=27017))
    MONGO_HOST =            getenv('CARDIO_MONGO_HOST',         default='localhost')
    MONGO_DB_NAME =         getenv('CARDIO_MONGO_DB_NAME',      default='cardio')
    MONGO_TEST_DB_NAME =    getenv('CARDIO_MONGO_TEST_DB_NAME', default='cardio_test')
    MONGO_USER =            getenv('CARDIO_MONGO_USER',         default='admin')
    MONGO_PASSWORD =        getenv('CARDIO_MONGO_PASSWORD',     default='password')

    SECRET_KEY =            getenv('CARDIO_SECRET_KEY',         default='secret_key')
    PORT =              int(getenv('CARDIO_PORT',               default=80))
    HOST =                  getenv('CARDIO_HOST',               default='127.0.0.1')
    DEBUG =       strtobool(getenv('CARDIO_DEBUG',              default='false'))

    MODELS_DIR =            getenv('CARDIO_MODELS_DIR',         default='./models')
    PLUGINS_DIR =           getenv('CARDIO_PLUGINS_DIR',        default='./plugins')

    LOG_LEVEL =             getenv('CARDIO_LOG_LEVEL',          default='info')
    LOG_DIR =               getenv('CARDIO_LOG_DIR',            default='log')
