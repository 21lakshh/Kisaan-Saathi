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
from prediction import model_response
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

@app.get("/equipment-rental.html", response_class = HTMLResponse)
async def equipment_rental_page(request: Request):
    return templates.TemplateResponse("equipment-rental.html",{"request":request})

@app.get("/farmer-assistant.html", response_class = HTMLResponse)
async def farmer_assistant_page(request: Request):
    return templates.TemplateResponse("farmer-assistant.html",{"request":request})

@app.get("/soil-health.html", response_class = HTMLResponse)
async def soil_health_page(request: Request):
    return templates.TemplateResponse("soil-health.html",{"request":request})

@app.get("/weather-advisory.html", response_class = HTMLResponse)
async def weather_advisory_page(request: Request):
    return templates.TemplateResponse("weather-advisory.html",{"request":request})

# @app.get("/schemes.html", response_class = HTMLResponse)
# async def schemes_page(request: Request):
#     return templates.TemplateResponse("schemes.html",{"request":request})

# @app.get("/waste-exchange.html", response_class = HTMLResponse)
# async def waste_exchange_page(request: Request):
#     return templates.TemplateResponse("waste-exchange.html",{"request":request})

@app.post("/disease_prediction")
async def disease_prediction(file: UploadFile = File(...), selected_language: str = Form("")):
    try:
        # Read the uploaded image file
        contents = await file.read()
        
        # Validate the image format
        try:
            img = Image.open(io.BytesIO(contents))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

        # Save the image temporarily
        temp_image_path = f"temp_{file.filename}"
        with open(temp_image_path, "wb") as temp_file:
            temp_file.write(contents)

        # Call the classification function
        result = model_response(temp_image_path, selected_language)
        
        # Remove the temporary image file after processing
        os.remove(temp_image_path)
        
        return JSONResponse(status_code=200, content=result)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



import uvicorn
uvicorn.run(app, port=8000)