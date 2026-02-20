# Image Colorization using GANs & Deep Learning

> **Samsung Innovation Challenge (SIC) - Group Project**  
> Transform historical black & white photography into vibrant reality using state-of-the-art Deep Learning models (CNN/GAN).

![Project Preview](https://github.com/shivam6392/GAN-Image-Colorizer/assets/placeholder.png)

## 👥 Team Members

| Name | Student ID |
|:--- |:--- |
| **Arunangshu Roy** | 23BCS11789 |
| **Shivam Dwivedi** | 23BCS11887 |
| **Yuvraj Singh** | 23BCS11868 |
| **Saksham Rana** | 23BCS13526 |
| **Chanchal Karwasra** | 23BCS12557 |

---

## ✨ Features

-   **� Deep Learning Restoration**: Utilizes the **SIGGRAPH 2017** (Zhang et al.) Convolutional Neural Network (CNN) for high-fidelity results.
-   **🌌 Ethereal Cyberpunk UI**: Modern glassmorphic interface built with Next.js & Tailwind.
-   **⚡ Real-time Inference**: Optimized forward pass on CPU.
-   **🔍 Interactive Comparison**: Sliding tool to view Original vs. Generated Output.
-   **🖼️ Smart Resizing**: Handles all aspect ratios without cropping.

## 🛠️ Tech Stack

-   **Frontend**: Next.js 14, Tailwind CSS, Lucide React
-   **Backend**: FastAPI, PyTorch (Deep Learning Framework), Scikit-Image
-   **Architecture**: CNN (Convolutional Neural Network) / GAN-based approach
-   **Deployment**: Vercel (Frontend) + Render (Backend)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/shivam6392/GAN-Image-Colorizer.git
cd GAN-Image-Colorizer
```

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python download_model.py
python main.py
```
*Server runs on `http://localhost:8000`*

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*App runs on `http://localhost:3000`*

---

## ☁️ Deployment

### Backend (Render)
1.  Deploy `backend` folder as Web Service.
2.  **Build**: `pip install -r backend/requirements.txt`
3.  **Start**: `python backend/main.py`

### Frontend (Vercel)
1.  Import repo, set root to `frontend`.
2.  Env Var: `NEXT_PUBLIC_API_URL` -> Your Render Backend URL.

---

<p align="center">
  <b>Samsung Innovation Challenge</b> • Deep Learning Group Project
</p>
