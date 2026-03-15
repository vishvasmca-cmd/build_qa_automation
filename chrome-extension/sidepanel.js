import { GeminiClient } from './ai/gemini-client.js';
import { OllamaClient } from './ai/ollama-client.js'; // Import Ollama
import { QAReasoning } from './ai/qa-reasoning.js';

/**
 * QA Agent Side Panel Controller
 * Runs in the Side Panel context (persistent).
 * Manages connections to the active tab via chrome.debugger.
 */

class SidePanelAgent {
    constructor() {
        this.tabId = null;
        this.debuggerAttached = false;
        this.isRunning = false;

        // Smart Agent Memory & Queue
        this.memory = {
            visited: [],      // URLs visited
            interacted: [],   // Selectors/Text interacted with
            history: []       // Conversational history
        };
        this.actionQueue = []; // Queue for multi-step plans

        // Clients
        this.geminiClient = new GeminiClient('AIzaSyBhxsXVqBSXKax9zhRx73PxDyBNP8gDs2Y', 'gemini-2.0-flash');
        this.ollamaClient = new OllamaClient('moondream');

        this.currentClient = this.geminiClient; // Default to Gemini

        // UI Elements
        this.ui = {
            statusBadge: document.getElementById('status-badge'),
            statusDot: document.querySelector('.status-dot'),
            targetUrl: document.getElementById('target-url'),
            logs: document.getElementById('logs'),
            btnStart: document.getElementById('btn-start'),
            btnStop: document.getElementById('btn-stop'),
            goalInput: document.getElementById('goal-input'),
            providerSelect: document.getElementById('ai-provider') // New Selector
        };

        this.bindEvents();
        this.connectToActiveTab();
    }

