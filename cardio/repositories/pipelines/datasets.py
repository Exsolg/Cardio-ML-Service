import pymongo


def get(id: str) -> list[dict]:     # ТУТ Исправить так, чтобы не учитывалась удаленная дата
    return [
        {'$match': {
           '_id': id,
           'deletedAt': None,
        }},
        {'$lookup': {
            'from': 'data',
            'localField': '_id',
            'foreignField': 'datasetId',
            'as': 'data',
        }},
        {'$set': {
            'dataCount': { '$cond': { 'if': { '$isArray': '$data' }, 'then': { '$size': "$data" }, 'else': 0} }
        }},
        {'$unset': 'data'},

        {'$lookup': {
            'from': 'models',
            'localField': '_id',
            'foreignField': 'datasetId',
            'as': 'models',
        }},
        {'$set': {
            'modelsCount': { '$cond': { 'if': { '$isArray': '$models' }, 'then': { '$size': "$models" }, 'else': 0} }
        }},
        {'$unset': 'models'},
    ]


def get_list(skip: int, limit: int, filter: dict):
    pipeline = [
        {'$sort': {
            'createdAt': pymongo.ASCENDING
        }},
    ]

    if filter:
        pipeline.append({'$match': {**filter}})
    
    if skip:
        pipeline.append({'$skip': skip})

    if limit:
        pipeline.append({'$limit': limit})
    
    pipeline.extend([
        {'$lookup': {
            'from': 'data',
            'localField': '_id',
            'foreignField': 'datasetId',
            'as': 'data',
        }},
        {'$set': {
            'dataCount': { '$cond': { 'if': { '$isArray': '$data' }, 'then': { '$size': "$data" }, 'else': 0} }
        }},
        {'$unset': 'data'},

        {'$lookup': {
            'from': 'models',
            'localField': '_id',
            'foreignField': 'datasetId',
            'as': 'models',
        }},
        {'$set': {
            'modelsCount': { '$cond': { 'if': { '$isArray': '$models' }, 'then': { '$size': "$models" }, 'else': 0} }
        }},
        {'$unset': 'models'},

        {'$sort': {'deletedAt': 1}}
    ])

    return pipeline
