from flask_restx import Model, fields
from cardio.controllers.schemes.base import page
from cardio.controllers.schemes.plugins import simple_plugin


simple_dataset = Model('simple_dataset', {
    'id':            fields.String(attribute='_id'),
    'name':          fields.String,
    'description':   fields.String,
    'trainingSteps': fields.Integer,
    'newData':       fields.Integer,
    'dataCount':     fields.Integer,
    'modelsCount':   fields.Integer,
    'createdAt':     fields.DateTime,
    'bestModelId':   fields.String,
    'plugins':       fields.List(fields.String),
})

dataset = simple_dataset.clone('dataset', {
    'plugins': fields.List(fields.Nested(simple_plugin, skip_none=True)),
})

datasets = page.clone('datasets', {
    'contents': fields.List(fields.Nested(simple_dataset, skip_none=True)),
})

training_status = Model('training_status', {
    'participatesInTraining': fields.Boolean,
    'numberInQueue':          fields.String,
    'plugin':                 fields.String,
    'plugins':                fields.List(fields.String),
    'progress':               fields.Integer,
    'trainingStartDate':      fields.DateTime,
})
