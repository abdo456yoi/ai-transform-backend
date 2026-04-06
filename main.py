from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import replicate
import base64
import os

app = FastAPI()

# ✅ Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Replicate API
replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    ratio: str = Form(...)
):
    try:
        content = await image.read()

        image_base64 = base64.b64encode(content).decode("utf-8")
        image_data_url = f"data:image/png;base64,{image_base64}"

        # ✅ ONLY frontend prompt (no hardcoded prompt)
        full_prompt = prompt

        output = replicate_client.run(
            "black-forest-labs/flux-2-pro",
            input={
                "prompt": full_prompt,
                "input_images": [image_data_url],
                "aspect_ratio": ratio
            }
        )

        image_url = output[0] if isinstance(output, list) else output

        return {"image_url": image_url}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
