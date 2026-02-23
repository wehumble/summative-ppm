import json
import os

# Path to data file (relative to project root)
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'project_tracker.json')

def load_data():
    """Load data from JSON file. Returns empty dict if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, return empty dict (or could raise)
        return {}

def save_data(data):
    """Save data dictionary to JSON file, creating directories if needed."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)