import os
import json
import sys
import time
from datetime import datetime

def print_welcome():
    """Display a friendly welcome message"""
    print("\n🚀 Quick PDF Assistant at your service!")
    print("I'll help you get a quick overview of your documents.")
    print("Let's get started...\n")

def print_progress(message, delay=0.3):
    """Print a progress message with a small delay for better UX"""
    print(message)
    time.sleep(delay)

def load_json_file(file_path):
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Couldn't read the file {file_path}: {e}")
        return None

def load_persona(persona_file):
    """Load persona and job from JSON file."""
    try:
        data = load_json_file(persona_file)
        if not data:
            return '', '', [], {}
        
        persona_data = data.get('persona', {})
        persona = persona_data.get('role', '') if isinstance(persona_data, dict) else persona_data
        
        job_data = data.get('job_to_be_done', {})
        job = job_data.get('task', '') if isinstance(job_data, dict) else job_data
        
        documents_list = data.get('documents', [])
        
        return persona, job, documents_list, data
    except Exception as e:
        print(f"😕 Oops! Had trouble with the persona file: {e}")
        return '', '', [], {}

def save_output(result, output_dir):
    """Save analysis result to JSON file."""
    timestamp = result['metadata']['processing_timestamp'].replace(':', '-').replace('.', '-')
    
    challenge_id = "unknown"
    if 'challenge_info' in result['metadata']:
        challenge_id = result['metadata']['challenge_info'].get('challenge_id', 'unknown')
    
    persona = result['metadata']['persona']
    persona_role = persona.lower().replace(' ', '_')
    
    output_file = os.path.join(output_dir, f"{challenge_id}_{persona_role}_analysis_{timestamp}.json")
    
    try:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n✨ Perfect! I've saved your results to: {output_file}")
    except Exception as e:
        print(f"\n❌ Oh no! Couldn't save the output: {e}")

def main():
    print_welcome()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, 'input')
    output_dir = os.path.join(base_dir, 'output')
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.exists(input_dir):
        print(f"❌ Can't find the input directory at: {input_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    json_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.json')]
    
    if json_files:
        input_json = os.path.join(input_dir, json_files[0])
        print_progress(f"📄 Found your settings in: {json_files[0]}")
        persona_file = input_json
    else:
        persona_file = os.path.join(app_dir, 'persona.json')
        print_progress("📄 Using default settings from persona.json")
    
    persona, job, documents_list, persona_data = load_persona(persona_file)
    if not persona or not job:
        print("❌ I need both a persona and job description to help you effectively.")
        return
    
    print(f"\n👤 Working as: {persona}")
    print(f"🎯 Task: {job}")
    print(f"📚 Expected documents: {len(documents_list)}\n")
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    print_progress(f"🔍 Found {len(pdf_files)} PDF files in your input folder")
    
    if not pdf_files:
        print("❌ No PDF files found in the input directory.")
        if documents_list:
            print("\n📋 Here's what I'm looking for:")
            for doc in documents_list:
                print(f"   • {doc.get('filename', '')}")
        return
    
    print_progress("🎨 Creating a quick overview of your documents...")
    
    result = {
        "metadata": {
            "input_documents": [f for f in pdf_files],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    if 'challenge_info' in persona_data:
        result['metadata']['challenge_info'] = persona_data['challenge_info']
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print_progress(f"📄 Processing document {i}/{len(pdf_files)}: {pdf_file}", 0.2)
        
        section = {
            "document": pdf_file,
            "section_title": "Sample Section",
            "importance_rank": i,
            "page_number": 1
        }
        result["extracted_sections"].append(section)
        
        subsection = {
            "document": pdf_file,
            "refined_text": f"This is a placeholder for text extracted from {pdf_file}",
            "page_number": 1
        }
        result["subsection_analysis"].append(subsection)
    
    save_output(result, output_dir)
    print("\n🌟 All done! I've prepared a quick overview of your documents.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Okay, stopping here! See you next time!")
    except Exception as e:
        print(f"\n❌ Oops! Something unexpected happened: {e}")