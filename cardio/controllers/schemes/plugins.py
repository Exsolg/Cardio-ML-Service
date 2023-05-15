from flask_restx import Model, fields
from cardio.controllers.schemes.base import page_schema


schema_schema = Model('schema', {
    'type':       fields.String,
    'items':      fields.Raw(attribute=lambda x: {i: v for i, v in x['items'].items()      if v} if x.get('items')      else None),
    'properties': fields.Raw(attribute=lambda x: {i: v for i, v in x['properties'].items() if v} if x.get('properties') else None),
})

simple_plugin_schema = Model('simple_plugin', {
    'name':         fields.String,
    'description':  fields.String,
})

plugin_schema = simple_plugin_schema.clone('plugin', {
    'scheme_train':   fields.Nested(schema_schema, skip_none=True),
    'scheme_predict': fields.Nested(schema_schema, skip_none=True),
})

plugins_schema = page_schema.clone('plugins', {
    'contents': fields.List(fields.Nested(simple_plugin_schema, skip_none=True)),
})
