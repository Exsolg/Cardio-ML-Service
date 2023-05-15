from flask_restx import Model, fields


page_schema = Model('page', {
    'page':             fields.Integer,
    'limit':            fields.Integer,
    'totalPages':       fields.Integer,
    'totalElements':    fields.Integer,
})

error_schema = Model('error', {
    'message': fields.String
})
