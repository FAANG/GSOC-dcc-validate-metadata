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
    (ANALYSIS,EXPERIMENT): {'type':1, 'left_index_key': 'experimentAccessions', 'right_index_key': 'accession'},
    # TODO add explaination of right_index_key_path
    (ANALYSIS,ARTICLE):{'type':2,'left_index_key':'datasetAccession','right_index_key':'relatedDatasets','right_index_key_path':'accession'},
    (ANALYSIS,DATASET):{'type':1,'left_index_key':'datasetAccession','right_index_key':'accession'},
    # TODO add explaination of left_index_key_path
    (ANALYSIS,PROTOCOL_ANALYSIS):{'type':1,'left_index_key':'analysisProtocol','right_index_key':'key','left_index_key_path':'filename'},
    (ANALYSIS,SPECIMEN):{'type':1,'left_index_key':'sampleAccessions','right_index_key':'biosampleId'},
    
    (ARTICLE,ANALYSIS):{'type':1,'left_index_key':'relatedDatasets','right_index_key':'datasetAccession','left_index_key_path':'accession'},
    (ARTICLE,DATASET):{'type':1,'left_index_key':'relatedDatasets','right_index_key':'accession','left_index_key_path':'accession'},
    (ARTICLE,FILE):{'type':2,'left_index_key':'_id','right_index_key':'publishedArticles','right_index_key_path':'articleId'},
    (ARTICLE,SPECIMEN):{'type':2,'left_index_key':'_id','right_index_key':'publishedArticles','right_index_key_path':'articleId'},
    
    (DATASET,EXPERIMENT):{'type':1,'left_index_key':'experiment','right_index_key':'accession','left_index_key_path':'accession'},
    (DATASET,ANALYSIS):{'type':2,'left_index_key':'accession','right_index_key':'dataAccession'},
    (DATASET,ARTICLE):{'type':2,'left_index_key':'accession','right_index_key':'relatedDatasets','right_index_key_path':'accession'},
    (DATASET,FILE):{'type':1,'left_index_key':'file','right_index_key':'name','left_index_key_path':'name'},
    (DATASET,SPECIMEN):{'type':1,'left_index_key':'specimen','right_index_key':'biosampleId','left_index_key_path':'biosampleId'},
    
    (EXPERIMENT, ANALYSIS): {'type':2, 'left_index_key': 'accession', 'right_index_key': 'experimentAccessions'},
    (EXPERIMENT,DATASET):{'type':2,'left_index_key':'accession','right_index_key':'experiment','right_index_key_path':'accession'},
    (EXPERIMENT,FILE):{'type':2,'left_index_key':'accession','right_index_key':'experiment','right_index_key_path':'accession'},
    
    (FILE,ARTICLE):{'type':1,'left_index_key':'publishedArticles','right_index_key':'_id','left_index_key_path':'articleId'},
    (FILE,DATASET):{'type':2,'left_index_key':'name','right_index_key':'file','right_index_key_path':'name'},
    (FILE,EXPERIMENT):{'type':1,'left_index_key':'experiment','right_index_key':'accession','left_index_key_path':'accession'},
    (FILE,ORGANISM):{'type':1,'left_index_key':'organism','right_index_key':'biosampleId'},
    (FILE,PROTOCOL_FILES):{'type':2,'left_index_key':'experiment','right_index_key':'experiments','left_index_key_path':'accession','right_index_key_path':'accession'},
    (FILE,PROTOCOL_SAMPLES):{'type':2,'left_index_key':'specimen','right_index_key':'specimens','right_index_key_path':'id'},
    (FILE,SPECIMEN):{'type':1,'left_index_key':'specimen','right_index_key':'biosampleId'},
    
    (SPECIMEN,ANALYSIS):{'type':2,'left_index_key':'biosampleId','right_index_key':'sampleAccessions'},
    (SPECIMEN,ORGANISM):{'type':1,'left_index_key':'derivedFrom','right_index_key':'biosampleId'},
    (SPECIMEN,ARTICLE):{'type':1,'left_index_key':'publishedArticles','right_index_key':'_id','left_index_key_path':'articleId'},
    (SPECIMEN,DATASET):{'type':2,'left_index_key':'biosampleId','right_index_key':'specimen','right_index_key_path':'biosampleId'},
    (SPECIMEN,PROTOCOL_SAMPLES):{'type':2,'left_index_key':'biosampleId','right_index_key':'specimens','right_index_key_path':'id'},
    (SPECIMEN,FILE):{'type':1,'left_index_key':'biosampleId','right_index_key':'specimen'},
    
    
    (ORGANISM,SPECIMEN):{'type':2,'left_index_key':'biosampleId','right_index_key':'derivedFrom'},
    (ORGANISM,FILE):{'type':2,'left_index_key':'biosampleId','right_index_key':'organism'},
    (ORGANISM,PROTOCOL_SAMPLES):{'type':2,'left_index_key':'biosampleId','right_index_key':'specimens','right_index_key_path':'derivedFrom'},
    
    (PROTOCOL_ANALYSIS,ANALYSIS):{'type':2,'left_index_key':'key','right_index_key':'analysisProtocol','right_index_key_path':'filename'},
    
    (PROTOCOL_FILES,FILE):{'type':1,'left_index_key':'experiments','right_index_key':'experiment','left_index_key_path':'accession','right_index_key_path':'accession'},
    
    (PROTOCOL_SAMPLES,FILE):{'type':1,'left_index_key':'specimens','right_index_key':'specimen','left_index_key_path':'id'},
    (PROTOCOL_SAMPLES,SPECIMEN):{'type':1,'left_index_key':'specimens','right_index_key':'biosampleId','left_index_key_path':'id'},
    (PROTOCOL_SAMPLES,ORGANISM):{'type':1,'left_index_key':'specimens','right_index_key':'biosampleId','left_index_key_path':'derivedFrom'},
    

}

non_keyword_properties = set({'organism.text','libraryPreparationDate.text',"_id"})