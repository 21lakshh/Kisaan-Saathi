from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
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
import google.generativeai as genai
from pydantic import BaseModel

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
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

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
    return templates.TemplateResponse(
        "market-analysis.html",
        {
            "request": request,
            "data_gov_api_key": DATA_GOV_API_KEY
        }
    )

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

@app.get("/schemes.html", response_class = HTMLResponse)
async def schemes_page(request: Request):
    return templates.TemplateResponse("schemes.html",{"request":request})

# @app.get("/waste-exchange.html", response_class = HTMLResponse)
# async def waste_exchange_page(request: Request):
#     return templates.TemplateResponse("waste-exchange.html",{"request":request})

@app.post("/disease_prediction")
async def disease_prediction(file: UploadFile = File(...), selected_language: str = Form(...)):
    try:
        logger.info(f"Received request with file: {file.filename}, selected_language: {selected_language}")
        
        # Validate language
        if not selected_language:
            raise HTTPException(status_code=400, detail="Language is required")
            
        # Read the uploaded image file
        contents = await file.read()
        logger.info(f"Read {len(contents)} bytes from uploaded file")
        
        # Validate the image format
        try:
            img = Image.open(io.BytesIO(contents))
            img.verify()
            logger.info("Image format validated successfully")
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

        # Save the image temporarily
        temp_image_path = f"temp_{file.filename}"
        try:
            with open(temp_image_path, "wb") as temp_file:
                temp_file.write(contents)
            logger.info(f"Saved temporary file to: {temp_image_path}")

            # Call the classification function
            logger.info(f"Processing image with language: {selected_language}")
            response = model_response(temp_image_path, selected_language)
            logger.info(f"Model response type: {type(response)}")
            logger.info(f"Model response: {response}")
            
            # Check if there was an error in the response
            if "error" in response:
                logger.error(f"Model returned error: {response['error']}")
                raise HTTPException(status_code=500, detail=response["error"])
            
            # Return the response directly as it's already in the correct format
            return JSONResponse(status_code=200, content=response)
            
        except Exception as e:
            logger.error(f"Error in model_response: {str(e)}", exc_info=True)
            error_detail = str(e)
            if hasattr(e, 'detail'):
                error_detail = e.detail
            raise HTTPException(status_code=500, detail=f"Error in model processing: {error_detail}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
                logger.info(f"Removed temporary file: {temp_image_path}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'detail'):
            error_detail = e.detail
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {error_detail}"
        )

@app.post("/api/chat")
async def chat(request: Request):
    try:
        # Get the question from the request body
        body = await request.json()
        question = body.get('question', '')
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
            
        # Generate response using Gemini
        response = model.generate_content(
            f"""You are an AI assistant helping farmers understand government schemes. 
            Please provide detailed, accurate information about the following question related to government schemes for farmers.
            Format your response with:
            - Use **bold** for important points
            - Use *italics* for emphasis
            - Include relevant links where applicable
            - Use bullet points for lists
            - Add line breaks between sections
            - Keep the language simple and easy to understand
            
            If the question is not about government schemes, politely inform the user that you can only help with government scheme related queries.
            
            Question: {question}"""
        )
        
        return JSONResponse(content={"response": response.text})
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

import uvicorn
uvicorn.run(app, port=8000)