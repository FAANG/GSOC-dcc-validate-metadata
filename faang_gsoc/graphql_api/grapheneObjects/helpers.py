from collections import defaultdict
import json

from .constants import MAX_FILTER_QUERY_DEPTH, FAANG_dataset_index_relations, non_keyword_properties
from faang_gsoc.es import es
from functools import reduce
from .errors import QUERY_MAX_DEPTH_EXCEEDED, DERIVED_FROM_EMPTY

# '''
# This function takes in a string path and returns a value.

# Eg. e = {'a' : {'b' : {'c' : 'd'}}}

# deep_get(e,'a.b.c') => 'd'
# '''
def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

# '''
# For documents of some indices (eg File), the primary key is  _ id 
# which is not inside the _source property. Hence this function simply
# adds the _id property to document to be returned.
# '''
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

# '''
#  takes a nested dict and flattens its keys
#  example:
#  filter_basic_query = {
#      'organism':{
#          'sex':{
#              'text': ['female']
#          }
#      }
#  }
#  will be converted to ->
#  sanitized_query = {'organism.sex.text':['female']}
#  '''
def sanitize_filter_basic_query(filter_basic_query,sanitized_filter_basic_queries,prefix=''):

    for key in list(filter_basic_query):
        sanitized_key = prefix + '.' + key if prefix else key
        if isinstance(filter_basic_query[key],dict):
            sanitize_filter_basic_query(filter_basic_query[key],sanitized_filter_basic_queries,sanitized_key)
        else:
            # if sanitized_key not in non_keyword_properties:
            #     sanitized_key += '.keyword'
            sanitized_filter_basic_queries.append({"terms":{sanitized_key : filter_basic_query[key]}})


