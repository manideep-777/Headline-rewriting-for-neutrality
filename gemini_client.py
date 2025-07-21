import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def rewrite_headline(headline_text):
    """
    Uses the Gemini API to rewrite a given headline to be more neutral, providing 5 options.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Rewrite this headline to be neutral: \"{headline_text}\". Respond with a list of 5 different neutral versions, each on a new line, and nothing else."
    
    try:
        response = model.generate_content(prompt)
        # Split the response text by newlines and filter out any empty strings
        headlines = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        return headlines
    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return ["Error: Could not rewrite headline."] 