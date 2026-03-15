import { getScenariosForUrl } from '../demo-config.js';

/**
 * Popup UI Controller
 */

// Load saved configuration
chrome.runtime.sendMessage({ type: 'GET_CONFIG' }, (response) => {
    if (response.success) {
        const config = response.data;
        const defaultKey = 'AIzaSy' + '...DEMO_KEY'; // Placeholder to look real but invalid
        // Actually, let's not auto-fill a fake key as it will error. 
        // Just hide the config section if key exists, or show if missing.

        if (config.apiKey) {
            document.getElementById('apiKey').value = config.apiKey;
            document.querySelector('.config-section').style.display = 'none'; // Hide config by default
        } else {
            document.getElementById('apiKey').value = '';
        }
        document.getElementById('model').value = config.model || 'gemini-2.0-flash';
    }
});

// Save configuration
document.getElementById('saveConfig').addEventListener('click', async () => {
    const apiKey = document.getElementById('apiKey').value.trim();
    const model = document.getElementById('model').value;

    if (!apiKey) {
        showStatus('Please enter a valid API key', 'error');
        return;
    }

    chrome.runtime.sendMessage({
        type: 'UPDATE_CONFIG',
        payload: { apiKey, model }
    }, (response) => {
        if (response.success) {
            showStatus('✅ Configuration saved successfully', 'success');
        } else {
            showStatus('❌ Failed to save configuration', 'error');
        }
    });
});

// Show current target site
async function updateTargetSiteDisplay() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const targetDisplay = document.getElementById('targetSiteDisplay');
    const manualUrlInput = document.getElementById('manualUrlInput');

    if (tab && tab.url && (tab.url.startsWith('http') || tab.url.startsWith('https'))) {
        try {
            const url = new URL(tab.url);
            targetDisplay.innerHTML = `Running on: <span style="color: #38bdf8;">${url.hostname}</span>`;
            manualUrlInput.style.display = 'none';
            return tab.url;
        } catch {
            targetDisplay.textContent = 'Could not detect website';
            manualUrlInput.style.display = 'block';
            return null;
        }
    } else {
        targetDisplay.textContent = 'No active website detected. Enter URL below:';
        manualUrlInput.style.display = 'block';
        return null;
    }
}

// Start test
// Start test
document.getElementById('startTest').addEventListener('click', async () => {
    const goal = document.getElementById('testGoal').value.trim();
    const manualUrl = document.getElementById('manualUrlInput').value.trim();

    if (!goal) {
        showStatus('Please enter a test goal', 'error');
        return;
    }

    // Get active tab
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Determine target URL: prioritize manual input if it's a valid link
    let targetUrl = (manualUrl && manualUrl.startsWith('http')) ? manualUrl : tab?.url;

    if (!targetUrl || !targetUrl.startsWith('http')) {
        showStatus('Please navigate to a website or enter a valid URL', 'error');
        return;
    }

    console.log('[POPUP] Starting session:', { goal, url: targetUrl, tabId: tab.id });
    showStatus('🚀 Initiating agent... please wait', 'success');

    const startBtn = document.getElementById('startTest');
    const startSpinner = document.getElementById('startSpinner');

    // Show spinner and disable button
    startBtn.disabled = true;
    startSpinner.style.display = 'inline-block';

    chrome.runtime.sendMessage({
        type: 'START_TEST',
        payload: { goal, url: targetUrl, tabId: tab.id }
    }, (response) => {
        console.log('[POPUP] Response:', response);

        if (chrome.runtime.lastError) {
            console.error('[POPUP] Runtime error:', chrome.runtime.lastError);
            showStatus('Error: ' + chrome.runtime.lastError.message, 'error');
            startBtn.disabled = false;
            startSpinner.style.display = 'none';
            return;
        }

        if (response && response.success) {
            showStatus('🚀 Agent initiated!', 'success');
            // Close immediately to let the user see the sidebar on the page
            setTimeout(() => window.close(), 100);
        } else {
            showStatus('❌ Failed to start test: ' + (response?.error || 'Unknown error'), 'error');
            startBtn.disabled = false;
            startSpinner.style.display = 'none';
        }
    });
});

// Dynamic Quick Test Loader
async function loadQuickTests() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let url = tab?.url || '';

    if (!url.startsWith('http')) {
        url = 'http://generic.com'; // Force generic templates
    }

    const scenarios = getScenariosForUrl(url);
    const container = document.querySelector('.quick-tests');

    // Clear existing static buttons
    container.innerHTML = '<label>Quick Test Templates</label>';

    scenarios.forEach(scenario => {
        const btn = document.createElement('button');
        btn.className = 'quick-test-btn';
        btn.textContent = scenario.name;
        btn.title = scenario.description;
        btn.onclick = () => {
            document.getElementById('testGoal').value = scenario.goal;
        };
        container.appendChild(btn);
    });
}

// Load tests when popup opens
document.addEventListener('DOMContentLoaded', () => {
    loadQuickTests();
    updateTargetSiteDisplay();
});

function showStatus(message, type) {
    const statusDiv = document.getElementById('statusMessage');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    statusDiv.style.display = 'block';

    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 3000);
    }
}
