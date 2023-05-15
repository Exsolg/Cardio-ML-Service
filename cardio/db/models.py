from cardio.db.db import db


class Model:
    collection_name = 'models'

    @staticmethod
    def get(id: str) -> dict:
        print('GET:', db)
        return db[Model.collection_name].find_one({'_id': id})
