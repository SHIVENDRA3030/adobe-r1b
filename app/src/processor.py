import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

def identify_sections(text):
    """
    Identify section titles in the text using regex patterns.
    
    Args:
        text (str): Text content to analyze
        
    Returns:
        list: List of identified section titles
    """
    # Pattern to match section titles (uppercase words, numbered sections, etc.)
    patterns = [
        r'^\s*([A-Z][A-Z\s]+)\s*$',  # ALL CAPS
        r'^\s*(\d+\.\s+[A-Za-z\s]+)\s*$',  # Numbered sections
        r'^\s*([A-Z][a-z]+\s+[A-Za-z\s]+:)\s*$',  # Title case with colon
        r'^\s*(Form[s]?\s+[A-Za-z\s]+)\s*$',  # Form-related titles
        r'^\s*(Fillable\s+[A-Za-z\s]+)\s*$',  # Fillable form-related titles
        r'^\s*(Creating\s+[A-Za-z\s]+\s+Form[s]?)\s*$',  # Creating forms
        r'^\s*(Managing\s+[A-Za-z\s]+\s+Form[s]?)\s*$',  # Managing forms
        r'^\s*(How\s+to\s+[A-Za-z\s]+\s+Form[s]?)\s*$'  # How-to guides for forms
    ]
    
    section_titles = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        for pattern in patterns:
            matches = re.findall(pattern, line)
            if matches:
                section_titles.extend(matches)
                break
    
    return section_titles

def rank_sections(persona, job, docs_text):
    """
    Rank sections based on relevance to persona and job.
    
    Args:
        persona (str): User persona
        job (str): Job to be done
        docs_text (dict): Dictionary with filename as key and list of (page_num, text) as value
        
    Returns:
        list: List of dictionaries containing ranked sections
    """
    # For HR professionals looking for form creation, add some relevant keywords
    if "HR" in persona and "form" in job.lower():
        query = f"{persona} {job} fillable forms PDF forms create edit manage onboarding compliance"
    else:
        query = f"{persona} {job}"
        
    text_corpus = [query]
    metadata = []
    
    # Process each document and page
    for filename, content in docs_text.items():
        for page_num, text in content:
            # Identify sections in the text
            sections = identify_sections(text)
            
            # If no sections found, use the first line as a placeholder
            if not sections and text.strip():
                first_line = text.strip().split('\n')[0]
                if len(first_line) > 10:  # Ensure it's not too short
                    sections = [first_line[:50] + '...']
            
            # Add each section to the corpus
            for section in sections:
                text_corpus.append(text)
                metadata.append({
                    'document': filename,
                    'page': page_num,
                    'section_title': section
                })
    
    # If no sections were found, return empty list
    if len(text_corpus) <= 1:
        return []
    
    # Calculate TF-IDF and cosine similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(text_corpus)
        scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except Exception as e:
        print(f"Error in TF-IDF calculation: {e}")
        return []
    
    # Combine scores with metadata
    ranked_sections = []
    for i, score in enumerate(scores):
        section_data = metadata[i].copy()
        section_data['importance_rank'] = i + 1
        section_data['relevance_score'] = float(score)
        ranked_sections.append(section_data)
    
    # Sort by relevance score (descending)
    ranked_sections = sorted(ranked_sections, key=lambda x: x['relevance_score'], reverse=True)
    
    # Update importance rank after sorting
    for i, section in enumerate(ranked_sections):
        section['importance_rank'] = i + 1
    
    return ranked_sections[:5]  # Return top 5 sections

def extract_subsections(docs_text, ranked_sections):
    """
    Extract subsection text for the ranked sections.
    
    Args:
        docs_text (dict): Dictionary with filename as key and list of (page_num, text) as value
        ranked_sections (list): List of ranked sections
        
    Returns:
        list: List of dictionaries containing subsection analysis
    """
    subsections = []
    
    for section in ranked_sections:
        document = section['document']
        page = section['page']
        
        # Find the text for this page
        page_text = ""
        for p_num, text in docs_text[document]:
            if p_num == page:
                page_text = text
                break
        
        # Extract a portion of text around the section title
        section_title = section['section_title']
        try:
            start_idx = page_text.find(section_title)
            if start_idx != -1:
                # Extract text after the section title (up to 800 chars for form-related content)
                start_pos = start_idx + len(section_title)
                
                # For form-related content, extract more text
                if any(keyword in section_title.lower() for keyword in ['form', 'fill', 'sign', 'edit', 'creat']):
                    extract_length = 800
                else:
                    extract_length = 500
                    
                refined_text = page_text[start_pos:start_pos + extract_length].strip()
                
                # Add some context about the document
                doc_context = f"From '{document}' - {section_title}: "
                refined_text = doc_context + refined_text
                
                subsections.append({
                    'document': document,
                    'page': page,
                    'refined_text': refined_text
                })
        except Exception as e:
            print(f"Error extracting subsection: {e}")
    
    return subsections

def process_documents(persona, job, docs_text):
    """
    Process documents and generate analysis based on persona and job.
    
    Args:
        persona (str): User persona
        job (str): Job to be done
        docs_text (dict): Dictionary with filename as key and list of (page_num, text) as value
        
    Returns:
        dict: Analysis results
    """
    # Get document filenames
    documents = list(docs_text.keys())
    
    # Rank sections by relevance
    ranked_sections = rank_sections(persona, job, docs_text)
    
    # Extract subsections
    subsections = extract_subsections(docs_text, ranked_sections)
    
    # Create result dictionary
    result = {
        'metadata': {
            'input_documents': documents,
            'persona': persona,
            'job_to_be_done': job,
            'processing_timestamp': datetime.now().isoformat()
        },
        'extracted_sections': [
            {
                'document': section['document'],
                'section_title': section['section_title'],
                'importance_rank': section['importance_rank'],
                'page_number': section['page']
            } for section in ranked_sections
        ],
        'subsection_analysis': [
            {
                'document': subsection['document'],
                'refined_text': subsection['refined_text'],
                'page_number': subsection['page']
            } for subsection in subsections
        ]
    }
    
    return result