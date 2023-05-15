from flask_restx import Model, fields

predict_schema = Model('predict', {
    'predict': fields.Float
})

score_schema = Model('score', {
        'f1':           fields.Float,
        'recall':       fields.Float,
        'precision':    fields.Float,
        'accuracy':     fields.Float,
})


model_schema = Model('model', {
    'id':           fields.String(attribute='_id'),
    'method':       fields.String,
    'for':          fields.String,
    'create_date':  fields.String(attribute=lambda x: None if not x.get('create_date') else x['create_date'].isoformat()),
    'score':        fields.Nested(score_schema, skip_none=True)
})


models_schema = Model('models', {
    'models': fields.List(fields.Nested(model_schema, skip_none=True))
})

error_schema = Model('error', {
    'message': fields.String
})