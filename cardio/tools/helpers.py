from cardio.tools.enums import Score
from sklearn.base import BaseEstimator
from tqdm.contrib.itertools import product
from tqdm.auto import tqdm


class _TqdmProgress(tqdm):
    progress = 0

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value
        _TqdmProgress.progress = int(value / self.total * 100)


def grid_search(model_class: BaseEstimator,
                params: dict,
                fit_function,
                score_function,
                progress_function = None):
    keys = list(params.keys())

    best_model = None
    best_score = 0.0

    for param in product(*[params[j] for j in keys], tqdm_class=_TqdmProgress):
        if progress_function:
            progress_function(_TqdmProgress.progress)

        param = {v: param[i] for i, v in enumerate(keys)}
        
        model: BaseEstimator = model_class()

        model.set_params(**param)

        fit_function(model)
    
        score: float = score_function(model)
    
        if score > best_score:
            best_model = model
            best_score = score
    
    return best_model


def сompare_models_quality(scores: list[dict]) -> int:
    if not scores:
        return -1

    best = 0

    for i in range(1, len(scores)):
        if _compare_two_models_quality(scores[i], scores[best]):
            best = i
    
    return best


def _compare_two_models_quality(score1, score2):
    if Score.F1 in score1 and Score.F1 in score2:
        return score1[Score.F1] >= score2[Score.F1]

    if Score.RECALL in score1 and Score.RECALL in score2:
        return score1[Score.RECALL] >= score2[Score.RECALL]

    if Score.PRECISION in score1 and Score.PRECISION in score2:
        return score1[Score.PRECISION] >= score2[Score.PRECISION]
    
    if Score.ACCURACY in score1 and Score.ACCURACY in score2:
        return score1[Score.ACCURACY] >= score2[Score.ACCURACY]
    
    # ТУТ плохо, если разное количестов элементов
    return sum(score1.values()) >= sum(score2.values())
