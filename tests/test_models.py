from cardio.db.repositories import init_repositories
from cardio.db import models
from cardio.db.enums import For
from cardio.tests.config import Config
from pymongo import MongoClient
import uuid


db = MongoClient(f'mongodb://{Config.MONGO_USER}:{Config.MONGO_PASSWORD}@{Config.MONGO_HOST}:{Config.MONGO_PORT}/?authMechanism=DEFAULT')
db.drop_database(Config.MONGO_TEST_DB_NAME)
init_repositories(db[Config.MONGO_TEST_DB_NAME])


def test_create():
    model = {
        'description': 'description'
    }
    _for = For.COVID

    _id = models.create(model, _for)

    assert _id
    assert uuid.UUID(_id)


def test_get():
    model = {
        'description': 'description'
    }

    _id = models.create(model, For.COVID)

    db_model = models.get(_id, For.COVID)
    assert model['_id'] == _id
    assert model['description'] == db_model['description']
    assert model['for'] == For.COVID
    assert model['created_at'] is not None
    assert model.get('deleted_at') is None

    db_model = models.get(_id)
    assert model['_id'] == _id
    assert model['description'] == db_model['description']
    assert model['for'] == For.COVID
    assert model['created_at'] is not None
    assert model.get('deleted_at') is None

    db_model = models.get(str(uuid.uuid4()), For.COVID)
    assert db_model is None

    db_model = models.get('', For.COVID)
    assert db_model is None

    db_model = models.get(_id, For.CABS)
    assert db_model is None


def test_delete():
    model = {
        'description': 'description'
    }

    _id = models.create(model, For.COVID)

    deleted_model = models.delete(_id, For.COVID)
    assert deleted_model is True

    deleted_model = models.delete(str(uuid.uuid4()), For.COVID)
    assert deleted_model is None

    deleted_model = models.delete('', For.COVID)
    assert deleted_model is None

    _id = models.create(model, For.COVID)

    deleted_model = models.delete(_id, For.CABS)
    assert deleted_model is None

    deleted_model = models.delete(_id)
    assert deleted_model is True


def test_get_list():
    model = {
        'description': 'description'
    }

    mdls_covid = [
        models.create(model, For.COVID),
        models.create(model, For.COVID),
        models.create(model, For.COVID),
        models.create(model, For.COVID),
        models.create(model, For.COVID)
    ]
    mdls_cabs = [
        models.create(model, For.CABS),
        models.create(model, For.CABS),
        models.create(model, For.CABS),
        models.create(model, For.CABS),
        models.create(model, For.CABS),
    ]

    db_mdls = models.get_list()
    assert db_mdls
    assert len(db_mdls) == len(mdls_covid) + len(mdls_cabs)
    # assert db_mdls['contents']
    # assert db_mdls['page']
    # assert db_mdls['limit']
    # assert db_mdls['total_pages']
    # assert db_mdls['total_elements']
    for m in db_mdls:
        assert m['_id'] in mdls_covid or m['_id'] in mdls_cabs
    
    db_mdls = models.get_list(_for=For.COVID)
    assert db_mdls
    assert len(db_mdls) == len(mdls_covid)
    for m in db_mdls:
        assert m['_id'] in mdls_covid
        assert m['_id'] not in mdls_cabs
    
    db_mdls = models.get_list(_for=For.CABS)
    assert db_mdls
    assert len(db_mdls) == len(mdls_cabs)
    for m in db_mdls:
        assert m['_id'] in mdls_cabs
        assert m['_id'] not in mdls_covid
    
    db_mdls = models.get_list(limit=3)
    assert db_mdls
    assert len(db_mdls) == 3
    for m in db_mdls:
        assert m['_id'] in mdls_covid or m['_id'] in mdls_cabs
    
    db_mdls = models.get_list(limit=7)
    assert db_mdls
    assert len(db_mdls) == 7
    for m in db_mdls:
        assert m['_id'] in mdls_covid or m['_id'] in mdls_cabs
    
    db_mdls = models.get_list(limit=3, page=1)
    assert db_mdls
    assert len(db_mdls) == 3
    for m in db_mdls:
        assert m['_id'] in mdls_covid or m['_id'] in mdls_cabs
    
    mdls = mdls_covid + mdls_cabs

    db_mdls = models.get_list(limit=3, page=0)
    assert db_mdls
    assert len(db_mdls) == 3
    for m in db_mdls:
        assert m['_id'] in mdls[:3]
    
    db_mdls = models.get_list(limit=3, page=1)
    assert db_mdls
    assert len(db_mdls) == 3
    for m in db_mdls:
        assert m['_id'] in mdls[3:6]
    
    db_mdls = models.get_list(limit=3, page=2)
    assert db_mdls
    assert len(db_mdls) == 3
    for m in db_mdls:
        assert m['_id'] in mdls[6:9]
