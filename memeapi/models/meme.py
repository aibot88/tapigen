from typing import List, Literal

from pydantic import BaseModel


class MemeRequest(BaseModel):
    prompt: str
    image_count: int = 1
    random_seed: int = 42
    negative_prompt: str = ""


class MemeTaskResponse(BaseModel):
    ids: List[str]


class MemeTaskStatusResponse(BaseModel):
    status: Literal["PENDING", "STARTED", "RETRY", "FAILURE", "SUCCESS"]
