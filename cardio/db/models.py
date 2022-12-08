from cardio.db.repositoryes import get_models_repository


def get(id: str) -> dict:
    model_repo = get_models_repository()
    return model_repo.find_one({'_id': id})


def get_list() -> list:
    model_repo = get_models_repository()
    return list(model_repo.find())
