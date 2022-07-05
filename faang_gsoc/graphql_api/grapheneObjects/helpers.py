from collections import defaultdict
import json

from .constants import MAX_FILTER_QUERY_DEPTH, FAANG_dataset_index_relations, non_keyword_properties
from faang_gsoc.es import es

def check_filter_query_depth(filter,current_depth):
    if current_depth > MAX_FILTER_QUERY_DEPTH:
        return False
    if not 'join' in filter:
        return True

    for next_index in list(filter['join']):
        is_valid = check_filter_query_depth(filter['join'][next_index],current_depth+1)
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
def get_projected_data(parent_index,child_index,parent_index_data,child_index_data,inner_join = True):

    res = []
    
    if FAANG_dataset_index_relations[(parent_index,child_index)]['type'] == 2:
        child_index_map = {x[FAANG_dataset_index_relations[(parent_index,child_index)]['child_index_key']]:x for x in child_index_data}
        for parent in parent_index_data:
            parent['join'] = defaultdict(list)
            for child_index_key in parent[FAANG_dataset_index_relations[(parent_index,child_index)]['parent_index_key']]:
                if child_index_key in child_index_map:
                    parent['join'][child_index].append(child_index_map[child_index_key])
            if not inner_join or parent['join']:
                if not parent['join']:
                    parent['join'][child_index] = []
                res.append(parent)
            # res.append(parent)
    
    if FAANG_dataset_index_relations[(parent_index,child_index)]['type'] == 3:
        child_index_map = defaultdict(list)
        for child in child_index_data:
            for parent_key in child[FAANG_dataset_index_relations[(parent_index,child_index)]['child_index_key']]:
                child_index_map[parent_key].append(child)

        for parent in parent_index_data:
            parent['join'] = defaultdict(list)

            if parent[FAANG_dataset_index_relations[(parent_index,child_index)]['parent_index_key']] in child_index_map:
                parent['join'][child_index] = child_index_map[parent[FAANG_dataset_index_relations[(parent_index,child_index)]['parent_index_key']]]
            if not inner_join or parent['join']:
                if not parent['join']:
                    parent['join'][child_index] = []
                res.append(parent)
            # res.append(parent)
    return res
def resolve_with_join(filter,current_index):
    # print(check_filter_query_depth(filter,1))


    if not bool(filter):
        return resolve_all(current_index)

#  with basic filters
    sanitized_basic_filter_queries = []

    if 'basic' in filter:
        sanitize_filter_basic_query(filter['basic'],sanitized_basic_filter_queries)
        print(sanitized_basic_filter_queries)
    
    # filter_query = {"accession":['ERZ10183149', 'ERZ10183096', "ERX5463437","ERX5463438"]}
    # filter_query = {}
    # sanitize_filter_basic_query(filter_query,sanitized_basic_filter)
    current_index_data = resolve_all(current_index,filter=sanitized_basic_filter_queries)
    
    if not bool(current_index_data) or not 'join' in filter:
        return current_index_data

    for next_index in list(filter['join']):
        next_filter = filter['join'][next_index]
        next_index_data = resolve_with_join(next_filter,next_index)
        current_index_data = get_projected_data(current_index,next_index,current_index_data,next_index_data,bool('basic' in next_filter and next_filter['basic']))
    print(json.dumps(current_index_data,indent=4))
    return current_index_data
        

def resolve_all(index_name,**kwargs):
    filter_queries = kwargs['filter'] if 'filter' in kwargs else []
    print(filter_queries)

    query = {}
    if filter_queries:
        query = {
            "bool" : {
                        "filter": filter_queries
                        # "filter" : [
                        #     # "terms" : {
                        #     #     # filter terms only works if values are lowercase
                        #     #     # key_name : [key.lower() for key in keys]
                        #     # }
                        #    { "terms" : filter_query},
                        # #    {"terms":{"accession.keyword":["ERZ10183153"]}}
                        # ]
                    }
            }
    else:
        query = {
                'match_all' : {}
            }

    fetched_data = es.search(index = index_name,filter_path = ['hits.hits._source'],body = {
            'size' : 10000,
            'query': query
        })
    
    res = [x['_source'] for x in fetched_data['hits']['hits']] if fetched_data else []
    print('resresres')
    # print(json.dumps(res,indent=4))
    # print(json.dumps(fetched_data['hits']['hits'],indent=4))
    return res

def resolve_single_document(index_name,q, **kwargs):
    res =  es.search(index = index_name,q=q)['hits']['hits'][0]['_source']
    return res

def resolve_documents_with_key_list(index_name,key_name,keys):
    print(keys)
    
    res = [x['_source'] for x in es.search(index = index_name,
        body = {
                'size' : 10000,
                'query': {
                    "bool" : {
                        "filter" : {
                            "terms" : {
                                # filter terms only works if values are lowercase
                                key_name : [key.lower() for key in keys]
                            }
                        }
                    }
                }
            }
    )['hits']['hits']]
    return res
