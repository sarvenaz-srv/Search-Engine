from search_engine.constants import DATA_FILE_PATH
import json

def get_all_docs() -> dict:
    with open(DATA_FILE_PATH, encoding='utf-8') as f:
        return json.load(f)
    
