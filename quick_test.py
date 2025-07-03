#!/usr/bin/env python3
"""
Quick Test Script - Verify AI Health Assist PDF Setup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking Dependencies...")
    
    # Check Python packages
    required_packages = [
        'pdfplumber', 'pytesseract', 'PyPDF2', 'pdf2image', 
        'google.generativeai', 'dotenv', 'reportlab'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split('.')[0])
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_packages.append(package)
    
    # Check system dependencies
    system_deps = [
        ('tesseract', 'tesseract --version'),
        ('poppler', 'pdftoppm -h')
    ]
    
    for name, cmd in system_deps:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name} - MISSING")
        except FileNotFoundError:
            print(f"  ❌ {name} - MISSING")
    
    return len(missing_packages) == 0

def check_file_structure():
    """Check if project structure is correct"""
    print("\n📁 Checking File Structure...")
    
    required_dirs = [
        'Medical Reports',
        'Utils',
        'results',
    ]
    
    required_files = [
        'main.py',
        'requirements.txt',
        'Utils/Agents.py',
        'Utils/PDFProcessor.py',
        'Utils/__init__.py'
    ]
    
    all_good = True
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ - MISSING")
            all_good = False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            all_good = False
    
    return all_good

def create_test_pdf():
    """Create a simple test PDF"""
    print("\n📄 Creating Test PDF...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Ensure test directory exists
        test_dir = Path("Medical Reports")
        test_dir.mkdir(exist_ok=True)
        
        pdf_path = test_dir / "test_medical_report.pdf"
        
        # Create simple PDF
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        width, height = letter
        
        # Add content
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "TEST MEDICAL REPORT")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, "Patient: Test Patient")
        c.drawString(50, height - 120, "Age: 35")
        c.drawString(50, height - 140, "Chief Complaint: Chest pain and shortness of breath")
        c.drawString(50, height - 180, "Symptoms:")
        c.drawString(70, height - 200, "- Chest pain (sharp, sudden onset)")
        c.drawString(70, height - 220, "- Shortness of breath")
        c.drawString(70, height - 240, "- Palpitations")
        c.drawString(70, height - 260, "- Dizziness")
        
        c.save()
        print(f"  ✅ Test PDF created: {pdf_path}")
        return str(pdf_path)
        
    except Exception as e:
        print(f"  ❌ Failed to create test PDF: {e}")
        return None

def test_pdf_extraction(pdf_path):
    """Test PDF text extraction"""
    print(f"\n🔍 Testing PDF Extraction...")
    
    try:
        sys.path.append('.')
        from Utils.PDFProcessor import PDFProcessor
        
        processor = PDFProcessor(pdf_path)
        result = processor.process_pdf()
        
        if result['success']:
            print(f"  ✅ PDF extraction successful")
            print(f"  📄 Method: {result['method_used']}")
            print(f"  📝 Text length: {len(result['text'])} chars")
            
            # Show first 100 characters
            sample = result['text'][:100].replace('\n', ' ')
            print(f"  📋 Sample: {sample}...")
            return True
        else:
            print(f"  ❌ PDF extraction failed")
            return False
            
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Extraction error: {e}")
        return False

def test_api_key():
    """Test if API key is configured"""
    print(f"\n🔑 Checking API Configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv('apikey.env')
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and len(api_key) > 10:
            print(f"  ✅ API key configured")
            return True
        else:
            print(f"  ❌ API key not found or invalid")
            print(f"  💡 Create apikey.env with: GOOGLE_API_KEY=your_key_here")
            return False
            
    except Exception as e:
        print(f"  ❌ API key check failed: {e}")
        return False

def main():
    print("🧪 AI Health Assist - Quick Setup Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("API Key", test_api_key),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    # Additional PDF tests if basic tests pass
    if passed == total:
        print("\n🎯 Basic tests passed! Running PDF tests...")
        
        pdf_path = create_test_pdf()
        if pdf_path and test_pdf_extraction(pdf_path):
            passed += 1
            total += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 SUCCESS! Your system is ready to use.")
        print("\n🚀 Next steps:")
        print("  1. Run: python main.py --file 'Medical Reports/test_medical_report.pdf'")
        print("  2. Check results/ folder for output")
        print("  3. Try with your own PDF files")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Install system deps: sudo apt install tesseract-ocr poppler-utils")
        print("  - Create missing files from the tutorial guide")
        print("  - Set up API key in apikey.env")

if __name__ == "__main__":
    main()