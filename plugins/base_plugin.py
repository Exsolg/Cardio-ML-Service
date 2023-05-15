class Plugin:
    description = ''
    scheme_train: dict = {}
    scheme_predict: dict = {}

    def __init__(self) -> None:
        ...

    def train(self, data: scheme_train):
        ...

    def predict(self, data: scheme_predict) -> float:
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
