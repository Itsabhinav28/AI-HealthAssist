# AI Health Assist - Modular Dashboard Setup Script (PowerShell)
# Creates complete modular file structure with one command

Write-Host "🚀 Setting up AI Health Assist Modular Dashboard..." -ForegroundColor Green

# Create directory structure
Write-Host "📁 Creating directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "templates\components" | Out-Null
New-Item -ItemType Directory -Force -Path "templates\includes" | Out-Null
New-Item -ItemType Directory -Force -Path "static\css" | Out-Null
New-Item -ItemType Directory -Force -Path "static\js" | Out-Null
New-Item -ItemType Directory -Force -Path "uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "results" | Out-Null

# Create base.html
Write-Host "📄 Creating templates\base.html..." -ForegroundColor Cyan
@"
<!DOCTYPE html>
<html lang="en">
<head>
    {% include 'includes/head.html' %}
    <title>{% block title %}AI Health Assist - Medical Dashboard{% endblock %}</title>
</head>
<body>
    <div class="container">
        {% include 'includes/header.html' %}
        
        <main>
            {% block content %}{% endblock %}
        </main>
    </div>

    {% include 'includes/floating_stats.html' %}
    
    <!-- JavaScript Files -->
    <script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
    <script src="{{ url_for('static', filename='js/analysis.js') }}"></script>
    <script src="{{ url_for('static', filename='js/history.js') }}"></script>
    <script src="{{ url_for('static', filename='js/modal.js') }}"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
"@ | Out-File -FilePath "templates\base.html" -Encoding UTF8

# Create dashboard.html
Write-Host "📄 Creating templates\dashboard.html..." -ForegroundColor Cyan
@"
{% extends "base.html" %}

{% block content %}
    <!-- Upload Section -->
    {% include 'components/upload_section.html' %}

    <!-- Patient Information -->
    <div class="patient-info hidden" id="patientInfo">
        <h3>👤 Analysis Information</h3>
        <div class="patient-details" id="patientDetails">
            <!-- Patient details will be populated dynamically -->
        </div>
    </div>

    <!-- Analysis Grid -->
    {% include 'components/analysis_grid.html' %}

    <!-- Final Diagnosis -->
    <div class="final-diagnosis hidden" id="finalDiagnosis">
        <h3>🏥 Final Multidisciplinary Diagnosis</h3>
        <div class="status-indicator">
            <div class="status-dot status-waiting" id="finalStatus"></div>
            <span id="finalStatusText">Waiting for team analysis...</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="finalProgress"></div>
        </div>
        <div class="final-diagnosis-content hidden" id="finalContent"></div>
    </div>

    <!-- History Section -->
    {% include 'components/history_section.html' %}

    <!-- Report Modal -->
    {% include 'components/report_modal.html' %}
{% endblock %}
"@ | Out-File -FilePath "templates\dashboard.html" -Encoding UTF8

# Create includes/head.html
Write-Host "📄 Creating templates\includes\head.html..." -ForegroundColor Cyan
@"
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="AI Health Assist - Advanced Medical Analysis Dashboard">
<meta name="keywords" content="AI, Medical Analysis, Healthcare, Dashboard">

<!-- CSS Files -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/modal.css') }}">

<!-- Favicon -->
<link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
"@ | Out-File -FilePath "templates\includes\head.html" -Encoding UTF8

# Create includes/header.html
Write-Host "📄 Creating templates\includes\header.html..." -ForegroundColor Cyan
@"
<div class="header">
    <h1>🧠 AI Health Assist</h1>
    <p>Advanced Multidisciplinary Medical Analysis Dashboard</p>
</div>
"@ | Out-File -FilePath "templates\includes\header.html" -Encoding UTF8

