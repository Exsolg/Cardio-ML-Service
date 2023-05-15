from config import Config
from cardio.app import create_app
from jsonschema import validate


def main():
    create_app(Config).run(port=Config.PORT, host=Config.HOST, debug=Config.DEBUG)


if __name__ == '__main__':
    main()
