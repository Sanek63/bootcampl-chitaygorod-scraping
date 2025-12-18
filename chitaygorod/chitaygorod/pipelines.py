import pymongo

from itemadapter import ItemAdapter


class MongoPipeline:
    mongo_db: str
    mongo_uri: str

    def __init__(self):
        self.mongo_db = "items"
        self.mongo_uri = f"mongodb://admin:adminpass@localhost:27017/{self.mongo_db}?authSource=admin"
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if item:
            self.db["collection"].insert_one(ItemAdapter(item).asdict())

    def close_spider(self, spider, reason):
        self.client.close()
