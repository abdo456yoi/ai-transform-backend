import replicate
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API running 🚀"}

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        content = await image.read()

        image_base64 = base64.b64encode(content).decode("utf-8")
        image_data_url = f"data:image/png;base64,{image_base64}"

        full_prompt = f"""
same person, identical face, do not change identity,
keep original face unchanged,
preserve natural skin texture and imperfections,
clear visible transformation, strong but realistic change
same pose and same background,

photorealistic,
realistic lighting,
high detail,
avoid artificial look,
avoid plastic skin,

User request: {prompt}
"""

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

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
