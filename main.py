from config import Config
from cardio.app import create_app


def main():
    create_app(Config).run(port=Config.PORT, debug=Config.DEBUG)


if __name__ == '__main__':
    main()
