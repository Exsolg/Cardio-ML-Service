from cardio.db import models
from cardio.db.enums import For
from cardio.controllers import errors
from joblib import dump, load
from loguru import logger
from uuid import uuid4
from os import makedirs
from os.path import exists


def get(id: str) -> dict:
    try:
        model = models.get(id, For.COVID)
        if not model:
            raise errors.NotFoundError(f'Model {id} not found')
        return model
    
    except errors.NotFoundError as e:
        logger.debug(f'NotFoundError: {e}')
        raise e
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def get_list() -> list:
    try:
        return models.get_list(For.COVID)
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)

def delete(id: str) -> bool:
    get(id)

    try:
        return models.delete(id, For.COVID)
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def predict(id: str, params: dict) -> float:
    model = get(id)

    try:
        if 'file_path' not in model:
            raise errors.FieldNotExistError(f'Field "file_path" does not exist in the model {id}')

        model = load(model['file_path'])
        return model.predict([prepare_params(params)])[0]

    except errors.FieldNotExistError as e:
        logger.error(f'FieldNotExistError: {e}')
        raise e
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def create(model_file) -> dict:
    try:
        model = load(model_file)

        file_path = f'models/{uuid4()}.joblib'
        
        if not exists('models'):
            makedirs('models')
        
        dump(model, filename=file_path)

        _id = models.create({
            'python_type': str(type(model)),
            'file_path': file_path,
            'params': model.get_params()
        }, For.COVID)

    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)
    
    return get(_id)


def prepare_params(params: dict) -> list:
    return [
        0 if params['sex'] == 'male' else 1,
        params['age'],
        params['urea'] if params.get('urea') else 0,
        params['creatinine'] if params.get('creatinine') else 0,
        params['SKF'] if params.get('SKF') else 0,
        params['AST'] if params.get('AST') else 0,
        params['ALT'] if params.get('ALT') else 0,
        params['CRP'] if params.get('CRP') else 0,
        params['glucose'] if params.get('glucose') else 0,
        params['leukocytes'] if params.get('leukocytes') else 0,
        params['platelets'] if params.get('platelets') else 0,
        params['neutrophils'] if params.get('neutrophils') else 0,
        params['lymphocytes'] if params.get('lymphocytes') else 0,
        params['neutrophil-lymphocyteRatio'] if params.get('neutrophil-lymphocyteRatio') else 0,
        0 if params.get('severity') == 'severe' else 0.5 if params.get('severity') == 'medium' else 1,
        params['D-dimer'] if params.get('D-dimer') else 0,
        1 if params.get('AG') else 0,
        1 if params.get('SD') else 0,
        1 if params.get('IBS') else 0,
        1 if params.get('HOBL') else 0,
        1 if params.get('HBP') else 0,
    ]
