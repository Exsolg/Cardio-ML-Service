from flask_restx import Model, fields


create = Model('create_dataset', {
    'name':          fields.String(required=True),
    'description':   fields.String(required=False),
    'trainingSteps': fields.Integer(default=10, required=False),
    'plugins':       fields.List(fields.String, required=True),
})

update = Model('update_dataset', {
    'name':          fields.String(required=False),
    'description':   fields.String(required=False),
    'trainingSteps': fields.Integer(required=False),
    'plugins':       fields.List(fields.String, required=False),
})
