from flask_restx.reqparse import RequestParser, FileStorage
from flask_restx.inputs import boolean


covid_predict_parser = RequestParser()
covid_predict_parser.add_argument('age',                        type=int)
covid_predict_parser.add_argument('urea',                       type=float)
covid_predict_parser.add_argument('creatinine',                 type=float)
covid_predict_parser.add_argument('SKF',                        type=float)
covid_predict_parser.add_argument('AST',                        type=float)
covid_predict_parser.add_argument('ALT',                        type=float)
covid_predict_parser.add_argument('CRP',                        type=float)
covid_predict_parser.add_argument('glucose',                    type=float)
covid_predict_parser.add_argument('leukocytes',                 type=float)
covid_predict_parser.add_argument('platelets',                  type=float)
covid_predict_parser.add_argument('neutrophils',                type=float)
covid_predict_parser.add_argument('lymphocytes',                type=float)
covid_predict_parser.add_argument('neutrophil-lymphocyteRatio', type=float)
covid_predict_parser.add_argument('D-dimer',                    type=float)
covid_predict_parser.add_argument('severity',                   type=str, choices=['light', 'medium', 'severe'])
covid_predict_parser.add_argument('AG',                         type=boolean)
covid_predict_parser.add_argument('SD',                         type=boolean)
covid_predict_parser.add_argument('IBS',                        type=boolean)
covid_predict_parser.add_argument('HOBL',                       type=boolean)
covid_predict_parser.add_argument('HBP',                        type=boolean)

covid_model_create_parser = RequestParser()
covid_model_create_parser.add_argument('model', required=True, type=FileStorage, location='files')
