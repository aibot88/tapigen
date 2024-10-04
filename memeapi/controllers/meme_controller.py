from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from models.meme_request import MemeRequest
from services.meme_service import generate_image, save_meme_data, fetch_meme_by_key
from bson import ObjectId
import base64
from utils.params_filter import filter_params
from io import BytesIO
import traceback

router = APIRouter()

@router.post("/generate")
async def generate_meme(request: MemeRequest):
    # try:
    #     allowed_params = ["prompt", "image_count", "random_seed", "negative_prompt"]
    #     filtered_params = filter_params(request, allowed_params)
    # except Exception as e:
    #     # 打印错误信息
    #     print(f"Error occurred: {e}")
    #     # 打印详细的堆栈信息
    #     traceback.print_exc()
    #     pass
    keys = []
    for _ in range(request.image_count):
        img_io = generate_image(request.prompt, request.random_seed)
        img_data = img_io.getvalue()
        meme_data = {
            "prompt": request.prompt,
            "random_seed": request.random_seed,
            "negative_prompt": request.negative_prompt,
            "image": img_data
        }
        keys.append(save_meme_data(meme_data))
    return JSONResponse(content={"keys": keys})

@router.get("/get_meme/{key}")
async def get_meme(key: str):
    try:
        meme_data = fetch_meme_by_key(ObjectId(key))
        img_bytes = meme_data.get("image", "")
        if img_bytes is None:
            raise HTTPException(status_code=404, detail="Meme not found")
        image_stream = BytesIO(img_bytes)
        image_stream.seek(0, 2)
        content_length = image_stream.tell()
        image_stream.seek(0)
        return StreamingResponse(
            image_stream,
            media_type="image/jpeg",
            headers={"Content-Length": str(content_length),   
                     "Content-Disposition": "inline; filename=image.jpg",
                     "Pragma": "no-cache",
                     "Expires": "0"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gen_meme_tg")
async def gen_meme_tg(request: MemeRequest):
    try:
        allowed_params = ["prompt", "image_count", "random_seed", "negative_prompt"]
        filtered_params = filter_params(request, allowed_params)
    except:
        return 
    images = []
    for _ in range(request.image_count):
        img_io = generate_image(request.prompt, request.random_seed)
        img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
        images.append(img_data)
    
    meme_data = {
        "prompt": request.prompt,
        "random_seed": request.random_seed,
        "negative_prompt": request.negative_prompt,
        "images": images
    }
    key = save_meme_data(meme_data)
    meme = fetch_meme_by_key(ObjectId(key))
    
    if meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    
    return JSONResponse(content={"images": meme["images"]})

@router.get("/")
async def read_index():
    return FileResponse("static/index.html")