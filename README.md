![github-submission-banner](https://github.com/user-attachments/assets/a1493b84-e4e2-456e-a791-ce35ee2bcf2f)

# 🌾 Kisaan Saathi – Empowering Farmers with AI

> A one-stop AI-powered dashboard revolutionizing farming decisions through disease diagnosis, water management, market analysis, and real-time assistance.

---

## 📌 Problem Statement

**Problem Statement 1 – Weave AI magic with Groq**

---

## 🎯 Objective

Kisaan Saathi is designed to empower Indian farmers by integrating AI into everyday agricultural practices.  
It addresses key challenges like disease detection, market pricing, resource management, and access to government schemes, helping farmers make smarter, faster, and more profitable decisions.

---

## 🧠 Team & Approach

### Team Name:  
`BLOOM`

### Team Members:  
- Lakshya Paliwal ([GitHub](https://github.com/21lakshh))

### Your Approach:  
- Selected to solve real agricultural inefficiencies impacting millions of farmers.  
- Focused on making AI accessible and usable at the grassroots level.  
- Tackled challenges like multi-language support, real-time clustering, and integrating external APIs.  
- Pivoted towards multi-agent systems to better personalize farmer assistance.

---

## 🛠️ Tech Stack

### Core Technologies Used:
- **Frontend:** HTML5, TailwindCSS, JavaScript, Chart.js
- **Backend:** FastAPI, Uvicorn
- **Database:** ChromaDB (for vector storage)
- **APIs:** Weather API, Market Price APIs, Gemini API
- **Hosting:** Local Deployment / Cloud-ready

### Sponsor Technologies Used (if any):
- ✅ **Groq:**

---

## ✨ Key Features

- ✅ 🧬 Crop Care & Disease Detection (38-category Xception model + LLM for Cause/Prevention/Treatment)
- ✅ 💧 Water Footprint Calculator (ML-driven irrigation needs estimation)
- ✅ 🤖 Farmer AI Assistant (Multi-agent RAG for mental health, farming tips, market guidance)
- ✅ 📊 Market Analysis Dashboard (Real-time crop prices, price trends)
- ✅ 🏛️ Government Schemes Hub (Eligibility & Application guidance)
- ✅ 🌦️ Weather Advisory (Forecasts + Crop Advice)
- ✅ 🔁 Crop Waste Exchange Platform
- ✅ 🚜 Equipment Rental Finder

---

## 📽️ Demo & Deliverables

- **Demo Video Link:** [Watch Here](https://youtu.be/XoOM4berjAY)  

---

## ✅ Tasks & Bonus Checklist

- [✅] **All members completed mandatory social media and form tasks**  
- [✅] **Bonus Task 1 - Shared badges on social media**  
- [✅] **Bonus Task 2 - Signed up for Sprint.dev and filled form**

---

## 🧪 How to Run the Project

### Requirements:
- Python 3.8+
- Git
- API Keys (Groq, Gemini, Weather API, Market Price API)
- `.env` file setup

### Local Setup:
```bash
# Clone the repo
git clone https://github.com/21lakshh/Kisaan-Sathi.git   
cd Kisaan-Sathi

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt // Not added yet

# Setup Environment Variables
# Create a .env file and add the following:
GROQ_API_KEY=your_groq_key_here
DATA_GOV_API_KEY=your_data_gov_key_here
GEMINI_API_KEY=your_gemini_key_here
OPEN_WEATHER_API_KEY=your_weather_api_key_here

# Run the Application
python app.py
