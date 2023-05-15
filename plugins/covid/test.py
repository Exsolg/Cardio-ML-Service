from plugins.base_plugin import Plugin


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
        ...

    def train(self, data):
        ...

    def predict(self, data) -> float:
        ...
    
    def get_params(self,) -> dict:
        ...
    
    def get_score(self,) -> dict:
        ...

    def load_from_file(self, file: str) -> None:
        ...

    def save_in_file(self) -> str:
        ...

    def on_load() -> None:
        ...
