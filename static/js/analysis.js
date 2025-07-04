// Analysis Management JavaScript

async function startAnalysis() {
    if (!currentFile || analysisInProgress) return;

    analysisInProgress = true;
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="loading-spinner"></span> Uploading...';

    // Reset all UI elements
    resetAnalysisUI();

    try {
        // Upload file to Flask backend
        const formData = new FormData();
        formData.append('file', currentFile);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            currentAnalysisId = result.analysis_id;
            
            // Show patient info section
            patientInfo.classList.remove('hidden');
            patientInfo.classList.add('fade-in');
            populatePatientInfo(result.filename);

            // Show final diagnosis section
            finalDiagnosis.container.classList.remove('hidden');
            finalDiagnosis.container.classList.add('fade-in');

            // Start polling for status updates
            startStatusPolling();

            analyzeBtn.innerHTML = '<span class="loading-spinner"></span> Analyzing with AI...';
        } else {
            showError(result.error || 'Upload failed');
            resetAnalysisState();
        }
    } catch (error) {
        showError('Network error: ' + error.message);
        resetAnalysisState();
    }
}

function resetAnalysisUI() {
    // Reset agent statuses
    Object.values(agents).forEach(agent => {
        agent.status.className = 'status-dot status-waiting';
        agent.statusText.textContent = 'Waiting for analysis...';
        agent.progress.style.width = '0%';
        agent.content.classList.add('hidden');
        agent.content.textContent = '';
    });

    // Reset final diagnosis
    finalDiagnosis.status.className = 'status-dot status-waiting';
    finalDiagnosis.statusText.textContent = 'Waiting for team analysis...';
    finalDiagnosis.progress.style.width = '0%';
    finalDiagnosis.content.classList.add('hidden');
    finalDiagnosis.content.innerHTML = '';
}

function startStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }

    statusCheckInterval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${currentAnalysisId}`);
            const status = await response.json();

            updateAnalysisStatus(status);

            if (status.status === 'completed' || status.status === 'error') {
                clearInterval(statusCheckInterval);
                analysisInProgress = false;
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '🔍 Analyze Another Report';
                
                if (status.status === 'completed') {
                    // Add to history
                    addToHistory(currentFile.name, status.results);
                    loadAnalysisHistory();
                } else if (status.status === 'error') {
                    showError('Analysis failed: ' + (status.error || 'Unknown error'));
                }
            }
        } catch (error) {
            console.error('Status check failed:', error);
        }
    }, 1000);
}

function updateAnalysisStatus(status) {
    if (!status.agent_progress) return;

    // Update individual agents
    Object.keys(agents).forEach(agentKey => {
        const agentStatus = status.agent_progress[agentKey];
        const agentUI = agents[agentKey];

        if (agentStatus) {
            agentUI.status.className = `status-dot status-${agentStatus.status}`;
            
            const statusText = {
                'waiting': 'Waiting for analysis...',
                'processing': '🔄 Analyzing with AI...',
                'completed': '✅ Analysis completed'
            };
            agentUI.statusText.textContent = statusText[agentStatus.status] || agentStatus.status;
            agentUI.progress.style.width = (agentStatus.progress || 0) + '%';

            if (agentStatus.status === 'completed' && status.results) {
                const agentName = agentKey.charAt(0).toUpperCase() + agentKey.slice(1);
                const result = status.results[agentName];
                if (result) {
                    agentUI.content.innerHTML = formatMedicalText(result);
                    agentUI.content.classList.remove('hidden');
                    agentUI.content.classList.add('fade-in');
                }
            }
        }
    });

    // Update final diagnosis
    const finalStatus = status.agent_progress.final;
    if (finalStatus) {
        finalDiagnosis.status.className = `status-dot status-${finalStatus.status}`;
        
        const statusText = {
            'waiting': 'Waiting for team analysis...',
            'processing': '🔄 Generating multidisciplinary diagnosis...',
            'completed': '✅ Final diagnosis completed'
        };
        finalDiagnosis.statusText.textContent = statusText[finalStatus.status] || finalStatus.status;
        finalDiagnosis.progress.style.width = (finalStatus.progress || 0) + '%';

        if (finalStatus.status === 'completed' && status.results && status.results.FinalDiagnosis) {
            finalDiagnosis.content.innerHTML = formatMedicalText(status.results.FinalDiagnosis);
            finalDiagnosis.content.classList.remove('hidden');
            finalDiagnosis.content.classList.add('fade-in');
        }
    }
}