from pymongo.collection import Collection


_models_repository:   Collection | None = None
_datasets_repository: Collection | None = None
_data_repository:  Collection | None = None


def init(db):
    global _models_repository
    global _datasets_repository
    global _data_repository

    _models_repository =   db['models']
    _datasets_repository = db['datasets']
    _data_repository =  db['data']


def models() -> Collection:
    global _models_repository
    return _models_repository

def datasets() -> Collection:
    global _datasets_repository
    return _datasets_repository

def data() -> Collection:
    global _data_repository
    return _data_repository
