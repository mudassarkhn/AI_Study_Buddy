from State.AI_Study_buddy_state import StudyBuddyState
import PyPDF2 
import docx
import json
import re
# ============ NODE 1: FILE PROCESSING ============
def file_processing(state: StudyBuddyState) -> StudyBuddyState:
    """Step 2: Extract text from uploaded file or pasted text"""
    print("📄 Processing file...")
    
    extracted_text = ""
    
    # If user pasted text directlys
    if state['file_type'] == 'text':
        extracted_text = state['raw_text']
    
    # If user uploaded PDF file
    elif state['file_type'] == 'pdf':
        with open(state['file_path'], 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()
    
    # If user uploaded Word document
    elif state['file_type'] == 'docx':
        doc = docx.Document(state['file_path'])
        for para in doc.paragraphs:
            extracted_text += para.text + "\n"
    
    # If user uploaded text file
    elif state['file_type'] == 'txt':
        with open(state['file_path'], 'r', encoding='utf-8') as file:
            extracted_text = file.read()
    
    # Clean up extra spaces
    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
    
    # Save to state
    state['extracted_text'] = extracted_text
    state['messages'] = [f"✅ Extracted {len(extracted_text)} characters from file"]
    state['print'] = f"Extracted text: {extracted_text}"
    
    return state