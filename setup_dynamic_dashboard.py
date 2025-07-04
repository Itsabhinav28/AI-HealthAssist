#!/usr/bin/env python3
"""
Setup script for Dynamic AI Health Assist Dashboard
This ensures your web interface connects to real AI agents
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create required directories"""
    directories = [
        'templates',
        'uploads', 
        'static/css',
        'static/js',
        'results'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_files():
    """Check if required files exist"""
    required_files = [
        'app.py',
        'Utils/Agents.py',
        'Utils/PDFProcessor.py',
        'apikey.env'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    return missing_files

def check_api_key():
    """Check if API key is configured"""
    try:
        with open('apikey.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY=' in content and len(content.strip()) > 20:
                print("✅ API key appears to be configured")
                return True
            else:
                print("❌ API key not properly configured in apikey.env")
                return False
    except FileNotFoundError:
        print("❌ apikey.env file not found")
        return False

def backup_old_template():
    """Backup any existing template"""
    old_template = 'templates/dashboard.html'
    if os.path.exists(old_template):
        backup_name = 'templates/dashboard_backup.html'
        shutil.copy2(old_template, backup_name)
        print(f"✅ Backed up existing template to: {backup_name}")

def create_dynamic_template():
    """Create the dynamic template file"""
    template_content = '''<!-- This file should be replaced with the dynamic dashboard template -->
<!-- Save the "Dynamic Dashboard" artifact content as templates/dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>AI Health Assist - Setup Required</title>
</head>
<body>
    <h1>⚠️ Setup Required</h1>
    <p>Please save the Dynamic Dashboard template as templates/dashboard.html</p>
    <p>The template should connect to Flask backend for real AI analysis.</p>
</body>
</html>'''
    
    template_path = 'templates/dashboard.html'
    if not os.path.exists(template_path):
        with open(template_path, 'w') as f:
            f.write(template_content)
        print(f"⚠️ Created placeholder template: {template_path}")
        print("   You need to replace this with the actual dynamic template!")
    else:
        print(f"✅ Template exists: {template_path}")

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask',
        'google.generativeai', 
        'pdfplumber',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('.', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    return missing_packages

def main():
    print("🚀 Setting up Dynamic AI Health Assist Dashboard")
    print("=" * 60)
    
    # Create directories
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Check files
    print("\n📋 Checking required files...")
    missing_files = check_files()
    
    # Check dependencies
    print("\n📦 Checking Python dependencies...")
    missing_packages = check_dependencies()
    
    # Check API key
    print("\n🔑 Checking API configuration...")
    api_configured = check_api_key()
    
    # Handle template
    print("\n🌐 Setting up web template...")
    backup_old_template()
    create_dynamic_template()
    
    # Summary
    print("\n📊 SETUP SUMMARY")
    print("=" * 30)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required files found")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install " + " ".join(missing_packages))
    else:
        print("✅ All required packages installed")
    
    if not api_configured:
        print("❌ API key not configured")
        print("   Add your Google API key to apikey.env:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
    else:
        print("✅ API key configured")
    
    # Final instructions
    print("\n🎯 NEXT STEPS:")
    print("1. Replace templates/dashboard.html with the Dynamic Dashboard template")
    print("2. Ensure your apikey.env has a valid Google API key")
    print("3. Run: python app.py")
    print("4. Open: http://localhost:5000")
    print("5. Upload a medical report and see REAL AI analysis!")
    
    print("\n⚠️ IMPORTANT:")
    print("The dashboard will only show results from actual AI analysis.")
    print("No mock/demo data will be displayed.")
    print("Each uploaded file will generate unique results.")

if __name__ == "__main__":
    main()