from django.urls import path
from . import views

app_name = 'nextflow_upload'
urlpatterns = [
    path('upload/<str:dir_name>', views.upload_tracks, name='upload_tracks')
]