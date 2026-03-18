from __future__ import annotations

import random
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="mock-text-to-image")


class GenerateRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate(req: GenerateRequest):
    # Mocked response
    seed = random.randint(1, 9999)
    return {
        "prompt": req.prompt,
        "seed": seed,
        "image_url": f"https://images.example.com/{seed}.png",
    }


@app.get("/health")
async def health():
    return {"ok": True}
