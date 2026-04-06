from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import replicate
import base64
import os

app = FastAPI()

# ✅ Enable CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load API key
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    print("❌ ERROR: Missing REPLICATE_API_TOKEN")

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)


@app.get("/")
def home():
    return {"status": "backend running 🚀"}


@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    ratio: str = Form(...)
):
    try:
        print("📥 New request received")

        # ✅ Read image
        content = await image.read()

        if not content:
            return {"error": "Empty image file"}

        # ✅ Convert to base64
        image_base64 = base64.b64encode(content).decode("utf-8")
        image_data_url = f"data:image/png;base64,{image_base64}"

        print("🖼 Image processed")

        # ✅ Use prompt from frontend ONLY
        full_prompt = prompt.strip()

        if not full_prompt:
            return {"error": "Prompt is empty"}

        print("🧠 Prompt:", full_prompt)
        print("📐 Ratio:", ratio)

        # ✅ Call Replicate
        output = replicate_client.run(
            "black-forest-labs/flux-2-pro",
            input={
                "prompt": full_prompt,
                "input_images": [image_data_url],
                "aspect_ratio": ratio
            }
        )

        print("✅ Replicate response received")

        # ✅ Extract URL
        image_url = output[0] if isinstance(output, list) else output

        return {
            "image_url": image_url
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "error": str(e)
        }
