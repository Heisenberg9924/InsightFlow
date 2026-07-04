from pymongo import MongoClient
from pymongo.database import Database

from app.database.config import MONGODB_URI, DATABASE_NAME


class MongoConnection:

    _client: MongoClient | None = None

    @classmethod
    def get_database(cls) -> Database:

        if cls._client is None:
            cls._client = MongoClient(MONGODB_URI)

        return cls._client.get_database(DATABASE_NAME)