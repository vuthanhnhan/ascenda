from motor.motor_asyncio import AsyncIOMotorClient
import os

class Database(object):
    def __init__(self) -> None:
        database_driver = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
        self.database = database_driver[os.getenv("DATABASE_NAME")]
    def get_database(self):
        return self.database

db = Database().get_database()

class BaseModel:
    def __init__(self, collection: str, db = db) -> None:
        self.collection = db[collection]
        self.collection_name = collection

    async def __to_dictionary(self, data):
        data['_id'] = str(data['_id'])
        return data

    async def save_many(self, data):
        result = await self.collection.insert_many(data)
        if result:
            return True
        return False

    async def get_all_by_condition(self, condition: dict):
        documents = self.collection.find(condition)
    
        if documents:
            results = []
            async for document in documents:
                document = await self.__to_dictionary(document)
                results.append(document)
            return results
        else:
            return None

    async def delete_all(self):
        await self.collection.delete_many({})