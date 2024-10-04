import requests
from models.meme import MemeRequest
import os

API_URL = os.getenv("API_URL", "https://tapi.theemogen.com")

def generate_meme(prompt):
    url = API_URL + "/gen_meme_tg"
    prompt = "pepe: " + prompt
    data = MemeRequest(prompt=prompt).dict()
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json().get("images")[-1]
    return None