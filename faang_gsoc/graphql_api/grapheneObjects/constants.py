MAX_FILTER_QUERY_DEPTH = 3

ANALYSIS  = 'analysis'
EXPERIMENT = 'experiment'
SPECIMEN = 'specimen'
  
FAANG_dataset_index_relations = {
    (ANALYSIS,EXPERIMENT): {'type':2, 'parent_index_key': 'experimentAccessions', 'child_index_key': 'accession'},
    (EXPERIMENT, ANALYSIS): {'type':3, 'parent_index_key': 'accession', 'child_index_key': 'experimentAccessions'},
    (ANALYSIS,SPECIMEN):{'type':2,'parent_index_key':'sampleAccessions','child_index_key':'biosampleId'}
}

non_keyword_properties = set({'organism.text','libraryPreparationDate.text'})