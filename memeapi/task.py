import random

import numpy as np
import torch
from config import model_path
from diffusers import DiffusionPipeline
from PIL import Image
from safetensors.torch import load_file


def _get_sd_pipeline(model_path: str):
    model_name = "stabilityai/sdxl-turbo"
    pipe = DiffusionPipeline.from_pretrained(
        model_name, torch_dtype=torch.float16, safety_checker=None
    )
    lora_state_dict = load_file(model_path)
    pipe.unet.load_state_dict(lora_state_dict, strict=False)
    pipe.to("cuda")
    return pipe


pipe = _get_sd_pipeline(model_path=model_path)
image_path = "pepememe.jpeg"
init_image = Image.open(image_path).convert("RGB")
init_image = init_image.resize((512, 512))  # 确保尺寸合适


def generate_meme_images(
    prompt: str,
    negative_prompt: str,
    seed: int = 42,
    num_inference_steps=10,
):
    # prompt = "(pepe meme): A man feel really happy in the room with the milk tea in the hand"
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    img = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        image=init_image,
        strength=1,     
        guidance_scale=5,
        safety_checker=None,
        height=512,
        width=512,
    ).images[0]
    return img.resize((256, 256))