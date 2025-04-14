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
from FarmerAssistant import app as farmer_assistant_app, main as init_farmer_assistant
from langchain_core.messages import HumanMessage, AIMessage
import joblib
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")   

# Load the water footprint model
try:
    water_footprint_model = joblib.load('Water Footprint Model/Model/water_footprint_model.pkl')
    logger.info("Water footprint model loaded successfully")
except Exception as e:
    logger.error(f"Error loading water footprint model: {str(e)}")
    water_footprint_model = None

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

# Initialize Farmer Assistant
init_farmer_assistant()

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

@app.get("/water-footprint.html", response_class = HTMLResponse)
async def water_footprint_page(request: Request):
    return templates.TemplateResponse("water-footprint.html",{"request":request})

@app.get("/weather-advisory.html", response_class = HTMLResponse)
async def weather_advisory_page(request: Request):
    return templates.TemplateResponse("weather-advisory.html",{"request":request})

@app.get("/schemes.html", response_class = HTMLResponse)
async def schemes_page(request: Request):
    return templates.TemplateResponse("schemes.html",{"request":request})

@app.get("/waste-exchange.html", response_class = HTMLResponse)
async def waste_exchange_page(request: Request):
    return templates.TemplateResponse("waste-exchange.html",{"request":request})

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

@app.post("/api/farmer-chat")
async def farmer_chat(request: Request):
    try:
        # Get the request data
        body = await request.json()
        question = body.get('question', '')
        chat_history = body.get('chat_history', [])  # Expect array of strings
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        # Convert string history to LangChain messages
        lc_history = []
        try:
            for i in range(0, len(chat_history), 2):
                if i+1 < len(chat_history):
                    lc_history.append(HumanMessage(content=chat_history[i]))
                    lc_history.append(AIMessage(content=chat_history[i+1]))
        except Exception as e:
            logger.error(f"Error converting chat history: {str(e)}")
            # If there's an error with history, start fresh
            lc_history = []

        # Process through LangChain
        try:
            current_state = {
                "query": question,
                "chat_history": lc_history
            }
            final_state = farmer_assistant_app.invoke(current_state)

            # Convert LangChain messages back to strings
            serialized_history = []
            for msg in final_state["chat_history"]:
                if isinstance(msg, (HumanMessage, AIMessage)):
                    serialized_history.append(msg.content)
            print(final_state["response"])
            return JSONResponse(content={
                "response": final_state["response"],
                "chat_history": serialized_history
            })
        
        except Exception as e:
            logger.error(f"Error in LangChain processing: {str(e)}")
            # Return a basic response if LangChain processing fails
            return JSONResponse(content={
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again later.",
                "chat_history": chat_history  # Keep existing history
            })
        
    except Exception as e:
        logger.error(f"Error in farmer chat: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Chat processing error: {str(e)}"}
        )

@app.post("/api/calculate-water-footprint")
async def calculate_water_footprint(request: Request):
    try:
        if water_footprint_model is None:
            raise HTTPException(status_code=500, detail="Water footprint model not available")
            
        data = await request.json()
        
        # Create input DataFrame
        input_data = pd.DataFrame([{
            'CropType': data['cropType'],
            'Region': data['region'],
            'SoilType': data['soilType'],
            'IrrigationMethod': data['irrigationMethod'],
            'Rainfall': float(data['rainfall']),
            'Temperature': float(data['temperature']),
            'Humidity': float(data['humidity'])
        }])
        
        # Make prediction
        prediction = water_footprint_model.predict(input_data)[0]
        
        # Calculate daily and weekly requirements
        area = float(data['area'])
        total_water = prediction * area / 1000  # Convert to cubic meters per hectare
        water_per_day = total_water / 90  # Assuming 90 days growing period
        water_per_week = water_per_day * 7
        
        return JSONResponse(content={
            'totalWater': total_water,
            'dailyWater': water_per_day,
            'weeklyWater': water_per_week
        })
        
    except Exception as e:
        logger.error(f"Error calculating water footprint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Remove or comment out the direct uvicorn run
# import uvicorn
# uvicorn.run(app, port=8000)

# Replace with this:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)