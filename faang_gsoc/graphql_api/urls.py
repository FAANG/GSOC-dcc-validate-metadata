from django.urls import path
from graphene_django.views import GraphQLView
from decouple import config

DEBUG = config('DEBUG',default=False)

urlpatterns = [
    path("", GraphQLView.as_view(graphiql=DEBUG)),
]