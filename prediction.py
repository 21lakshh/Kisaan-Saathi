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
    prediction_model = tf.keras.models.load_model(os.path.join(working_dir, "Disease prediction Model", "trained_model", "plant_disease_prediction.h5"))
    class_indices_path = os.path.join(working_dir, "Disease prediction model", "class_indices.json")

    with open(class_indices_path, "r") as f:
        content = f.read()
        # print("File content:", content)
        class_indices = json.loads(content)

    return prediction_model, class_indices

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

def model_response(image_path, selected_language):

    disease = predict_disease(image_path)

    if not disease:
        raise ValueError("Could not classify disease from the given input image.")
    lang_code = LANGUAGES[selected_language]
    
    