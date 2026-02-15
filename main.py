from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from generator import generate_captions, generate_image
from models import GenerateRequest
from prompt import build_caption_prompt, build_image_prompt

app = FastAPI()

# ===================================================================
# CORS MIDDLEWARE - Allows frontend to connect to backend
# ===================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Netlify URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def default_size_for_platform(platform: str) -> str:
    p = platform.lower()

    if p == "linkedin":
        return "1024x1536"   # vertical professional

    if p == "instagram":
        return "1024x1536"   # vertical feed optimized

    if p in ("twitter", "x"):
        return "1536x1024"   # horizontal

    return "1024x1024"

@app.post("/generate")
def generate(request: GenerateRequest):
    if not request.want_images and not request.want_captions:
        raise HTTPException(status_code=400, detail="Select want_images or want_captions")

    result = {}

    if request.want_images:
        image_prompt = build_image_prompt(request)
        size = default_size_for_platform(request.platform)

        images = generate_image(
            username=request.username,
            prompt=image_prompt,
            n=request.num_images,
            size=size
        )
        result["images"] = images
        result["image_prompt"] = image_prompt
        result["size"] = size

    if request.want_captions:
        caption_prompt = build_caption_prompt(
            request.platform,
            request.company,
            request.event,
            request.title,
            request.product_description,
            request.num_captions,
            request.Target_audience,
            request.Product,
            request.call_to_action
        )

        captions = generate_captions(
            prompt=caption_prompt,
            n=request.num_captions
        )
        result["captions"] = captions
        result["caption_prompt"] = caption_prompt

    return result

# Health check endpoint for Railway
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Spark Studio API is running"}
