import base64
import os
import time

import requests
from models.meme import MemeRequest, MemeTaskResponse, MemeTaskStatusResponse

API_URL = os.getenv("API_URL", "https://tapi.theemogen.com")


def _create_meme_task(prompt: str):
    try:
        resp = requests.post(
            f"{API_URL}/meme", json=MemeRequest(prompt=prompt).model_dump()
        )
        resp.raise_for_status()

        res = MemeTaskResponse.model_validate(resp.json())
        return res.ids[0]
    except Exception as e:
        print(f"create meme task error: {e}")
        raise e


def _wait_meme_task_success(task_id: str, interval: float = 1):
    try:
        while True:
            resp = requests.get(f"{API_URL}/meme/{task_id}/status")
            resp.raise_for_status()

            res = MemeTaskStatusResponse.model_validate(resp.json())
            if res.status == "FAILURE":
                raise ValueError(f"Meme task {task_id} failed")
            elif res.status == "SUCCESS":
                return
            time.sleep(interval)
    except Exception as e:
        print(f"wait meme task error: {e}")
        raise e


def _get_meme_task_img(task_id: str):
    try:
        resp = requests.get(f"{API_URL}/meme/{task_id}")
        resp.raise_for_status()

        img_bytes = b""
        for chunk in resp.iter_content(4096, decode_unicode=False):
            img_bytes += chunk
        return img_bytes
    except Exception as e:
        print(f"get meme task img error: {e}")
        raise e


def generate_meme(prompt):
    # create generate meme task
    task_id = _create_meme_task(prompt=prompt)

    _wait_meme_task_success(task_id=task_id)

    return _get_meme_task_img(task_id=task_id)

def generate_meme_url(prompt):
    # create generate meme task
    task_id = _create_meme_task(prompt=prompt)

    _wait_meme_task_success(task_id=task_id)

    return f"{API_URL}/meme/{task_id}"