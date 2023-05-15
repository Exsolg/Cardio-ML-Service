from pymongo.collection import Collection


_models_repository: Collection | None = None


def init_repositories(db):
    global _models_repository
    _models_repository = db['models']


def get_models_repository() -> Collection:
    global _models_repository
    return _models_repository
