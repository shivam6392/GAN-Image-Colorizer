from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from model.inference import Colorizer

app = FastAPI(title="Image Colorizer API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Colorizer
import os
from download_model import download_model

# Resolve paths relative to this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "checkpoints", "siggraph17.onnx")

# Download model if not present or too small
success = download_model()

if os.path.exists(model_path) and os.path.getsize(model_path) > 1024*1024:
    print(f"Loading model from {model_path} ({os.path.getsize(model_path)/1024/1024:.1f}MB)")
else:
    print(f"WARNING: Model file missing or invalid at {model_path}.")
    model_path = None

colorizer = Colorizer(model_path=model_path)

@app.get("/")
@app.get("/health")
@app.head("/")
@app.head("/health")
def read_root():
    return {"status": "healthy", "model_loaded": model_path is not None}

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
    # Use PORT environment variable for Render
    port = int(os.environ.get("PORT", 8000))
    # Render Free Tier has strict 512MB RAM limit. Limit workers to 1 to prevent OOM
    uvicorn.run("main:app", host="0.0.0.0", port=port, workers=1)
