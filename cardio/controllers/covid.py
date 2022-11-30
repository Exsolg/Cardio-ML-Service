from cardio.db.models import Model

class CovidController:
    @staticmethod
    def get(id: str):
        return Model.get(id)
