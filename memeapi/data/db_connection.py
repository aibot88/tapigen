from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meme_db"]
collection = db["memes"]