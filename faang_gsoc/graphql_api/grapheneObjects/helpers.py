from graphene import ObjectType,String
from elasticsearch import Elasticsearch
from decouple import config
import json

es = Elasticsearch(hosts=[{"host":config("NODE",default="localhost")}])
def resolve_all(index_name):
    print(index_name)
    res = [x['_source'] for x in es.search(index = index_name,filter_path = ['hits.hits._source'],body = {
            'size' : 10000,
            'query': {
                'match_all' : {}
            }
        })['hits']['hits']]
    # print(json.dumps(res,indent=4))
    return res

def resolve_single_document(index_name,q, **kwargs):
    res =  es.search(index = index_name,q=q)['hits']['hits'][0]['_source']
    return res

def resolve_documents_with_key_list(index_name,keys):
    print(keys)
    
    res = [x['_source'] for x in es.search(index = index_name,
        body = {
                'size' : 10000,
                'query': {
                    "bool" : {
                        "filter" : {
                            "terms" : {
                                # filter terms only works if values are lowercase
                                "biosampleId" : [key.lower() for key in keys]
                            }
                        }
                    }
                }
            }
    )['hits']['hits']]
    return res
   