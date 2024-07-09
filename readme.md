## Firestore-DynamoDB

### Migrate your Firestore to DynamoDB or DynamoDB to firestore
![migration diagram made with lucid.app](migration.jpeg)

*migration diagram made with lucid.app*


## Migration package consists of 3 submodules:
- Source - to extract data
- Destination - to load data 
- Migrate - to run the migration


## Usage example for Firestore - DynamoDB:

### Initialize clients and configs
```python
# set batch_size for migration
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
```
## Run Firebase -> DynamoDB migration
```python
# init source
source_firebase = source.Firebase(firestore_collection, BATCH_SIZE)
# init destination
destination_dynamodb = destination.DynamoDB(table)
# run migration
migrate = migrate.DatabaseMigration(source_firebase, destination_dynamodb)
migrate.run()
```

## Run DynamoDB -> Firebase migration
```python
# init source
source_dynamodb = source.DynamoDB(table, BATCH_SIZE)
# init destination
destination_firebase = destination.Firebase(firestore_client, firestore_collection)
# run migration
migrate = migrate.DatabaseMigration(source_dynamodb, destination_firebase)
migrate.run()
```

