from fastapi import FastAPI
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

# 私有OpenAI API配置
client = OpenAI(
    api_key="06141e22-a494-41e3-b585-fd4f65952707",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

@app.get("/api/chat")
def chat():
    completion = client.chat.completions.create(
        model = "你的模型ID",
        messages = [
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": "常见的十字花科植物有哪些？"},
        ],
    )
    return JSONResponse(content={
        "reply": completion.choices[0].message.content
    })
