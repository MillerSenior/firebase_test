from flask import Flask, render_template, redirect, url_for, session, request, g
from modules.auth import auth_bp
from modules.crud import crud_bp
from dotenv import load_dotenv
import os
from functools import wraps
import logging
import secrets

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
