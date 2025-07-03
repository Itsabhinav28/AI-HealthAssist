#!/usr/bin/env python3
"""
Setup script for AI Health Assist with PDF processing capabilities
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_system_dependencies():
    """Install system dependencies for PDF processing"""
    print("🔧 Installing system dependencies...")
    
    # Instructions for different operating systems
    print("""
    SYSTEM DEPENDENCIES REQUIRED:
    
    For Ubuntu/Debian:
    sudo apt-get update
    sudo apt-get install tesseract-ocr poppler-utils
    
    For macOS (with Homebrew):
    brew install tesseract poppler
    
    For Windows:
    1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
    2. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
    3. Add both to your PATH environment variable
    """)

def create_directories():
    """Create necessary directories"""
    directories = [
        "Medical Reports",
        "results",
        "Utils"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def main():
    print("🚀 Setting up AI Health Assist with PDF Processing...")
    
    create_directories()
    install_requirements()
    install_system_dependencies()
    
    print("""
    ✅ Setup complete!
    
    USAGE:
    # Analyze text file (existing functionality)
    python main.py --file "Medical Reports/report.txt"
    
    # Analyze PDF file (new functionality)
    python main.py --file "Medical Reports/incident_report.pdf"
    
    # Use default file
    python main.py
    """)

if __name__ == "__main__":
    main()