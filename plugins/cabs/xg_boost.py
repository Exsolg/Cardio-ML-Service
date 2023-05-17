from cardio.tools.base_plugin import Plugin
from cardio.tools.model_files import directory
from cardio.tools.helpers import grid_search
from cardio.tools.enums import Score

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score
from xgboost import XGBClassifier

import joblib
import json
from numpy import linspace
from pandas import DataFrame, concat
from uuid import uuid4
from loguru import logger
from os.path import exists
from os import makedirs
from time import time


class CabsXGBoost(Plugin):
    description = '''
    Predicting cabs patient outcome using XGBoost method
    '''

    scheme_sample: dict
    scheme_prediction: dict
    plugin_dir = 'cabs_xg_boost'


    def __init__(self) -> None:
        self.model: XGBClassifier = None
        self.x_test =  None
        self.y_test =  None
        self.medians = {}
        self.progress = 0


    def train(self, data: list[dict]) -> None:
        data: DataFrame = self._prepare_data(data)

        logger.info(list(data.columns))

        x_train, x_test, y_train, y_test = train_test_split(
            data.drop(['MI', 'CI', 'insultOutcome', 'death', 'comb'], axis=1), 
            data[['MI', 'CI', 'insultOutcome', 'death', 'comb']],
            random_state=int(time()),
            test_size=0.2
        )

        self.x_test = x_test
        self.y_test = y_test

        self.model = grid_search(XGBClassifier, {
            'n_estimators': list(range(20, 161, 20)),
            'max_depth': list(range(5, 51, 4)),
            'min_child_weight': list(range(1, 12, 2)),
            'subsample': linspace(0.3, 1, 3),
            'colsample_bytree': linspace(0.3, 1, 3),
            'random_state': [int(time())]
        },
        lambda model: model.fit(x_train, y_train),
        lambda model: f1_score(self.y_test, model.predict(self.x_test), average='weighted'),
        self._set_progress
        )


    def predict(self, data: list[dict]) -> list[dict]:
        samples = self._prepare_samples(data)
        predictions = self.model.predict(samples)
        return [{
            'MI': bool(i[0]),
            'CI': bool(i[1]),
            'insultOutcome': bool(i[2]),
            'death': bool(i[3]),
            'comb': bool(i[4]),
        } for i in predictions]


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
        path = f'{CabsXGBoost.plugin_dir}/{str(uuid4())}'
        dir_path = f'{directory()}/{path}'

        makedirs(dir_path)

        joblib.dump(self.model, f'{dir_path}/model.joblib')

        with open(f'{dir_path}/medians.json', 'w', encoding='utf-8') as f:
            json.dump(self.medians, f, ensure_ascii=False, indent=4)

        return path


    def on_load() -> None:
        if not exists(f'{directory()}/{CabsXGBoost.plugin_dir}'):
            makedirs(f'{directory()}/{CabsXGBoost.plugin_dir}')

        with open('./plugins/cabs/schemas/data_schema.json', 'r') as file:
            CabsXGBoost.scheme_sample = json.load(file)

        with open('./plugins/cabs/schemas/outcome_schema.json', 'r') as file:
            CabsXGBoost.scheme_prediction = json.load(file)


    def get_progress(self) -> int:
        return self.progress

    def _set_progress(self, progress: int) -> None:
        self.progress = progress

    def _prepare_data(self, data: list[dict]) -> DataFrame:
        sample_keys =     self.scheme_sample['properties'].keys()
        prediction_keys = self.scheme_prediction['properties'].keys()

        df = DataFrame(columns=list(self.scheme_sample['properties'].keys()) + list(self.scheme_prediction['properties'].keys()))

        data: DataFrame = concat([df, DataFrame([
                {k: v for k, v in i['sample'].items() if k in sample_keys} | {k: v for k, v in i['prediction'].items() if k in prediction_keys}
                for i in data
            ])])

        data.loc[data.sex == 'male',   'sex'] = 0.
        data.loc[data.sex == 'female', 'sex'] = 1.

        data['anginaFuncClass'] = data.loc[:, ('anginaFuncClass')].map({'1-2': 0, '3-4': 1})
        data['chronicHeartFailureFuncClass'] = data.loc[:, ('chronicHeartFailureFuncClass')].map({'1-2': 0, '3': 1})
        data['cardioplegiaNumber'] = data.loc[:, ('cardioplegiaNumber')].map({'0-2': 0, '3-4': 1})
        data['revascularizationIdx'] = data.loc[:, ('revascularizationIdx')].map({'2-3': 0, '4-5': 1})

        for column in ['litaDischarge', 'ritaDischarge']:
            data.loc[data[column] == 'skeleton',   [f'{column}_skeleton', f'{column}_flap', f'{column}_no']] = [1.0, 0.0, 0.0]
            data.loc[data[column] == 'flap',  [f'{column}_skeleton', f'{column}_flap', f'{column}_no']] = [0.0, 1.0, 0.0]
            data.loc[data[column] == 'no',  [f'{column}_skeleton', f'{column}_flap', f'{column}_no']] = [0.0, 0.0, 1.0]

            data = data.drop(column, axis=1)
        
            self.medians = dict(data.drop([f'{column}_skeleton', f'{column}_flap', f'{column}_no'], axis=1).median().dropna())

        data = data.astype('float64')

        data = data.fillna(self.medians)
        data = data.fillna(0.0)
        
        return data

    def _prepare_samples(self, data: list[dict]) -> DataFrame:
        df = DataFrame(columns=list(self.scheme_sample['properties'].keys()))

        data: DataFrame = concat([df, DataFrame([{**i['sample']} for i in data])])

        data.loc[data.sex == 'male',   'sex'] = 0.
        data.loc[data.sex == 'female', 'sex'] = 1.

        data['anginaFuncClass'] = data.loc[:, ('anginaFuncClass')].map({'1-2': 0, '3-4': 1})
        data['chronicHeartFailureFuncClass'] = data.loc[:, ('chronicHeartFailureFuncClass')].map({'1-2': 0, '3': 1})
        data['cardioplegiaNumber'] = data.loc[:, ('cardioplegiaNumber')].map({'0-2': 0, '3-4': 1})
        data['revascularizationIdx'] = data.loc[:, ('revascularizationIdx')].map({'2-3': 0, '4-5': 1})

        for column in ['litaDischarge', 'ritaDischarge']:
            data.loc[data[column] == 'skeleton',   [f'{column}_skeleton', f'{column}_flap', f'{column}_no']] = [1.0, 0.0, 0.0]
            data.loc[data[column] == 'flap',  [f'{column}_skeleton', f'{column}_flap', f'{column}_no']] = [0.0, 1.0, 0.0]
            data.loc[data[column] == 'no',  [f'{column}_skeleton', f'{column}_flap', f'{column}_no']] = [0.0, 0.0, 1.0]

            data = data.drop(column, axis=1)

        data = data.astype('float64')

        data = data.fillna(self.medians)
        data = data.fillna(0.0)

        return data
