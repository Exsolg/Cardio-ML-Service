from config import Config
from fastapi import FastAPI
from cardio.app import create_app
from uvicorn import run

app: FastAPI | None = None


def main():
    global app
    app = create_app(Config)


if __name__ == 'main':
    main()


if __name__ == '__main__':
    main()
    run(app, host=Config.HOST, port=Config.PORT)
