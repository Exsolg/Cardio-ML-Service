from flask_restx import Model, fields

predict_schema = Model('predict', {
    'predict': fields.Float(min=0, max=1)
})

score_schema = Model('score', {
        'f1':           fields.Float(min=0, max=1),
        'recall':       fields.Float(min=0, max=1),
        'precision':    fields.Float(min=0, max=1),
        'accuracy':     fields.Float(min=0, max=1),
})

simple_model_schema = Model('simple_model', {
    'id':           fields.String(attribute='_id'),
    'method':       fields.String,
    'for':          fields.String,
    'created_at':   fields.DateTime,
    'score':        fields.Nested(score_schema, skip_none=True),
    'description':  fields.String
})

model_schema = simple_model_schema.clone('model', {
    'params': fields.Raw(attribute=lambda x: {i: v for i, v in x['params'].items() if v})
})

models_schema = Model('models', {
    'contents':         fields.List(fields.Nested(simple_model_schema, skip_none=True)),
    'page':             fields.Integer,
    'limit':            fields.Integer,
    'totalPapes':       fields.Integer,
    'totalElements':    fields.Integer 
})

error_schema = Model('error', {
    'message': fields.String
})