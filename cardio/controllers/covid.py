from cardio.db import models


def get(id: str):
    return models.get(id)


def get_list():
    return models.get_list()


def predict(id: str, params: dict):
    
    return 0
