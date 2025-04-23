import logging
from flask import Blueprint, jsonify
from modules.models import Crud
from modules.database import load_data, save_data

crud_bp = Blueprint('crud', __name__)

logging.basicConfig(level=logging.INFO)

def create_crud(title, content):
    """➕ Create a new CRUD entry and save it to the database file."""
    logging.info(f"➕ Attempting to create CRUD entry: {title}")
    try:
        data = load_data()
        cruds = data['cruds']
        new_crud = Crud(id=len(cruds) + 1 if cruds else 1, title=title, content=content)
        cruds.append(new_crud.to_dict())
        save_data(data)
        logging.info(f"✅ CRUD entry created successfully: {title}")
        return new_crud
    except Exception as e:
        logging.error(f"➖ Failed to create CRUD entry: {title} - {e}")
        return None

def read_crud(crud_id):
    """📖 Read a CRUD entry by ID from the database file."""
    logging.info(f"📖 Attempting to read CRUD entry with ID: {crud_id}")
    try:
        data = load_data()
        cruds = data['cruds']
        crud_data = next((c for c in cruds if c['id'] == crud_id), None)
        if crud_data is None:
            logging.warning(f"⚠️ CRUD entry not found with ID: {crud_id}")
            return None
        crud = Crud.from_dict(crud_data)
        logging.info(f"✅ CRUD entry found: {crud.title}")
        return crud
    except Exception as e:
        logging.error(f"➖ Failed to read CRUD entry with ID {crud_id}: {e}")
        return None

def update_crud(crud_id, title, content):
    """🔄 Update a CRUD entry by ID in the database file."""
    logging.info(f"🔄 Attempting to update CRUD entry with ID: {crud_id}")
    try:
        data = load_data()
        cruds = data['cruds']
        for crud_data in cruds:
            if crud_data['id'] == crud_id:
                crud_data['title'] = title
                crud_data['content'] = content
                save_data(data)
                logging.info(f"✅ CRUD entry updated successfully: {title}")
                return Crud.from_dict(crud_data)        
        logging.warning(f"⚠️ CRUD entry not found with ID: {crud_id}")
        return None    
    except Exception as e:
        logging.error(f"➖ Failed to update CRUD entry with ID {crud_id}: {e}")
        return None

def delete_crud(crud_id):
    """🗑️ Delete a CRUD entry by ID from the database file."""
    logging.info(f"🗑️ Attempting to delete CRUD entry with ID: {crud_id}")
    try:
        data = load_data()
        cruds = data['cruds']
        crud_index = next((i for i, c in enumerate(cruds) if c['id'] == crud_id), None)
        if crud_index is not None:
            cruds.pop(crud_index)
            save_data(data)
            logging.info(f"✅ CRUD entry deleted successfully: {crud_id}")
            return True
        else:            
            logging.warning(f"⚠️ CRUD entry not found with ID: {crud_id}")
            return False
    except Exception as e:
        db.session.rollback()
        logging.error(f"➖ Failed to delete CRUD entry with ID {crud_id}: {e}")
        return False
