from flask_restx import Resource, Namespace


cabs_api = Namespace('cabs')


@cabs_api.route('/<id>')
class Model(Resource):
    def get(self, id):
        print(id)
        return id
