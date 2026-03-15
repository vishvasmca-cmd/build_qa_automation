/**
 * eCommerce Autonomous QA - Background Service Worker
 * Handles AI reasoning, test orchestration, and state management
 */

import { GeminiClient } from './ai/gemini-client.js';
import { QAReasoning } from './ai/qa-reasoning.js';

class QAOrchestrator {
    constructor() {
        this.gemini = null;
        this.activeTests = new Map();
        this.startingTabs = new Set(); // Concurrency Lock: Track tabs currently initializing
        this.readyWaiters = new Map(); // tabId -> resolve function
        this.config = {
            // HARDCODED API Key & Model
            apiKey: 'AIzaSyBhxsXVqBSXKax9zhRx73PxDyBNP8gDs2Y',
            model: 'gemini-2.0-flash',
            autoStart: false
        };

        this.initPromise = this.init();

        // Ensure Side Panel opens on click
        if (chrome.sidePanel) {
            chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true })
                .catch((error) => console.error('[QA-AGENT] Failed to set panel behavior:', error));
        }

        // Listen for messages from content script (Register synchronously!)
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            // we need to return true for async response, so we wrapper handleMessage
            this.handleMessage(message, sender, sendResponse);
            return true;
        });

        // PERSISTENCE MONITOR: Detect page reloads and re-inject
        chrome.tabs.onUpdated.addListener((tabId, info, tab) => {
            if (info.status === 'complete') {
                this.checkAndResumeTest(tabId);
            }
        });
    }

    async checkAndResumeTest(tabId) {
        // Find if this tab has an active test
        let activeTestKey = null;
        for (const [key, test] of this.activeTests.entries()) {
            if (test.tabId === tabId) {
                activeTestKey = key;
                break;
            }
        }

        if (activeTestKey) {
            const test = this.activeTests.get(activeTestKey);
            console.log(`[QA-AGENT] Detected reload on tab ${tabId}. Resuming test ${activeTestKey} in 300ms...`);

            // Wait slightly for page to settle
            setTimeout(async () => {
                // Re-inject and resume
                try {
                    const payload = {
                        goal: test.goal,
                        url: test.url,
                        tabId: tabId
                    };
                    await this.startTest(tabId, payload, true); // true = resume mode

                    if (test.testPlan) {
                        await this.sendMessageWithRetry(tabId, {
                            type: 'RESUME_TEST',
                            payload: {
                                testId: activeTestKey,
                                goal: test.goal,
                                testPlan: test.testPlan,
                                scenarioIndex: test.scenarioIndex || 0,
                                stepIndex: test.stepIndex || 0
                            }
                        });
                    }
                } catch (err) {
                    console.error('[QA-AGENT] Failed to resume test after reload:', err);
                }
            }, 300);
        }
    }

    async init() {
        // Load config from storage
        const stored = await chrome.storage.local.get(['qaConfig']);
        if (stored.qaConfig) {
            // Merge stored config, but ensure we don't overwrite hardcoded defaults with empty values
            const cleanStored = {};
            for (const [key, value] of Object.entries(stored.qaConfig)) {
                if (value) cleanStored[key] = value;
            }
            this.config = { ...this.config, ...cleanStored };
        }

        // Force critical settings just in case
        // FORCE OVERRIDE: Always use gemini-2.0-flash and hardcoded key
        this.config.apiKey = 'AIzaSyBhxsXVqBSXKax9zhRx73PxDyBNP8gDs2Y';
        this.config.model = 'gemini-2.0-flash';

        // Save back the potentially corrected config so popup sees it
        await chrome.storage.local.set({ qaConfig: this.config });

        // Initialize Gemini if API key exists

        // Initialize Gemini if API key exists
        if (this.config.apiKey) {
            this.gemini = new GeminiClient(this.config.apiKey, this.config.model);
        }

        console.log('[QA-AGENT] Background service worker initialized');
    }

    async handleMessage(message, sender, sendResponse) {
        // Ensure init is done before handling messages that depend on config
        await this.initPromise;

        const { type, payload } = message;

        switch (type) {
            case 'PING':
                console.log('[QA-AGENT] PING received from content script on tab', sender.tab.id);
                sendResponse({ success: true });
                break;
            case 'CONTENT_READY':
                console.log('[QA-AGENT] Content script ready on tab', sender.tab.id);
                if (this.readyWaiters.has(sender.tab.id)) {
                    this.readyWaiters.get(sender.tab.id)();
                    this.readyWaiters.delete(sender.tab.id);
                }
                sendResponse({ success: true });
                break;
            case 'MODULE_ERROR':
                console.error('[QA-AGENT] Content module failed to load on tab', sender.tab.id, payload);
                if (this.readyWaiters.has(sender.tab.id)) {
                    this.readyWaiters.delete(sender.tab.id); // Don't hang on error
                }
                sendResponse({ success: true });
                break;
            case 'START_TEST':
                const targetTabId = payload.tabId || sender.tab?.id;
                if (!targetTabId) {
                    sendResponse({ success: false, error: 'No target tab ID found' });
                    return;
                }

                // Fire and forget the start process (it handles its own async steps)
                this.startTest(targetTabId, payload).catch(err => {
                    console.error('[QA-AGENT] Async start failed:', err);
                });

                sendResponse({ success: true }); // Respond immediately
                break;

            case 'REASON_NEXT_STEP':
                this.reasonNextStep(payload)
                    .then(data => sendResponse({ data }))
                    .catch(error => sendResponse({ error: error.message }));
                break;
            case 'FIND_ELEMENT_AI':
                this.reasonElement(payload)
                    .then(data => sendResponse({ data }))
                    .catch(error => sendResponse({ error: error.message }));
                break;
            case 'RECONCILE_STATE_AI':
                this.reasonReconcile(payload)
                    .then(data => sendResponse({ data }))
                    .catch(error => sendResponse({ error: error.message }));
                break;

            case 'UPDATE_CONFIG':
                await this.updateConfig(payload);
                sendResponse({ success: true });
                break;

            case 'REPORT_PROGRESS':
                const test = Array.from(this.activeTests.values()).find(t => t.tabId === sender.tab.id);
                if (test) {
                    test.scenarioIndex = payload.scenarioIndex;
                    test.stepIndex = payload.stepIndex;
                    console.log(`[QA-AGENT] Progress synced for tab ${sender.tab.id}: Scenario ${payload.scenarioIndex}, Step ${payload.stepIndex}`);
                }
                sendResponse({ success: true });
                break;

            case 'GET_CONFIG':
                sendResponse({ success: true, data: this.config });
                break;

            default:
                console.warn('[QA-AGENT] Unknown message type:', type);
                sendResponse({ success: false, error: 'Unknown message type' });
        }
    }

    async startTest(tabId, { goal, url }, isResume = false) {
        // CONCURRENCY LOCK: Prevent multiple starts on the same tab
        if (this.startingTabs.has(tabId)) {
            console.warn(`[QA-AGENT] Test already starting for tab ${tabId}. Ignoring duplicate request.`);
            return;
        }

        console.log(`[QA-AGENT] ${isResume ? 'Resuming' : 'Starting'} test session for tab ${tabId}: ${goal}`);
        this.startingTabs.add(tabId);

        try {
            // 0. Initial Navigation (if URL provided and different and NOT resuming)
            if (url && !isResume) {
                const tab = await chrome.tabs.get(tabId);
                if (tab.url !== url && url.startsWith('http')) {
                    console.log(`[QA-AGENT] Navigating tab ${tabId} to: ${url}`);
                    await chrome.tabs.update(tabId, { url });

                    // Wait for navigation to complete
                    await new Promise((resolve) => {
                        const listener = (updatedTabId, info) => {
                            if (updatedTabId === tabId && info.status === 'complete') {
                                chrome.tabs.onUpdated.removeListener(listener);
                                resolve();
                            }
                        };
                        chrome.tabs.onUpdated.addListener(listener);
                        setTimeout(() => {
                            chrome.tabs.onUpdated.removeListener(listener);
                            resolve();
                        }, 10000);
                    });
                }
            }

            // 1. PROGRAMMATICALLY INJECT CONTENT SCRIPT (BEFORE AI PLANNING)
            try {
                console.log(`[QA-AGENT] Injecting content script into tab ${tabId}...`);

                // Set up waiter BEFORE injection
                const readyPromise = new Promise((resolve) => {
                    const timeout = setTimeout(resolve, 5000); // 5s timeout fallback
                    this.readyWaiters.set(tabId, () => {
                        clearTimeout(timeout);
                        resolve();
                    });
                });

                await chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    files: ['content.js']
                });

                console.log(`[QA-AGENT] Content script injected successfully, waiting for handshake...`);
                await readyPromise;
                console.log(`[QA-AGENT] Handshake successful for tab ${tabId}`);

                // Short sleep to allow the script to register its listener
                await new Promise(resolve => setTimeout(resolve, 300));

                // Initialize UI immediately with "Planning" status
                const testId = isResume ? null : `test_${Date.now()}`;
                if (!isResume) {
                    this.activeTests.set(testId, {
                        tabId,
                        goal,
                        url,
                        startTime: Date.now(),
                        scenarioIndex: 0,
                        stepIndex: 0,
                        testPlan: null
                    });
                }

                await this.sendMessageWithRetry(tabId, {
                    type: 'INIT_TEST',
                    payload: { testId, goal, url, planning: !isResume, isResume }
                });
                console.log(`[QA-AGENT] Test UI initiated on tab ${tabId}.`);

                // Continue with plan generation ONLY if not resuming
                if (!isResume) {
                    this.runTestProcess(tabId, testId, goal, url).catch(err => {
                        console.error('[QA-AGENT] Post-init process failed:', err);
                    });
                }

            } catch (error) {
                console.error('[QA-AGENT] Failed to initiate UI:', error);
                // Final fallback: try to report the error if a listener ever appears
                try {
                    await this.sendMessageWithRetry(tabId, {
                        type: 'QA_ERROR',
                        payload: { error: 'Communication failure: ' + error.message }
                    });
                } catch (e) { /* ignore */ }
            }
        } finally {
            // ALWAYS release the lock
            this.startingTabs.delete(tabId);
        }
    }

    async runTestProcess(tabId, testId, goal, url) {
        try {
            // 2. Generate test plan (AI Discovery & Reasoning)
            console.log(`[QA-AGENT] Capturing DOM context for discovery-based planning...`);
            const contextResponse = await this.sendMessageWithRetry(tabId, { type: 'CAPTURE_CONTEXT' });
            const pageContext = contextResponse?.data || { url, interactiveElements: [] };

            console.log(`[QA-AGENT] Generating test plan in background for test ${testId} (Discovery Mode)...`);
            await this.sendMessageWithRetry(tabId, {
                type: 'QA_STATUS',
                payload: { status: 'AI is discovering page elements...', phase: 'PLANNING' }
            });

            const testPlan = await this.generateTestPlan(goal, url, pageContext);

            await this.sendMessageWithRetry(tabId, {
                type: 'QA_STATUS',
                payload: { status: 'Finalizing e-commerce scenarios...', phase: 'PLANNING' }
            });

            // Save plan for persistence
            const test = this.activeTests.get(testId);
            if (test) test.testPlan = testPlan;

            console.log(`[QA-AGENT] Test plan generated successfully for test ${testId}`);

            // 3. Deliver the ready plan
            await this.sendMessageWithRetry(tabId, {
                type: 'TEST_PLAN_READY',
                payload: testPlan
            });

            console.log(`[QA-AGENT] Test mission delivered to tab ${tabId} for test ${testId}`);

        } catch (error) {
            console.error(`[QA-AGENT] Background process failed for test ${testId}:`, error);
            await this.sendMessageWithRetry(tabId, {
                type: 'QA_ERROR',
                payload: { error: 'Background failure: ' + error.message }
            }).catch(() => { }); // Catch to prevent unhandled promise rejection if tab is gone
        }
    }

    async sendMessageWithRetry(tabId, message, maxRetries = 10) {
        for (let i = 0; i < maxRetries; i++) {
            try {
                return await chrome.tabs.sendMessage(tabId, message);
            } catch (error) {
                if (error.message.includes('Could not establish connection') || error.message.includes('Receiving end does not exist')) {
                    if (i === maxRetries - 1) throw error;
                    console.log(`[QA-AGENT] Content script not ready. Retrying (${i + 1}/${maxRetries})...`);
                    await new Promise(resolve => setTimeout(resolve, 500));
                    continue;
                }
                throw error; // Throw other errors immediately
            }
        }
    }

    async generateTestPlan(goal, url, context) {
        if (!this.gemini) {
            throw new Error('Gemini API not configured. Please add your API key in the extension popup.');
        }

        const reasoning = new QAReasoning(this.gemini);
        return await reasoning.generateTestPlan(goal, url, context);
    }

    async reasonNextStep({ goal, currentState, pageContext }) {
        if (!this.gemini) {
            return { action: 'error', message: 'AI not configured' };
        }

        const reasoning = new QAReasoning(this.gemini);
        return await reasoning.reasonNextStep(goal, currentState, pageContext);
    }

    async reasonElement({ description, action, context }) {
        if (!this.gemini) throw new Error('AI not configured');
        const reasoning = new QAReasoning(this.gemini);

        // Build the prompt centrally in background
        const prompt = `You are an AI element finder for automated testing.
TARGET: "${description}" for action "${action}"
PAGE: ${context.url}
ELEMENTS: ${JSON.stringify(context.interactiveElements)}

DECISION RULES:
1. Return the index of the element that BEST matches.
2. IDEMPOTENCY: If the action is "click" on "Add to cart" and you see a button that says "Remove" for that item, return it. The agent will handle the skip.
3. SEMANTIC REASONING (AI MCP): You have access to specialized e-commerce tools. A cart badge is often a small span or label near the cart icon. If the requirement is "validate cart count", find the most likely element containing a number near the cart.
4. Be fuzzy but accurate.

IMPORTANT: Respond ONLY with a valid JSON object. No preamble, no explanation outside the JSON.

Respond JSON: {"found": true, "elementIndex": N, "reasoning": "..."}`;

        const response = await this.gemini.generateContent(prompt);
        return this.gemini.extractJSON(response);
    }

    async reasonReconcile({ steps, currentIndex, context }) {
        if (!this.gemini) throw new Error('AI not configured');
        const currentStep = steps[currentIndex];
        const prompt = `Determine if we are ALREADY PAST this step: "${currentStep.description}"
URL: ${context.url}
PAGE TYPE: ${context.pageType}
LOGGED IN: ${context.isLoggedIn ? 'YES' : 'NO'}

Response JSON: {"past": true, "skipTo": integer_index, "reason": "..."}
NOTE: "skipTo" MUST be the integer index of the NEXT step to execute. If unsure, return currentIndex + 1.

LOGIC RULES:
1. If you are on an internal page (inventory/cart) and the step is 'Login', return "past": true.
2. If finding a "Cart Badge" and the page is 'Cart' and items are visible, you may be past the 'Add to cart' step.
3. Use the presence of logout/profile indicators to confirm login status.

IMPORTANT: Respond ONLY with a valid JSON object. No preamble, no explanation outside the JSON.

Response JSON: {"past": true, "skipTo": index, "reason": "..."}`;

        const response = await this.gemini.generateContent(prompt);
        const result = this.gemini.extractJSON(response);

        // STATE-BASED LEARNING: If we are past a step, log it as a learned rule
        if (result && result.past) {
            console.log(`[QA-LEARNING] Site Rule Discovered: On ${context.url}, step "${currentStep.description}" is PAST. Reason: ${result.reason}`);
        }

        return result;
    }

    async updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        await chrome.storage.local.set({ qaConfig: this.config });

        // Reinitialize Gemini if API key changed
        if (newConfig.apiKey) {
            this.gemini = new GeminiClient(newConfig.apiKey, this.config.model);
        }
    }
}

// Initialize orchestrator
const orchestrator = new QAOrchestrator();
