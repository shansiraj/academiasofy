from collections import defaultdict
from src.modules.pre_processor import preprocess_text
import math
from src.modules.crawler import load_index,load_total_docs

def calculate_idf(positional_index, total_docs):
    """Calculate IDF for each term in the positional index."""
    idf = {}
    for token, docs in positional_index.items():
        df = len(docs)  # Number of documents containing the term
        idf[token] = math.log(total_docs / (df + 1))  # Adding 1 to avoid division by zero
    return idf

def search(query):
    """Search for a query in the positional index using TF-IDF ranking."""
    positional_index = load_index()
    total_docs = load_total_docs()
    query_tokens = preprocess_text(query)
    idf = calculate_idf(positional_index, total_docs)  # Calculate IDF for each term
    matching_docs = defaultdict(float)

    # Iterate through each query token
    for token in query_tokens:
        if token in positional_index:
            # Calculate TF for each document containing the token
            for doc, positions in positional_index[token].items():
                tf = len(positions)  # Term frequency in the document
                tf_idf = tf * idf[token]  # Compute TF-IDF score
                matching_docs[doc] += tf_idf  # Add to the document's score

    # Sort documents by their TF-IDF score in descending order
    sorted_results = sorted(matching_docs.items(), key=lambda x: x[1], reverse=True)
    return sorted_results