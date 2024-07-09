from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class Extractor(ABC):
    @abstractmethod
    def extract(self):
        pass


class Firebase(Extractor):
    def __init__(self, collection, batch_size) -> None:
        self.collection = collection
        self.batch_size = batch_size

    def extract(self, last_document):
        '''Extract data from Firestore in chunks using pagination'''
        logger.info(f'extracting from firestore')
        
        query = self.collection.order_by('__name__').limit(int(self.batch_size))
        if last_document:
            last_doc = self.collection.document(last_document).get()
            query = query.start_after(last_doc)

        docs = list(query.stream())
        data = [doc.to_dict() for doc in docs]
        last_document = docs[-1].id if data else None

        logger.info(f"extracted {len(data)} documents")
        return data, last_document



class DynamoDB(Extractor):
    def __init__(self, table, batch_size) -> None:
        self.table = table
        self.batch_size = batch_size

    def extract(self, last_document):
        '''Extract data from DynamoDB in chunks using pagination'''
        logger.info(f'extracting from dynamodb')

        if last_document:
            response = self.table.scan(
                        Limit=int(self.batch_size),
                        ExclusiveStartKey=last_document
                    )
        else:
                response = self.table.scan(Limit=int(self.batch_size))
        
        data = response['Items']
        last_document = response.get('LastEvaluatedKey', None)
        
        logger.info(f"extracted {len(data)} documents")
        return data, last_document