from config import mongo_collection, mongo_db, mongo_url
from pymongo import MongoClient

client = MongoClient(mongo_url)
db = client[mongo_db]
collection = db[mongo_collection]
