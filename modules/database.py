import json
import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global db variable
db = None

# Instead of using SQLAlchemy, we'll use a JSON file for data storage
DB_FILE = 'data.json'

# This function will load the data from the JSON file
def load_data():
    logger.info("🔄 Attempting to load data from the file.")
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                logger.info(f"✅ Data successfully loaded from '{DB_FILE}'.")
                return data
        else:
            logger.warning(f"⚠️ Data file '{DB_FILE}' not found. Creating a new empty data structure.")
            return {'users': [], 'cruds': []}
    except Exception as e:
        logger.error(f"➖ Error loading data from the file: {e}")
        return {'users': [], 'cruds': []}

# This function will save the data to the JSON file
def save_data(data):
    logger.info("💾 Attempting to save data to the file.")
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"✅ Data successfully saved to '{DB_FILE}'.")
    except Exception as e:
        logger.error(f"➖ Error saving data to the file: {e}")

# Load environment variables
load_dotenv()
# find_dotenv() is added to allow multiple .env files
load_dotenv(find_dotenv())

# Get MongoDB URI and DB Name from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

try:
    client = MongoClient(MONGO_URI)
    # The ping command is cheap and does not require auth.
    client.admin.command('ping')
    logger.info("✅ MongoDB connection successful.")
    # Access database
    db = client[MONGO_DB_NAME]

    if 'users' not in db.list_collection_names():
        db.create_collection('users')
        logger.info("✅ 'users' collection created.")

except ConnectionFailure as e:
    logger.error(f"❌ MongoDB connection failed: {e}")

# Test collection
def query_all_users():
    try:
        users_collection = db['users']
        users = list(users_collection.find({}))
        return users
    except Exception as e:
        logger.error(f"➖ Error querying users: {e}")
        return []
    
def print_all_users():
    users = query_all_users()
    if users:
        logger.info("👥 Users in database:")
        for user in users:
            logger.info(user)

data = load_data() # load data from json file
print_all_users() # print users from mongo db

