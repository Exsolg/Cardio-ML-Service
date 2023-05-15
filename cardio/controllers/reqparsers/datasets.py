from flask_restx import Model, fields


create = Model('create_dataset', {
    'name':  fields.String,
    'description': fields.String,
    'plugins': fields.List(fields.String),
})

update = create.clone('update_dataset', {})
