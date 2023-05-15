from flask_restx import Model, fields
from cardio.controllers.schemes.base import page
from cardio.controllers.schemes.datasets import simple_dataset


simple_data = Model('simple_data', {
    'id':      fields.String(attribute='_id'),
    'sample':  fields.Raw(attribute='sample'),
    'target':  fields.Raw(attribute='target'),
    'dataset': fields.String(attribute='datasetId'),
})

data = simple_data.clone('data', {
    'dataset': fields.Nested(simple_dataset, skip_none=True),
})

data_list = page.clone('data_list', {
    'contents': fields.List(fields.Nested(simple_data, skip_none=True)),
})
