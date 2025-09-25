from flask import Flask, render_template, request, jsonify, session
from gemini_client import rewrite_headline
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# In-memory storage for demo (use a database in production)
user_histories = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rewrite', methods=['POST'])
def rewrite():
    data = request.get_json()
    headline = data.get('headline')

    if not headline:
        return jsonify({'error': 'Headline is required'}), 400

    # Get or create user session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']

    try:
        neutral_headlines = rewrite_headline(headline)
        
        # Store in server-side history (optional)
        if user_id not in user_histories:
            user_histories[user_id] = []
        
        history_item = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'original': headline,
            'neutrals': neutral_headlines
        }
        
        user_histories[user_id].insert(0, history_item)
        # Keep only last 50 items
        if len(user_histories[user_id]) > 50:
            user_histories[user_id] = user_histories[user_id][:50]
        
        return jsonify({'neutral_headlines': neutral_headlines})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({'history': []})
    
    user_id = session['user_id']
    history = user_histories.get(user_id, [])
    return jsonify({'history': history})

@app.route('/history', methods=['DELETE'])
def clear_history():
    if 'user_id' in session:
        user_id = session['user_id']
        user_histories[user_id] = []
    return jsonify({'success': True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
