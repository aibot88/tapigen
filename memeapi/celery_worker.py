from celery.app import Celery
from config import redis_url
from services import save_meme_data
from task import generate_meme_images
from utils import encode_image_bytes

celery = Celery("memeapi", broker=redis_url, backend=redis_url, include=["celery_worker"])


@celery.task(bind=True)
def generate_meme(
    self,
    prompt: str,
    negative_prompt: str,
    seed: int = 42,
    num_inference_steps: int = 10,
):
    task_id = self.request.id
    img = generate_meme_images(
        prompt=prompt,
        negative_prompt=negative_prompt,
        seed=seed,
        num_inference_steps=num_inference_steps,
    )

    meme_data = {
        "id": task_id,
        "prompt": prompt,
        "random_seed": seed,
        "negative_prompt": negative_prompt,
        "image": encode_image_bytes(img),
    }
    save_meme_data(meme_data)
    return task_id


if __name__ == "__main__":
    celery.worker_main(
        [
            "worker",
            "--loglevel=INFO",
            "--concurrency=1",
            "--prefetch-multiplier=1",
            "--pool=threads",
        ]
    )