# Create includes/floating_stats.html
Write-Host "📄 Creating templates\includes\floating_stats.html..." -ForegroundColor Cyan
@"
<div class="floating-stats">
    <h4>📊 Analysis Stats</h4>
    <div class="stat-item">
        <div class="stat-icon cardiologist">❤️</div>
        <span>Cardiac Analysis</span>
    </div>
    <div class="stat-item">
        <div class="stat-icon psychologist">🧠</div>
        <span>Psychological Assessment</span>
    </div>
    <div class="stat-item">
        <div class="stat-icon pulmonologist">🫁</div>
        <span>Pulmonary Evaluation</span>
    </div>
    <div class="stat-item">
        <div class="stat-icon multidisciplinary">🏥</div>
        <span>Team Diagnosis</span>
    </div>
</div>
"@ | Out-File -FilePath "templates\includes\floating_stats.html" -Encoding UTF8

# Create components/upload_section.html
Write-Host "📄 Creating templates\components\upload_section.html..." -ForegroundColor Cyan
@"
<div class="upload-section">
    <h3>📋 Upload Medical Report</h3>
    <div class="upload-area" id="uploadArea">
        <div>
            <p>📄 Drag & Drop your medical report here</p>
            <p>or</p>
            <button class="btn" onclick="document.getElementById('fileInput').click()">
                Choose File
            </button>
            <input type="file" id="fileInput" accept=".pdf,.txt" style="display: none;">
        </div>
    </div>
    <div id="fileInfo" class="hidden"></div>
    <button class="btn" id="analyzeBtn" disabled>
        🔍 Start Analysis
    </button>
</div>
"@ | Out-File -FilePath "templates\components\upload_section.html" -Encoding UTF8

# Create components/analysis_grid.html
Write-Host "📄 Creating templates\components\analysis_grid.html..." -ForegroundColor Cyan
@"
<div class="analysis-grid">
    <!-- Cardiologist Card -->
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon cardiologist">❤️</div>
            <div class="agent-title">Cardiologist</div>
        </div>
        <div class="status-indicator">
            <div class="status-dot status-waiting" id="cardioStatus"></div>
            <span id="cardioStatusText">Waiting for analysis...</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="cardioProgress"></div>
        </div>
        <div class="analysis-content hidden" id="cardioContent"></div>
    </div>

    <!-- Psychologist Card -->
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon psychologist">🧠</div>
            <div class="agent-title">Psychologist</div>
        </div>
        <div class="status-indicator">
            <div class="status-dot status-waiting" id="psychoStatus"></div>
            <span id="psychoStatusText">Waiting for analysis...</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="psychoProgress"></div>
        </div>
        <div class="analysis-content hidden" id="psychoContent"></div>
    </div>

    <!-- Pulmonologist Card -->
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon pulmonologist">🫁</div>
            <div class="agent-title">Pulmonologist</div>
        </div>
        <div class="status-indicator">
            <div class="status-dot status-waiting" id="pulmoStatus"></div>
            <span id="pulmoStatusText">Waiting for analysis...</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="pulmoProgress"></div>
        </div>
        <div class="analysis-content hidden" id="pulmoContent"></div>
    </div>
</div>
"@ | Out-File -FilePath "templates\components\analysis_grid.html" -Encoding UTF8

# Create components/history_section.html
Write-Host "📄 Creating templates\components\history_section.html..." -ForegroundColor Cyan
@"
<div class="history-section">
    <h3>📊 Analysis History</h3>
    <div class="history-grid" id="historyGrid">
        <p>No previous analyses found. Upload a file to get started!</p>
    </div>
</div>
"@ | Out-File -FilePath "templates\components\history_section.html" -Encoding UTF8

# Create components/report_modal.html
Write-Host "📄 Creating templates\components\report_modal.html..." -ForegroundColor Cyan
@"
<div class="report-viewer" id="reportViewer">
    <div class="report-content">
        <div class="report-header">
            <h2 id="reportTitle">Medical Analysis Report</h2>
            <button class="close-btn" onclick="closeReportViewer()">×</button>
        </div>
        <div class="report-body" id="reportBody">
            <!-- Report content will be loaded here -->
        </div>
    </div>
