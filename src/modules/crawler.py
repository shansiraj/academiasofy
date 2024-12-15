import os
import json
from PyPDF2 import PdfReader
from src.modules.pre_processor import preprocess_text
from src.modules.pdf_reader import extract_text_from_pdf
from conf.configurator import get_positional_index,get_research_paper_repository,get_total_docs

# Loading the configuration

def read_robots_txt(folder):
    """Read and parse the robots.txt file."""
    robots_path = os.path.join(folder, 'robots.txt')
    allowed_files = []
    if os.path.exists(robots_path):
        with open(robots_path, 'r') as file:
            for line in file:
                if line.startswith('Allow:'):
                    allowed_files.append(line.split(':')[1].strip())
    return allowed_files

def crawl_folders():
    """Crawl folders, process allowed files, and build a positional index."""
    RESEARCH_PAPER_REPOSITORY = get_research_paper_repository()
    positional_index = {}
    total_docs = 0  # Initialize a counter for total documents
    for folder in os.listdir(RESEARCH_PAPER_REPOSITORY):
        folder_path = os.path.join(RESEARCH_PAPER_REPOSITORY, folder)
        if os.path.isdir(folder_path):
            print ("Accessing Folder \t: ",folder_path)
            allowed_files = read_robots_txt(folder_path)
            for file in allowed_files:
                file_path = os.path.join(folder_path, file)
                if os.path.exists(file_path) and file.endswith('.pdf'):
                    total_docs += 1  # Increment total_docs for each PDF found
                    text = extract_text_from_pdf(file_path)
                    tokens = preprocess_text(text)
                    for position, token in enumerate(tokens):
                        if token not in positional_index:
                            positional_index[token] = {}
                        if file not in positional_index[token]:
                            positional_index[token][file] = []
                        positional_index[token][file].append(position)
    return positional_index,total_docs

def save_index(index):
    """Save the index to a JSON file."""
    POSITIONAL_INDEX = get_positional_index()

    with open(POSITIONAL_INDEX, 'w') as file:
        json.dump(index, file, indent=4)
        print ("Index is saved...")

def load_index():
    """Load the index from a JSON file."""
    POSITIONAL_INDEX = get_positional_index()
    with open(POSITIONAL_INDEX, 'r') as file:
        return json.load(file)
    
def save_total_docs(index):
    """Save the total number of docs to a JSON file."""
    TOTAL_DOCS = get_total_docs()

    with open(TOTAL_DOCS, 'w') as file:
        json.dump(index, file, indent=4)
        print ("Total number of docs is saved...")

def load_total_docs():
    """Load the total number of docs from a JSON file."""
    TOTAL_DOCS = get_total_docs()
    with open(TOTAL_DOCS, 'r') as file:
        return json.load(file)
    
def main():
    
    # Crawl folders and build positional index
    positional_index,total_docs = crawl_folders()
    # Save the positional index
    save_index(positional_index)
    # Save the total docs
    save_total_docs(total_docs)

if __name__ == "__main__":
    main()
    
