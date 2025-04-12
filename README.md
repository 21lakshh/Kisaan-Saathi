# 🌾 Kisaan Saathi – Empowering Farmers with AI

**Kisaan Saathi** is a comprehensive **AI-powered Farmer Dashboard** designed to support Indian farmers through real-time data, smart decision-making tools, and access to vital resources. From intelligent crop disease diagnosis to market price analysis, equipment rental, and weather forecasting — Kisaan Saathi is your digital companion in the field.

---

## 🚀 Features

### 🧬 Crop Care & Disease Detection  
- Powered by a **custom-trained Xception model** to detect crop diseases across **38 unique categories**.  
- Detected disease details are passed to an **LLM** to generate:
  - ✅ Cause  
  - 🌱 Prevention  
  - 💊 Treatment  
- Equipped with an **AI-powered hotspot mapping system** using **DBSCAN** clustering to:
  - Visualize disease-affected areas.
  - Help **government agencies** prioritize land inspections based on report density.

---

### 🤖 Farmer AI Assistant – Multi-Agent RAG System  
- Built with a **multi-agent architecture**.  
- Uses **RAG (Retrieval-Augmented Generation)** with **ChromaDB vector storage** for Mental Health Support.  
- Ask anything – from farming tips to market advice.

---

### 📊 Market Analysis  
- Real-time crop pricing via external **agri-market APIs**.  
- Helps farmers counter unfair middlemen pricing with live rate insights.  
- Enables better selling decisions and pricing power.

---

### 🏛️ Government Schemes  
- A centralized page for all **ongoing agricultural schemes**.  
- View **eligibility**, **benefits**, and **application steps** in one place.

---

### 🌦️ Weather Advisory  
- Fetches accurate weather updates via **Weather API**.  
- Offers actionable insights:
  - Rain alerts  
  - Sowing/harvesting time suggestions  
  - Extreme condition warnings  

---

### 🔁 Crop Waste Exchange  
- Farmers can **sell/exchange crop waste** for monetary value.  
- Supports government initiatives for **biogas and biofuel** production.

---

### 🚜 Equipment Rental  
- Access to nearby **equipment rental options** at affordable rates.  
- Makes farming resources more accessible to small and marginal farmers.

---

## 🛠️ Tech Stack

- **Frontend:** HTML, TailwindCSS, JavaScript  
- **Backend:** FastAPI  
- **Machine Learning:** TensorFlow, Scikit-learn  
- **AI/LLM Integration:** LangChain, LangGraph, ChromaDB (for vector storage), Groq LLM, Gemini API  
- **APIs:** Weather API, Market Price APIs

---

## 📸 Screenshots  
*Add screenshots of the dashboard, crop detection page, AI assistant chat, and hotspot maps here.*

---

## 📌 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/kisaan-saathi.git
cd kisaan-saathi
```bash
# Install backend dependencies
pip install -r requirements.txt

# Run the FastAPI backend
uvicorn main:app --reload

# Serve frontend (via live server or integrate with FastAPI templates)
