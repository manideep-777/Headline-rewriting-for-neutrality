# Headline Rewriter for Neutrality

This web application reframes emotionally loaded or biased headlines into neutral versions using the Google Gemini API. Users can input a headline, and the tool will provide five alternative, more objective headlines.

## Features

- **Simple Web Interface**: A clean and easy-to-use UI for submitting headlines.
- **AI-Powered Rewriting**: Leverages the Google Gemini API to generate neutral text.
- **Multiple Options**: Provides a list of 5 alternative headlines for the user to choose from.
- **Asynchronous Requests**: Fetches rewritten headlines from the backend without reloading the page.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Google Gemini (`gemini-1.5-flash`)

## Setup and Installation

Follow these steps to run the project locally.

### 1. Prerequisites

- Python 3.8+
- A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository

```bash
git clone <repository-url>
cd "Headline rewriting for neutrality"
```

### 3. Create and Activate a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Open the `gemini_client.py` file and replace the placeholder `"YOUR_API_KEY"` with your actual Google Gemini API key.

```python
# In gemini_client.py
genai.configure(api_key="YOUR_API_KEY") # <-- Paste your key here
```

### 6. Run the Application

```bash
python app.py
```

The application will be running at `http://127.0.0.1:5000`.

## How to Use

1.  Open your web browser and navigate to `http://127.0.0.1:5000`.
2.  Enter an emotionally charged or biased headline into the text area.
3.  Click the **Rewrite** button.
4.  A list of five neutral headline suggestions will appear below the form.

## Deployment

This is a Flask application with a Python backend, so it cannot be deployed directly to static hosting services like Netlify.

For deployment, you should use a platform that supports Python web applications, such as:
- **Render**
- **Heroku**
- **PythonAnywhere**
- **Vercel** (requires adapting the app to a serverless function structure) 