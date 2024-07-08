import boto3
from dotenv import load_dotenv
import os
load_dotenv("../.env")

# Get AWS credentials and region from environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_REGION')

# Create a Boto3 session with the AWS credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)


# Create a DynamoDB resource
dynamodb = session.resource('dynamodb')

# Define the table schema
table_name = 'Products'
attribute_definitions = [
    {'AttributeName': '_id', 'AttributeType': 'S'},  # Partition key
    {'AttributeName': 'category', 'AttributeType': 'S'}  # Sort key (optional)
]
key_schema = [
    {'AttributeName': '_id', 'KeyType': 'HASH'},  # Partition key
    {'AttributeName': 'category', 'KeyType': 'RANGE'}  # Sort key (optional)
]

# Create the DynamoDB table
try:
    table = dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=attribute_definitions,
        KeySchema=key_schema,
        BillingMode='PAY_PER_REQUEST' 
    )
    table.wait_until_exists()  # Wait until the table is created
    print(f"Table '{table_name}' created successfully!")
except Exception as e:
    print(f"Error creating table: {e}")
