from io import BytesIO

from celery.app import Celery
from config import redis_url
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models import MemeRequest, MemeTaskResponse, MemeTaskStatusResponse
from services import fetch_meme_by_id

celery_client = Celery("memeapi", broker=redis_url, backend=redis_url)

router = APIRouter(prefix="/meme")


@router.post("/", response_model=MemeTaskResponse)
def generate_meme(request: MemeRequest):
    ids = []
    for _ in range(request.image_count):
        task = celery_client.send_task(
            "memeapi.generate_meme",
            kwargs={
                "prompt": request.prompt,
                "negative_prompt": request.negative_prompt,
                "seed": request.random_seed,
            },
        )
        ids.append(task.id)
    return MemeTaskResponse(ids=ids)


@router.get("/{id}/status", response_model=MemeTaskStatusResponse)
def get_meme_task_status(id: str):
    task = celery_client.AsyncResult(id)
    return MemeTaskStatusResponse(status=task.status)


@router.get("/{id}")
def get_meme(id: str):
    meme_data = fetch_meme_by_id(id)
    if meme_data is None:
        return HTTPException(status_code=404, detail="Meme not found")

    task_id = meme_data["id"]
    task = celery_client.AsyncResult(id=task_id)
    task.forget()

    img_bytes = meme_data["image"]
    image_stream = BytesIO(img_bytes)
    image_stream.seek(0, 2)
    content_length = image_stream.tell()
    image_stream.seek(0)
    return StreamingResponse(
        image_stream,
        media_type="image/jpeg",
        headers={
            "Content-Length": str(content_length),
            "Content-Disposition": "inline; filename=image.jpg",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
