import logging
import traceback

from  migration.destination import Loader
from migration.source import Extractor


class DatabaseMigration:
    def __init__(self, extractor: Extractor, loader: Loader) -> None:
        self.extractor = extractor
        self.loader = loader
        self.logger = logging.getLogger(__name__)

    def run(self):
        last_document = False
        try:
            while True:
                    data, last_document = self.extractor.extract(last_document)
                    if data:
                        self.loader.load(data)
                    else:
                        break
                    self.logger.info("Migration complete")
        except Exception as e:
                stack_trace = traceback.format_exc()
                logging.error(stack_trace)
                logging.error(f"Error when migrating data: {e}")
