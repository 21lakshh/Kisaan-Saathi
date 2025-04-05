from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, JSONResponse 
import base64
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os
import logging
from fastapi.staticfiles import StaticFiles
import pandas as pd
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")   

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API KEY is not set in the .env file")

@app.get("/", response_class = HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/donation.html", response_class = HTMLResponse)
async def donation_page(request: Request):
    return templates.TemplateResponse("donation.html",{"request":request})

@app.get("/dashboard.html", response_class = HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request":request})

@app.get("/crop-care.html", response_class = HTMLResponse)
async def crop_care_page(request: Request):
    return templates.TemplateResponse("crop-care.html",{"request":request})

@app.get("/market-analysis.html", response_class = HTMLResponse)
async def market_analysis_page(request: Request):
    return templates.TemplateResponse("market-analysis.html",{"request":request})

import uvicorn
uvicorn.run(app, port=8000)