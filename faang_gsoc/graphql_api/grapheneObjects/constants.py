ANALYSIS  = 'analysis'
EXPERIMENT = 'experiment'

  
FAANG_dataset_index_relations = {
    (ANALYSIS,EXPERIMENT): {'type':2, 'parent_index_key': 'experimentAccessions', 'child_index_key': 'accession'},
    (EXPERIMENT, ANALYSIS): {'type':3, 'parent_index_key': 'accession', 'child_index_key': 'experimentAccessions'}
}