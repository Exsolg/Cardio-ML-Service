from pymongo.database import Database


db: Database | None = None


def init_db(_db: Database):
    print('INIT:', _db)
    global db
    db = _db 
    print(type(db))
