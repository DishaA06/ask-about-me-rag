from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.rag_chain import load_chain, ask

app = FastAPI(title="Ask About Me API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
chain = load_chain()


class Message(BaseModel):
    role: str
    content: str


class Question(BaseModel):
    question: str
    history: Optional[List[Message]] = None


@app.get("/")
def root():
    return {"status": "Ask About Me API is running"}


@app.post("/ask")
def ask_endpoint(payload: Question):
    if not payload.question.strip():
        raise HTTPException(400, "Empty question")
    hist = [m.model_dump() for m in payload.history or []]
    return ask(payload.question, chain, hist)
