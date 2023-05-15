from sklearn.base import BaseEstimator
from tqdm.contrib.itertools import product


def grid_search(model_class: BaseEstimator,
                params: dict,
                fit_function,
                score_function):
    keys = list(params.keys())
    
    best_model = None
    best_score = 0.0
  
    for param in product(*[params[j] for j in keys]):
        param = {v: param[i] for i, v in enumerate(keys)}
        
        model: BaseEstimator = model_class()

        model.set_params(**param)

        fit_function(model)
    
        score: float = score_function(model)
    
        if score > best_score:
            best_model = model
            best_score = score
    
    return best_model
