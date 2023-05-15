from flask_restx import Model, fields
from cardio.controllers.schemes.base import page


schema = Model('schema', {
    'type':       fields.String,
    'properties': fields.Raw(attribute='properties'),
    'required':   fields.List(fields.String)
})

simple_plugin = Model('simple_plugin', {
    'name':         fields.String,
    'description':  fields.String,
})

plugin = simple_plugin.clone('plugin', {
    'shchemaSample':     fields.Nested(schema, skip_none=True),
    'shchemaPrediction': fields.Nested(schema, skip_none=True),
})

plugins = page.clone('plugins', {
    'contents': fields.List(fields.Nested(simple_plugin, skip_none=True)),
})
