import google.generativeai as genai
import os
from dotenv import load_dotenv
import tensorflow as tf
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")
# Load environment variables
genai.configure(api_key=GEMINI_API_KEY)

models = genai.list_models()
for model in models:
    print(model.name)

print(tf.__version__)