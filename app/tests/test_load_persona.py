import os
import json

def load_persona_test(persona_file):
    """Simple function to load persona.json without dependencies"""
    try:
        with open(persona_file, 'r') as f:
            data = json.load(f)
        
        # Extract persona and job from the new format
        persona = data.get('persona', {}).get('role', '')
        job = data.get('job_to_be_done', {}).get('task', '')
        
        # Extract document list if available
        documents_list = data.get('documents', [])
        
        return persona, job, documents_list
    except Exception as e:
        print(f"Error loading persona file: {e}")
        return '', '', []

def test_load_persona():
    # Get the path to persona.json
    persona_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'persona.json')
    
    # Load persona, job, and document list
    persona, job, documents_list = load_persona_test(persona_file)
    
    # Print the results
    print(f"Persona: {persona}")
    print(f"Job: {job}")
    print(f"Number of documents: {len(documents_list)}")
    print("\nDocument list:")
    for doc in documents_list:
        print(f"  - {doc.get('filename', '')}: {doc.get('title', '')}")

if __name__ == "__main__":
    test_load_persona()