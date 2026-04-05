import replicate
import os

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    gender: str = Form(...),
    goal: str = Form(...)
):
    # Read uploaded image
    content = await image.read()

    # 🔥 Build prompt (VERY IMPORTANT)
    prompt = f"{gender} body transformation, {goal}, realistic fitness result, same person, before and after style, high quality, photorealistic"

    # 🔥 Call Replicate (FLUX PRO)
    output = replicate.run(
        "black-forest-labs/flux-2-pro",
        input={
            "prompt": prompt,
            "aspect_ratio": "9:16",  # vertical like TikTok
        }
    )

    # output = image URL
    image_url = output[0] if isinstance(output, list) else output

    return {
        "image_url": image_url
    }
