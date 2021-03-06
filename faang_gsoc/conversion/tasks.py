from .ReadExcelFile import ReadExcelFile
from faang_gsoc.celery import app
from faang_gsoc.helpers import send_message
from faang_gsoc.constants import ALLOWED_TEMPLATES
from celery import Task
from celery.utils.log import get_task_logger
from celery.signals import after_setup_logger
import logging
import os.path

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
def read_excel_file(room_id, conversion_type, file):
    """
    This task will convert excel file to proper json format
    :param room_id: room id to create ws url
    :param conversion_type: could be 'samples' or 'experiments'
    :param file: file to read
    :return: converted data
    """

    print("room_id:", room_id)
    if conversion_type not in ALLOWED_TEMPLATES:
        send_message(
            room_id=room_id, conversion_status='Error',
            errors='This type is not supported')
        return 'Error', dict()

    read_excel_file_object = ReadExcelFile(
        file_path=file, json_type=conversion_type)

    # test = 10/0

    # # added by Koosum
    # try:
    #     raise ValueError('Represents a hidden bug, do not catch this')
    # except ValueError as error:
    #     print('Caught this error: ' + repr(error))

    results = read_excel_file_object.start_conversion()
    if 'Error' in results[0]:
        send_message(
            room_id=room_id, conversion_status='Error', errors=results[0])
    else:
        if results[2]:
            send_message(room_id=room_id, conversion_status='Success',
                         bovreg_submission=True)
        else:
            send_message(room_id=room_id, conversion_status='Success')
    return results[0], results[1]
