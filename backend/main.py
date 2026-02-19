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
model_path = "checkpoints/siggraph17-df00044c.pth"
if not os.path.exists(model_path):
    print("No trained model found. Using random weights.")
    model_path = None
else:
    print(f"Loading model from {model_path}")

colorizer = Colorizer(model_path=model_path)

@app.get("/")
def read_root():
    return {"message": "Image Colorizer API is running"}

@app.post("/colorize")
async def colorize_image(file: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await file.read()
    
    # Run inference
    # Note: Since the model is untrained, output will be noise/random colors
    colorized_img = colorizer.predict(image_bytes)
    
    # Convert back to bytes
    img_io = io.BytesIO()
    colorized_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return StreamingResponse(img_io, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
