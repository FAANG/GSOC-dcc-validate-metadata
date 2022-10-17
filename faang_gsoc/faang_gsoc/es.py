# from elasticsearch import Elasticsearch
# from decouple import config

# es = Elasticsearch(hosts=[{"host":config("NODE",default="localhost")}])

from elasticsearch import Elasticsearch, RequestsHttpConnection
from decouple import config

ELASTICSEARCH_HOST = config("ELASTICSEARCH_HOST",default="localhost")
ELASTICSEARCH_PORT = config("ELASTICSEARCH_PORT","9200")
ELASTICSEARCH_USER = config("ELASTICSEARCH_USER","")
ELASTICSEARCH_PASSWORD = config("ELASTICSEARCH_PASSWORD","")
ELASTICSEARCH_NODE_URL = f'{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'

es = Elasticsearch(
        [ELASTICSEARCH_NODE_URL], 
        connection_class=RequestsHttpConnection, 
        http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD), 
        use_ssl=False, 
        verify_certs=False
    )