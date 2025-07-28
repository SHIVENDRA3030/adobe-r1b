import os
import json
import sys
import time
from utils import extract_all_pdfs
from processor import process_documents

def print_welcome():
    """Display a friendly welcome message"""
    print("\n✨ Welcome to your PDF Assistant! ✨")
    print("I'm here to help you find exactly what you need in your documents.")
    print("Let me get everything ready for you...\n")

def print_progress(message, delay=0.5):
    """Print a progress message with a small delay for better UX"""
    print(message)
    time.sleep(delay)

def load_persona(persona_file):
    """Load persona and job from JSON file."""
    try:
        with open(persona_file, 'r') as f:
            data = json.load(f)
        
        persona_data = data.get('persona', {})
        persona = persona_data.get('role', '') if isinstance(persona_data, dict) else persona_data
        
        job_data = data.get('job_to_be_done', {})
        job = job_data.get('task', '') if isinstance(job_data, dict) else job_data
        
        documents_list = data.get('documents', [])
        
        return persona, job, documents_list
    except Exception as e:
        print(f"😕 Oops! Couldn't read the persona file: {e}")
        return '', '', []

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
        print(f"\n✅ Great! I've saved your analysis to: {output_file}")
    except Exception as e:
        print(f"\n❌ Oh no! I couldn't save the output: {e}")

def main():
    print_welcome()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, 'input')
    output_dir = os.path.join(base_dir, 'output')
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.exists(input_dir):
        print(f"❌ I couldn't find the input directory at: {input_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    json_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.json')]
    
    if json_files:
        input_json = os.path.join(input_dir, json_files[0])
        print_progress(f"📄 I found your settings in: {json_files[0]}")
        persona_file = input_json
    else:
        persona_file = os.path.join(app_dir, 'persona.json')
        print_progress("📄 Using default settings from persona.json")
    
    persona, job, documents_list = load_persona(persona_file)
    if not persona or not job:
        print("❌ I need both a persona and job description to help you effectively.")
        return
    
    print(f"\n👤 I'll be your assistant for: {persona}")
    print(f"🎯 Focus area: {job}\n")
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"❌ I couldn't find any PDF files in {input_dir}")
        
        if documents_list:
            print("\n📋 I'm looking for these documents:")
            for doc in documents_list:
                print(f"   • {doc.get('filename', '')}")
        return
    
    print_progress(f"📚 Found {len(pdf_files)} PDF files to analyze...")
    docs_text = extract_all_pdfs(input_dir)
    
    print_progress("🔍 Analyzing your documents...")
    result = process_documents(persona, job, docs_text)
    
    with open(persona_file, 'r') as f:
        persona_data = json.load(f)
        if 'challenge_info' in persona_data:
            result['metadata']['challenge_info'] = persona_data['challenge_info']
    
    save_output(result, output_dir)
    print("\n🎉 All done! Your documents have been analyzed and the results are ready.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Okay, stopping here! See you next time!")
    except Exception as e:
        print(f"\n❌ Oops! Something unexpected happened: {e}")