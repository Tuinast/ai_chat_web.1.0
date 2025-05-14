from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import time

# 实例化 FastAPI
app = FastAPI()

# 允许所有跨域，方便部署到 Vercel、Railway 等前后端分离场景
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 如果安全需求，可以替换成你的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置 OpenAI 客户端
client = OpenAI(
    api_key="06141e22-a494-41e3-b585-fd4f65952707",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

# 配置模板和静态文件目录
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 首页路由，返回聊天页面
@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# AI流式输出接口 (SSE)
@app.get("/chat_stream")
async def chat_stream(message: str):
    def event_stream():
        messages = [
            {"role": "system", "content": "你是人工智能助手，乐于助人，回答简洁明了。"},
            {"role": "user", "content": message}
        ]

        try:
            stream = client.chat.completions.create(
                model="ep-20250318141151-mftt4",
                messages=messages,
                stream=True
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield f"data: {content}\n\n"
                    time.sleep(0.02)

        except Exception as e:
            yield f"data: 出现错误：{str(e)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
