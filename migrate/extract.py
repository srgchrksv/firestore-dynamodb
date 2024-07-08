import logging

logger = logging.getLogger(__name__)

def firestore(colletion, last_document, batch):
    '''Extract data from Firestore in chunks using pagination'''
    logger.info(f'extracting from firestore')
    
    query = colletion.order_by('__name__').limit(int(batch))
    if last_document:
        last_doc = colletion.document(last_document).get()
        query = query.start_after(last_doc)

    docs = list(query.stream())
    data = [doc.to_dict() for doc in docs]
    last_document = docs[-1].id if data else None

    logger.info(f"extracted {len(data)} documents")
    return data, last_document


# function exctract_dynamodb extracts all documents in chunks using pagiantion
def dynamodb(table, last_document, batch):
    '''Extract data from DynamoDB in chunks using pagination'''
    logger.info(f'extracting from dynamodb')

    if last_document:
         response = table.scan(
                    Limit=int(batch),
                    ExclusiveStartKey=last_document
                )
    else:
            response = table.scan(Limit=int(batch))
    
    data = response['Items']
    last_document = response.get('LastEvaluatedKey', None)
    
    logger.info(f"extracted {len(data)} documents")
    return data, last_document