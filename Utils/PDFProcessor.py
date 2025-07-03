import os
import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import PyPDF2
import re
from typing import Dict, List, Optional

class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.extracted_text = ""
        self.structured_data = {}
        
    def extract_text_pdfplumber(self) -> str:
        """Extract text using pdfplumber (best for forms and structured PDFs)"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            print(f"❌ Error with pdfplumber: {e}")
            return ""
    
    def extract_text_pypdf2(self) -> str:
        """Fallback method using PyPDF2"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ Error with PyPDF2: {e}")
            return ""
    
    def extract_text_ocr(self) -> str:
        """Extract text using OCR for scanned PDFs"""
        try:
            # Convert PDF to images
            images = convert_from_path(self.pdf_path)
            text = ""
            
            for i, image in enumerate(images):
                # Use OCR to extract text from image
                page_text = pytesseract.image_to_string(image)
                text += f"--- Page {i+1} ---\n{page_text}\n"
            
            return text
        except Exception as e:
            print(f"❌ Error with OCR: {e}")
            return ""
    
    def extract_form_data(self) -> Dict:
        """Extract structured form data from medical incident reports"""
        form_data = {}
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    # Extract tables if any
                    tables = page.extract_tables()
                    if tables:
                        form_data['tables'] = tables
                    
                    # Extract text and look for form fields
                    text = page.extract_text()
                    if text:
                        # Parse common medical form fields
                        form_data.update(self.parse_medical_form_fields(text))
                        
        except Exception as e:
            print(f"❌ Error extracting form data: {e}")
            
        return form_data
    
    def parse_medical_form_fields(self, text: str) -> Dict:
        """Parse common medical form fields using regex patterns"""
        fields = {}
        
        # Common patterns for medical forms
        patterns = {
            'patient_name': r'(?:Name|Patient Name|PATIENT NAME)[\s:]*([A-Za-z\s]+)',
            'date_of_birth': r'(?:DOB|Date of Birth|Birth Date)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'incident_date': r'(?:Date|Incident Date|Date of Incident)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'age': r'(?:Age)[\s:]*(\d{1,3})',
            'gender': r'(?:Gender|Sex)[\s:]*([MF]|Male|Female)',
            'staff_id': r'(?:Staff ID|Staff No|Employee ID)[\s:]*(\d+)',
            'location': r'(?:Location|Where)[\s:]*([A-Za-z\s]+)',
            'symptoms': r'(?:Symptoms|Signs|Complaint)[\s:]*([A-Za-z\s,.-]+)',
            'injury_type': r'(?:Injury|Type of Injury)[\s:]*([A-Za-z\s,.-]+)',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields[field] = match.group(1).strip()
        
        return fields
    
    def process_pdf(self) -> Dict:
        """Main method to process PDF and extract all relevant information"""
        result = {
            'success': False,
            'text': '',
            'structured_data': {},
            'method_used': ''
        }
        
        print(f"🔍 Processing PDF: {self.pdf_path}")
        
        # Try different extraction methods
        methods = [
            ('pdfplumber', self.extract_text_pdfplumber),
            ('pypdf2', self.extract_text_pypdf2),
            ('ocr', self.extract_text_ocr)
        ]
        
        for method_name, method_func in methods:
            print(f"📄 Trying {method_name}...")
            text = method_func()
            
            if text and len(text.strip()) > 50:  # Ensure meaningful text
                result['text'] = text
                result['method_used'] = method_name
                result['success'] = True
                print(f"✅ Successfully extracted text using {method_name}")
                break
        
        # Extract structured form data
        if result['success']:
            result['structured_data'] = self.extract_form_data()
            
        return result
    
    def format_for_agents(self, extraction_result: Dict) -> str:
        """Format extracted data for medical agents"""
        if not extraction_result['success']:
            return "Error: Could not extract text from PDF"
        
        formatted_text = f"""
Medical Report Analysis
=======================
Extraction Method: {extraction_result['method_used']}

RAW TEXT CONTENT:
{extraction_result['text']}

STRUCTURED DATA EXTRACTED:
"""
        
        structured_data = extraction_result['structured_data']
        if structured_data:
            for key, value in structured_data.items():
                if key != 'tables':
                    formatted_text += f"{key.replace('_', ' ').title()}: {value}\n"
            
            # Add tables if present
            if 'tables' in structured_data:
                formatted_text += "\nTABULAR DATA:\n"
                for i, table in enumerate(structured_data['tables']):
                    formatted_text += f"Table {i+1}:\n{table}\n"
        
        return formatted_text