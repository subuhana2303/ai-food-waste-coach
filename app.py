import os
import logging
from flask import Flask
from flask_session import Session
from flask_cors import CORS

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)

# Configure secret key for sessions
app.secret_key = os.environ.get("SESSION_SECRET", "ai-food-waste-coach-secret-key-2024")

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# Enable CORS for API requests
CORS(app)

# Import routes after app creation to avoid circular imports
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
