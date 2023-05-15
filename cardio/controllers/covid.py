from cardio.db import models
from cardio.db.enums import For
from cardio.controllers import errors
from joblib import dump, load
from loguru import logger
from uuid import uuid4
from os import makedirs
from os.path import exists
from pandas import DataFrame, Series
from math import ceil


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


def get_list(page: int = 1, limit: int = 3) -> dict:
    page = page if page > 0 else 1

    try:
        total = models.get_total_count()
        return {
            'contents': models.get_list(page=page, limit=limit, _for=For.COVID),
            'page': page,
            'limit': limit,
            'totalPapes': ceil(total / page),
            'totalElements': total
        }
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
        return model.predict(prepare_params(params))[0]

    except errors.FieldNotExistError as e:
        logger.error(f'FieldNotExistError: {e}')
        raise e
    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)


def create(model_file, description:str = None) -> dict:
    try:
        model = load(model_file)

        file_path = f'models/{uuid4()}.joblib'
        
        if not exists('models'):
            makedirs('models')
        
        dump(model, filename=file_path)

        _id = models.create({
            'python_type': str(type(model)),
            'file_path': file_path,
            'params': model.get_params(),
            'description': description
        }, For.COVID)

    except Exception as e:
        logger.error(f'Error: {e}')
        raise errors.InternalError(e)
    
    return get(_id)


def prepare_params(params: dict) -> DataFrame:
    return DataFrame(data=[Series(data={
        'sex':                          0 if params['sex'] == 'male' else 1,
        'age':                          params['age'],
        'urea':                         params['urea'] if params.get('urea') else 7.8,
        'creatinine':                   params['creatinine'] if params.get('creatinine') else 85,
        'SKF':                          params['SKF'] if params.get('SKF') else 73.5,
        'AST':                          params['AST'] if params.get('AST') else 36,
        'ALT':                          params['ALT'] if params.get('ALT') else 30,
        'CRP':                          params['CRP'] if params.get('CRP') else 69.1,
        'glucose':                      params['glucose'] if params.get('glucose') else 6.7,
        'leukocytes':                   params['leukocytes'] if params.get('leukocytes') else 9.09,
        'platelets':                    params['platelets'] if params.get('platelets') else 216,
        'neutrophils':                  params['neutrophils'] if params.get('neutrophils') else 7.8,
        'lymphocytes':                  params['lymphocytes'] if params.get('lymphocytes') else 0.9,
        'neutrophilLymphocyteRatio':    params['neutrophilLymphocyteRatio'] if params.get('neutrophilLymphocyteRatio') else 9.359375,
        'DDimer':                       params['DDimer'] if params.get('DDimer') else 2013,
        'AG':                           1 if params.get('AG') else 1,
        'SD':                           1 if params.get('SD') else 0,
        'IBS':                          1 if params.get('IBS') else 1,
        'HOBL':                         1 if params.get('HOBL') else 0,
        'HBP':                          1 if params.get('HBP') else 0,
        'severityLight':                1 if params.get('severity') == 'light' else 0,
        'severityMedium':               1 if params.get('severity') == 'medium' else 0,
        'severitySevere':               1 if params.get('severity') == 'severe' else 0
        # Если степень тяжести не подано, нужно заполнять медианой
    })])
