from flask_restx import Model, fields
from cardio.controllers.schemes.base import page_schema


predict_schema = Model('predict', {
    'predict': fields.Float(min=0, max=1),
})

score_schema = Model('score', {
    'name': fields.String,
    'value': fields.Float(min=0, max=1),
})

simple_model_schema = Model('simple_model', {
    'id':           fields.String(attribute='_id'),
    'method':       fields.String,
    'for':          fields.String,
    'created_at':   fields.DateTime,
    'score':        fields.List(fields.Nested(score_schema, skip_none=True)),
    'description':  fields.String,
})

model_schema = simple_model_schema.clone('model', {
    'params': fields.Raw(attribute=lambda x: {i: v for i, v in x['params'].items() if v}),
})

models_schema = page_schema.clone('models', {
    'contents': fields.List(fields.Nested(simple_model_schema, skip_none=True)),
})
