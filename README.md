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

## 🚀 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/21lakshh/Kisaan-Sathi.git   
   cd Kisaan-Sathi
   ```
2. Install dependencies: // NEED TO ADD
   ```bash
   pip install -r requirements.txt
   ```
3. Create a **.env** file in the root directory and add your API keys:
   ```bash
   GROQ_API_KEY=your_groq_key_here
   DATA_GOV_API_KEY=your_data_gov_key_here
   GEMINI_API_KEY=your_gemini_key_here
   ```
4. Run the application:
   ```bash
   python app.py
   ```
