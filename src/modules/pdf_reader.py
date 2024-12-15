from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def extract_metadata(pdf_path):
    """Extract metadata like title and abstract from a PDF."""
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        first_page = reader.pages[0].extract_text() if reader.pages else ""
        
        name = metadata.get("/Title", "Unknown Title")
        abstract = first_page.split("Abstract:")[1].split("\n")[0] if "Abstract:" in first_page else ""
        return {"name": name, "abstract": abstract}
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {"name": "Unknown Title", "abstract": "Abstract not available."}
    
def extract_relevant_snippet(query, pdf_path):
    """Extract a relevant snippet from the PDF based on the query."""
    try:
        reader = PdfReader(pdf_path)
        query_tokens = query.lower().split()
        
        for page in reader.pages:
            text = page.extract_text().lower()
            if any(token in text for token in query_tokens):
                # Return a snippet with context around the query terms
                for token in query_tokens:
                    if token in text:
                        start = max(text.find(token) - 50, 0)
                        end = min(text.find(token) + 500, len(text))
                        snippet = text[start:end]
                        
                        # Bold the query token in the snippet
                        for token in query_tokens:
                            snippet = snippet.replace(token, f"<b style='color: blue;'>{token}</b>")
                        
                        # Return the snippet with bolded query terms
                        return snippet
        return "No relevant snippet found."
    except Exception as e:
        print(f"Error extracting snippet: {e}")
        return "Error extracting snippet."
    

    