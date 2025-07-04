// History Management JavaScript

function addToHistory(filename, results) {
    const historyItem = {
        id: Date.now().toString(),
        filename: extractPatientInfo(filename),
        originalFilename: filename,
        date: new Date().toLocaleDateString(),
        fileType: filename.split('.').pop().toUpperCase(),
        results: results
    };
    
    analysisHistory.unshift(historyItem);
    
    // Keep only last 10 analyses
    if (analysisHistory.length > 10) {
        analysisHistory = analysisHistory.slice(0, 10);
    }
}

function loadAnalysisHistory() {
    const historyGrid = document.getElementById('historyGrid');
    
    if (analysisHistory.length === 0) {
        historyGrid.innerHTML = '<p>No previous analyses found. Upload a file to get started!</p>';
        return;
    }

    historyGrid.innerHTML = analysisHistory.map(item => `
        <div class="history-card" onclick="viewReport('${item.id}')">
            <div class="history-card-header">
                <div class="history-file-info">
                    <div class="history-file-name">📄 ${item.filename}</div>
                    <div class="history-file-meta">
                        <div><strong>Date:</strong> ${item.date}</div>
                        <div><strong>Type:</strong> ${item.fileType}</div>
                    </div>
                </div>
                <button class="view-report-btn" onclick="event.stopPropagation(); viewReport('${item.id}')">
                    👁️ View Report
                </button>
            </div>
        </div>
    `).join('');
}