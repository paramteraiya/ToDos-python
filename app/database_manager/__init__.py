import os
from pymongo import MongoClient
# from dotenv import load_dotenv

class DatabaseManager:
    def __init__(self):
        MONGO_URI = os.getenv("MONGO_URI") + "/" + os.getenv("DB_NAME")
        mongo_client = MongoClient(MONGO_URI)
        self.db = mongo_client.get_database(os.getenv("DB_NAME"))
    
    def get_db(self):
        return self.db
