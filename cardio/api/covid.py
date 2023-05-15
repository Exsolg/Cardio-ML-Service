from flask_restx import Resource, Namespace
from cardio.controllers import covid
from cardio.api.reqparsers import covid_predict_parser
from cardio.api.schemes import predict_schema, model_schema


covid_api = Namespace('covid')
covid_api.models['predict'] = predict_schema
covid_api.models['model'] = model_schema

@covid_api.route('/')
class Model(Resource):
    def get(self):
        models = covid.get_list()
        return str(models)


@covid_api.route('/<id>',)
class Model(Resource):
    @covid_api.marshal_with(model_schema)
    def get(self, id):
        model = covid.get(id)
        return str(model)


@covid_api.route('/<id>/predict')
class Model(Resource):
    @covid_api.marshal_with(predict_schema)
    def post(self, id):
        args = covid_predict_parser.parse_args()
        return covid.predict(id, args)
