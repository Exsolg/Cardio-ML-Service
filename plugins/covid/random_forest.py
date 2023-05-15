from cardio.tools.base_plugin import Plugin
from cardio.tools.model_files import directory
from cardio.tools.helpers import grid_search
from cardio.tools.enums import Score

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score

import joblib
import json
from numpy import nan
from pandas import DataFrame, concat
from uuid import uuid4
from loguru import logger
from os.path import exists
from os import makedirs
from time import time


class CovidRandomForest(Plugin):
    description = '''
    Predicting covid-19 patient outcome using random forest method
    '''

    scheme_sample: dict = {
        'type': 'object',
        'properties': {
            'sex': {
                'type': 'string',
                'enum': ['male', 'female']
            },
            'age': {
                'type': 'integer'
            },
            'urea': {
                'type': 'number'
            },
            'creatinine': {
                'type': 'number'
            },
            'SKF': {
                'type': 'number'
            },
            'AST': {
                'type': 'number'
            },
            'ALT': {
                'type': 'number'
            },
            'CRP': {
                'type': 'number'
            },
            'glucose': {
                'type': 'number'
            },
            'leukocytes': {
                'type': 'number'
            },
            'platelets': {
                'type': 'number'
            },
            'neutrophils': {
                'type': 'number'
            },
            'lymphocytes': {
                'type': 'number'
            },
            'neutrophilLymphocyteRatio': {
                'type': 'number'
            },
            'DDimer': {
                'type': 'number'
            },
            'severity': {
                'type': 'string',
                'enum': ['light', 'medium', 'severe']
            },
            'AG': {
                'type': 'boolean'
            },
            'SD': {
                'type': 'boolean'
            },
            'IBS': {
                'type': 'boolean'
            },
            'HOBL': {
                'type': 'boolean'
            },
            'HBP': {
                'type': 'boolean'
            },
        },
        'required': ['sex', 'age', 'severity'],
    }


    scheme_prediction: dict = {
        'type': 'object',
        'properties': {
            'survived': {
                'type': 'boolean',
            },
        },
        'required': ['survived'],
    }

    plugin_dir = 'covid_random_forest'


    def __init__(self) -> None:
        self.model: RandomForestClassifier = None
        self.x_test =  None
        self.y_test =  None
        self.medians = {}
        self.progress = 0


    def train(self, data: list[dict]) -> None:
        data: DataFrame = self._prepare_data(data)

        logger.info(list(data.columns))

        x_train, x_test, y_train, y_test = train_test_split(data.drop('survived', axis=1), data['survived'], random_state=1, test_size=0.3)

        self.x_test = x_test
        self.y_test = y_test

        self.model = grid_search(RandomForestClassifier,
                                 {
                                     'criterion': ['gini', 'entropy'],
                                     'n_estimators': list(range(1, 21, 2)),
                                     'max_depth': list(range(5, 51, 2)),
                                     'min_samples_split': list(range(10, 51, 10)),
                                     'random_state': [int(time())]
                                 },
                                 lambda model: model.fit(x_train, y_train),
                                 lambda model: f1_score(self.y_test, model.predict(self.x_test), average='weighted'),
                                 self._set_progress
                                 )


    def predict(self, data: list[dict]) -> list[dict]:
        samples = self._prepare_samples(data)
        predictions = self.model.predict(samples)
        return [{'survived': bool(i)} for i in predictions]


    def get_params(self,) -> dict:
        return self.model.get_params()
    
    
    def get_score(self) -> dict:
        return {
            Score.F1:           f1_score(self.y_test, self.model.predict(self.x_test), average='weighted'),
            Score.RECALL:       recall_score(self.y_test, self.model.predict(self.x_test), average='weighted'),
            Score.PRECISION:    precision_score(self.y_test, self.model.predict(self.x_test), average='weighted'),
            Score.ACCURACY:     accuracy_score(self.y_test, self.model.predict(self.x_test)),
            }


    def load_from_file(self, path: str) -> None:
        self.model = joblib.load(f'{directory()}/{path}/model.joblib')

        with open(f'{directory()}/{path}/medians.json', 'r', encoding='utf-8') as f:
            self.medians = json.load(f)


    def save_in_file(self) -> str:
        path = f'{CovidRandomForest.plugin_dir}/{str(uuid4())}'
        dir_path = f'{directory()}/{path}'

        makedirs(dir_path)

        joblib.dump(self.model, f'{dir_path}/model.joblib')

        with open(f'{dir_path}/medians.json', 'w', encoding='utf-8') as f:
            json.dump(self.medians, f, ensure_ascii=False, indent=4)

        return path


    def on_load() -> None:
        if not exists(f'{directory()}/{CovidRandomForest.plugin_dir}'):
            makedirs(f'{directory()}/{CovidRandomForest.plugin_dir}')


    def get_progress(self) -> int:
        return self.progress

    def _set_progress(self, progress: int) -> None:
        self.progress = progress

    def _prepare_data(self, data: list[dict]) -> DataFrame:
        df = DataFrame(columns=list(self.scheme_sample['properties'].keys()) + list(self.scheme_prediction['properties'].keys()))

        data: DataFrame = concat([df, DataFrame([{**i['sample'], **i['prediction']} for i in data])])

        data.loc[data.sex == 'male',   'sex'] = 0.
        data.loc[data.sex == 'female', 'sex'] = 1.

        data.loc[data['severity'] == 'light',   ['severity_light', 'severity_medium', 'severity_severe']] = [1.0, 0.0, 0.0]
        data.loc[data['severity'] == 'medium',  ['severity_light', 'severity_medium', 'severity_severe']] = [0.0, 1.0, 0.0]
        data.loc[data['severity'] == 'severe',  ['severity_light', 'severity_medium', 'severity_severe']] = [0.0, 0.0, 1.0]

        data = data.drop('severity', axis=1)

        data = data.astype('float64')
        
        self.medians = dict(data.drop(['severity_light', 'severity_medium', 'severity_severe'], axis=1).median().dropna())
        
        data = data.fillna(self.medians)
        data = data.fillna(0.0)
        
        return data

    def _prepare_samples(self, data: list[dict]) -> DataFrame:
        df = DataFrame(columns=list(self.scheme_sample['properties'].keys()))

        data: DataFrame = concat([df, DataFrame([{**i['sample']} for i in data])])

        data.loc[data.sex == 'male',   'sex'] = 0.
        data.loc[data.sex == 'female', 'sex'] = 1.

        data.loc[data['severity'] == 'light',   ['severity_light', 'severity_medium', 'severity_severe']] = [1.0, 0.0, 0.0]
        data.loc[data['severity'] == 'medium',  ['severity_light', 'severity_medium', 'severity_severe']] = [0.0, 1.0, 0.0]
        data.loc[data['severity'] == 'severe',  ['severity_light', 'severity_medium', 'severity_severe']] = [0.0, 0.0, 1.0]

        data = data.drop('severity', axis=1)

        data = data.fillna(self.medians)
        data = data.fillna(0.0)

        return data
