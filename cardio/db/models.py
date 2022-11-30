from pymongo.database import Database


class Model:
    def __init__(self, db:Database) -> None:
        self.db = db
        self.collection_name = 'models'
        pass

    def get(self, id: str) -> dict:
        return self.db[self.collection_name].find_one({'_id': id})
