from flask import Flask, render_template, redirect, url_for, session, request, g
from modules.auth import auth_bp
from modules.crud import crud_bp
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from functools import wraps
from modules.database import query_all_users
import logging
import secrets

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Database configuration from environment variables
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DATABASE = 'my_database'
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')


try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    # Test the database connection
    client.admin.command('ping')
    logger.info("✅ Connected to MongoDB successfully!")
    db = client[MONGO_DATABASE]  # Access the specified database
    users = query_all_users()
    logger.info(f"✅ Users in the database: {users}")
except Exception as e:
    logger.exception("❌ Failed to connect to MongoDB")
    exit(1)

app.register_blueprint(auth_bp)
app.register_blueprint(crud_bp)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)            
        else:
            logger.warning("⛔️ Unauthenticated user attempted to access a protected route.")
            return redirect(url_for('auth.login'))
    return decorated_function

@app.route('/welcome')
@login_required
def welcome():
    logger.info(f"🔑 User is authenticated. Welcome page.")
    return render_template('welcome.html', username=session['username'])

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']

@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"🚫 404 Error: Page not found - {request.url}")
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"🔥 500 Error: Internal server error - {request.url} - {e}")
    return render_template('error.html'), 500

if __name__ == '__main__':
    logger.info("🚀 Application starting up.")

    app.run(debug=True)
