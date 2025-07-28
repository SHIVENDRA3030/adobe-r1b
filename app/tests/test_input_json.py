import os
import json

def load_json_file(file_path):
    """Load and parse a JSON file with explicit encoding"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                data = json.load(f)
            print(f"Successfully loaded with latin-1 encoding: {file_path}")
            return data
        except Exception as e2:
            print(f"Also failed with latin-1 encoding: {e2}")
            return None

def compare_json_files():
    # Get paths to both JSON files
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_json = os.path.join(base_dir, 'input', '1.json')
    persona_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'persona.json')
    
    # Load both files
    input_data = load_json_file(input_json)
    persona_data = load_json_file(persona_json)
    
    if not input_data or not persona_data:
        return
    
    # Compare structure
    print("Comparing JSON files:")
    print(f"Input JSON: {input_json}")
    print(f"Persona JSON: {persona_json}")
    print()
    
    # Check if they have the same keys at the top level
    input_keys = set(input_data.keys())
    persona_keys = set(persona_data.keys())
    
    print(f"Input JSON keys: {input_keys}")
    print(f"Persona JSON keys: {persona_keys}")
    print(f"Same top-level keys: {input_keys == persona_keys}")
    print()
    
    # Check if they have the same number of documents
    input_docs = input_data.get('documents', [])
    persona_docs = persona_data.get('documents', [])
    
    print(f"Input JSON document count: {len(input_docs)}")
    print(f"Persona JSON document count: {len(persona_docs)}")
    print(f"Same document count: {len(input_docs) == len(persona_docs)}")
    print()
    
    # Check if persona and job are the same
    input_persona = input_data.get('persona', {}).get('role', '')
    persona_persona = persona_data.get('persona', {}).get('role', '')
    
    input_job = input_data.get('job_to_be_done', {}).get('task', '')
    persona_job = persona_data.get('job_to_be_done', {}).get('task', '')
    
    print(f"Input JSON persona: {input_persona}")
    print(f"Persona JSON persona: {persona_persona}")
    print(f"Same persona: {input_persona == persona_persona}")
    print()
    
    print(f"Input JSON job: {input_job}")
    print(f"Persona JSON job: {persona_job}")
    print(f"Same job: {input_job == persona_job}")

if __name__ == "__main__":
    compare_json_files()