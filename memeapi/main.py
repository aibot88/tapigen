from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import meme_controller

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(meme_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)