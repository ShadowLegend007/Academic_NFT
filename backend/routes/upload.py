from fastapi import UploadFile, HTTPException, Depends
import os
import PyPDF2
import docx
from typing import Dict, Any
from utils.firebase_auth import require_student_role

def handle_upload(file: UploadFile, file_id: str) -> Dict[str, Any]:
    """
    Handle file upload and save to disk
    """
    # Validate file extension
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Check file extension
    ext = filename.split('.')[-1].lower()
    if ext not in ['pdf', 'docx', 'txt']:
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file format. Please upload PDF, DOCX, or TXT files."
        )
    
    # Create file path
    file_path = f"uploads/{file_id}_{filename}"
    
    return {
        "id": file_id,
        "filename": filename,
        "path": file_path,
        "extension": ext
    }

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from uploaded file based on file extension
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    # Get file extension
    ext = file_path.split('.')[-1].lower()
    
    # Extract text based on file type
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext == 'txt':
        return extract_text_from_txt(file_path)
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format: {ext}"
        )

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error extracting text from PDF: {str(e)}"
        )

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error extracting text from DOCX: {str(e)}"
        )

def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from TXT file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error reading TXT file: {str(e)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading TXT file: {str(e)}"
        )