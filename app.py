#!/usr/bin/env python3
"""
Flask Server for AI Health Assist Dashboard
Integrates with existing Main.py analysis system for REAL AI analysis
Updated with improved history management
"""
import os
import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from dotenv import load_dotenv

# Import your existing modules
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from Utils.PDFProcessor import PDFProcessor

# Load environment variables
load_dotenv('apikey.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('results', exist_ok=True)
os.makedirs('templates', exist_ok=True)

class AnalysisManager:
    def __init__(self):
        self.current_analyses = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def start_analysis(self, file_path, analysis_id):
        """Start analysis in background thread"""
        logger.info(f"🚀 Starting analysis {analysis_id} for file: {file_path}")
        
        self.current_analyses[analysis_id] = {
            'status': 'starting',
            'progress': 0,
            'results': {},
            'start_time': datetime.now(),
            'file_path': file_path,
            'original_filename': os.path.basename(file_path),
            'agent_progress': {
                'cardiologist': {'status': 'waiting', 'progress': 0},
                'psychologist': {'status': 'waiting', 'progress': 0},
                'pulmonologist': {'status': 'waiting', 'progress': 0},
                'final': {'status': 'waiting', 'progress': 0}
            }
        }
        
        # Start analysis in background
        future = self.executor.submit(self._run_analysis, file_path, analysis_id)
        return analysis_id
    
    def _run_analysis(self, file_path, analysis_id):
        """Run the actual analysis (background thread)"""
        try:
            logger.info(f"🔍 Starting analysis for: {file_path}")
            
            # Update status
            self.current_analyses[analysis_id]['status'] = 'processing_file'
            self.current_analyses[analysis_id]['progress'] = 10
            
            # Process the file using your existing process_medical_report function
            medical_report = self._process_medical_report(file_path)
            if not medical_report:
                self.current_analyses[analysis_id]['status'] = 'error'
                self.current_analyses[analysis_id]['error'] = 'Failed to process file'
                logger.error(f"❌ Failed to process file: {file_path}")
                return
            
            logger.info(f"✅ Successfully processed file. Content length: {len(medical_report)}")
            self.current_analyses[analysis_id]['progress'] = 25
            
            # Initialize agents with the actual medical report content
            agents = {
                "Cardiologist": Cardiologist(medical_report),
                "Psychologist": Psychologist(medical_report),
                "Pulmonologist": Pulmonologist(medical_report)
            }
            
            logger.info("🤖 Running AI agents in parallel...")
            self.current_analyses[analysis_id]['status'] = 'running_agents'
            self.current_analyses[analysis_id]['progress'] = 30
            
            # Function to run individual agents (matches your main.py approach)
            def get_response(agent_name, agent):
                try:
                    logger.info(f"🔄 Starting {agent_name} analysis...")
                    
                    # Update agent status to processing
                    agent_key = agent_name.lower()
                    if agent_key in self.current_analyses[analysis_id]['agent_progress']:
                        self.current_analyses[analysis_id]['agent_progress'][agent_key]['status'] = 'processing'
                        self.current_analyses[analysis_id]['agent_progress'][agent_key]['progress'] = 25
                    
                    # Run the actual AI agent
                    result = agent.run()
                    
                    # Update progress
                    if agent_key in self.current_analyses[analysis_id]['agent_progress']:
                        self.current_analyses[analysis_id]['agent_progress'][agent_key]['progress'] = 75
                        time.sleep(0.5)  # Brief pause for UI update
                        self.current_analyses[analysis_id]['agent_progress'][agent_key]['progress'] = 100
                    
                    logger.info(f"✅ {agent_name} completed analysis")
                    return agent_name, result
                except Exception as e:
                    logger.error(f"⚠️ Error in {agent_name}: {e}")
                    return agent_name, f"Analysis error: {str(e)}"
            
            # Run agents concurrently (exactly like your main.py)
            responses = {}
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
                
                for future in as_completed(futures):
                    agent_name, response = future.result()
                    responses[agent_name] = response
                    
                    # Update agent status in real-time
                    agent_key = agent_name.lower()
                    if agent_key in self.current_analyses[analysis_id]['agent_progress']:
                        self.current_analyses[analysis_id]['agent_progress'][agent_key]['status'] = 'completed'
                        self.current_analyses[analysis_id]['agent_progress'][agent_key]['progress'] = 100
                        self.current_analyses[analysis_id]['results'][agent_name] = response
                    
                    logger.info(f"✅ {agent_name} analysis completed and stored")
            
            # Update progress after individual agents complete
            self.current_analyses[analysis_id]['progress'] = 80
            
            # Run multidisciplinary team analysis (exactly like your main.py)
            logger.info("🏥 Running multidisciplinary team analysis...")
            self.current_analyses[analysis_id]['agent_progress']['final']['status'] = 'processing'
            
            team_agent = MultidisciplinaryTeam(
                cardiologist_report=responses.get("Cardiologist", ""),
                psychologist_report=responses.get("Psychologist", ""),
                pulmonologist_report=responses.get("Pulmonologist", "")
            )
            
            final_diagnosis = team_agent.run()
            logger.info("✅ Final diagnosis completed")
            
            # Complete analysis
            self.current_analyses[analysis_id]['results']['FinalDiagnosis'] = final_diagnosis
            self.current_analyses[analysis_id]['agent_progress']['final']['status'] = 'completed'
            self.current_analyses[analysis_id]['agent_progress']['final']['progress'] = 100
            self.current_analyses[analysis_id]['status'] = 'completed'
            self.current_analyses[analysis_id]['progress'] = 100
            self.current_analyses[analysis_id]['end_time'] = datetime.now()
            
            # Save results to files (with timestamp to avoid conflicts)
            self._save_results(analysis_id, responses, final_diagnosis)
            
            logger.info(f"✅ Analysis {analysis_id} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Analysis error: {e}")
            self.current_analyses[analysis_id]['status'] = 'error'
            self.current_analyses[analysis_id]['error'] = str(e)
    
    def _process_medical_report(self, file_path):
        """Process medical report from file - exactly like your main.py"""
        if not os.path.exists(file_path):
            logger.error(f"❌ File not found: {file_path}")
            return None
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            logger.info("📄 Processing PDF file...")
            try:
                pdf_processor = PDFProcessor(file_path)
                extraction_result = pdf_processor.process_pdf()
                
                if extraction_result['success']:
                    medical_report = pdf_processor.format_for_agents(extraction_result)
                    logger.info("✅ PDF processed successfully")
                    
                    # Save extracted text for reference (like your main.py)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    extracted_text_path = os.path.join("results", f"{timestamp}_extracted_pdf_text.txt")
                    os.makedirs(os.path.dirname(extracted_text_path), exist_ok=True)
                    with open(extracted_text_path, "w", encoding="utf-8") as f:
                        f.write(medical_report)
                    logger.info(f"📝 Extracted text saved to: {extracted_text_path}")
                    
                    return medical_report
                else:
                    logger.error("❌ Failed to extract text from PDF")
                    return None
                    
            except Exception as e:
                logger.error(f"❌ Error processing PDF: {e}")
                return None
                
        elif file_extension == '.txt':
            logger.info("📝 Processing text file...")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    medical_report = file.read()
                logger.info("✅ Text file processed successfully")
                return medical_report
            except Exception as e:
                logger.error(f"❌ Error reading text file: {e}")
                return None
        else:
            logger.error(f"❌ Unsupported file format: {file_extension}")
            logger.error("Supported formats: .pdf, .txt")
            return None
    
    def _save_results(self, analysis_id, responses, final_diagnosis):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save individual reports (only for file system, not shown in UI history)
        for agent_name, response in responses.items():
            filename = f"results/{timestamp}_{agent_name.lower()}_report.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"### {agent_name} Report:\n\n{response}")
            logger.info(f"📁 Saved {agent_name} report: {filename}")
        
        # Save final diagnosis
        filename = f"results/{timestamp}_final_diagnosis.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"### Final Diagnosis:\n\n{final_diagnosis}")
        logger.info(f"📁 Saved final diagnosis: {filename}")
    
    def get_analysis_status(self, analysis_id):
        """Get current analysis status"""
        return self.current_analyses.get(analysis_id, {})

# Initialize analysis manager
analysis_manager = AnalysisManager()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and start analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Secure filename and save
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            saved_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(file_path)
            
            logger.info(f"📁 File saved to: {file_path}")
            logger.info(f"📊 File size: {os.path.getsize(file_path)} bytes")
            
            # Start analysis
            analysis_id = f"analysis_{timestamp}"
            analysis_manager.start_analysis(file_path, analysis_id)
            
            logger.info(f"🚀 Started analysis with ID: {analysis_id}")
            
            return jsonify({
                'success': True,
                'analysis_id': analysis_id,
                'filename': filename,  # Return original filename for UI
                'saved_as': saved_filename
            })
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status/<analysis_id>')
def get_status(analysis_id):
    """Get analysis status"""
    status = analysis_manager.get_analysis_status(analysis_id)
    if not status:
        return jsonify({'error': 'Analysis not found'}), 404
    
    # Convert datetime objects to strings for JSON serialization
    status_copy = status.copy()
    if 'start_time' in status_copy:
        status_copy['start_time'] = status_copy['start_time'].isoformat()
    if 'end_time' in status_copy:
        status_copy['end_time'] = status_copy['end_time'].isoformat()
    
    return jsonify(status_copy)

@app.route('/results')
def list_results():
    """List summary of analysis results (simplified for new UI)"""
    try:
        # For the new UI, we return a simplified list
        # The detailed results are managed client-side
        results = []
        results_dir = 'results'
        
        if os.path.exists(results_dir):
            files = [f for f in os.listdir(results_dir) if f.endswith('_final_diagnosis.txt')]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(results_dir, x)), reverse=True)
            
            for file in files[:10]:  # Last 10 analyses
                file_path = os.path.join(results_dir, file)
                stat = os.stat(file_path)
                
                # Extract timestamp from filename
                timestamp_str = file.split('_')[0] + '_' + file.split('_')[1]
                try:
                    analysis_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    formatted_date = analysis_date.strftime('%d/%m/%Y')
                except:
                    formatted_date = datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y')
                
                results.append({
                    'id': timestamp_str,
                    'filename': file.replace('_final_diagnosis.txt', '').replace(timestamp_str + '_', ''),
                    'date': formatted_date,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download result file"""
    return send_from_directory('results', filename)

@app.route('/debug')
def debug_info():
    """Debug endpoint to check system status"""
    debug_data = {
        'api_key_configured': bool(os.getenv('GOOGLE_API_KEY')),
        'uploads_directory': os.path.exists('uploads'),
        'results_directory': os.path.exists('results'),
        'templates_directory': os.path.exists('templates'),
        'current_analyses': len(analysis_manager.current_analyses),
        'server_time': datetime.now().isoformat()
    }
    return jsonify(debug_data)

if __name__ == '__main__':
    print("🚀 Starting AI Health Assist Dashboard...")
    print("📍 Dashboard will be available at: http://localhost:5000")
    print("📊 Upload medical reports and view real-time analysis results")
    print("🔍 Debug endpoint available at: http://localhost:5000/debug")
    
    # Check API key on startup
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️ WARNING: GOOGLE_API_KEY not found in apikey.env")
        print("   Make sure to add your API key before uploading files!")
    else:
        print(f"✅ API Key configured (length: {len(api_key)})")
    
    app.run(debug=True, host='0.0.0.0', port=5000)