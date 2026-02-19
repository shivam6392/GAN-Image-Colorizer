# This script creates a professional README.md file using pypandoc as required.

import pypandoc

# README content
readme_content = """
# 🎨 ChromaLab – AI Image Colorizer
**Project ID:** SIC/AI/010

ChromaLab is an AI-powered web application that transforms black & white images into realistic color images using deep learning and the SIGGRAPH 2017 colorization model.

---

## 📌 Overview

ChromaLab uses a pretrained PyTorch model to automatically colorize grayscale images. It combines a FastAPI backend with a modern Next.js frontend to provide fast and accurate results.

---

## 🧠 Model Details

- Model: Interactive Deep Colorization (SIGGRAPH 2017)
- Framework: PyTorch
- Model Size: 136MB
- Source: https://github.com/richzhang/colorization

---

## 🚀 Tech Stack

### Backend
- FastAPI
- PyTorch
- Python
- NumPy
- OpenCV
- Pillow

### Frontend
- Next.js 14
- Tailwind CSS
- Lucide React

### AI / Data Tools
- PyTorch
- Pandas
- Matplotlib

---

## ⚙️ Project Structure

ChromaLab/
│
├── backend/
│   ├── main.py
│   ├── download_model.py
│   ├── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── package.json
│
└── README.md

---

## 🛠️ Local Setup

### Backend Setup

cd backend

python -m venv venv

Windows:
venv\\Scripts\\activate

Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

python download_model.py

python main.py

Backend runs at:
http://localhost:8000

---

### Frontend Setup

cd frontend

npm install

npm run dev

Frontend runs at:
http://localhost:3000

---

## 🌐 Deployment

### Frontend (Vercel)

- Push repo to GitHub
- Import in Vercel
- Deploy

### Backend (Render)

Build Command:
pip install -r backend/requirements.txt

Start Command:
python backend/main.py

---

## ✨ Features

- Automatic image colorization
- Deep learning powered model
- Fast REST API backend
- Modern responsive frontend
- Easy deployment

---

## 🎯 Applications

- Historical photo restoration
- Photo enhancement
- AI research projects
- Educational purposes

---

## 👨‍💻 Author

Shivam Dwivedi  
B.Tech CSE  
AI & Full Stack Developer

---

## 📜 License

This project is for educational purposes.
"""

# Save using pypandoc
output_path = "/mnt/data/README.md"
pypandoc.convert_text(readme_content, 'md', format='md', outputfile=output_path, extra_args=['--standalone'])

output_path
