import replicate
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Root route (to avoid "Not Found")
@app.get("/")
def root():
    return {"status": "API is running 🚀"}


# ✅ Generate endpoint
@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # Read uploaded image
        content = await image.read()

        # Convert image to base64
        image_base64 = base64.b64encode(content).decode("utf-8")
        image_data_url = f"data:image/png;base64,{image_base64}"

        # 🔥 Strong prompt (VERY IMPORTANT for quality)
        full_prompt = f"""
same person, same face, same identity,
do not change person, do not replace face,

Transformation:
fit athletic body,
realistic fat loss,
natural muscles,
before and after fitness transformation,

Style:
photorealistic,
realistic lighting,
high detail skin,
8k quality,

User request: {prompt}
"""

        # 🚀 Run FLUX 2 PRO model
        output = replicate.run(
            "black-forest-labs/flux-2-pro",
            input={
                "prompt": full_prompt,
                "input_images": [image_data_url],
                "aspect_ratio": "9:16",
                "output_format": "webp",
                "output_quality": 90
            }
        )

        # Extract image URL
        image_url = output[0] if isinstance(output, list) else output

        return {"image_url": image_url}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
