from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from model.inference import Colorizer

app = FastAPI(title="Image Colorizer API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Colorizer (Model weights would be loaded here if we had them)
import os
from download_model import download_model

# Resolve paths relative to this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "checkpoints", "siggraph17.onnx")

# Download model if not present
download_model()

if not os.path.exists(model_path):
    print("No trained ONNX model found. Using dummy fallback.")
    model_path = None
else:
    print(f"Loading ONNX model from {model_path}")

colorizer = Colorizer(model_path=model_path)

@app.get("/")
def read_root():
    return {"message": "Image Colorizer API is running"}

@app.post("/colorize")
async def colorize_image(file: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await file.read()
    
    # Run inference
    colorized_img = colorizer.predict(image_bytes)
    
    # Convert back to bytes
    img_io = io.BytesIO()
    colorized_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return StreamingResponse(img_io, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    # Render Free Tier has strict 512MB RAM limit. Limit workers to 1 to prevent OOM
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
