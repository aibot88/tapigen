from random import seed
from data.db_connection import collection
from io import BytesIO


def save_meme_data(meme_data: dict) -> str:
    result = collection.insert_one(meme_data)
    return str(result.inserted_id)

def fetch_meme_by_id(id):
    return collection.find_one({"id": id})
