import os
import json
import sys
from datetime import datetime

def load_json_file(file_path):
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error loading JSON file {file_path}: {e}\n")
        return None

def create_test_output():
    """Create a test output file in the expected format"""
    # Get directory paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'output')
    
    # Ensure output directory exists and is writable
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Test write permissions
        test_file = os.path.join(output_dir, '.test')
        with open(test_file, 'w') as f:
            f.write('')
        os.remove(test_file)
    except Exception as e:
        sys.stderr.write(f"Error accessing output directory: {e}\n")
        return None
    
    # Create a test result structure
    result = {
        "metadata": {
            "input_documents": [
                "Learn Acrobat - Create and Convert_1.pdf",
                "Learn Acrobat - Create and Convert_2.pdf",
                "Learn Acrobat - Edit_1.pdf",
                "Learn Acrobat - Edit_2.pdf",
                "Learn Acrobat - Export_1.pdf"
            ],
            "persona": "HR professional",
            "job_to_be_done": "Create and manage fillable forms for onboarding and compliance.",
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": "Learn Acrobat - Fill and Sign.pdf",
                "section_title": "Change flat forms to fillable (Acrobat Pro)",
                "importance_rank": 1,
                "page_number": 12
            },
            {
                "document": "Learn Acrobat - Create and Convert_1.pdf",
                "section_title": "Create multiple PDFs from multiple files",
                "importance_rank": 2,
                "page_number": 12
            }
        ],
        "subsection_analysis": [
            {
                "document": "Learn Acrobat - Fill and Sign.pdf",
                "refined_text": "To create an interactive form, use the Prepare Forms tool. See Create a form from an existing document.",
                "page_number": 12
            },
            {
                "document": "Learn Acrobat - Fill and Sign.pdf",
                "refined_text": "To enable the Fill & Sign tools, from the hamburger menu (File menu in macOS) choose Save As Other > Acrobat Reader Extended PDF > Enable More Tools (includes Form Fill-in & Save).",
                "page_number": 12
            }
        ]
    }
    
    # Add challenge info
    result['metadata']['challenge_info'] = {
        "challenge_id": "round_1b_003",
        "test_case_name": "create_manageable_forms",
        "description": "Creating manageable forms"
    }
    
    # Create descriptive filename
    timestamp = result['metadata']['processing_timestamp'].replace(':', '-').replace('.', '-')
    challenge_id = result['metadata']['challenge_info'].get('challenge_id', 'unknown')
    persona_role = result['metadata']['persona'].lower().replace(' ', '_')
    output_file = os.path.join(output_dir, f"{challenge_id}_{persona_role}_test_output_{timestamp}.json")
    
    # Save the test output
    try:
        with open(output_file, 'w') as f:
            json.dump(result, f)
        # Verify the file was written correctly
        with open(output_file, 'r') as f:
            json.load(f)
        return output_file
    except Exception as e:
        sys.stderr.write(f"Error with test output file: {e}\n")
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass
        return None

def compare_with_expected(test_output_file):
    """Compare the test output with the expected format"""
    test_data = load_json_file(test_output_file)
    if not test_data:
        return False
    
    # Define all required fields
    structure = {
        'metadata': ['input_documents', 'persona', 'job_to_be_done', 'processing_timestamp'],
        'extracted_sections': ['document', 'section_title', 'importance_rank', 'page_number'],
        'subsection_analysis': ['document', 'refined_text', 'page_number']
    }
    
    # Check main structure
    if not all(field in test_data for field in structure):
        return False
        
    # Check metadata fields
    if not all(field in test_data['metadata'] for field in structure['metadata']):
        return False
    
    # Check sections structure
    if test_data['extracted_sections'] and not all(field in test_data['extracted_sections'][0] for field in structure['extracted_sections']):
        return False
    
    # Check subsections structure
    if test_data['subsection_analysis'] and not all(field in test_data['subsection_analysis'][0] for field in structure['subsection_analysis']):
        return False
    
    return True

def main():
    test_output_file = create_test_output()
    if not test_output_file or not compare_with_expected(test_output_file):
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()