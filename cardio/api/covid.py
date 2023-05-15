from flask_restx import Resource, Namespace
from cardio.controllers.covid import CovidController 


covid_api = Namespace('covid')


@covid_api.route('/<id>',)
class Model(Resource):
    def get(self, id):
        model = CovidController.get(id)
        return str(model)
