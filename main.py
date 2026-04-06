import replicate
import os
import base64
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    content = await image.read()
    image_base64 = base64.b64encode(content).decode("utf-8")
    image_data_url = f"data:image/png;base64,{image_base64}"

    full_prompt = f"{prompt}, same person, realistic fitness transformation, photorealistic"

    output = replicate.run(
        "black-forest-labs/flux-2-pro",
        input={
            "prompt": full_prompt,
            "input_images": [image_data_url],
            "aspect_ratio": "9:16"
        }
    )

    image_url = output[0] if isinstance(output, list) else output
    return {"image_url": image_url}
