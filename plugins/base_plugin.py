class Plugin:
    description = ''
    scheme_sample: dict = {}
    scheme_prediction: dict = {}

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
