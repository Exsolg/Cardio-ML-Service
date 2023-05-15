from flask_restx import Model, fields


sample = Model('sample', {
    'sample': fields.Raw(attribute='sample'),
})
