import os
import google.generativeai as genai

# It's recommended to set your API key as an environment variable
# For example: os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY'
# For simplicity here, we will configure it directly.
# IMPORTANT: Replace "YOUR_API_KEY" with your actual key.
try:
    genai.configure(api_key="AIzaSyAt1wbl0tARh6pgEyu0edlgjNQ7vNFaZOU")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    # Handle the case where the API key is not set or invalid

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