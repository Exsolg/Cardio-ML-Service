from cardio.tools.base_plugin import Plugin

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score

from pandas import DataFrame
from joblib import dump, load
from uuid import uuid4
from os.path import exists
from os import makedirs


class Test(Plugin):
    description = 'Тестовый плагин'
    
    scheme_sample: dict = {
        'type': 'object',
        'properties': {
            'x': {
                'type': 'integer',
            },
            'y': {
                'type': 'integer',
            },
        }
    }
    
    scheme_prediction: dict = {
        'type': 'object',
        'properties': {
            'z': {
                'type': 'integer',
            },
        }
    }

    def __init__(self) -> None:
        self.model: DecisionTreeClassifier = None
        self.x_test = None
        self.y_test = None
        self.x_train = None
        self.y_train = None


    def train(self, data: list):
        data = self._prepare_data(data)
        x_train, x_test, y_train, y_test = train_test_split(data.drop('z', axis=1), data['z'], random_state=1, test_size=0.3)

        self.x_test = x_test
        self.y_test = y_test

        self.model = DecisionTreeClassifier(random_state=1)
        self.model.fit(x_train, y_train)

    def predict(self, data) -> float:
        ...
    
    def get_params(self,) -> dict:
        return self.model.get_params()
    
    def get_score(self) -> dict:
        return {
            'f1': f1_score(self.y_test, self.model.predict(self.x_test), average='weighted'),
            'recall': recall_score(self.y_test, self.model.predict(self.x_test), average='weighted'),
            'precision': precision_score(self.y_test, self.model.predict(self.x_test), average='weighted'),
            'accuracy': accuracy_score(self.y_test, self.model.predict(self.x_test)),
            }

    def load_from_file(self, file: str) -> None:
        self.model = load(file)

    def save_in_file(self) -> str:
        path = f'models/test/{str(uuid4())}.joblib'
        dump(self.model, path)
        return path

    def on_load() -> None:
        if not exists('models/test'):
            makedirs('models/test')

    def _prepare_data(self, data: list) -> DataFrame:
        data = [{
            'x': i['sample']['x'],
            'y': i['sample']['y'],
            'z': i['prediction']['z'],
        } for i in data]

        return DataFrame(data)
