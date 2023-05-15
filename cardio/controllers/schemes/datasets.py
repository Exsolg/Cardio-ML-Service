from flask_restx import Model, fields
from cardio.controllers.schemes.base import page_schema
from cardio.controllers.schemes.plugins import simple_plugin_schema


simple_dataset_schema = Model('simple_dataset', {
    'id':          fields.String(attribute='_id'),
    'name':        fields.String,
    'description': fields.String,
    'rowsCount':   fields.Integer,
    'plugins':     fields.List(fields.String),
})

dataset_schema = simple_dataset_schema.clone('dataset', {
    'plugins':      fields.List(fields.Nested(simple_plugin_schema, skip_none=True))
})

datasets_schema = page_schema.clone('datasets', {
    'contents': fields.List(fields.Nested(simple_dataset_schema, skip_none=True)),
})
