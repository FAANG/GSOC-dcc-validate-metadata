from promise import Promise
from promise.dataloader import DataLoader
from ..helpers import resolve_documents_with_key_list

class ExperimentLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        fetched_documents = resolve_documents_with_key_list('experiment','accession',keys)
        documents = {doc['accession']: doc for doc in fetched_documents}
        
        return Promise.resolve([documents.get(doc_id) for doc_id in keys])
        