from migration import source, destination, migrate
from google.cloud import firestore
import boto3
from dotenv import load_dotenv
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Specify sys.stdout for standard output
    ],
)

load_dotenv()

if __name__ == "__main__":

    BATCH_SIZE = os.environ.get("BATCH_SIZE")
    # Set up Firestore and Dynamodb configurations
    FIRESTORE_DATABASE = os.environ.get("FIRESTORE_DATABASE")
    FIRESTORE_COLLECTION = os.environ.get("FIRESTORE_COLLECTION")
    DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE")

    # Initialize Firestore
    firestore_client = firestore.Client(database=FIRESTORE_DATABASE)
    firestore_collection = firestore_client.collection(FIRESTORE_COLLECTION)

    # Initialize DynamoDB
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )
    dynamodb = session.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)

    source_firebase = source.Firebase(firestore_collection, BATCH_SIZE)
    destination_dynamodb = destination.DynamoDB(table)

    migrate = migrate.DatabaseMigration(source_firebase, destination_dynamodb)
    migrate.run()
