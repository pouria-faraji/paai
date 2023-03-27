import os

from fastapi import Request
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase


class DBSettings():
    """Settings class for database connection
    """

    username = os.environ.get('MONGODB_USERNAME', 'mongodb-admin')
    password = os.environ.get('MONGODB_PASSWORD', 'mongodb-password')
    database = os.environ.get('MONGODB_DATABASE', 'mongodb-database')
    host     = os.environ.get('MONGODB_HOST', 'mongo:27017')

    def __init__(self) -> None:
        self.connection_uri = f"mongodb://{self.username}:{self.password}@{self.host}/{self.database}?authSource={self.database}&readPreference=primary&directConnection=true&ssl=false"

async def __get_database(request: Request) -> AsyncIOMotorDatabase:
    # this is a FastAPI yield dependency.
    # Check the docs here: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    """
    retrieve a database connection.
    It assumes that the db client is already created and available at `request.app.state.db_client`.
    This should be done in the FastAPI startup event handler.
    """

    # retrieve the database specified in the connection URI
    db: AsyncIOMotorDatabase = request.app.state.db_client.get_default_database()
    return db

# Rename and make the previous function a FastAPI dependency
# so it can be used inside routes
DBDependency = Depends(__get_database)