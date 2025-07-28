import os
import json

def load_json_file(file_path):
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def test_load_input_json():
    # Get paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, 'input')
    input_json = os.path.join(input_dir, '1.json')
    
    # Load the input JSON file
    data = load_json_file(input_json)
    if not data:
        print(f"Failed to load input JSON file: {input_json}")
        return
    
    # Extract persona, job, and document list
    persona = data.get('persona', {}).get('role', '')
    job = data.get('job_to_be_done', {}).get('task', '')
    documents_list = data.get('documents', [])
    
    # Print the results
    print(f"Successfully loaded input JSON file: {input_json}")
    print(f"Persona: {persona}")
    print(f"Job: {job}")
    print(f"Number of documents: {len(documents_list)}")
    
    # Check if any PDF files exist in the input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    print(f"\nPDF files found in input directory: {len(pdf_files)}")
    if pdf_files:
        print("PDF files:")
        for pdf in pdf_files:
            print(f"  - {pdf}")
    else:
        print("No PDF files found in input directory.")
        print("\nDocuments specified in input JSON:")
        for doc in documents_list:
            print(f"  - {doc.get('filename', '')}")

if __name__ == "__main__":
    test_load_input_json()