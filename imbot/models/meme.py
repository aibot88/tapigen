from pydantic import BaseModel

class MemeRequest(BaseModel):
    prompt: str
    image_count: int = 1
    random_seed: int = 42
    negative_prompt: str = ""