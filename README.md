# 🎨 ChromaLab - AI Image Colorizer

> **Relive the colors of the past.**  
> Transform historical black & white photography into vibrant reality using state-of-the-art deep learning.

![Project Preview](https://github.com/shivam6392/GAN-Image-Colorizer/assets/placeholder.png)

## ✨ Features

-   **🪄 AI-Powered Restoration**: Uses the **SIGGRAPH 2017** (Zhang et al.) Interactive Deep Colorization model for high-fidelity results.
-   **🌌 Ethereal Cyberpunk UI**: A modern, glassmorphic interface with neon aesthetics and smooth animations.
-   **⚡ Real-time Processing**: Fast inference on CPU/GPU.
-   **🔍 Interactive Comparison**: Sliding compare tool to view the original vs. colorized image side-by-side.
-   **🖼️ Smart Resizing**: Automatically handles different aspect ratios without cropping.
-   **📥 Instant Download**: high-resolution export of your colorized masterpieces.

## �️ Tech Stack

### Frontend (The Face)
-   **Framework**: Next.js 14 (App Router)
-   **Styling**: Tailwind CSS v3/v4 & Custom CSS Variables
-   **Icons**: Lucide React
-   **Effects**: Glassmorphism, CSS Animations

### Backend (The Brain)
-   **API Framework**: FastAPI (Python)
-   **ML Framework**: PyTorch
-   **Image Processing**: Scikit-Image, PIL, NumPy
-   **Model Architecture**: CNN (Convolutional Neural Network) based on Siggraph17.

---

## 🚀 Getting Started

Follow these instructions to run the project locally.

### Prerequisites
-   Python 3.9+
-   Node.js 18+
-   Git

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/shivam6392/GAN-Image-Colorizer.git
cd GAN-Image-Colorizer
```

### 2️⃣ Backend Setup (Python)
Navigate to the backend folder and set up the environment.

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# 📥 Download Model Weights (Critical Step!)
# This script fetches the 136MB pre-trained model file.
python download_model.py

# Start the Server
python main.py
```
*The backend will start at `http://localhost:8000`*

### 3️⃣ Frontend Setup (Next.js)
Open a new terminal, navigate to the frontend folder.

```bash
cd frontend

# Install dependencies
npm install

# Start the Development Server
npm run dev
```
*The frontend will start at `http://localhost:3000`*

---

## ☁️ Deployment

### Backend (Render/Railway)
1.  Push this repo to GitHub.
2.  Deploy the `backend` folder as a **Web Service**.
3.  **Build Command**: `pip install -r backend/requirements.txt`
4.  **Start Command**: `python backend/main.py`
5.  *Note: The `download_model.py` script ensures weights are available during build/runtime if configured.*

### Frontend (Vercel)
1.  Import the repo to Vercel.
2.  Set Root Directory to `frontend`.
3.  Add Environment Variable: `NEXT_PUBLIC_API_URL` -> `https://your-backend-url.onrender.com`

---

## 📚 Acknowledgements
-   Based on the research paper: *Real-Time User-Guided Image Colorization with Learned Deep Priors* (Richard Zhang et al., SIGGRAPH 2017).
-   Original Model Implementation: [richzhang/colorization](https://github.com/richzhang/colorization)

---

<p align="center">
  Made with ❤️ by Shivam
</p>
