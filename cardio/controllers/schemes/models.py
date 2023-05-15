from flask_restx import Model, fields
from cardio.controllers.schemes.base import page
from cardio.controllers.schemes.datasets import simple_dataset


score = Model('score', {
    'name':  fields.String,
    'value': fields.Float(min=0, max=1),
})

prediction = Model('predict', {
    'prediction': fields.Raw(attribute='prediction'),
})

simple_model = Model('simple_model', {
    'id':          fields.String(attribute='_id'),
    'created_at':  fields.DateTime,
    'description': fields.String,
    'score':       fields.Raw(attribute='score'),
    'dataset':     fields.String,
})

model = simple_model.clone('model', {
    'params':            fields.Raw(attribute='params'),
    'dataset':           fields.Nested(simple_dataset, skip_none=True),
})

models = page.clone('models', {
    'contents': fields.List(fields.Nested(simple_model, skip_none=True)),
})
