import logging
from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import query_all_users, db


auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')

            if not username or not password or not email:
                logger.error("➖ Missing username, password, or email during registration")
                flash("Missing username, password, or email", "error")
                return redirect(url_for('auth.register'))

            users_collection = db['users']
            existing_user = users_collection.find_one({'username': username})

            if existing_user:
                logger.error(f"➖ Username '{username}' already exists during registration")
                flash("Username already exists", "error")
                return redirect(url_for('auth.register'))  # Redirect back to registration

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Insert the new user into the database
            users_collection.insert_one({
                'username': username, 
                'password': hashed_password, 
                'email': email})

            logger.info(f"➕ User '{username}' registered successfully")
            flash("Registration successful", "success")
            return redirect(url_for('welcome'))

        except Exception as e :
            logger.error(f"➖ Error during registration: {e}")
            flash("Error during registration", "error")
            return redirect(url_for('auth.register'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                logger.error("⛔️ Missing username or password during login")
                flash("Missing username or password", "error")
                return redirect(url_for('auth.login'))

            users_collection = db['users']
            user = users_collection.find_one({'username': username})

            if user and check_password_hash(user['password'], password):               
                session['username'] = username
                logger.info(f"🔑 User: {username} has logged in successfully")
                flash(f"Welcome {username}", "success")
                # Add user to session
                return redirect(url_for('welcome'))  # Redirect to the welcome page

            logger.error(f"⛔️ Invalid credentials for user: {username}")
            flash("Invalid credentials", "error")
            return redirect(url_for('auth.login'))

        except Exception as e:
            logger.error(f"⛔️ Error during login: {e}")
            flash("Error during login", "error")
            return redirect(url_for('auth.login'))
    return render_template('login.html')









