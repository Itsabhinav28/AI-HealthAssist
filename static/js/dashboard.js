// Dashboard Main JavaScript - Core Functionality with Enhanced Text Formatting

// Global variables
let currentFile = null;
let analysisInProgress = false;
let currentAnalysisId = null;
let statusCheckInterval = null;
let analysisHistory = [];

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const analyzeBtn = document.getElementById('analyzeBtn');
const patientInfo = document.getElementById('patientInfo');
const patientDetails = document.getElementById('patientDetails');

// Agent elements
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

// Enhanced text formatting function to handle both formats consistently
function formatMedicalText(text) {
    if (!text) return '';
    
    return text
        // Handle triple dashes as section separators
        .replace(/---\s*\n/g, '')
        .replace(/---/g, '')
        
        // Convert "Section: Title" format to proper headings
        .replace(/Section:\s*([^\n]+)/g, '<h3>$1</h3>')
        
        // Convert markdown-style headers (both ** and ### formats)
        .replace(/\*\*([^*]+)\*\*/g, '<h3>$1</h3>')
        .replace(/### (.*?)(?:\n|$)/g, '<h3>$1</h3>')
        .replace(/## (.*?)(?:\n|$)/g, '<h4>$1</h4>')
        
        // Convert bold text (remaining ** that aren't headers)
        .replace(/\*([^*\n]+)\*/g, '<strong>$1</strong>')
        
        // Convert bullet points (handle multiple formats)
        .replace(/^\s*[\*\-\•]\s+\*\*([^*]+)\*\*\s*(.*)$/gm, '<li><strong>$1</strong> $2</li>')
        .replace(/^\s*[\*\-\•]\s+([^\n]+)$/gm, '<li>$1</li>')
        
        // Wrap consecutive list items in ul tags
        .replace(/(<li>.*?<\/li>)(\s*<li>.*?<\/li>)*/gs, function(match) {
            return '<ul>' + match + '</ul>';
        })
        
        // Convert line breaks and paragraphs
        .replace(/\n\n+/g, '</p><p>')
        .replace(/\n/g, '<br>')
        
        // Wrap content in paragraphs if not already wrapped
        .replace(/^(?!<[uh]|<p)(.+?)(?=<[uh]|<p|$)/gm, '<p>$1</p>')
        
        // Clean up empty paragraphs and fix formatting issues
        .replace(/<p><\/p>/g, '')
        .replace(/<p><br><\/p>/g, '')
        .replace(/<p>(<h[3-4]>)/g, '$1')
        .replace(/(<\/h[3-4]>)<\/p>/g, '$1')
        .replace(/<p>(<ul>)/g, '$1')
        .replace(/(<\/ul>)<\/p>/g, '$1')
        
        // Ensure proper spacing after headings
        .replace(/(<\/h[3-4]>)(<p>)/g, '$1<br>$2')
        .replace(/(<\/h[3-4]>)(<ul>)/g, '$1<br>$2');
}

// File handling functions
function handleFile(file) {
    currentFile = file;
    
    // Validate file type
    const allowedTypes = ['.pdf', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showError('Please select a PDF or TXT file.');
        return;
    }

    // Show file info
    fileInfo.innerHTML = `
        <div class="success-message">
            <strong>File Selected:</strong> ${file.name}<br>
            <strong>Size:</strong> ${(file.size / 1024 / 1024).toFixed(2)} MB<br>
            <strong>Type:</strong> ${file.type || 'Unknown'}
        </div>
    `;
    fileInfo.classList.remove('hidden');
    
    // Enable analyze button
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = '🔍 Start Analysis';
}

function extractPatientInfo(filename) {
    const patterns = [
        /Medical Report - (.*?) -/,
        /report_(.+?)_/,
        /(.+?)_medical/,
        /(\w+)\s+(\w+)/
    ];
    
    for (const pattern of patterns) {
        const match = filename.match(pattern);
        if (match) {
            return match[1].replace(/_/g, ' ').trim();
        }
    }
    
    return filename.replace(/\.[^/.]+$/, "").replace(/_/g, ' ');
}

function populatePatientInfo(filename) {
    const currentDate = new Date().toLocaleDateString();
    const extractedName = extractPatientInfo(filename);
    
    patientDetails.innerHTML = `
        <div class="patient-detail">
            <strong>File Name:</strong>
            ${extractedName}
        </div>
        <div class="patient-detail">
            <strong>Analysis Date:</strong>
            ${currentDate}
        </div>
        <div class="patient-detail">
            <strong>File Type:</strong>
            ${filename.split('.').pop().toUpperCase()}
        </div>
        <div class="patient-detail">
            <strong>Analysis Status:</strong>
            <span style="color: #28a745;">Processing with AI</span>
        </div>
    `;
}

function showError(message) {
    fileInfo.innerHTML = `<div class="error-message">${message}</div>`;
    fileInfo.classList.remove('hidden');
}

function resetAnalysisState() {
    analysisInProgress = false;
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = '🔍 Start Analysis';
    
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
}

// Initialize event listeners
function initializeEventListeners() {
    // File drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Analysis button
    analyzeBtn.addEventListener('click', startAnalysis);
}

// Initialize dashboard
window.addEventListener('load', () => {
    initializeEventListeners();
    loadAnalysisHistory();
});