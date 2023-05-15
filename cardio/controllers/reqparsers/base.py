from flask_restx.reqparse import RequestParser


get_list = RequestParser()
get_list.add_argument('page', type=int, default=1)
get_list.add_argument('limit', type=int, default=10)
