import logging
from utils import convert

logger = logging.getLogger(__name__)


def dynamodb(table, data):
    '''Load data into DynamoDB in batches'''
    logger.info(f"Loading to dynamodb")

    data = convert.floats_to_decimals(data)
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)
    logger.info(f"Loaded {len(data)} documents")

def firestore(firestore_client, colletion, data):
    '''Load data into Firestore in batches'''
    logger.info(f"Loading to Firestore")

    batch = firestore_client.batch()
    data = convert.decimals_to_floats(data)

    for item in data:
        doc_ref = colletion.document(item.get('_id'))
        batch.set(doc_ref, item)
        
    batch.commit()
    logger.info(f"Loaded {len(data)} documents")
