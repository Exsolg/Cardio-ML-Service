from cardio.tools import plugins as plugin_tools
from cardio.tools.helpers import сompare_models_quality
from cardio.tools.base_plugin import Plugin

from threading import Thread
from datetime import datetime
from loguru import logger


_training_queue: list['TrainingThread'] = []
_training_thread: 'TrainingThread' = None


def add_to_training_queue(dataset_id: str, plugins: list[str], data: list[dict], save_model_function) -> None:
    global _training_thread
    global _training_queue

    if dataset_id in [i.dataset_id for i in _training_queue]:
        index = [i.dataset_id for i in _training_queue].index(dataset_id)
        _training_queue.pop(index)

    _training_queue.append(TrainingThread(dataset_id, plugins, data, save_model_function))

    if _training_thread is None:
        _training_thread = _training_queue.pop(0)
        _training_thread.start()


def training_status(dataset_id: str) -> dict:
    global _training_thread
    global _training_queue

    if _training_thread is not None and _training_thread.dataset_id == dataset_id:
        return {
            'participatesInTraining': True,
            'numberInQueue':          0,
            'plugin':                 _training_thread.plugin.__class__.__name__,
            'plugins':                [i.__name__ for i in _training_thread.plugins],
            'progress':               _training_thread.get_progress(),
            'trainingStartDate':      _training_thread.start_date,
        }
    
    if dataset_id in [i.dataset_id for i in _training_queue]:
        index = [i.dataset_id for i in _training_queue].index(dataset_id)

        return {
            'participatesInTraining': True,
            'numberInQueue':          index + 1,
            'plugins':                [i.__name__ for i in _training_queue[index]],
        }

    return {
        'participatesInTraining': False,
    }


class TrainingThread(Thread):
    def __init__(self, dataset_id: str, plugins_list: list[str], data: list[dict], save_model_function) -> None:
        super().__init__(daemon=True)

        plugins: list[Plugin] = []
        for name in plugins_list:
            plugin = plugin_tools.get(name)

            if not plugin:
                logger.warning(f'Plugin {name} was not found when the dataset {dataset_id} was being prepared for training')
                continue

            plugins.append(plugin)

        self.plugins: list[Plugin] = plugins
        self.plugin: Plugin =        None
        self.dataset_id: str =       dataset_id
        self.data: list[dict] =      data
        self.start_date: datetime =  None
        self.save_model_function =   save_model_function

    def get_progress(self) -> int:
        return self.plugin.get_progress()

    def run(self):
        try:
            logger.info(f'Starting training for dataset {self.dataset_id}. Data count: {len(self.data)}')
            self.start_date = datetime.utcnow()

            learning_plugins: list[Plugin] = []

            for p in self.plugins:
                plugin: Plugin = p()
                self.plugin = plugin

                plugin.train(self.data)

                learning_plugins.append(plugin)

            if (best_plugin_index := сompare_models_quality([i.get_score() for i in learning_plugins])) >= 0:
                self.save_model_function(self.dataset_id, learning_plugins[best_plugin_index])
            
            else:
                logger.warning(f'Failed to determine the best model for dataset {self.dataset_id}')

            logger.info(f'End training for dataset {self.dataset_id}')

        except Exception as e:
            logger.error(f'Model training error for dataset {self.dataset_id}: {e}')

        global _training_thread

        if _training_queue:
            _training_thread = _training_queue.pop(0)
            _training_thread.start()
            return
    
        _training_thread = None
