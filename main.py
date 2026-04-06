import replicate
import os
import base64

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# 🔥 Load API token from Render env
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

app = FastAPI()

# 🔥 Enable CORS (VERY IMPORTANT for frontend)
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
        # ✅ Read image
        content = await image.read()
        image_base64 = base64.b64encode(content).decode("utf-8")

        # ⚠️ Use correct mime type
        image_data_url = f"data:{image.content_type};base64,{image_base64}"

        # ✅ Enhance prompt
        full_prompt = f"{prompt}, same person, realistic fitness transformation, photorealistic"

        # 🔥 CALL REPLICATE (SAFE MODEL)
        output = replicate.run(
            "stability-ai/sdxl",
            input={
                "prompt": full_prompt
            }
        )

        # ✅ Extract image URL
        image_url = output[0] if isinstance(output, list) else output

        return {"image_url": image_url}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
