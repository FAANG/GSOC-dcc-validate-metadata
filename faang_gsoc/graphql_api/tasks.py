from faang_gsoc.celery import app
from faang_gsoc.helpers import send_message
from faang_gsoc.constants import ALLOWED_TEMPLATES
from celery import Task
from celery.utils.log import get_task_logger
from celery.signals import after_setup_logger
import logging
import os.path
import time

APP_PATH = os.path.dirname(os.path.realpath(__file__))
logger = get_task_logger(__name__)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(f'{APP_PATH}/logs.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


class LogErrorsTask(Task):
    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        send_message(room_id=args[0], conversion_status='Error',
                     errors=f'There is a problem with the conversion process. Error: {exc}')


@app.task(base=LogErrorsTask)
def graphql_task():
    time.sleep(20)
    print('I am graphql Task')
    return {'werk':'it'}