from plugins.base_plugin import Plugin


class CovidRandomForest(Plugin):
    description = '''
    Predicting covid-19 patient outcome using random forest method
    '''

    scheme: dict = {
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
            }
        }
    }

    def __init__(self) -> None:
        ...

    def predict(self, data: scheme) -> float:
        ...

    def load_from_file(self, file: str) -> None:
        ...

    def save_in_file(self) -> str:
        ...

    def on_load() -> None:
        ...
