import logging
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
from llama2 import run_llama2  # llama2.pyから関数をインポート
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    text: str

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    text: str

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    traceback_str = ''.join(traceback.format_tb(exc.__traceback__))
    logging.error(f"Traceback: {traceback_str}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "traceback": traceback_str},
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    japanese_text = request.text

    # 日本語を英語に翻訳
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://127.0.0.1:8000/ja_to_en", json={"text": japanese_text})
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error translating Japanese to English")

        translated_text = response.json().get("translated_text")

    if not translated_text:
        raise HTTPException(status_code=500, detail="Translated text from Japanese to English is None")

    # 英語のテキストを用いてllama2関数を実行
    try:
        llama2_response = run_llama2(translated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing llama2 function: {e}")

    if not llama2_response:
        raise HTTPException(status_code=500, detail="Llama2 response is None")

    # 英語の応答を日本語に翻訳
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://127.0.0.1:8000/en_to_ja", json={"text": llama2_response})
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error translating English to Japanese")

        translated_response = response.json().get("translated_text")

    if not translated_response:
        raise HTTPException(status_code=500, detail="Translated response from English to Japanese is None")

    return ChatResponse(text=translated_response)