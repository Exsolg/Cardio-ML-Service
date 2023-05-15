from flask_restx.reqparse import RequestParser, FileStorage
from flask_restx.inputs import boolean


covid_predict_parser = RequestParser()
covid_predict_parser.add_argument('sex',                        type=str, choices=['male', 'female'], required=True, location='json')
covid_predict_parser.add_argument('age',                        type=int, required=True, location='json')
covid_predict_parser.add_argument('urea',                       type=float, location='json')
covid_predict_parser.add_argument('creatinine',                 type=float, location='json')
covid_predict_parser.add_argument('SKF',                        type=float, location='json')
covid_predict_parser.add_argument('AST',                        type=float, location='json')
covid_predict_parser.add_argument('ALT',                        type=float, location='json')
covid_predict_parser.add_argument('CRP',                        type=float, location='json')
covid_predict_parser.add_argument('glucose',                    type=float, location='json')
covid_predict_parser.add_argument('leukocytes',                 type=float, location='json')
covid_predict_parser.add_argument('platelets',                  type=float, location='json')
covid_predict_parser.add_argument('neutrophils',                type=float, location='json')
covid_predict_parser.add_argument('lymphocytes',                type=float, location='json')
covid_predict_parser.add_argument('neutrophilLymphocyteRatio',  type=float, location='json')
covid_predict_parser.add_argument('DDimer',                     type=float, location='json')
covid_predict_parser.add_argument('severity',                   type=str,   choices=['light', 'medium', 'severe'], location='json')
covid_predict_parser.add_argument('AG',                         type=boolean, location='json')
covid_predict_parser.add_argument('SD',                         type=boolean, location='json')
covid_predict_parser.add_argument('IBS',                        type=boolean, location='json')
covid_predict_parser.add_argument('HOBL',                       type=boolean, location='json')
covid_predict_parser.add_argument('HBP',                        type=boolean, location='json')

covid_model_create_parser = RequestParser()
covid_model_create_parser.add_argument('model', required=True, type=FileStorage, location='files')
covid_model_create_parser.add_argument('description', type=str, location='json')

model_list_parser = RequestParser()
model_list_parser.add_argument('page', type=int, default=0)
model_list_parser.add_argument('limit', type=int, default=3)
