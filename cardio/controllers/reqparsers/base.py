from flask_restx.reqparse import RequestParser


get_list_parser = RequestParser()
get_list_parser.add_argument('page', type=int, default=1)
get_list_parser.add_argument('limit', type=int, default=5)