def get_projected_data(left_index,right_index,left_index_data,right_index_data,inner_join = True):

    #  this is going to be our joined resultant data
    res = []
    
    # There are two types of joins, which I have named Type 1 and Type 2.

    # Let's take an example for understanding:

    # Analysis : {
    #     accession : 'ERZ10183149', # primary key for analysis index
    #     experimentAccesions : ['ERX5463437', 'ERX5463436', 'ERX5463438', 'ERX5463435'] # foreign keys
    # }

    # Experiment : {
    #     accession : 'ERX5463437' # primary key for experiment index
    # }

    # Type 1 Join (ANALYSIS JOIN EXPERIMENT):

    # Left index : Analysis
    # Right index: Experiment

    # The foreign key of LEFT INDEX contains reference to RIGHT index
    # (Here, experimentAccessions is foreign key)

    # Type 2 Join (EXPERIMENT JOIN ANALYSIS):

    # Left index:  Experiment
    # Right index: Analysis

    # The foreign key of RIGHT INDEX contains reference to LEFT index


    if FAANG_dataset_index_relations[(left_index,right_index)]['type'] == 1:
        # Eg. ANALYSIS JOIN EXPERIMENT
        #  Left Index :  ANALYSIS
        #  Right Index: EXPERIMENT

        
        # We make a map of all right index documents. 
        # The key is the value of the primary key of the RIGHT index document.
        # The value is the RIGHT index document itself. 
        # Eg. For our right index EXPERIMENT suppose we have a document:
        
        # right_index_data = [
        #     {
        #         "accession": "ERX5463437",
        #         "libraryName": "P-70dpf-Lg-Pool-3",
        #     },
        #     {
        #         "accession": "ERX5463435",
        #         "libraryName": "P-70dpf-Lg-Pool-1",
        #     }           
        # ]

        # =>

        # right_index_map  = {
        #     # Note that this key is primary key of EXPERIMENT
        #     "ERX5463437" : {
        #         "accession": "ERX5463437",
        #         "libraryName": "P-70dpf-Lg-Pool-3",
        #     },
        #     "ERX5463435" : {
        #         "accession": "ERX5463435",
        #         "libraryName": "P-70dpf-Lg-Pool-1",
        #     }
        # }

        
        right_index_map = {deep_get(x,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key']):x for x in right_index_data}
        for left_document in left_index_data:
            if 'join' not in left_document:
                left_document['join'] = defaultdict(list)
            # left_document_join_details is either the foreign key or list of foreign keys
            left_document_join_details = deep_get(left_document,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key'])
            if isinstance(left_document_join_details,list):
                # right_document_details can be the key itself or dict containing the key
                for right_document_details in left_document_join_details:
                    right_document_primary_key_value = deep_get(right_document_details,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key_path']) if isinstance(right_document_details,dict) else right_document_details
                    # This step performs the join
                    # Only the Right Index documents which are present in the 
                    # foreign key details of the Left Index are added to left_document['join']
                    # thereby performing a join
                    if right_document_primary_key_value in right_index_map:
                        left_document['join'][right_index].append(right_index_map[right_document_primary_key_value])       
            else:
                # right_document_details can be the key itself or dict containing the key
                right_document_details = left_document_join_details
                right_document_primary_key_value = deep_get(right_document_details,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key_path']) if isinstance(right_document_details,dict) else right_document_details
                    
                if right_document_primary_key_value in right_index_map:
                    # This step performs the join
                    # Only the Right Index documents which are present in the 
                    # foreign key details of the Left Index are added to left_document['join']
                    # thereby performing a join
                    left_document['join'][right_index].append(right_index_map[right_document_primary_key_value])
            
            # For left join and handling parallel joins
            if not inner_join or left_document['join'][right_index]:
                if not left_document['join'][right_index]:
                    left_document['join'][right_index] = []
                res.append(left_document)

    if FAANG_dataset_index_relations[(left_index,right_index)]['type'] == 2:
        
        # Eg. EXPERIMENT JOIN ANALYSIS
        #  Left Index :  EXPERIMENT
        #  Right Index: ANALYSIS

        
        # We make a map of all right index documents. 
        # The key is the value of the primary key of the LEFT INDEX document.
        # The value is the RIGHT index document itself. 
        
        # right_index_data = [
        #     {
        #     "accession": "ERZ10183149",
        #     "experimentAccessions": ['ERX5463437', 'ERX5463436', 'ERX5463438', 'ERX5463435']
        #     }
        # ]

        # =>

        # right_index_map  = {
        #     # Note that this key is the value of primary key (accession) of LEFT Index (EXPERIMENT)
        #     "ERX5463437" : {
        #         "accession": "ERZ10183149",
        #         "experimentAccessions": ['ERX5463437', 'ERX5463436', 'ERX5463438', 'ERX5463435']
        #     },
        #     "ERX5463436" : {
        #         "accession": "ERZ10183149",
        #         "experimentAccessions": ['ERX5463437', 'ERX5463436', 'ERX5463438', 'ERX5463435']
        #     },
        #     "ERX5463438" : {
        #         "accession": "ERZ10183149",
        #         "experimentAccessions": ['ERX5463437', 'ERX5463436', 'ERX5463438', 'ERX5463435']
        #     },
        #     "ERX5463435" : {
        #         "accession": "ERZ10183149",
        #         "experimentAccessions": ['ERX5463437', 'ERX5463436', 'ERX5463438', 'ERX5463435']
        #     },
        # }

        right_index_map = defaultdict(list)
        
        for right_document in right_index_data:
            #  right_document_join_details is the foreign key itself or the list fof foreign keys inside Right index document
            right_document_join_details = deep_get(right_document,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key'])
            
            if isinstance(right_document_join_details,list):
                #  left_document_details can be the key itself or dict containing the key
                for left_document_details in right_document_join_details:
                    left_document_primary_key_value = deep_get(left_document_details,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key_path']) if isinstance(left_document_details,dict) else left_document_details
                    right_index_map[left_document_primary_key_value].append(right_document)
            else:
                #  left_document_details can be the key itself or dict containing the key
                left_document_details = right_document_join_details
                left_document_primary_key_value = deep_get(left_document_details,FAANG_dataset_index_relations[(left_index,right_index)]['right_index_key_path']) if isinstance(left_document_details,dict) else left_document_details
                right_index_map[left_document_primary_key_value].append(right_document)

        for left_document in left_index_data:
            if 'join' not in left_document:
                left_document['join'] = defaultdict(list)

            #  left_document_details can be the key itself or dict containing the key
            left_document_details =  deep_get(left_document,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key'])
            left_document_primary_key_value = deep_get(left_document_details,FAANG_dataset_index_relations[(left_index,right_index)]['left_index_key_path']) if isinstance(left_document_details,dict) else left_document_details
            
            if left_document_primary_key_value  in right_index_map:
                # This step performs the join
                # Only the Right Index documents whose foreign key details
                # contain the details of the Left Index document are added to left_document['join']
                # thereby performing a join
                left_document['join'][right_index] = right_index_map[left_document_primary_key_value]
            
            if not inner_join or left_document['join'][right_index]:
                if not left_document['join'][right_index]:
                    left_document['join'][right_index] = []
                res.append(left_document)
        

    return res

def resolve_with_join(filter,left_index):
    

    # check how deep is the query for join. That is if we have a join between more than
    # 3 indices then the query is invalid and hence throw an exception
    if not is_filter_query_depth_valid(filter):
        raise Exception(QUERY_MAX_DEPTH_EXCEEDED)

    # if filter object is empty return all the documents of the index
    if not bool(filter):
        # this function returns all the documents of the specified index
        return resolve_all(left_index)
    
    sanitized_basic_filter_queries = []
    if 'basic' in filter:
        # Please read about what we are doing here in function definition
        # for sanitize_filter_basic_query above
        sanitize_filter_basic_query(filter['basic'],sanitized_basic_filter_queries)
        
    # returns all the documents of specified index ans also applies filter conditions
    left_index_data = resolve_all(index_name=left_index,filter=sanitized_basic_filter_queries)
    
    if not bool(left_index_data) or not 'join' in filter:
        return left_index_data
   
    for right_index in list(filter['join']):
        right_index_filter = filter['join'][right_index]
        
        # This is where join happens.
        # Lets take an example of the a query:
        
        # query{
        #     allAnalysis(
        #         filter:
        #         # resolve_with_join function takes two arguments: filter_query dict and index_name (here analyis)
        #         # hence this dict below is what we pass to resolve_with_join on the first call
        #         {
        #             basic : {}
        #             join:{ 
        #                 # Here we specify that with our left index (analysis) make a join with right index (experiment)
        #                 # We call resolve_with_join at this point RECURSIVELY. We use this dict below as the 
        #                 # filter_query argument and index_name as that of the right index (here experiment)
        #                 # right_index_filter = filter['join'][right_index]
        #                 experiment: {
        #                     basic : {}
        #                 }
        #             }
        #         }
        #     )
        # }
        
        right_index_data = resolve_with_join(right_index_filter,right_index)
        
        # Hence we have both data of left index (analysis for our example) and we just fetched right_index_data.
        
        # We pass both left_index and right_index names as well their respective data that we fetched to
        # get_projected_data below. It also takes a last argument which decides if the join is inner join or left join.
        # It returns the data where each record of the left_index has a new property called 'join' which 
        # contains all the joined right index records. And hence we reassign this data to left_index_data.
        left_index_data = get_projected_data(left_index,right_index,left_index_data,right_index_data,bool('basic' in right_index_filter and right_index_filter['basic']))
        
    # return the joined result data
    return left_index_data
        

def resolve_all(index_name,**kwargs):

    if index_name in ['derived_from_specimen','derives_specimen_sample']:
        index_name = 'specimen'
    elif index_name == 'derived_from_organism':
        index_name = 'organism'

    filter_queries = kwargs['filter'] if 'filter' in kwargs else []

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

# The primary key for file index can be derived from "name" field by removing file extension.
# Eg. if name of file document is SRR7165835_2.fastq.gz, then its primary key is SRR7165835_2.
def getFileIndexPrimaryKeyFromName(fileName):
    return fileName.split('.',1)[0]