    bindEvents() {
        this.ui.btnStart.addEventListener('click', () => this.startGoal());
        this.ui.btnStop.addEventListener('click', () => this.stopGoal());

        // Provider Switching
        this.ui.providerSelect.addEventListener('change', (e) => {
            const val = e.target.value;

            if (val.startsWith('ollama')) {
                const model = val.split('-')[1]; // llava or moondream
                this.ollamaClient = new OllamaClient(model); // Re-init with selected model
                this.currentClient = this.ollamaClient;
                this.log(`Switched to Local Ollama (${model})`, 'info');
            } else {
                this.currentClient = this.geminiClient;
                this.log('Switched to Gemini 2.0 Flash', 'info');
            }
        });

        // Listen for tab updates (navigation) - (code continues...)
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            if (tabId === this.tabId && changeInfo.status === 'complete') {
                this.log(`Tab navigated to: ${tab.url}`, 'info');
                this.ui.targetUrl.textContent = tab.url;
            }
        });

        // Listen for tab activation (switching tabs)
        chrome.tabs.onActivated.addListener(activeInfo => {
            this.connectToActiveTab(activeInfo.tabId);
        });

        // Listen for external detachment
        chrome.debugger.onDetach.addListener((source, reason) => {
            if (source.tabId === this.tabId) {
                this.debuggerAttached = false;
                // Silent state update, no log per user request
            }
        });
    }

    // ... (rest of class)

    async runAIControlLoop(goal) {
        let stepCount = 0;
        const MAX_STEPS = 50;

        while (this.isRunning && stepCount < MAX_STEPS) {
            stepCount++;

            // 1. Process Queue (Efficiency)
            if (this.actionQueue.length > 0) {
                const step = this.actionQueue.shift();
                this.log(`Executing Planned Action: ${step.action} on ${step.selector || 'target'}`, 'info');
                try {
                    await this.executeAction(step);
                    // Update Memory
                    if (step.selector) this.memory.interacted.push(step.selector);
                    this.memory.history.push(`Executed: ${step.action} ${step.selector}`);
                    await new Promise(r => setTimeout(r, 500)); // Small delay
                    continue; // Skip AI generation, keep draining queue
                } catch (e) {
                    this.log(`Plan Step Failed: ${e.message}`, 'warn');
                    this.memory.history.push(`Failed: ${step.action} ${step.selector} - ${e.message}`);
                    this.actionQueue = []; // Clear queue on failure to re-plan
                }
            }

            // Auto-recover connection
            await this.ensureDebuggerAttached();

            this.log(`Thinking... (Step ${stepCount})`, 'info');

            // 2. Capture State (Vision + URL)
            const screenshotBase64 = await this.captureScreenshot();
            const { result: { value: currentUrl } } = await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Runtime.evaluate', { expression: 'window.location.href' });

            if (!this.memory.visited.includes(currentUrl)) {
                this.memory.visited.push(currentUrl);
            }

            // --- WEB MCP INTEGRATION ---
            let modelScript = '';
            try {
                // Fetch the robust model from file
                const response = await fetch(chrome.runtime.getURL('automation/semantic-page-model.js'));
                const fileContent = await response.text();
                // Clean up export statement to make it executable in console
                modelScript = fileContent.replace('export class SemanticPageModel', 'class SemanticPageModel') + '\nnew SemanticPageModel().getState();';
            } catch (e) {
                this.log('Failed to load Semantic Model: ' + e.message, 'error');
            }

            let semanticState = {};
            try {
                const { result } = await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Runtime.evaluate', {
                    expression: `(() => { ${modelScript} })()`,
                    returnByValue: true
                });
                semanticState = result.value || {};
            } catch (e) {
                console.log('Semantic Injection Failed:', e);
            }

            // 3. Ask Gemini (Smart Planner)
            try {
                const prompt = `
                    GOAL: ${goal}
                    CURRENT URL: ${currentUrl}
                    MEMORY: ${JSON.stringify(this.memory)}
                    SEMANTIC STATE (WebMCP): ${JSON.stringify(semanticState)}
                    
                    You are a Smart Autonomous Agent.
                    1. Analyze the state and MEMORY.
                    2. **CRITICAL**: Do NOT repeat actions in MEMORY (check 'interacted').
                    3. **PLANNING**: Return a SEQUENCE of actions. If you need to click 5 buttons, return ALL 5 actions in the Plan.
                    4. **SELECTORS**: Prefer 'data-test' or 'id'. Use XPath indexing for lists: (//*[class='btn'])[2].
                    
                    Response JSON:
                    {
                        "thought": "I see 5 items. I will add the first 3 to the cart.",
                        "plan": [
                            { "action": "click", "selector": "(//*[text()='Add to cart'])[1]" },
                            { "action": "click", "selector": "(//*[text()='Add to cart'])[2]" },
                            { "action": "click", "selector": "(//*[text()='Add to cart'])[3]" }
                        ]
                    }
                    
                    OR if done: { "thought": "Done", "plan": [{ "action": "done" }] }
                `;

                // We send the screenshot as an image part to the selected Client
                const response = await this.currentClient.generateContent(prompt, [screenshotBase64]);
                const data = this.currentClient.extractJSON(response);

                // Log the "Human" thought as a Test Step
                if (data.thought) {
                    this.log(data.thought, 'driver', stepCount);
                }

                if (data.plan && Array.isArray(data.plan)) {
                    // Push plan to Queue
                    this.actionQueue = data.plan;
                }

                // Wait for stability if queue was empty (meaning we just thought)
                await new Promise(r => setTimeout(r, 1000));

            } catch (error) {
                // Filter out "Element not found" errors per user request
                const msg = error.message || '';
                if (msg.includes('not found') || msg.includes('Element')) {
                    console.log(`[Suppressed] AI Loop Error: ${msg}`);
                } else {
                    this.log(`AI Loop Error: ${msg}`, 'error');
                }

                // Don't crash loop, try again? Or stop?
                await new Promise(r => setTimeout(r, 2000));
            }
        }

        if (this.isRunning) {
            this.log('Max steps reached. Stopping.', 'error');
            this.stopGoal();
        }
    }

    async connectToActiveTab(specificTabId = null) {
        try {
            let tab;
            if (specificTabId) {
                tab = await chrome.tabs.get(specificTabId);
            } else {
                const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
                tab = tabs[0];
            }

            if (!tab) return;

            this.tabId = tab.id;
            this.ui.targetUrl.textContent = tab.url || 'New Tab';
            this.log(`Connected to tab: ${tab.title}`, 'info');

        } catch (error) {
            this.log(`Connection error: ${error.message}`, 'error');
        }
    }

    async ensureDebuggerAttached() {
        if (this.debuggerAttached) return;
        try {
            await chrome.debugger.attach({ tabId: this.tabId }, '1.3');
            this.debuggerAttached = true;
            await chrome.debugger.sendCommand({ tabId: this.tabId }, 'DOM.enable');
            await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Page.enable');
        } catch (error) {
            // If we can't attach, we can't proceed.
            // But we might be already attached and state is out of sync?
            if (error.message.includes('Already attached')) {
                this.debuggerAttached = true;
            } else {
                throw new Error(`Failed to re-attach debugger: ${error.message}`);
            }
        }
    }

    async startGoal() {
        const goal = this.ui.goalInput.value;
        if (!goal) {
            this.log('Please enter a test case', 'error');
            return;
        }

        this.isRunning = true;
        this.setStatus('Running', 'active');
        this.log(`Executing Test Case: ${goal}`, 'info');

        // Disable inputs
        this.ui.btnStart.disabled = true;
        this.ui.goalInput.disabled = true;
        this.ui.providerSelect.disabled = true;

        try {
            await this.ensureDebuggerAttached();
            await this.runAIControlLoop(goal);
        } catch (e) {
            this.log(`Execution failed: ${e.message}`, 'error');
            this.stopGoal();
        }
    }

    async stopGoal() {
        this.isRunning = false;
        this.setStatus('Stopped', 'error');

        // Re-enable inputs
        this.ui.btnStart.disabled = false;
        this.ui.goalInput.disabled = false;
        this.ui.providerSelect.disabled = false;

        // Log removed per user request
        await this.detachDebugger();
    }

    setStatus(text, type) {
        this.ui.statusBadge.textContent = text;
        this.ui.statusBadge.className = `status-badge ${type}`;
    }

    log(message, type = 'info', stepNumber = null) {
        const entry = document.createElement('div');
        entry.className = `log-entry log-${type}`;

        if (stepNumber) {
            const numParams = document.createElement('span');
            numParams.className = 'step-number';
            numParams.textContent = `#${stepNumber}`;
            entry.appendChild(numParams);
        }

        const msgSpan = document.createElement('span');
        msgSpan.textContent = message;
        entry.appendChild(msgSpan);

        this.ui.logs.appendChild(entry);
        this.ui.logs.scrollTop = this.ui.logs.scrollHeight;
    }

    // --- AI CONTROL LOOP ---

    async runAIControlLoop(goal) {
        let stepCount = 0;
        const MAX_STEPS = 50;
        let planOriginUrl = null;

        while (this.isRunning && stepCount < MAX_STEPS) {
            stepCount++;

            // 0. Check for Navigation (Stale Plan Protection)
            try {
                const { result } = await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Runtime.evaluate', { expression: 'window.location.href' });
                if (result && result.value) {
                    const currentUrl = result.value;
                    if (planOriginUrl && currentUrl !== planOriginUrl) {
                        this.log(`Navigation detected. Clearing queue to re-plan.`, 'warn');
                        this.actionQueue = [];
                        planOriginUrl = currentUrl;
                    }
                }
            } catch (e) { }

            // 1. Process Queue (Efficiency)
            if (this.actionQueue.length > 0) {
                const step = this.actionQueue.shift();
                this.log(`Executing Planned Action: ${step.action} on ${step.selector || 'target'}`, 'info');
                try {
                    await this.executeAction(step);
                    // Update Memory
                    if (step.selector) this.memory.interacted.push(step.selector);
                    this.memory.history.push(`Executed: ${step.action} ${step.selector}`);
                    await new Promise(r => setTimeout(r, 500)); // Small delay
                    continue; // Skip AI generation, keep draining queue
                } catch (e) {
                    this.log(`Plan Step Failed: ${e.message}`, 'warn');
                    this.memory.history.push(`Failed: ${step.action} ${step.selector} - ${e.message}`);
                    this.actionQueue = []; // Clear queue on failure to re-plan
                }
            }

            // Auto-recover connection
            await this.ensureDebuggerAttached();

            this.log(`Thinking... (Step ${stepCount})`, 'info');

            // 2. Capture State (Vision + URL)
            const screenshotBase64 = await this.captureScreenshot();
            const { result: { value: currentUrl } } = await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Runtime.evaluate', { expression: 'window.location.href' });

            if (!this.memory.visited.includes(currentUrl)) {
                this.memory.visited.push(currentUrl);
            }

            // 3. Ask Gemini (Smart Planner)
            try {
                const prompt = `
                    GOAL: ${goal}
                    CURRENT URL: ${currentUrl}
                    MEMORY: ${JSON.stringify(this.memory)}
                    
                    You are a Smart Autonomous Agent.
                    1. Analyze the state and MEMORY.
                    2. **CRITICAL**: Do NOT repeat actions in MEMORY (check 'interacted').
                    3. **PLANNING**: Return a SEQUENCE of actions. If you need to click 5 buttons, return ALL 5 actions in the Plan.
                    4. **SELECTORS**: Prefer 'data-test' or 'id'. Use XPath indexing for lists: (//*[class='btn'])[2].
                    
                    Response JSON:
                    {
                        "thought": "I see 5 items. I will add the first 3 to the cart.",
                        "plan": [
                            { "action": "click", "selector": "(//*[text()='Add to cart'])[1]" },
                            { "action": "click", "selector": "(//*[text()='Add to cart'])[2]" },
                            { "action": "click", "selector": "(//*[text()='Add to cart'])[3]" }
                        ]
                    }
                    
                    OR if done: { "thought": "Done", "plan": [{ "action": "done" }] }
                `;

                const response = await this.currentClient.generateContent(prompt, [screenshotBase64]);
                const data = this.currentClient.extractJSON(response);

                if (data.thought) this.log(data.thought, 'driver', stepCount);

                if (data.plan && Array.isArray(data.plan)) {
                    // Push plan to Queue
                    this.actionQueue = data.plan;
                }

                // Wait for stability if queue was empty (meaning we just thought)
                await new Promise(r => setTimeout(r, 1000));

            } catch (error) {
                const msg = error.message || '';
                if (msg.includes('not found') || msg.includes('Element')) {
                    console.log(`[Suppressed] AI Loop Error: ${msg}`);
                } else {
                    this.log(`AI Loop Error: ${msg}`, 'error');
                }
                await new Promise(r => setTimeout(r, 2000));
            }
        }

        if (this.isRunning) {
            this.log('Max steps reached. Stopping.', 'error');
            this.stopGoal();
        }
    }

    async executeAction(plan) {
        const { action, selector, value } = plan;

        switch (action) {
            case 'click':
                await this.executeClick(selector);
                break;
            case 'type':
            case 'fill': // Alias
                await this.executeType(selector, value);
                break;
            case 'navigate':
            case 'goto': // Alias
                await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Page.navigate', { url: value });
                break;
            default:
                // Unknown actions are ignored silently per user request
                break;
        }
    }

    // --- DEBUGGER PRIMITIVES ---

    async executeClick(selector) {
        // Poll for element existence (Simulating Playwright's auto-wait)
        const startTime = Date.now();
        const timeout = 5000; // 5 seconds wait
        let found = false;
        let coords = null;

        while (Date.now() - startTime < timeout) {
            const expression = `
                    (function () {
                        let el = null;
                        let selector = ${JSON.stringify(selector)};



                        // 1. Try Standard CSS
                        try {
                            el = document.querySelector(selector);
                        } catch (e) { }

                        // 2. Try XPath / Text Fallback
                        if (!el) {
                            try {
                                let xpath = selector;
                                // Handle 'text=' syntax
                                if (selector.startsWith('text=')) {
                                    const text = selector.substring(5);
                                    xpath = "//*[contains(text(), '" + text + "')]";
                                }
                                // If it looks like XPath (starts with / or text= processed)
                                if (xpath.startsWith('/') || xpath.startsWith('(')) {
                                    const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                                    el = result.singleNodeValue;
                                }
                            } catch (e) { }
                        }

                        // 3. ID Fallback (for weirdly escaped IDs)
                        if (!el && selector.startsWith('#')) {
                            try {
                                el = document.getElementById(selector.substring(1));
                            } catch (e) { }
                        }

                        if (!el) return null;
                        const rect = el.getBoundingClientRect();
                        return {
                            x: rect.left + rect.width / 2,
                            y: rect.top + rect.height / 2,
                            exists: true
                        };
                    })()
            `;
            const { result } = await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Runtime.evaluate', { expression, returnByValue: true });

            if (result && result.value) {
                found = true;
                coords = result.value;
                break;
            }
            // Wait 500ms before retry
            await new Promise(r => setTimeout(r, 500));
        }

        if (!found) {
            throw new Error(`Element ${selector} not found in DOM after 5s`);
        }

        const { x, y } = coords;

        // 2. Dispatch Mouse Events (Input.dispatchMouseEvent)
        await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Input.dispatchMouseEvent', {
            type: 'mousePressed', x, y, button: 'left', clickCount: 1
        });
        await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Input.dispatchMouseEvent', {
            type: 'mouseReleased', x, y, button: 'left', clickCount: 1
        });
    }

    async executeType(selector, text) {
        if (!text) {
            console.log(`[WARN] No text provided for type action on ${selector}`);
            return;
        }

        // 1. Focus Element (using same robust logic as Click)
        // We reuse executeClick logic to find coordinates + click to focus
        try {
            await this.executeClick(selector);
        } catch (e) {
            console.log(`[WARN] Focus failed for ${selector}, attempting direct type anyway.`);
        }

        // 2. Dispatch Key Events (Simulate Typing)
        for (const char of String(text)) {
            await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Input.dispatchKeyEvent', {
                type: 'keyDown', text: char, unmodifiedText: char
            });
            await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Input.dispatchKeyEvent', {
                type: 'keyUp', text: char, unmodifiedText: char
            });
            await new Promise(r => setTimeout(r, 50)); // Typing delay
        }
    }

    async captureScreenshot() {
        const { data } = await chrome.debugger.sendCommand({ tabId: this.tabId }, 'Page.captureScreenshot', { format: 'jpeg', quality: 50 });
        // Scanning log removed per user request
        return data;
    }
}

// Initialize
const agent = new SidePanelAgent();
