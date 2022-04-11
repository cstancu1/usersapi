import logging
import motor.motor_asyncio
import config

class DatabaseClient:
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        ):
        self.user = user
        self.password = password
        self.host = host
        self.connect_to_db()

    def connect_to_db(self):
        logging.info(f"[*] Connecting to database {self.host}")
        connection_string = f"mongodb://{self.user}:{self.password}@{self.host}"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(connection_string, serverSelectionTimeoutMS=5000, uuidRepresentation="standard")
        self.db = self.client[config.MONGO_DB_NAME]
        logging.info(self.client)
        logging.info(self.db)

    async def insert_data(self, collection: str, data):
        try:
            result = await self.db[collection].insert_one(data)
            return result
        except Exception as ex:
            print(ex)
            return False
    
    async def delete(self, collection: str, _id: str):
        try:
            obj = await self.db["users"][collection].find_one({"_id": _id})
            if obj:
                await self.db[collection].delete_one({"_id":_id})
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
            return False

    async def update(self, collection, _id: str, data: dict):
        col = self.db[collection]
        res = await self.db.col.find_one({"_id":_id})
        if res:
            updated = await self.database[collection].update_one({"_id": _id}, {"$set": data})
            if not updated:
                return False
            return True

    async def retrieve(self, collection, query):
        try:
            result = await self.db[collection].find_one(query)
            if not result:
                return False
            else:
                return result
        except Exception as ex:
            print(ex)
            return False

    async def retrieve_many(self, collection, query):
        try:
            result = await self.db[collection].find_one(query)
            if not result:
                return False
            else:
                return result
        except Exception as ex:
            print(ex)
            return False

database = DatabaseClient(config.MONGO_USER, config.MONGO_PASSWORD, config.MONGO_HOST)