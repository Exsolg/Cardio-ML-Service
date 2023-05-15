from flask_restx.reqparse import RequestParser


create_parser = RequestParser()
create_parser.add_argument('name',        type=str, required=True)
create_parser.add_argument('description', type=str)
create_parser.add_argument('plugins',     type=list, required=True)
