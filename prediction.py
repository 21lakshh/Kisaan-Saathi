import os
import tensorflow as tf
import json
from PIL import Image
import numpy as np
import io
import logging
import base64
import requests
from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

working_dir = os.getcwd()

# print("Your working directory is: ", working_dir)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API KEY is not set in the .env file")
def load_resources():
    try:
        model_path = os.path.join(working_dir, "Disease prediction Model", "trained_model", "plant_disease_prediction.h5")
        class_indices_path = os.path.join(working_dir, "Disease prediction Model", "class_indices.json")

        logger.info(f"Loading model from: {model_path}")
        logger.info(f"Loading class indices from: {class_indices_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        if not os.path.exists(class_indices_path):
            raise FileNotFoundError(f"Class indices file not found at: {class_indices_path}")

        prediction_model = tf.keras.models.load_model(model_path)
        logger.info("Model loaded successfully")

        with open(class_indices_path, "r") as f:
            content = f.read()
            class_indices = json.loads(content)
            logger.info("Class indices loaded successfully")

        return prediction_model, class_indices
    except Exception as e:
        logger.error(f"Error loading resources: {str(e)}", exc_info=True)
        raise

prediction_model, class_indices = load_resources()

LANGUAGES = {
    "English": "en", # English 
    "हिन्दी": "hi", # Hindi 
    "ਪੰਜਾਬੀ": "pa", # Punjabi 
    "ಕನ್ನಡ": "kn" # Kannada
}
def load_and_preprocess_image(image):
    img = Image.open(image).resize((224, 224))
    return np.expand_dims(np.array(img)/255.0, axis=0)

def predict_disease(image):
    processed_image = load_and_preprocess_image(image)
    predictions = prediction_model.predict(processed_image)
    predicted_class = class_indices[str(np.argmax(predictions))]
    return predicted_class

def model_response(image_path: str, selected_language: str) -> dict:
    try:
        logger.info(f"Processing image: {image_path}")
        logger.info(f"Selected language: {selected_language}")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        disease = predict_disease(image_path)
        logger.info(f"Predicted disease: {disease}")

        if not disease:
            raise ValueError("Could not classify disease from the given input image.")
        
        if selected_language not in LANGUAGES:
            raise ValueError(f"Unsupported language: {selected_language}")
        
        lang_code = LANGUAGES[selected_language]
        logger.info(f"Using language code: {lang_code}")

        # Read and encode the image
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()
            encoded_image = base64.b64encode(image_content).decode("utf-8")
            logger.info("Image encoded successfully")

        # Validate the image format
        try:
            img = Image.open(io.BytesIO(image_content))
            img.verify()
            logger.info("Image format validated successfully")
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}", exc_info=True)
            return {"error": f"Invalid image format: {str(e)}"}
        
        query = f"Given the crop disease: {disease}, please provide a detailed explanation of its causes, prevention methods, and treatment options. Respond in the following language: {selected_language}."
        logger.info(f"Generated query: {query}")

        # Format the message according to GROQ API requirements
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # API Request
        logger.info("Sending request to GROQ API")
        response = requests.post(
            GROQ_API_URL,
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "max_tokens": 4000
            },
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            logger.info("Successfully received response from GROQ API")
            return result
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"error": error_msg}
        
    except FileNotFoundError as e:
        error_msg = f"Image file not found: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON response: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
    
if __name__ == "__main__":
    from fastapi.responses import HTMLResponse, JSONResponse 
    image_path = "C:/Users/LAKSHYA PALIWAL/Downloads/Deploy using streamlit/Crop Disease Deteciton/0b943ada-01a9-4ce0-a607-e799394856de___Crnl_L.Mold 7008.JPG"
      # Replace with actual uploaded image path
    additional_info = "The dog seems to be limping and has a small wound on its leg."
    result = model_response(image_path, selected_language="English")
    # result = response.json()
    print(result["choices"][0]["message"]["content"])