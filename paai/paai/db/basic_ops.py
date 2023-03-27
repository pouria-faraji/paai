from bson import CodecOptions
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase


def aggregate(db: AsyncIOMotorDatabase, collection_name: str, pipeline):
    '''
    Perform an aggregation pipeline\n
    :param aggregation_pipeline: the pipeline to be executed
    '''
    return __collection_with_option(db, collection_name).aggregate(pipeline)

def __collection_with_option(db: AsyncIOMotorDatabase, collection_name: str) -> AsyncIOMotorCollection:
    codec_option = CodecOptions(tz_aware=True)
    return db[collection_name].with_options(codec_option)
