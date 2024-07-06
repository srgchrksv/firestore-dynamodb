
from google.cloud import firestore
import boto3
from dotenv import load_dotenv
import os 
from decimal import Decimal
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
load_dotenv()

# convert floats to decimals for dynamodb
def convert_floats_to_decimals(data):
    """ Recursively convert float values to Decimal in the given data """
    if isinstance(data, list):
        return [convert_floats_to_decimals(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_floats_to_decimals(v) for k, v in data.items()}
    elif isinstance(data, float):
        return Decimal(str(data))
    else:
        return data

        
def extract_firestore(firestore_client, firestore_collection, last_document, batch):
    '''Extract data from Firestore in chunks using pagination'''
    logging.info(f'extracting from firestore')
    query = firestore_client.collection(firestore_collection).order_by('__name__').limit(batch)
    if last_document != False:
        last_doc = firestore_client.collection(firestore_collection).document(last_document).get()
        query = query.start_after(last_doc)
    docs = query.stream()
    data = [doc.to_dict() for doc in docs]
    last_document = data[-1].get('_id') if data else None
    logging.info(f"extracted {len(data)} documents")
    return data, last_document

def load_dynamodb(table, data):
    '''Load data into DynamoDB in batches'''
    logging.info(f"Loading to dynamodb")
    data = convert_floats_to_decimals(data)
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)
        # check the put items later  on
        # batch.put_items([{'PutRequest': {'Item': item}} for item in data])


if __name__ == "__main__":

    BATCH_SIZE = os.environ.get('BATCH_SIZE')
    # Set up Firestore and Dynamodb configurations
    FIRESTORE_DATABASE = os.environ.get('FIRESTORE_DATABASE')
    FIRESTORE_COLLECTION = os.environ.get('FIRESTORE_COLLECTION')
    DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')

    # Initialize Firestore
    firestore_client = firestore.Client(database=FIRESTORE_DATABASE)

    # Initialize DynamoDB
    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)

    # run migration
    last_document = False
    try:
        logging.info(f"Starting migration")
        while not last_document:
                data, last_document = extract_firestore(firestore_client, FIRESTORE_COLLECTION, last_document, BATCH_SIZE)
                if data:
                    load_dynamodb(table, data)
        logging.info(f"End migration")
    except Exception as e:
        logging.error(f"Error when migrating data: {e}")