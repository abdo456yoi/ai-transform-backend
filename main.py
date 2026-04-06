import replicate
import os
import base64

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# Load API token from environment
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

app = FastAPI()

# Enable CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def root():
    return {"message": "API is working 🚀"}

# Main AI endpoint
@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # Convert image to base64
        content = await image.read()
        image_base64 = base64.b64encode(content).decode("utf-8")
        image_data_url = f"data:image/png;base64,{image_base64}"

        # Strong prompt
        full_prompt = f"{prompt}, same person, realistic fitness transformation, lean body, photorealistic, high detail"

        # Run AI model
        output = replicate.run(
            "black-forest-labs/flux-dev",
            input={
                "prompt": full_prompt,
                "input_images": [image_data_url]
            }
        )

        # Extract image URL
        image_url = output[0] if isinstance(output, list) else output

        return {"image_url": image_url}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
