import replicate
import os

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    import base64

content = await image.read()
image_base64 = base64.b64encode(content).decode("utf-8")
image_data_url = f"data:image/png;base64,{image_base64}"

    full_prompt = f"{prompt}, realistic fitness transformation, same person, photorealistic"

    output = replicate.run(
        "black-forest-labs/flux-2-pro",
        input={
            "prompt": full_prompt,
            "aspect_ratio": "9:16"
        }
    )

    image_url = output[0] if isinstance(output, list) else output

    return {"image_url": image_url}
