from promise import Promise
from promise.dataloader import DataLoader
from ..helpers import getFileIndexPrimaryKeyFromName, resolve_documents_with_key_list

class FileLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # TODO handle file primary key _id which is outside source
        fetched_documents = resolve_documents_with_key_list('file','_id',keys)
        documents = {doc['_id']: doc for doc in fetched_documents}
        
        return Promise.resolve([documents.get(doc_id) for doc_id in keys])
        