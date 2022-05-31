from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from faang_gsoc.helpers import send_message
from .tasks import read_excel_file
from faang_gsoc.constants import root_path


def index(request):
    return render(request, 'conversion/index.html')


@csrf_exempt
def convert_template(request, task_id):
    if request.method == 'POST':
        fileid = list(request.FILES.keys())[0]
        send_message(room_id=fileid, conversion_status="Waiting")

        with open(f'{root_path}/data/conversion/{fileid}.xlsx', 'wb+') as destination:
            for chunk in request.FILES[fileid].chunks():
                destination.write(chunk)
        res = read_excel_file.apply_async((fileid, task_id,
                                           f'{root_path}/data/conversion/{fileid}.xlsx'),
                                          queue='conversion')

        res.get()
        print("inside conversion", res.status)
        return HttpResponse(res.id)
    return HttpResponse("Please use POST method for conversion!")
