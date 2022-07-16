from collections import defaultdict
import json

from .constants import MAX_FILTER_QUERY_DEPTH, FAANG_dataset_index_relations, non_keyword_properties
from faang_gsoc.es import es
from functools import reduce
from .errors import QUERY_MAX_DEPTH_EXCEEDED
def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

def add_id_to_document(document):
    _id = document['_id'] if '_id' in document else ''
    document = document['_source']
    document['_id'] = _id
    return document

def is_filter_query_depth_valid(filter,current_depth=1):
    if current_depth > MAX_FILTER_QUERY_DEPTH:
        return False
    if not 'join' in filter:
        return True

    for right_index in list(filter['join']):
        is_valid = is_filter_query_depth_valid(filter['join'][right_index],current_depth+1)
        if not is_valid: return False
    return True


# takes a nested dict and flattens its keys
# example:
# filter_basic_query = {
#     'organism':{
#         'sex':{
#             'text': ['female']
#         }
#     }
# }
# will be converted to ->
# sanitized_query = {'organism.sex.text':['female']}
def sanitize_filter_basic_query(filter_basic_query,sanitized_filter_basic_queries,prefix=''):

    for key in list(filter_basic_query):
        sanitized_key = prefix + '.' + key if prefix else key
        if isinstance(filter_basic_query[key],dict):
            sanitize_filter_basic_query(filter_basic_query[key],sanitized_filter_basic_queries,sanitized_key)
        else:
            if sanitized_key not in non_keyword_properties:
                sanitized_key += '.keyword'
            sanitized_filter_basic_queries.append({"terms":{sanitized_key : filter_basic_query[key]}})
            
def get_projected_data(left_index,right_index,left_index_data,right_index_data,inner_join = True):

    res = []
    
    if FAANG_dataset_index_relations[(left_index,right_index)]['type'] == 1:
        right_index_map = {deep_get(x,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key']):x for x in right_index_data}
        for left_document in left_index_data:
            if 'join' not in left_document:
                left_document['join'] = defaultdict(list)
            right_document_values = deep_get(left_document,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key'])
            # print(deep_get(left_document,'experiment'))
            if isinstance(right_document_values,list):
                for right_document in right_document_values:
                    right_index_key_value = deep_get(right_document,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key_path']) if isinstance(right_document,dict) else right_document
                    if right_index_key_value in right_index_map:
                        left_document['join'][right_index].append(right_index_map[right_index_key_value])       
            else:
                right_document = right_document_values
                right_index_key_value = deep_get(right_document,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key_path']) if isinstance(right_document,dict) else right_document
                    
                if right_index_key_value in right_index_map:
                        left_document['join'][right_index].append(right_index_map[right_index_key_value])
            if not inner_join or left_document['join'][right_index]:
                if not left_document['join'][right_index]:
                    left_document['join'][right_index] = []
                res.append(left_document)
            # res.append(left_document)
    
    if FAANG_dataset_index_relations[(left_index,right_index)]['type'] == 2:
        right_index_map = defaultdict(list)
        for right_document in right_index_data:
            left_values = deep_get(right_document,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key'])
            if isinstance(left_values,list):
                for left_document in left_values:
                    left_document_key_value = deep_get(left_document,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key_path']) if isinstance(left_document,dict) else left_document
                    right_index_map[left_document_key_value].append(right_document)
            else:
                left_document = left_values
                left_document_key_value = deep_get(left_document,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key_path']) if isinstance(left_document,dict) else left_document
                right_index_map[left_document_key_value].append(right_document)

        for left_document in left_index_data:
            if 'join' not in left_document:
                left_document['join'] = defaultdict(list)
            left_document_key_value = deep_get(left_document,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key'])
            if left_document_key_value  in right_index_map:
                left_document['join'][right_index] = right_index_map[left_document_key_value]
            if not inner_join or left_document['join'][right_index]:
                if not left_document['join'][right_index]:
                    left_document['join'][right_index] = []
                res.append(left_document)
            # res.append(left_document)
    return res

def resolve_with_join(filter,left_index):
    
    if not is_filter_query_depth_valid(filter):
        raise Exception(QUERY_MAX_DEPTH_EXCEEDED)

    if not bool(filter):
        return resolve_all(left_index)

    sanitized_basic_filter_queries = []

    if 'basic' in filter:
        sanitize_filter_basic_query(filter['basic'],sanitized_basic_filter_queries)
        print(sanitized_basic_filter_queries)
    
    left_index_data = resolve_all(left_index,filter=sanitized_basic_filter_queries)
    
    if not bool(left_index_data) or not 'join' in filter:
        return left_index_data

    for right_index in list(filter['join']):
        right_index_filter = filter['join'][right_index]
        right_index_data = resolve_with_join(right_index_filter,right_index)
        
        left_index_data = get_projected_data(left_index,right_index,left_index_data,right_index_data,bool('basic' in right_index_filter and right_index_filter['basic']))
        
    return left_index_data
        

def resolve_all(index_name,**kwargs):
    filter_queries = kwargs['filter'] if 'filter' in kwargs else []
    print(filter_queries)

    query = {}
    if filter_queries:
        query = {
            "bool" : {
                        "filter": filter_queries
                    }
            }
    else:
        query = {
                'match_all' : {}
            }

    fetched_data = es.search(index = index_name,body = {
            'size' : 10000,
            'query': query
        })
    
    res = [add_id_to_document(x) for x in fetched_data['hits']['hits']] if fetched_data else []
    return res

def resolve_single_document(index_name,id,primary_keys):
    
    body = {
        "query":{
            "bool":{
                # We append '.keyword' to the key name because otherwise elasticsearch 
                # returns nothing. Hence we need to either append '.keyword' to key name
                # or convert all the values to lower case. This is because these fields
                # are not analysed by elasticsearch.
                "should":[{"term":{key + '.keyword':id}} for key in primary_keys]
            }
        }
    }

    res =  es.search(index = index_name,body=body)['hits']['hits']
    return res[0]['_source'] if res else None

def resolve_documents_with_key_list(index_name,key_name,keys):
    print(index_name,key_name,keys)
    
    res = [add_id_to_document(x) for x in es.search(index = index_name,
        body = {
                'size' : 10000,
                'query': {
                    "bool" : {
                        "filter" : {
                            "terms" : {
                                # filter terms only works if values are lowercase
                                key_name: keys if index_name == 'file' else [key.lower() for key in keys]
                            }
                        }
                    }
                }
            }
    )['hits']['hits']]
    # print(res)
    return res
    
def getFileIndexPrimaryKeyFromName(fileName):
    return fileName.split('.',1)[0]