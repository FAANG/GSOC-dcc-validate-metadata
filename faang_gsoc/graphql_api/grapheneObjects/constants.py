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
    # TODO add explaination of child_index_key_path
    (ANALYSIS,ARTICLE):{'type':2,'parent_index_key':'datasetAccession','child_index_key':'relatedDatasets','child_index_key_path':'accession'},
    (ANALYSIS,DATASET):{'type':1,'parent_index_key':'datasetAccession','child_index_key':'accession'},
    # TODO add explaination of parent_index_key_path
    (ANALYSIS,PROTOCOL_ANALYSIS):{'type':1,'parent_index_key':'analysisProtocol','child_index_key':'key','parent_index_key_path':'filename'},
    (ANALYSIS,SPECIMEN):{'type':1,'parent_index_key':'sampleAccessions','child_index_key':'biosampleId'},
    
    (ARTICLE,ANALYSIS):{'type':1,'parent_index_key':'relatedDatasets','child_index_key':'datasetAccession','parent_index_key_path':'accession'},
    (ARTICLE,DATASET):{'type':1,'parent_index_key':'relatedDatasets','child_index_key':'accession','parent_index_key_path':'accession'},
    (ARTICLE,FILE):{'type':2,'parent_index_key':'_id','child_index_key':'publishedArticles','child_index_key_path':'articleId'},
    (ARTICLE,SPECIMEN):{'type':2,'parent_index_key':'_id','child_index_key':'publishedArticles','child_index_key_path':'articleId'},
    
    (DATASET,EXPERIMENT):{'type':1,'parent_index_key':'experiment','child_index_key':'accession','parent_index_key_path':'accession'},
    (DATASET,ANALYSIS):{'type':2,'parent_index_key':'accession','child_index_key':'dataAccession'},
    (DATASET,ARTICLE):{'type':2,'parent_index_key':'accession','child_index_key':'relatedDatasets','child_index_key_path':'accession'},
    (DATASET,FILE):{'type':1,'parent_index_key':'file','child_index_key':'name','parent_index_key_path':'name'},
    (DATASET,SPECIMEN):{'type':1,'parent_index_key':'specimen','child_index_key':'biosampleId','parent_index_key_path':'biosampleId'},
    
    (EXPERIMENT, ANALYSIS): {'type':2, 'parent_index_key': 'accession', 'child_index_key': 'experimentAccessions'},
    (EXPERIMENT,DATASET):{'type':2,'parent_index_key':'accession','child_index_key':'experiment','child_index_key_path':'accession'},
    (EXPERIMENT,FILE):{'type':2,'parent_index_key':'accession','child_index_key':'experiment','child_index_key_path':'accession'},
    
    (FILE,ARTICLE):{'type':1,'parent_index_key':'publishedArticles','child_index_key':'_id','parent_index_key_path':'articleId'},
    (FILE,DATASET):{'type':2,'parent_index_key':'name','child_index_key':'file','child_index_key_path':'name'},
    (FILE,EXPERIMENT):{'type':1,'parent_index_key':'experiment','child_index_key':'accession','parent_index_key_path':'accession'},
    (FILE,ORGANISM):{'type':1,'parent_index_key':'organism','child_index_key':'biosampleId'},
    (FILE,PROTOCOL_FILES):{'type':2,'parent_index_key':'experiment','child_index_key':'experiments','parent_index_key_path':'accession','child_index_key_path':'accession'},
    (FILE,PROTOCOL_SAMPLES):{'type':2,'parent_index_key':'specimen','child_index_key':'specimens','child_index_key_path':'id'},
    (FILE,SPECIMEN):{'type':1,'parent_index_key':'specimen','child_index_key':'biosampleId'},
    
    (SPECIMEN,ANALYSIS):{'type':2,'parent_index_key':'biosampleId','child_index_key':'sampleAccessions'},
    (SPECIMEN,ORGANISM):{'type':1,'parent_index_key':'derivedFrom','child_index_key':'biosampleId'},
    (SPECIMEN,ARTICLE):{'type':1,'parent_index_key':'publishedArticles','child_index_key':'_id','parent_index_key_path':'articleId'},
    (SPECIMEN,DATASET):{'type':2,'parent_index_key':'biosampleId','child_index_key':'specimen','child_index_key_path':'biosampleId'},
    (SPECIMEN,PROTOCOL_SAMPLES):{'type':2,'parent_index_key':'biosampleId','child_index_key':'specimens','child_index_key_path':'id'},
    (SPECIMEN,FILE):{'type':1,'parent_index_key':'biosampleId','child_index_key':'specimen'},
    
    
    (ORGANISM,SPECIMEN):{'type':2,'parent_index_key':'biosampleId','child_index_key':'derivedFrom'},
    (ORGANISM,FILE):{'type':2,'parent_index_key':'biosampleId','child_index_key':'organism'},
    (ORGANISM,PROTOCOL_SAMPLES):{'type':2,'parent_index_key':'biosampleId','child_index_key':'specimens','child_index_key_path':'derivedFrom'},
    
    (PROTOCOL_ANALYSIS,ANALYSIS):{'type':2,'parent_index_key':'key','child_index_key':'analysisProtocol','child_index_key_path':'filename'},
    
    (PROTOCOL_FILES,FILE):{'type':1,'parent_index_key':'experiments','child_index_key':'experiment','parent_index_key_path':'accession','child_index_key_path':'accession'},
    
    (PROTOCOL_SAMPLES,FILE):{'type':1,'parent_index_key':'specimens','child_index_key':'specimen','parent_index_key_path':'id'},
    (PROTOCOL_SAMPLES,SPECIMEN):{'type':1,'parent_index_key':'specimens','child_index_key':'biosampleId','parent_index_key_path':'id'},
    (PROTOCOL_SAMPLES,ORGANISM):{'type':1,'parent_index_key':'specimens','child_index_key':'biosampleId','parent_index_key_path':'derivedFrom'},
    

}

non_keyword_properties = set({'organism.text','libraryPreparationDate.text',"_id"})