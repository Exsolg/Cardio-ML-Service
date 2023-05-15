from flask_restx import Model, fields


data = Model('create_data', {
    'sample': fields.Raw(attribute='sample'),
    'target': fields.Raw(attribute='target'),
})

data_list = Model('create_data_list', {
    'data': fields.List(fields.Nested(data))
})
