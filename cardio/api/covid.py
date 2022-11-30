from flask_restx import Resource, Namespace


covid_api = Namespace('covid')


@covid_api.route('/<id>',)
class Model(Resource):
    def get(self, id):
        return id
