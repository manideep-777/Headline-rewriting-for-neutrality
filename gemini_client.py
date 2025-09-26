import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

# Load environment variables from a .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
    # Configure for Google AI Studio (not Vertex AI)
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def rewrite_headline(headline_text: str) -> List[str]:
    """
    Uses the Gemini API to rewrite a given headline to be more neutral, providing 5 options.
    
    Args:
        headline_text (str): The original headline to rewrite
        
    Returns:
        List[str]: List of 5 neutral alternative headlines
    """
    try:
        # Use gemini-1.5-flash (the correct model name for Google AI Studio)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert journalist and editor specialized in neutral, unbiased reporting. 
        Your task is to rewrite emotionally charged, biased, or loaded headlines into neutral, factual alternatives.

        Please rewrite the following headline to be more neutral and objective. Provide exactly 5 different neutral versions.

        Original headline: "{headline_text}"

        Guidelines:
        1. Remove emotional language and loaded words
        2. Focus on facts rather than opinions
        3. Use neutral, descriptive language
        4. Maintain the core information
        5. Avoid sensationalism
        6. Keep headlines concise and clear

        Provide your response as a numbered list of exactly 5 neutral headlines:
        1. [headline]
        2. [headline]
        3. [headline]
        4. [headline]
        5. [headline]
        """
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("No response from Gemini API")
        
        # Parse the response to extract headlines
        lines = response.text.strip().split('\n')
        neutral_headlines = []
        
        for line in lines:
            line = line.strip()
            # Look for numbered items (1., 2., etc.)
            if line and any(line.startswith(str(i) + '.') for i in range(1, 6)):
                # Remove numbering and clean up
                clean_line = line
                # Remove common numbering patterns
                for pattern in ['1.', '2.', '3.', '4.', '5.']:
                    if clean_line.startswith(pattern):
                        clean_line = clean_line[len(pattern):].strip()
                        break
                
                if clean_line and len(clean_line) > 10:  # Ensure it's a substantial headline
                    neutral_headlines.append(clean_line)
        
        # If we don't have exactly 5, try a different parsing approach
        if len(neutral_headlines) < 5:
            # Split by lines and look for any content that looks like headlines
            all_lines = response.text.split('\n')
            neutral_headlines = []
            
            for line in all_lines:
                line = line.strip()
                if line and len(line) > 15 and len(line) < 200:
                    # Remove various numbering patterns
                    for pattern in ['1.', '2.', '3.', '4.', '5.', '1)', '2)', '3)', '4)', '5)', '•', '-', '*']:
                        if line.startswith(pattern):
                            line = line[len(pattern):].strip()
                            break
                    
                    if line and not line.lower().startswith(('here are', 'neutral', 'alternative', 'guidelines', 'original')):
                        neutral_headlines.append(line)
                        
                    if len(neutral_headlines) >= 5:
                        break
        
        # Ensure we have exactly 5 headlines
        neutral_headlines = neutral_headlines[:5]  # Take first 5
        
        # If still not enough, add fallbacks
        while len(neutral_headlines) < 5:
            neutral_headlines.append(f"Neutral version of: {headline_text}")
        
        return neutral_headlines
        
    except Exception as e:
        print(f"An error occurred during API call: {e}")
        # Return fallback neutral headlines
        return [
            f"Report: {headline_text.replace('BREAKING:', '').replace('URGENT:', '').strip()}",
            f"Update regarding recent developments",
            f"News report on current situation",
            f"Information about ongoing events",
            f"Details on recent developments"
        ] 