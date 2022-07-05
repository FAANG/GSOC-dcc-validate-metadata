from elasticsearch import Elasticsearch
from decouple import config

es = Elasticsearch(hosts=[{"host":config("NODE",default="localhost")}])