</div>
"@ | Out-File -FilePath "templates\components\report_modal.html" -Encoding UTF8

# Create CSS files
Write-Host "🎨 Creating CSS files..." -ForegroundColor Magenta

# Create main.css
@"
/* Main Styles - Core Layout and Base Elements */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
    overflow-x: hidden;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    margin-bottom: 40px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.header h1 {
    color: white;
    font-size: 2.5em;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.header p {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.2em;
}

.btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    font-size: 1em;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 10px;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.progress-bar {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    width: 0%;
    transition: width 0.3s ease;
}

.status-indicator {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 10px;
    animation: pulse 2s infinite;
}

.status-waiting { background: #ffc107; }
.status-processing { background: #17a2b8; }
.status-completed { background: #28a745; }
.status-error { background: #dc3545; }

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.hidden {
    display: none;
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.error-message {
    background: #f8d7da;
    color: #721c24;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border: 1px solid #f5c6cb;
}

.success-message {
    background: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border: 1px solid #c3e6cb;
}

h3 {
    color: #667eea;
    font-size: 1.2em;
    margin: 15px 0 10px 0;
    border-bottom: 2px solid #667eea;
    padding-bottom: 5px;
}

h4 {
    color: #333;
    font-size: 1.1em;
    margin: 12px 0 8px 0;
    font-weight: 600;
}

strong {
    color: #333;
    font-weight: 600;
}

ul {
    margin: 10px 0;
    padding-left: 20px;
}

li {
    margin: 5px 0;
    line-height: 1.5;
}
"@ | Out-File -FilePath "static\css\main.css" -Encoding UTF8

# Create components.css
Write-Host "🎨 Creating static\css\components.css..." -ForegroundColor Magenta
@"
/* Component Styles - Specific UI Components */

.upload-section {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.upload-area {
    border: 3px dashed #667eea;
    border-radius: 10px;
    padding: 40px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.upload-area:hover {
    background: rgba(102, 126, 234, 0.05);
    border-color: #764ba2;
}

.upload-area.dragover {
    background: rgba(102, 126, 234, 0.1);
    border-color: #764ba2;
}

.analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.agent-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    min-height: 300px;
}

.agent-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.agent-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
}

.agent-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.agent-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    margin-right: 15px;
    color: white;
}

.cardiologist { background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
.psychologist { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
.pulmonologist { background: linear-gradient(135deg, #45b7d1, #96c93d); }
.multidisciplinary { background: linear-gradient(135deg, #f093fb, #f5576c); }

.agent-title {
    font-size: 1.4em;
    font-weight: 600;
    color: #333;
}

.analysis-content {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
    margin-top: 15px;
    max-height: 300px;
    overflow-y: auto;
    font-size: 0.9em;
    line-height: 1.6;
}

.patient-info {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.patient-info h3 {
    color: #333;
    margin-bottom: 15px;
    font-size: 1.3em;
}

.patient-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.patient-detail {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}

.patient-detail strong {
    color: #333;
    display: block;
    margin-bottom: 5px;
}

.final-diagnosis {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 15px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.final-diagnosis h3 {
    font-size: 1.8em;
    margin-bottom: 20px;
    text-align: center;
}

.final-diagnosis-content {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    line-height: 1.6;
}

.history-section {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin-top: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.history-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.history-card {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #dee2e6;
    transition: all 0.3s ease;
    cursor: pointer;
}

.history-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.history-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    border-bottom: 2px solid #667eea;
    padding-bottom: 10px;
}

.history-file-info {
    flex: 1;
}

.history-file-name {
    font-size: 1.1em;
    font-weight: 600;
    color: #333;
    margin-bottom: 5px;
}

.history-file-meta {
    font-size: 0.9em;
    color: #666;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.view-report-btn {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9em;
    cursor: pointer;
    transition: all 0.3s ease;
}

.view-report-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.floating-stats {
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    z-index: 1000;
    min-width: 200px;
}

.stat-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.stat-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    font-size: 0.8em;
    color: white;
}
"@ | Out-File -FilePath "static\css\components.css" -Encoding UTF8

# Create modal.css
Write-Host "🎨 Creating static\css\modal.css..." -ForegroundColor Magenta
@"
/* Modal Styles - Report Viewer */

.report-viewer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(5px);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.report-viewer.active {
    opacity: 1;
    visibility: visible;
}

.report-content {
    background: white;
    border-radius: 20px;
    width: 90%;
    max-width: 1200px;
    max-height: 85vh;
    overflow-y: auto;
    transform: scale(0.8);
    transition: all 0.3s ease;
}

.report-viewer.active .report-content {
    transform: scale(1);
}

.report-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 20px 30px;
    border-radius: 20px 20px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.2em;
    transition: all 0.3s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: rotate(90deg);
}

.report-body {
    padding: 30px;
}

.report-section {
    margin-bottom: 30px;
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid;
}

.cardiologist-section {
    background: rgba(255, 107, 107, 0.1);
    border-left-color: #ff6b6b;
}

.psychologist-section {
    background: rgba(78, 205, 196, 0.1);
    border-left-color: #4ecdc4;
}

.pulmonologist-section {
    background: rgba(69, 183, 209, 0.1);
    border-left-color: #45b7d1;
}

.final-section {
    background: rgba(240, 147, 251, 0.1);
    border-left-color: #f093fb;
}

.section-title {
    font-size: 1.4em;
    font-weight: 600;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
}

.section-icon {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    color: white;
    font-size: 1.2em;
}
"@ | Out-File -FilePath "static\css\modal.css" -Encoding UTF8

# Create JavaScript files
Write-Host "⚙️ Creating JavaScript files..." -ForegroundColor Blue

# Create dashboard.js with truncated content for brevity
@"
// Dashboard Main JavaScript - Core Functionality

let currentFile = null;
let analysisInProgress = false;
let currentAnalysisId = null;
let statusCheckInterval = null;
let analysisHistory = [];

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const analyzeBtn = document.getElementById('analyzeBtn');
const patientInfo = document.getElementById('patientInfo');
const patientDetails = document.getElementById('patientDetails');

const agents = {
    cardiologist: {
        status: document.getElementById('cardioStatus'),
        statusText: document.getElementById('cardioStatusText'),
        progress: document.getElementById('cardioProgress'),
        content: document.getElementById('cardioContent')
    },
    psychologist: {
        status: document.getElementById('psychoStatus'),
        statusText: document.getElementById('psychoStatusText'),
        progress: document.getElementById('psychoProgress'),
        content: document.getElementById('psychoContent')
    },
    pulmonologist: {
        status: document.getElementById('pulmoStatus'),
        statusText: document.getElementById('pulmoStatusText'),
        progress: document.getElementById('pulmoProgress'),
        content: document.getElementById('pulmoContent')
    }
};

const finalDiagnosis = {
    container: document.getElementById('finalDiagnosis'),
    status: document.getElementById('finalStatus'),
    statusText: document.getElementById('finalStatusText'),
    progress: document.getElementById('finalProgress'),
    content: document.getElementById('finalContent')
};

function formatMedicalText(text) {
    if (!text) return '';
    
    return text
        .replace(/### (.*?)(?:\n|$)/g, '<h3>$1</h3>')
        .replace(/## (.*?)(?:\n|$)/g, '<h4>$1</h4>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
        .replace(/^\s*[\*\-\•]\s+(.*?)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, function(match) {
            return '<ul>' + match + '</ul>';
        })
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.+)/, '<p>$1')
        .replace(/(.+)$/, '$1</p>')
        .replace(/<p><\/p>/g, '')
        .replace(/<p><br><\/p>/g, '');
}

function handleFile(file) {
    currentFile = file;