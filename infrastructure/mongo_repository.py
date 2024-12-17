from pymongo.mongo_client import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_URI')

client = MongoClient(uri)

db = client.judoCoroDB

user_collection = db["user"]
