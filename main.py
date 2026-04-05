from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API working 🚀"}

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    gender: str = Form(...),
    goal: str = Form(...)
):
    content = await image.read()

    return {
        "message": "Received successfully",
        "filename": image.filename,
        "gender": gender,
        "goal": goal,
        "size": len(content)
    }
