from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from .basic_ops import aggregate

COLLECTION_NAME = 'aggregated_messages'
class QueryDataBaseService(object):
    """Requiered methods to get aggregation data from MongoDB
    """
    @staticmethod
    async def get_average_by_device_id(db: AsyncIOMotorDatabase,
                                       device_id: str,
                                       since:datetime = None,
                                       to:datetime = None):
        """Creating a pipeline to calculate average, in a time frame
        """
        # If since is not specified, a timestamp in far past is considered.
        if since is None:
            since = datetime(1980, 1, 1, 0, 0, 0, 0)
        # If to is not specified, current timestamp is considered.
        if to is None:
            to = datetime.now()
        pipeline = [
            {
                '$match': {'device_id': device_id, 'window.start':{'$gte': since}, "window.end": {'$lte': to}}
            },
            {
                '$group': {'_id': None, 'totalAverage': {'$avg': '$avg'}}
            }
        ]
        cursor = aggregate(db, COLLECTION_NAME, pipeline)
        results = []
        async for doc in cursor:
            results.append(doc)
        return results

    @staticmethod
    async def get_maximum_by_device_id(db: AsyncIOMotorDatabase,
                                       device_id: str,
                                       since:datetime = None,
                                       to:datetime = None):
        """Creating a pipeline to calculate maximum, in a time frame
        """
        # If since is not specified, a timestamp in far past is considered.
        if since is None:
            since = datetime(1980, 1, 1, 0, 0, 0, 0)
        # If to is not specified, current timestamp is considered.
        if to is None:
            to = datetime.now()
        pipeline = [
            {
                '$match': {'device_id': device_id, 'window.start':{'$gte': since}, "window.end": {'$lte': to}}
            },
            {
                '$group': {'_id': None, 'totalMaximum': {'$max': '$max'}}
            }
        ]
        cursor = aggregate(db, COLLECTION_NAME, pipeline)
        results = []
        async for doc in cursor:
            results.append(doc)
        return results

    @staticmethod
    async def get_minimum_by_device_id(db: AsyncIOMotorDatabase,
                                       device_id: str,
                                       since:datetime = None,
                                       to:datetime = None):
        """Creating a pipeline to calculate minimum, in a time frame
        """
        # If since is not specified, a timestamp in far past is considered.
        if since is None:
            since = datetime(1980, 1, 1, 0, 0, 0, 0)
        if to is None:
            to = datetime.now()
        pipeline = [
            {
                '$match': {'device_id': device_id, 'window.start':{'$gte': since}, "window.end": {'$lte': to}}
            },
            {
                '$group': {'_id': None, 'totalMinimum': {'$min': '$min'}}
            }
        ]
        cursor = aggregate(db, COLLECTION_NAME, pipeline)
        results = []
        async for doc in cursor:
            results.append(doc)
        return results