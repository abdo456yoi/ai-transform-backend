import replicate
import os
import base64

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is working 🚀"}

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        full_prompt = f"{prompt}, realistic fitness transformation, photorealistic"

        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": full_prompt
            }
        )

        image_url = output[0] if isinstance(output, list) else output

        return {"image_url": image_url}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
