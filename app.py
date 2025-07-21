from flask import Flask, render_template, request, jsonify
from gemini_client import rewrite_headline
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rewrite', methods=['POST'])
def rewrite():
    data = request.get_json()
    headline = data.get('headline')

    if not headline:
        return jsonify({'error': 'Headline is required'}), 400

    neutral_headlines = rewrite_headline(headline)
    return jsonify({'neutral_headlines': neutral_headlines})

# if __name__ == '__main__':
#     app.run(debug=True) 

# for production
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
