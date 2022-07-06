MAX_FILTER_QUERY_DEPTH = 3

ANALYSIS  = 'analysis'
EXPERIMENT = 'experiment'
SPECIMEN = 'specimen'
ORGANISM = 'organism'
ARTICLE = 'article'
DATASET = 'dataset'
FILE = 'file'
PROTOCOL_ANALYSIS = 'protocol_analysis'
PROTOCOL_FILES = 'protocol_files'
PROTOCOL_SAMPLES = 'protocol_samples'
  
FAANG_dataset_index_relations = {
    (ANALYSIS,EXPERIMENT): {'type':1, 'parent_index_key': 'experimentAccessions', 'child_index_key': 'accession'},
    (EXPERIMENT, ANALYSIS): {'type':2, 'parent_index_key': 'accession', 'child_index_key': 'experimentAccessions'},
    (ANALYSIS,SPECIMEN):{'type':1,'parent_index_key':'sampleAccessions','child_index_key':'biosampleId'},
    (SPECIMEN,ANALYSIS):{'type':2,'parent_index_key':'biosampleId','child_index_key':'sampleAccessions'},
    (SPECIMEN,ORGANISM):{'type':1,'parent_index_key':'derivedFrom','child_index_key':'biosampleId'},
    (ORGANISM,SPECIMEN):{'type':2,'parent_index_key':'biosampleId','child_index_key':'derivedFrom'},
    # TODO add explaination of parent_index_key_path
    (DATASET,EXPERIMENT):{'type':1,'parent_index_key':'experiment','child_index_key':'accession','parent_index_key_path':'accession'},
    # TODO add explaination of child_index_key_path
    (EXPERIMENT,DATASET):{'type':2,'parent_index_key':'accession','child_index_key':'experiment','child_index_key_path':'accession'}
}

non_keyword_properties = set({'organism.text','libraryPreparationDate.text',"_id"})