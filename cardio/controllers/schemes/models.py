from flask_restx import Model, fields
from cardio.controllers.schemes.base import page
from cardio.controllers.schemes.plugins import plugin


prediction = Model('predict', {
    'prediction': fields.Raw(attribute='prediction'),
})

simple_model = Model('simple_model', {
    'id':          fields.String(attribute='_id'),
    'createdAt':   fields.DateTime,
    'score':       fields.Raw(attribute='score'),
    'plugin':      fields.String()
})

model = simple_model.clone('model', {
    'params':  fields.Raw(attribute='params'),
    'plugin':  fields.Nested(plugin, skip_none=True),
})

models = page.clone('models', {
    'contents': fields.List(fields.Nested(simple_model, skip_none=True)),
})
