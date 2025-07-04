// Modal Management JavaScript with Enhanced Text Formatting

const reportViewer = document.getElementById('reportViewer');
const reportBody = document.getElementById('reportBody');
const reportTitle = document.getElementById('reportTitle');

// Enhanced text formatting function for modal (same as dashboard but for consistency)
function formatMedicalTextForModal(text) {
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

function viewReport(historyId) {
    const item = analysisHistory.find(h => h.id === historyId);
    if (!item || !item.results) return;

    reportTitle.textContent = `Medical Analysis - ${item.filename}`;
    
    let reportHTML = `
        <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px;">
            <h3 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 5px;">📋 Report Summary</h3>
            <p><strong>Patient:</strong> ${item.filename}</p>
            <p><strong>Analysis Date:</strong> ${item.date}</p>
            <p><strong>File Type:</strong> ${item.fileType}</p>
        </div>
    `;

    // Add each specialist report with consistent formatting
    if (item.results.Cardiologist) {
        reportHTML += `
            <div class="report-section cardiologist-section">
                <div class="section-title">
                    <div class="section-icon cardiologist">❤️</div>
                    Cardiologist Analysis
                </div>
                <div class="modal-content-wrapper">${formatMedicalTextForModal(item.results.Cardiologist)}</div>
            </div>
        `;
    }

    if (item.results.Psychologist) {
        reportHTML += `
            <div class="report-section psychologist-section">
                <div class="section-title">
                    <div class="section-icon psychologist">🧠</div>
                    Psychologist Analysis
                </div>
                <div class="modal-content-wrapper">${formatMedicalTextForModal(item.results.Psychologist)}</div>
            </div>
        `;
    }

    if (item.results.Pulmonologist) {
        reportHTML += `
            <div class="report-section pulmonologist-section">
                <div class="section-title">
                    <div class="section-icon pulmonologist">🫁</div>
                    Pulmonologist Analysis
                </div>
                <div class="modal-content-wrapper">${formatMedicalTextForModal(item.results.Pulmonologist)}</div>
            </div>
        `;
    }

    if (item.results.FinalDiagnosis) {
        reportHTML += `
            <div class="report-section final-section">
                <div class="section-title">
                    <div class="section-icon multidisciplinary">🏥</div>
                    Final Multidisciplinary Diagnosis
                </div>
                <div class="modal-content-wrapper">${formatMedicalTextForModal(item.results.FinalDiagnosis)}</div>
            </div>
        `;
    }

    reportBody.innerHTML = reportHTML;
    reportViewer.classList.add('active');
}

function closeReportViewer() {
    reportViewer.classList.remove('active');
}

// Close modal when clicking outside
reportViewer.addEventListener('click', (e) => {
    if (e.target === reportViewer) {
        closeReportViewer();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && reportViewer.classList.contains('active')) {
        closeReportViewer();
    }
});