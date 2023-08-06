from mario.sinks.base import Sink
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from mario.pipeline import Pipeline


class MongoSink(Sink):
    """MongoSink
    Very basic Mongo connection and insert capability
    """
    def __init__(self, host: str, port: int, database: str ="mario", collection: str = "executions", **kwargs):
        super().__init__(name="Mongo")
        self.database = database
        self.collection = collection
        self.client = MongoClient(host=host, port=port, **kwargs)

    def write(self, pipeline: Pipeline) -> InsertOneResult:
        _database = self.client[self.database]
        _collection = _database[self.collection]
        _collection.create_index("id")
        object_id = _collection.insert_one(pipeline.result)
        return object_id
