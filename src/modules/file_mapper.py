import os
import json
from conf.configurator import get_research_paper_repository,get_research_paper_file_map

def generate_file_map():
    """Traverse subdirectories and create a map of filenames and their full paths."""
    DATA_PATH = get_research_paper_repository()
    FILE_MAP = get_research_paper_file_map()
    file_map = {}
    
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                file_map[file] = file_path
    
    # Save the map to a JSON file
    with open(FILE_MAP, "w") as json_file:
        json.dump(file_map, json_file)

def load_file_map():
    """Load the file map from the JSON file."""
    FILE_MAP = get_research_paper_file_map()
    with open(FILE_MAP, "r") as json_file:
        return json.load(json_file)


