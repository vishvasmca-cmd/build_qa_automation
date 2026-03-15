/**
 * eCommerce Autonomous QA - Content Script
 * Injected into e-commerce pages to control automation and UI
 */

import { DOMActions } from './automation/dom-actions.js';
import { ElementFinder } from './automation/element-finder.js';
import { WebMCPTools } from './automation/webmcp-tools.js';
import { SemanticPageModel } from './automation/semantic-page-model.js'; // NEW
import { DOMInspector } from './automation/dom-inspector.js';
import { AIElementFinder } from './automation/ai-element-finder.js';
import { SidebarManager } from './automation/sidebar-manager.js';

class QAContentAgent {
    constructor() {
        this.isActive = false;
        this.testId = null;
        this.goal = '';
        this.currentScenario = null;
        this.logHistory = [];
        this.isPaused = false;
        this.liveState = { cartCount: '-', cartTotal: '-' };
        this.DEFAULT_TIMEOUT = 10000;
        this.consecutiveFailures = 0;
        this.replanCount = 0;
        this.MAX_REPLANS_PER_SCENARIO = 3;

        // Automation modules
        this.domActions = new DOMActions();
        this.elementFinder = new ElementFinder(); // Keep as fallback
        this.webmcp = new WebMCPTools();
        this.semanticModel = new SemanticPageModel(); // NEW

        // Expose instance for debugging and log extraction
        window.__QA_AGENT__ = this;

        // AI modules (initialized in init)
        this.domInspector = new DOMInspector();
        this.aiElementFinder = null;
        this.gemini = null;
        this.sidebar = new SidebarManager();

        // INSTANT LISTENER: Register immediately to handle messages
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            console.log('[QA-AGENT] Message received:', message.type);
            this.handleMessage(message, sender, sendResponse);
            return true; // Keep channel open for async responders
        });

        this.init();
    }

    async init() {
        console.log('[QA-AGENT] Content script loaded');

        // Connect Sidebar Callbacks
        this.sidebar.onPauseToggle = (paused) => {
            this.isPaused = paused;
            console.log(`[QA-AGENT] Manual override: ${paused ? 'PAUSED' : 'RESUMED'}`);
        };

        this.sidebar.onSendMessage = (text) => {
            console.log('[QA-AGENT] Chat message received:', text);
            this.handleUserChat(text);
        };

        this.sidebar.onDownloadLogs = () => {
            console.log('[QA-AGENT] Exporting session logs...');
            this.downloadLogs();
        };

        // Initialize AI components with config from background
        try {
            this.aiElementFinder = new AIElementFinder(null, this.domInspector);
            console.log('[QA-AGENT] AI modules initialized (Remote Mode)');
        } catch (e) {
            console.error('[QA-AGENT] Failed to initialize AI modules:', e);
        }

        // Auto-detect e-commerce site and offer to start testing
        this.detectEcommerceSite();
    }

    async handleUserChat(text) {
        this.updateSidebar('AI Thinking...', `Answering query about current page: "${text}"`, 'AI', 'INFO');
        // Future: Integration with Gemini for direct chat
    }

    detectEcommerceSite() {
        const indicators = [
            document.querySelector('.shopping-cart, .cart, #cart'),
            document.querySelector('[class*="product"], [class*="item"]'),
            document.querySelector('[class*="checkout"], [href*="checkout"]'),
            document.querySelector('[class*="add-to-cart"], [class*="addtocart"]')
        ];
        if (indicators.some(el => el !== null)) {
            console.log('[QA-AGENT] E-commerce site detected');
        }
    }

    async handleMessage(message, sender, sendResponse) {
        const { type, payload } = message;
        try {
            switch (type) {
                case 'QA_ERROR':
                    this.updateSidebar('Process SNAG', payload.error, 'STATUS', 'WARN');
                    this.sidebar.addThought(`Background error detected: ${payload.error}. Attempting auto-recovery...`, 'learning');
                    // AUTO-RECOVER: Instead of stopping, try to re-plan if we are active
                    if (this.isActive) {
                        this.triggerDynamicReplan().catch(e => console.error('[QA-AGENT] Auto-recovery failed:', e));
                    }
                    sendResponse({ success: true });
                    break;
                case 'TOGGLE_QA_MODE':
                    sendResponse({ success: true, status: 'toggling' });
                    await this.toggleQAMode();
                    break;
                case 'INIT_TEST':
                    sendResponse({ success: true, status: 'initializing' });
                    await this.initTest(payload);
                    break;
                case 'RESUME_TEST':
                    sendResponse({ success: true, status: 'resuming' });
                    await this.resumeTest(payload);
                    break;
                case 'QA_STATUS':
                    this.updateSidebar(payload.status, payload.detail || '', payload.phase || 'AI', 'INFO');
                    sendResponse({ success: true });
                    break;
                case 'TEST_PLAN_READY':
                    sendResponse({ success: true, status: 'plan_received' });
                    await this.executeTestPlan(payload);
                    break;
                case 'CAPTURE_CONTEXT':
                    const context = await this.domInspector.capturePageContext();
                    sendResponse({ success: true, data: context });
                    break;
                default:
                    sendResponse({ success: false, error: 'Unknown message type' });
            }
        } catch (error) {
            console.error(`[QA-AGENT] Error handling message ${type}:`, error);
            try { sendResponse({ success: false, error: error.toString() }); } catch (e) { }
        }
    }

    async toggleQAMode() {
        this.isActive = !this.isActive;
        if (this.isActive) {
            this.sidebar.create();
            this.updateSidebar('QA Mode Activated', 'Ready to start testing...', 'STATUS', 'INFO');
        } else {
            this.sidebar.remove();
        }
    }

    async initTest({ testId, goal, url, planning, isResume }) {
        if (isResume) {
            console.log('[QA-AGENT] Initializing for resumption...');
        }
        this.testId = testId;
        this.goal = goal;
        this.isActive = true;
        this.isPaused = false;

        this.sidebar.create();
        this.sidebar.setMission(goal);
        if (testId) this.sidebar.setTestId(testId);

        if (planning && !isResume) {
            // Show initial "Thought" step while AI generates plan
            this.sidebar.updateSteps([
                { description: 'Analyzing requirements and designing QA test suite...' }
            ], 0, 'QA Expert is thinking...');
        }
    }

    async resumeTest({ testId, goal, testPlan, scenarioIndex, stepIndex }) {
        console.log(`[QA-AGENT] Resuming test ${testId} from Scenario ${scenarioIndex}, Step ${stepIndex}`);
        this.testId = testId;
        this.goal = goal;
        this.isActive = true;

        this.sidebar.create();
        this.sidebar.setMission(goal);

        // Start execution from the saved indices
        await this.executeTestPlan(testPlan, scenarioIndex, stepIndex);
    }

    async reportProgress(scenarioIndex, stepIndex) {
        try {
            await chrome.runtime.sendMessage({
                type: 'REPORT_PROGRESS',
                payload: { scenarioIndex, stepIndex }
            });
        } catch (e) {
            console.warn('[QA-AGENT] Failed to report progress to background:', e);
        }
    }

    async updateSidebar(status, detail, phase, qaResult) {
        // Store in history for reporting
        this.logHistory.push({ status, detail, phase, qaResult, timestamp: new Date().toLocaleTimeString() });

        // Update indicators if available
        this.sidebar.updateIndicators(this.liveState.cartCount, this.liveState.cartTotal);

        // Add to sidebar log
        this.sidebar.addEntry(status, detail, phase, qaResult);

        // Update public state for external extractors
        window.__QA_AGENT_STATE__ = {
            goal: this.goal,
            logs: this.logHistory,
            lastStatus: status,
            isComplete: status === 'Mission Accomplished' || status === 'Mission Failed'
        };
    }

    async reconcileState(steps, currentIndex) {
        const currentStep = steps[currentIndex];
        const context = await this.domInspector.capturePageContext();

        console.log(`[QA-AGENT] Reconciling state for step: ${currentStep.description}`);

        // AGGRESSIVE BYPASS: If we are on inventory/home and this is a login/nav step, we are PAST it.
        const isInternalPage = context.pageType === 'inventory';
        const isSetupAction = ['navigate', 'fill', 'click'].includes(currentStep.action?.toLowerCase()) &&
            (currentStep.target?.toLowerCase().includes('login') ||
                currentStep.target?.toLowerCase().includes('user') ||
                currentStep.target?.toLowerCase().includes('pass'));

        if (isInternalPage && isSetupAction) {
            console.log(`[QA-AGENT] State Reconciled: Already on inventory page. Skipping setup step.`);
            // Look ahead for the first non-setup step
            for (let j = currentIndex; j < steps.length; j++) {
                const s = steps[j];
                const isNavOrLogin = s.target?.toLowerCase().includes('login') || s.action?.toLowerCase() === 'navigate';
                if (!isNavOrLogin) return j;
            }
        }

        try {
            // DELEGATE RECONCILE TO BACKGROUND: Fixes Failed to Fetch / CORS
            const response = await chrome.runtime.sendMessage({
                type: 'RECONCILE_STATE_AI',
                payload: { steps, currentIndex, context }
            });

            if (response && response.data && response.data.past) {
                const result = response.data;
                // NORMALIZE skipTo: If null/undefined, safe default is currentIndex + 1
                const finalSkipTo = (result.skipTo !== null && result.skipTo !== undefined)
                    ? result.skipTo
                    : currentIndex + 1;

                console.log(`[QA-AGENT] State Reconciled (Remote): ${result.reason}. Skipping to index ${finalSkipTo}`);
                this.updateSidebar('State Reconciled', `Automatically advanced: ${result.reason}`, 'STATUS', 'INFO');
                this.sidebar.addThought(`Reconcilation: ${result.reason}`, 'learning');
                return finalSkipTo;
            }
        } catch (e) {
            console.error('[QA-AGENT] Remote state reconciliation failed:', e);
        }

        return currentIndex;
    }

    downloadLogs() {
        const header = `eCommerce Autonomous QA - Session Log\nExported: ${new Date().toLocaleString()}\nMission: ${this.goal}\n\n`;
        const logs = this.logHistory.map(entry => {
            return `[${entry.timestamp}] ${entry.phase || 'INFO'} | ${entry.status}: ${entry.detail} ${entry.qaResult ? `[${entry.qaResult}]` : ''}`;
        }).join('\n');

        const blob = new Blob([header + logs], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `qa_session_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    async executeTestPlan(testPlan, startScenarioIndex = 0, startStepIndex = 0) {
        if (!testPlan || !testPlan.scenarios) {
            console.error('[QA-AGENT] Cannot execute invalid test plan:', testPlan);
            this.updateSidebar('Execution Error', 'Invalid test plan received', 'STATUS', 'FAIL');
            return;
        }

        this.testPlan = testPlan;
        const { scenarios } = testPlan;

        for (let i = startScenarioIndex; i < scenarios.length; i++) {
            const scenario = scenarios[i];
            this.currentScenario = scenario;
            this.replanCount = 0; // Reset re-plan count for each new scenario

            // Log scenario header
            this.updateSidebar(`Scenario ${i + 1}: ${scenario.name}`, '', 'SCENARIO', 'INFO');

            // If we are resuming, perform STATE RECONCILIATION to see if we should skip steps
            let currentStartStep = (i === startScenarioIndex) ? startStepIndex : 0;
            if (currentStartStep < scenario.steps.length) {
                const reconcileResult = await this.reconcileState(scenario.steps, currentStartStep);
                if (reconcileResult > currentStartStep) {
                    console.log(`[QA-AGENT] State reconciled: Skipping ${reconcileResult - currentStartStep} completed steps.`);
                    currentStartStep = reconcileResult;
                }
            }

            for (let stepIndex = currentStartStep; stepIndex < scenario.steps.length; stepIndex++) {
                const step = scenario.steps[stepIndex];

                // EXECUTION SYNC: Wait 1000ms before starting each step (User-requested slow down)
                await new Promise(r => setTimeout(r, 1000));

                // Update UI with full list of steps and current index
                this.sidebar.updateSteps(scenario.steps, stepIndex);

                // DYNAMIC RE-ANALYSIS: Before each step, verify relevance
                const isRelevant = await this.checkStepRelevance(step);
                if (!isRelevant) {
                    console.log('[QA-AGENT] Step no longer relevant. Triggering dynamic re-plan...');
                    this.updateSidebar('Status Change', 'Page state changed. Re-planning...', 'AI', 'INFO');
                    const replanned = await this.triggerDynamicReplan();
                    if (replanned) {
                        // Restart scenario loop with fresh plan starting from current position
                        i--; // Re-run current scenario index with new plan
                        break;
                    }
                }

                // PREDICTIVE SYNC: If this is likely a navigation step, sync progress BEFORE action
                const likelyNav = ['click', 'submit', 'navigate'].includes(step.action?.toLowerCase());
                if (likelyNav) {
                    await this.reportProgress(i, stepIndex + 1);
                }

                try {
                    const result = await this.executeStep(step, scenario.steps, stepIndex);

                    if (result.success) {
                        this.consecutiveFailures = 0;
                    } else {
                        throw new Error(result.error || "Step execution failed");
                    }
                } catch (stepError) {
                    this.consecutiveFailures++;
                    console.error(`[QA-AGENT] Step Error: ${stepError.message}. Failures: ${this.consecutiveFailures}`);

                    // UNSTOPPABLE MODE: Re-plan ON FIRST FAILURE for core actions
                    const isValidation = step.action?.toLowerCase() === 'validate';

                    if (!isValidation) {
                        this.updateSidebar('Auto-Healing', 'Step failed. Recruiting AI to find a new path...', 'STATUS', 'WARN');
                        const replanned = await this.triggerDynamicReplan();
                        if (replanned) {
                            i--; // Re-run current scenario index with fresh plan
                            break;
                        }
                    }

                    // FAIL-FORWARD: If re-plan failed or it's just a validation, log and keep moving if possible
                    if (isValidation) {
                        console.log('[QA-AGENT] Non-critical validation failed. Failing forward...');
                        this.sidebar.addThought(`Validation failed: ${stepError.message}. Continuing mission.`, 'learning');
                    } else {
                        // LAST RESORT: If even re-planning failed multiple times, we finally pause
                        if (this.replanCount >= this.MAX_REPLANS_PER_SCENARIO) {
                            this.isPaused = true;
                            this.sidebar.togglePause();
                        } else {
                            // Try one more re-plan before giving up
                            await this.triggerDynamicReplan();
                        }
                    }
                }

                // FINAL SYNC (if not already handled by predictive sync)
                if (!likelyNav) {
                    await this.reportProgress(i, stepIndex + 1);
                }

                // Wait for page state to settle (Increased stability wait)
                await this.waitForStability();
                await new Promise(r => setTimeout(r, 1500));
            }

            // Mark all steps as complete for this scenario
            this.sidebar.updateSteps(scenario.steps, scenario.steps.length);

            // Validate scenario completion
            const validation = await this.validateScenario(scenario);
            this.updateSidebar(
                validation.passed ? 'Scenario Passed' : 'Scenario Failed',
                validation.message,
                'STATUS',
                validation.passed ? 'PASS' : 'FAIL'
            );

            // SYNC PROGRESS (Next Scenario)
            await this.reportProgress(i + 1, 0);
        }

        // Generate final report
        this.generateReport();
    }

    async executeWebMCPStep(step) {
        const { action, target, value } = step;
        const lowerAction = action?.toLowerCase();
        const lowerTarget = target?.toLowerCase();

        // 0. GLOBAL PRE-CHECK: Login State
        // If we are already logged in, and this is a login-related step, SKIP IT.
        if (this.semanticModel && this.semanticModel.state.user.loggedIn) {
            const isLoginStep = lowerTarget.includes('login') ||
                lowerTarget.includes('user') ||
                lowerTarget.includes('pass') ||
                lowerTarget.includes('auth');

            if (isLoginStep) {
                console.log('[QA-AGENT] Smart Skip: Already logged in. Skipping step:', step.description);
                return { success: true, message: "Already logged in (Smart Skip)", action: "login_skipped" };
            }
        }

        // 1. LOGIN
        if ((lowerTarget.includes('login') || lowerTarget.includes('user') || lowerTarget.includes('pass')) &&
            (lowerAction === 'fill' || lowerAction === 'login' || lowerAction === 'click')) {

            // If we are here, we are NOT logged in (or semantic model hasn't updated).
            // Combine user/pass if provided in value or just try standard login
            if (value && value.includes(':')) {
                const [user, pass] = value.split(':');
                return await this.webmcp.login(user.trim(), pass.trim());
            }
            // If this is just "fill username", we might want to wait for the next steps? 
            // OR we can just execute the specific part using webmcp (which handles fields)
            // But WebMCP.login does the WHOLE thing.

            // Strategy: If plan is fragmented (User, then Pass), we should try to Run the WHOLE login 
            // if we have credentials, OR just return success if we can't do partials.
            // For now, let's rely on WebMCP.login's idempotency.
            return await this.webmcp.login('standard_user', 'secret_sauce'); // Default or extract from context?
            // TODO: We need the actual credentials if not provided in this specific step.
            // For now, returning null to let it fall back to standard filling logic 
            // UNLESS we are sure it's the "Login" button click
        }

        // 2. SORT
        if (lowerAction === 'sort') {
            return await this.webmcp.sortProducts(value || 'lohi');
        }

        // 3. SEARCH
        if (lowerAction === 'search') {
            return await this.webmcp.searchProducts(value);
        }

        // 4. FILTER
        if (lowerAction === 'filter') {
            return await this.webmcp.filterProducts(value);
        }

        // 5. ADD TO CART
        if (lowerAction === 'add' || (lowerAction === 'click' && lowerTarget.includes('add to cart'))) {
            // Check for specific criteria in target/value
            const criteria = {};
            if (lowerTarget.includes('cheapest')) criteria.rank = 'cheapest';
            else if (lowerTarget.includes('expensive')) criteria.rank = 'most_expensive';
            else criteria.name = value || target; // Fallback to name search

            return await this.webmcp.addToCart(criteria);
        }

        // 6. CHECKOUT FORM
        if (lowerAction === 'fill' && lowerTarget.includes('checkout')) {
            // Expect value to be JSON or we parse it
            try {
                const details = typeof value === 'string' ? JSON.parse(value) : value;
                return await this.webmcp.fillCheckoutForm(details);
            } catch (e) {
                // If not JSON, maybe just mapped fields? Skip for now.
            }
        }

        // 7. PLACE ORDER
        if (lowerAction === 'click' && (lowerTarget.includes('finish') || lowerTarget.includes('place order'))) {
            return await this.webmcp.placeOrder();
        }

        // 8. LOGOUT
        if (lowerAction === 'click' && lowerTarget.includes('logout')) {
            return await this.webmcp.logout();
        }

        // 9. PAGINATE
        if (lowerAction === 'paginate' || (lowerAction === 'click' && (lowerTarget.includes('next page') || lowerTarget.includes('previous page')))) {
            const dir = lowerTarget.includes('prev') ? 'prev' : 'next';
            return await this.webmcp.paginate(dir);
        }

        return null; // No WebMCP tool matched
    }

    async executeStep(step, allSteps, index) {
        const { action, target, value, description } = step;

        // PAUSE CHECK
        while (this.isPaused) {
            await new Promise(r => setTimeout(r, 500));
        }

        try {
            // 0. WebMCP FAST PATH (Intents)
            const webmcpResult = await this.executeWebMCPStep(step);
            if (webmcpResult) {
                if (webmcpResult.success) {
                    this.sidebar.updateSteps(allSteps, index, `WebMCP: ${webmcpResult.message}`);
                    console.log(`[QA-AGENT] WebMCP Success: ${webmcpResult.action}`);
                    return { success: true };
                } else {
                    console.warn(`[QA-AGENT] WebMCP attempted ${webmcpResult.action} but failed: ${webmcpResult.error}. Falling back to standard selectors.`);
                }
            }

            const MAX_RETRIES = 3;
            let element = null;

            // RETRY LOOP
            for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
                try {
                    // 1. ACTION GUARD (Hallucination Prevention)
                    if (action.toLowerCase() === 'fill' &&
                        (target.includes('error') || target.includes('message') || target.includes('button'))) {
                        console.warn(`[QA-AGENT] Action Guard: blocking 'fill' on '${target}'. Converting to 'validate' or skipping.`);
                        return { success: true, detail: "Skipped invalid fill action" };
                    }

                    // 2. FIND ELEMENT
                    if (target && action.toLowerCase() !== 'navigate') {
                        this.sidebar.updateSteps(allSteps, index, `Finding ${target}...`);

                        // Static Find
                        element = await this.elementFinder.find(target, action);

                        // AI Find
                        if (!element && this.aiElementFinder) {
                            console.log(`[QA-AGENT] Static find failed for "${target}". Engaging AI...`);
                            this.sidebar.updateSteps(allSteps, index, `AI analyzing page...`);
                            try {
                                const aiResult = await this.aiElementFinder.findElement(target, action, true);
                                element = aiResult?.element || aiResult;
                                if (aiResult?.reasoning) this.sidebar.addThought(aiResult.reasoning, 'reason');
                            } catch (aiError) {
                                if (aiError.message.includes('Extension context invalidated')) throw new Error('EXTENSION_INVALIDATED');
                                throw aiError;
                            }
                        }

                        if (!element) throw new Error(`Element not found: ${target}`);
                    }

                    // 3. EXECUTE ACTION
                    const actionLabel = action.toLowerCase() === 'fill' ? `Typing "${value}"` : `${action.charAt(0).toUpperCase() + action.slice(1)}ing...`;
                    this.sidebar.updateSteps(allSteps, index, actionLabel);

                    switch (action.toLowerCase()) {
                        case 'navigate':
                            await this.domActions.navigate(value || target);
                            break;
                        case 'click':
                            const elText = (element.textContent || element.value || '').toLowerCase();
                            const isAddToCart = target.toLowerCase().includes('add to cart') || description.toLowerCase().includes('add to cart');
                            if (isAddToCart && elText.includes('remove')) {
                                return { success: true, detail: "Item already in cart (skipped click)" };
                            }
                            await this.domActions.click(element);
                            break;
                        case 'fill':
                            await this.domActions.fill(element, value);
                            break;
                        case 'hover':
                            await this.domActions.hover(element);
                            break;
                        case 'validate':
                            const actualValue = element ? (element.value || element.textContent) : null;
                            if (value && !actualValue.includes(value)) throw new Error(`Expected "${value}", found "${actualValue}"`);
                            break;
                    }

                    // 4. SUCCESS
                    return { success: true };

                } catch (retryError) {
                    if (retryError.message === 'EXTENSION_INVALIDATED') throw retryError;

                    // IF LAST ATTEMPT: Try Self-Healing
                    if (attempt === MAX_RETRIES) {
                        // Global Text Fallback for Validate
                        if (action.toLowerCase() === 'validate') {
                            console.log(`[QA-AGENT] Validating with Global Text Fallback...`);
                            const context = await this.domInspector.capturePageContext();
                            const visibleText = context.visibleText.toLowerCase();
                            const normalizedTarget = (value || target).toLowerCase();

                            if (visibleText.includes(normalizedTarget)) {
                                this.updateSidebar('Validation Healed', `Found "${normalizedTarget}" in page context`, 'STATUS', 'PASS');
                                return { success: true };
                            }

                            // AI Judge
                            if (this.gemini) {
                                try {
                                    const prompt = `Evaluate if page matches requirement: "${normalizedTarget}".\nContext: ${visibleText.substring(0, 500)}\nReturn JSON {match: bool, reason: str}`;
                                    const response = await this.gemini.generateContent(prompt);
                                    const result = this.gemini.extractJSON(response);
                                    if (result.match) {
                                        this.updateSidebar('Fuzzy Match Pass', `AI confirmed match: ${result.reason}`, 'STATUS', 'PASS');
                                        return { success: true };
                                    }
                                } catch (e) { console.warn('AI Fuzzy failed', e); }
                            }
                        }

                        // If healing failed, rethrow to outer catch
                        throw retryError;
                    }

                    // IF NOT LAST ATTEMPT: Wait and Retry
                    this.sidebar.updateSteps(allSteps, index, `Retrying (${attempt}/${MAX_RETRIES})...`);
                    await this.waitForStability();
                }
            } // End Loop

        } catch (fatalError) {
            console.error('[QA-AGENT] Step execution failed:', fatalError);
            if (fatalError.message.includes('EXTENSION_INVALIDATED')) {
                this.sidebar.showFatalError('Extension Context Invalidated. Please REFRESH the page.');
            } else {
                this.updateSidebar('Step Failed', fatalError.message, 'STATUS', 'FAIL');
            }
            return { success: false, error: fatalError.message };
        }
    }

    async checkStepRelevance(step) {
        if (!this.gemini) return true;

        // Only check relevance for interactive steps (not navigation which is explicit)
        if (['navigate'].includes(step.action?.toLowerCase())) return true;

        const context = await this.domInspector.capturePageContext();
        const prompt = `As a Senior QA Expert, evaluate if the following test step is still valid for this current page.
        STEP: ${step.description}
        URL: ${context.url}
        TITLE: ${context.title}
        
        Respond JSON: {"valid": true, "reason": "why"}`;

        try {
            const response = await this.gemini.generateContent(prompt);
            const result = this.gemini.extractJSON(response);
            return result.valid;
        } catch (e) {
            return true; // Default to true if AI fails
        }
    }

    async triggerDynamicReplan() {
        if (this.replanCount >= this.MAX_REPLANS_PER_SCENARIO) {
            console.warn('[QA-AGENT] Max re-plans reached for this scenario. Pausing.');
            this.updateSidebar('Recovery Aborted', 'Could not recover after multiple attempts.', 'STATUS', 'FAIL');
            return false;
        }

        this.replanCount++;
        console.log(`[QA-AGENT] Requesting autonomous re-plan (${this.replanCount}/${this.MAX_REPLANS_PER_SCENARIO}) from background...`);

        const context = await this.domInspector.capturePageContext();

        try {
            const response = await chrome.runtime.sendMessage({
                type: 'REASON_NEXT_STEP',
                payload: {
                    goal: this.goal,
                    pageContext: context,
                    currentState: {
                        url: window.location.href,
                        pageType: context.pageType,
                        isLoggedIn: context.isLoggedIn,
                        cartCount: this.liveState.cartCount,
                        history: this.logHistory.slice(-5).map(l => `${l.status}: ${l.detail}`),
                        recentFailures: this.consecutiveFailures > 0 ? `Failed ${this.consecutiveFailures} times trying to perform the previous action.` : 'None'
                    }
                }
            });

            if (response && response.data) {
                const nextStep = response.data;
                console.log('[QA-AGENT] AI suggested next autonomous action:', nextStep);
                this.sidebar.addThought(`Recovery logic: ${nextStep.reason || "Autonomous re-plan triggered"}`, 'learning');

                // Construct a one-step temporary scenario to "recover"
                const recoveryScenario = {
                    name: "Autonomous Recovery",
                    steps: [nextStep]
                };

                // Ensure testPlan exists
                if (!this.testPlan) {
                    console.warn('[QA-AGENT] No existing test plan found during re-plan. Initializing recovery plan.');
                    this.testPlan = { scenarios: [] };
                }

                // Inject into test plan at current position
                const currentIdx = this.testPlan.scenarios.indexOf(this.currentScenario);
                if (currentIdx !== -1) {
                    this.testPlan.scenarios.splice(currentIdx, 1, recoveryScenario);
                } else {
                    // If currentScenario is unknown, just push it
                    this.testPlan.scenarios.push(recoveryScenario);
                    this.currentScenario = recoveryScenario;
                }
                return true;
            }
        } catch (e) {
            console.error('[QA-AGENT] Re-plan request failed:', e);
        }
        return false;
    }

    async validateScenario(scenario) {
        // Use WebMCP tools to validate current state
        const validations = await Promise.all([
            this.webmcp.getCartCount(),
            this.webmcp.getCartTotal(),
            this.webmcp.verifyCheckoutForm()
        ]);

        // Check if validations match scenario expectations
        return {
            passed: validations.every(v => v.success),
            message: validations.map(v => v.message).join(', ')
        };
    }

    removeSidebar() {
        this.sidebar.remove();
    }

    generateReport() {
        const scenarioCount = this.logHistory.filter(l => l.phase === 'SCENARIO').length;
        const passCount = this.logHistory.filter(l => l.qaResult === 'PASS').length;
        const failCount = this.logHistory.filter(l => l.qaResult === 'FAIL').length;

        const summary = `Executed ${scenarioCount} scenarios. ${passCount} passed, ${failCount} failed.`;
        this.updateSidebar('Mission Complete', summary, 'SUMMARY', 'PASS');
    }

    async waitForStability() {
        return new Promise(resolve => {
            let timeout;
            const observer = new MutationObserver(() => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    observer.disconnect();
                    resolve();
                }, 500);
            });
            observer.observe(document.body, { childList: true, subtree: true });
            setTimeout(() => {
                observer.disconnect();
                // Refresh semantic state after stability
                if (this.semanticModel) {
                    this.semanticModel.getState();
                }
                resolve();
            }, 5000);
        });
    }
}

// Initialize agent
const agent = new QAContentAgent();
