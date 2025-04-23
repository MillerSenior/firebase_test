import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

data = load_data()

