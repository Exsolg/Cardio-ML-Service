from cardio.tools import plugins as plugin_tools
from cardio.tools.base_plugin import Plugin

from time import sleep
from threading import Thread
from loguru import logger


_training_queue: list[Thread] = []
_training_thread: Thread = None


def add_to_training_queue(dataset: dict, data: list, save_models) -> None:
    _training_queue.append(Thread(target=_train, daemon=True, args=[dataset, data, save_models]))

    global _training_thread

    if _training_thread is None:
        _training_thread = _training_queue.pop(0)
        _training_thread.start()


def _train(dataset: dict, data: list, save_models) -> None:
    try:

        logger.info(f'Starting training for dataset {dataset["_id"]}. Data count: {len(data)}')

        plugins: list[Plugin] = []
        for name in dataset['plugins']:
            plugin = plugin_tools.get(name)

            if not plugin:
                logger.warning(f'Plugin {name} was not found when processing the dataset {dataset["_id"]}')
                continue

            plugins.append(plugin)
        
        models: list[dict] = []
        for p in plugins:
            plugin: Plugin = p()
            plugin.train(data)

            models.append({
                'score': plugin.get_score(),
                'params': plugin.get_params(),
                'filePath': plugin.save_in_file(),
                'plugin': p.__name__,
                'datasetId': dataset['_id']
            })
        
        save_models(models)

        logger.info(f'End training for dataset {dataset["_id"]}')

    except Exception as e:
        logger.error(f'Model training error for dataset {dataset["_id"]}: {e}')

    global _training_thread

    if _training_queue:
        _training_thread = _training_queue.pop(0)
        _training_thread.start()
        return
    
    _training_thread = None
