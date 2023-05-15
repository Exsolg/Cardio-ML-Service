from flask_restx import Model, fields


page = Model('page', {
    'page':             fields.Integer,
    'limit':            fields.Integer,
    'totalPages':       fields.Integer,
    'totalElements':    fields.Integer,
})

error = Model('error', {
    'message': fields.String
})
