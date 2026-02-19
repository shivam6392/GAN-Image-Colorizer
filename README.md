# ChromaLab - AI Image Colorizer

Transform black & white photos into vibrant color images using deep learning (Siggraph17).

![Preview](preview.png)

## 🚀 Tech Stack
-   **Frontend**: Next.js 14, Tailwind CSS, Lucide React
-   **Backend**: FastAPI, PyTorch
-   **Model**: [Interactive Deep Colorization (Siggraph 2017)](https://github.com/richzhang/colorization)

## 🛠️ Local Setup

### 1. Backend
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python download_model.py  # Download the 136MB model weights
python main.py
```
Server runs on `http://localhost:8000`.

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs on `http://localhost:3000`.

## 📦 Deployment

### Vercel (Frontend)
1.  Push this repo to GitHub.
2.  Import into Vercel.
3.  Set Environment Variables if needed.

### Render (Backend)
1.  Push to GitHub.
2.  Create a "Web Service" on Render.
3.  Connect repo.
4.  Build Command: `pip install -r backend/requirements.txt`
5.  Start Command: `python backend/main.py`