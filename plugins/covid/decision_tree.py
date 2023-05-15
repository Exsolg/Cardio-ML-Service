from cardio.tools.base_plugin import Plugin
from joblib import dump, load
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score
import pandas
from uuid import uuid4
from os.path import exists
from os import makedirs


class CovidDecisionTree(Plugin):
    description = '''
    Predicting covid-19 patient outcome using decision tree method
    '''

    scheme_prediction: dict = {
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
        }
    }


    scheme_sample: dict = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': dict(scheme_prediction['properties'], survived={'type': 'boolean'}),
        },
    }


    def __init__(self) -> None:
        self.model: DecisionTreeClassifier = None
        self.x_test = None
        self.y_test = None


    def train(self, data):
        data = self._prepare_data(data)
        x_train, x_test, y_train, y_test = train_test_split(data.drop('survived', axis=1), data['survived'], random_state=1, test_size=0.3)

        self.model = DecisionTreeClassifier(random_state=1)
        self.model.fit(x_train, y_train)

        self.x_test = x_test
        self.y_test = y_test


    def predict(self, data) -> float:
        return 0.5


    def get_params(self,) -> dict:
        return self.model.get_params()
    
    
    def get_score(self,) -> list[dict]:
        return [
            {
                'name': 'f1',
                'value': f1_score(self.y_test, self.model.predict(self.x_test)),
            },
            {
                'name': 'recall',
                'value': recall_score(self.y_test, self.model.predict(self.x_test)),
            },
            {
                'name': 'precision',
                'value': precision_score(self.y_test, self.model.predict(self.x_test)),
            },
            {
                'name': 'accuracy',
                'value': accuracy_score(self.y_test, self.model.predict(self.x_test)),
            }
        ]


    def load_from_file(self, file: str) -> None:
        self.model = load(file)


    def save_in_file(self) -> str:
        path = f'models/covid_decision_tree/{str(uuid4())}.joblib'
        dump(self.model, path)
        return path


    def on_load() -> None:
        if not exists('models/covid_decision_tree'):
            makedirs('models/covid_decision_tree')


    def _prepare_data(data: dict) -> pandas.DataFrame:
        data = pandas.DataFrame(data)
        
        data = data.fillna(data.median())

        severity = pandas.get_dummies(data[['severity']])
        data = data.drop('severity', axis=1)
        data = data.join(severity)
        
        data = data.astype('float64')
        
        return data
