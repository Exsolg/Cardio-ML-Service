class Plugin:
    description: str | None = None
    scheme_sample: dict | None = None
    scheme_prediction: dict | None = None

    def __init__(self) -> None:
        ...

    def train(self, data: list[dict]) -> None:
        ...

    def predict(self, data: list[dict]) -> list[dict]:
        ...
    
    def get_params(self) -> dict:
        ...
    
    def get_score(self) -> dict:
        ...

    def load_from_file(self, file: str) -> None:
        ...

    def save_in_file(self) -> str:
        ...

    def on_load() -> None:
        ...
    
    def get_progress(self) -> int:
        ...
