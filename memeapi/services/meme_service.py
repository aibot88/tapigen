from random import seed
from data.db_connection import collection
from io import BytesIO
from controllers.mem_gen import meme_gen

def generate_image(prompt: str, random_seed: int):
    def meme_generator(prompt: str, seed_val: int, negative_prompt: str=""):
        seed(seed_val)
        image = meme_gen(prompt, num_inference_steps=10)
        return image
    img_io = meme_generator(prompt, random_seed)
    return img_io

def save_meme_data(meme_data: dict) -> str:
    result = collection.insert_one(meme_data)
    return str(result.inserted_id)

def fetch_meme_by_key(key) -> dict:
    return collection.find_one({"_id": key})