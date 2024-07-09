from abc import ABC, abstractmethod
import logging
from migration.utils.convert import floats_to_decimals, decimals_to_floats

logger = logging.getLogger(__name__)


class Loader(ABC):
    @abstractmethod
    def load(self, data):
        pass


class Firebase(Loader):
    def __init__(self, client, collection) -> None:
        self.client = client
        self.collection = collection

    def load(self, data):
        """Load data into Firestore in batches"""
        logger.info(f"Loading to Firestore")

        batch = self.client.batch()
        data = decimals_to_floats(data)

        for item in data:
            doc_ref = self.colletion.document(item.get("_id"))
            batch.set(doc_ref, item)

        batch.commit()
        logger.info(f"Loaded {len(data)} documents")


class DynamoDB(Loader):
    def __init__(self, table) -> None:
        self.table = table


    def load(self, data):
        """Load data into DynamoDB in batches"""
        logger.info(f"Loading to dynamodb")

        data = floats_to_decimals(data)
        with self.table.batch_writer() as batch:
            for item in data:
                batch.put_item(Item=item)
        logger.info(f"Loaded {len(data)} documents")
