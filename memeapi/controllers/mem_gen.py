from diffusers import StableDiffusionPipeline, DiffusionPipeline
import torch
from safetensors.torch import save_file, load_file
from io import BytesIO

class StableDiffusionSingleton:
    _instance = None
    
    @classmethod
    def get_instance(cls, model_path):
        if cls._instance is None:
            cls._instance = cls(model_path)
        return cls._instance
    
    def __init__(self, model_path):
        if self._instance is not None:
            raise Exception("This class is a singleton!")
        model_name = "stabilityai/sdxl-turbo"
        self.pipe = DiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
        lora_state_dict = load_file(model_path)
        self.pipe.unet.load_state_dict(lora_state_dict, strict=False)
        self.pipe.to("cuda")

def __meme_generator(pipe, prompt, num_inference_steps=10):
    pipe.safety_checker = None
    img = pipe(prompt, num_inference_steps=20, guidance_scale=9.5,safety_checker=None, height=256, width=256).images[0]
    # img = pipe(prompt, num_inference_steps=100, guidance_scale=7.5,safety_checker=None, height=512, width=512).images[0]
    img_io = BytesIO()
    img.save(img_io, "JPEG", quality=95)  # 调整质量参数为 95，确保图片质量
    img_io.seek(0)
    return img_io

def meme_gen(prompt, num_inference_steps=10):
    pipe_instance = StableDiffusionSingleton.get_instance(model_path)
    # prompt = "(pepe meme): A man feel really happy in the room with the milk tea in the hand"
    image = __meme_generator(pipe_instance.pipe, prompt, num_inference_steps=10)
    return image
    

model_path = "/home/ubuntu/doge_lora/meme_lora/text_to_image/sd-memo-model-lora11/pytorch_lora_weights.safetensors"
pipe_instance = StableDiffusionSingleton.get_instance(model_path)

if __name__ == "__main__":
    # 生成 meme 图像并保存到本地文件
    from PIL import Image
    output_path = "meme_image.jpg"
    try:
        image_io = meme_gen("a happy pepe", num_inference_steps=10)
        with open(output_path, 'wb') as f:
            f.write(image_io.getvalue())
            print(f"[INFO] Image saved successfully to {output_path}.\n the image format: {Image.open(image_io).format}")
    except Exception as e:
        print(f"[ERROR] Error generating or saving meme: {e}")