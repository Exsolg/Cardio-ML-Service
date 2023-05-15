from flask_restx import Model, fields
from cardio.controllers.schemes.base import page
from cardio.controllers.schemes.datasets import simple_dataset


data = Model('data', {
    'id':      fields.String(attribute='_id'),
    'sample':  fields.Raw(attribute='sample'),
    'prediction':  fields.Raw(attribute='prediction'),
    'createdAt':   fields.DateTime,
})

data_list = page.clone('data_list', {
    'contents': fields.List(fields.Nested(data, skip_none=True)),
})
