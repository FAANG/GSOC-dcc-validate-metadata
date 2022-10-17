from faang_gsoc.celery import app
from faang_gsoc.helpers import get_dummy_response, send_message, send_message_graphql
from faang_gsoc.constants import ALLOWED_TEMPLATES
from graphql_api.grapheneObjects.helpers import resolve_with_join

from celery import Task
from celery.utils.log import get_task_logger
from celery.signals import after_setup_logger
import logging
import os.path
import time
import channels.layers

from asgiref.sync import async_to_sync

channel_layer = channels.layers.get_channel_layer()


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


@app.task(bind=True,base=LogErrorsTask)
def graphql_task(self,a1,a2):
    time.sleep(5)
    res = {'werk':[a1,a2]}
    send_message_graphql(self.request.id,res)
    return get_dummy_response()

class CallbackTask(LogErrorsTask):
    def on_success(self, retval, task_id, args, kwargs):
        send_message_graphql(task_id,'task finished')

@app.task(bind=True,base=CallbackTask)
def resolve_all_task(self,kwargs,left_index):
    time.sleep(2)
    send_message_graphql(self.request.id,'task received')    
    filter_query = kwargs['filter'] if 'filter' in kwargs else {}
    res = resolve_with_join(filter_query,left_index)
    # res = {'data':[{'biosampleId':'SAMEA1','name':'O1'},{'biosampleId':'SAMEA2','name':'O2'}]}
    send_message_graphql(self.request.id,'task about to finish')    

    
    return res