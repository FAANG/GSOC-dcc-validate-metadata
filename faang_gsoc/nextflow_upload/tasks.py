from faang_gsoc.celery import app
from faang_gsoc.helpers import send_message
import requests
from faang_gsoc.constants import root_path
import os


@app.task
def upload_without_val(fileid, dir_name, filename):
    send_message(submission_message="Uploading file", room_id=fileid)
    filepath = f"{root_path}/data/{fileid}"
    url = 'http://localhost/uploadfile'
    download_url = f'http://localhost/download/{filename}'
    data = {
        'path': dir_name,
        'name': filename
    }
    res = requests.post(url, files={'file': open(filepath,'rb')}, data=data)
    if res.status_code != 200:
        send_message(submission_message="Upload failed, "
                                        "please contact "
                                        "faang-dcc@ebi.ac.uk",
                        room_id=fileid)
        return 'Error'
    else:
        send_message(submission_message=f'Success! Please download your file at \n {download_url}', room_id=fileid)
        return 'Success'
