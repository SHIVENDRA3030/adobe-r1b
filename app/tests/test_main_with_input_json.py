import os
import json
import sys

def load_json_file(file_path):
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def load_persona(persona_file):
    """Load persona and job from JSON file."""
    try:
        data = load_json_file(persona_file)
        if not data:
            return '', '', []
        
        # Extract persona and job from the new format
        persona = data.get('persona', {}).get('role', '')
        job = data.get('job_to_be_done', {}).get('task', '')
        
        # Extract document list if available
        documents_list = data.get('documents', [])
        
        return persona, job, documents_list
    except Exception as e:
        print(f"Error loading persona file: {e}")
        return '', '', []

def main():
    # Get directory paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, 'input')
    output_dir = os.path.join(base_dir, 'output')
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Look for JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.json')]
    
    if json_files:
        # Use the first JSON file found
        input_json = os.path.join(input_dir, json_files[0])
        print(f"Found JSON file in input directory: {input_json}")
        persona_file = input_json
    else:
        # Fall back to persona.json in the app directory
        persona_file = os.path.join(app_dir, 'persona.json')
        print(f"No JSON files found in input directory, using: {persona_file}")
    
    # Load persona, job, and document list
    persona, job, documents_list = load_persona(persona_file)
    if not persona or not job:
        print("Persona or job not specified in the JSON file")
        return
    
    print(f"\nLoaded from: {persona_file}")
    print(f"Persona: {persona}")
    print(f"Job: {job}")
    print(f"Number of documents: {len(documents_list)}")
    
    # Check if we have documents in the input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    print(f"\nPDF files found in input directory: {len(pdf_files)}")
    
    if not pdf_files:
        print("No PDF files found in input directory.")
        if documents_list:
            print("\nDocuments specified in the JSON file:")
            for doc in documents_list:
                print(f"  - {doc.get('filename', '')}")
    else:
        print("PDF files:")
        for pdf in pdf_files:
            print(f"  - {pdf}")

if __name__ == "__main__":
    main()