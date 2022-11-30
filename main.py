from config import Config
from cardio.app import create_app


def main():
    create_app(Config).run()


if __name__ == '__main__':
    main()
