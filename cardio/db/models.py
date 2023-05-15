from cardio.db.repositoryes import get_models_repository
from cardio.db import enums
from uuid import uuid4
from datetime import datetime


def create(model: dict, _for: enums.For) -> str:
    model['_id'] = str(uuid4())
    model['for'] = _for
    model['create_date'] = datetime.utcnow()
    model['deleted'] = False
    model['delete_date'] = None

    try:
        model_repo = get_models_repository()
        return model_repo.insert_one(model).inserted_id
    except Exception as e:
        return None


def delete(id: str, _for: enums.For = None):
    filters = {'_id': id}

    if _for:
        filters['for'] = _for
    
    update = {'$set': {'deleted': True, 'delete_date': datetime.utcnow()}}

    try:
        model_repo = get_models_repository()
        return model_repo.update_one(filters, update).matched_count
    except Exception as e:
        return None


def get(id: str, _for: enums.For = None) -> dict:
    filters = {'_id': id}

    if _for:
        filters['for'] = _for

    try:
        model_repo = get_models_repository()
        return model_repo.find_one(filters)
    except Exception as e:
        return None


def get_list(_for: enums.For = None) -> list:
    filters = {}

    if _for:
        filters['for'] = _for

    try:
        model_repo = get_models_repository()
        return list(model_repo.find(filters))
    except Exception as e:
        return None
    
