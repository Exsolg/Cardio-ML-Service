import pymongo


def get(id: str) -> list[dict]:
    return [
        {'$match': {
           '_id': id 
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
        {'$unset': 'data'}
    ]


def get_list(skip: int, limit: int):
    return [
        {'$sort': {
            'created_at': pymongo.ASCENDING
        }},
        {'$skip': skip},
        {'$limit' : limit},
        {'$lookup': {
            'from': 'data',
            'localField': '_id',
            'foreignField': 'datasetId',
            'as': 'data',
        }},
        {'$set': {
            'dataCount': { '$cond': { 'if': { '$isArray': '$data' }, 'then': { '$size': "$data" }, 'else': 0} }
        }},
        {'$unset': 'data'}
    ]
