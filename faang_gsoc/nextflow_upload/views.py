import json
from celery import chain
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import upload_without_val
from faang_gsoc.constants import root_path
import os

import pathlib

@csrf_exempt
def upload_tracks(request, dir_name):
    if request.method == 'POST':
        fileid_list = list(request.FILES.keys())
        res_ids = []
        for fileid in fileid_list:
            file_name = request.FILES[fileid]
            with open(f'{root_path}/data/{fileid}', 'wb+') as destination:
                for chunk in request.FILES[fileid].chunks():
                    destination.write(chunk)
            upload_task = upload_without_val.s(fileid, dir_name, str(request.FILES[fileid])).set(queue='upload')
            res = upload_task.apply_async()
            res_ids.append(res.id)
        return HttpResponse(json.dumps({"id": res_ids}))
    return HttpResponse("Please use POST method for uploading tracks")



