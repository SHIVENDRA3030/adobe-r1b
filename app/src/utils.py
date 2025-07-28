import fitz
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF (fitz).
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of tuples containing (page_number, page_text)
    """
    doc = fitz.open(pdf_path)
    all_text = []
    for i, page in enumerate(doc):
        all_text.append((i + 1, page.get_text()))
    return all_text

def get_pdf_files(directory):
    """
    Get all PDF files in a directory.
    
    Args:
        directory (str): Directory path
        
    Returns:
        list: List of PDF file paths
    """
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files

def extract_all_pdfs(input_dir):
    """
    Extract text from all PDFs in the input directory.
    
    Args:
        input_dir (str): Input directory path
        
    Returns:
        dict: Dictionary with filename as key and list of (page_num, text) as value
    """
    pdf_files = get_pdf_files(input_dir)
    docs_text = {}
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        docs_text[filename] = extract_text_from_pdf(pdf_file)
    
    return docs_text