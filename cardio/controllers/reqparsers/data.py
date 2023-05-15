from flask_restx import Model, fields


data = Model('create_data', {
    'sample': fields.Raw(attribute='sample'),
    'prediction': fields.Raw(attribute='prediction'),
})
