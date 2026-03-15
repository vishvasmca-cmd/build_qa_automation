/**
 * Sidebar Manager 2.0 - Agentic UI
 * Professional high-fidelity progress and control interface
 */
export class SidebarManager {
    constructor() {
        this.sidebarId = 'antigravity-sidebar';
        this.width = '420px'; // Slightly wider for professional look
        this.container = null;
        this.logContainer = null;
        this.stepList = null;
        this.chatInput = null;
        this.cartCountEl = null;
        this.cartTotalEl = null;
        this.testIdEl = null;
        this.isCollapsed = false;
        this.isPaused = false;
        this.onPauseToggle = null;
        this.onSendMessage = null;
        this.onDownloadLogs = null;
    }

    create() {
        if (document.getElementById(this.sidebarId)) return;

        if (!document.body) {
            document.addEventListener('DOMContentLoaded', () => this.create());
            return;
        }

        this.injectStyles();
        this.shiftPage(true);

        this.container = document.createElement('div');
        this.container.id = this.sidebarId;
        this.container.style.cssText = `
            position: fixed;
            top: 0;
            right: 0;
            width: ${this.width};
            height: 100vh;
            background: #0f172a;
            color: #f8fafc;
            z-index: 2147483647;
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            font-size: 13px;
            border-left: 1px solid #1e293b;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
            box-shadow: -10px 0 50px rgba(0,0,0,0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            visibility: visible !important;
            opacity: 1 !important;
        `;

        this.container.innerHTML = `
            <!-- Top Controls -->
            <div style="padding: 16px; display: flex; align-items: center; justify-content: space-between; background: #1e293b; border-bottom: 1px solid #334155;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 8px; height: 8px; background: #10b981; border-radius: 50%;"></div>
                    <span style="font-weight: 700; color: #f8fafc; letter-spacing: 0.05em; font-size: 10px; text-transform: uppercase;">QA Agent Active</span>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button id="ag-btn-download" title="Download Session Logs" style="background: #334155; border: 1px solid #475569; color: #94a3b8; padding: 4px 8px; border-radius: 6px; cursor: pointer; font-size: 11px;">💾</button>
                    <button id="ag-btn-pause" style="background: #334155; border: 1px solid #475569; color: white; padding: 4px 12px; border-radius: 6px; cursor: pointer; font-size: 11px;">Pause</button>
                    <button id="ag-btn-collapse" style="background: transparent; border: none; color: #94a3b8; cursor: pointer; font-size: 16px;">×</button>
                </div>
            </div>

            <!-- Metadata Strip -->
            <div style="display: flex; align-items: center; gap: 16px; padding: 10px 20px; background: #0f172a; border-bottom: 1px solid #1e293b; color: #94a3b8; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                <div style="display: flex; gap: 6px;">
                    <span style="color: #64748b;">ID:</span>
                    <span id="ag-test-id" style="color: #f8fafc;">T-PENDING</span>
                </div>
                <div style="width: 1px; height: 10px; background: #334155;"></div>
                <div style="display: flex; gap: 6px;">
                    <span style="color: #64748b;">ITEMS:</span>
                    <span id="ag-cart-count" style="color: #38bdf8;">0</span>
                </div>
                <div style="width: 1px; height: 10px; background: #334155;"></div>
                <div style="display: flex; gap: 6px;">
                    <span style="color: #64748b;">TOTAL:</span>
                    <span id="ag-cart-total" style="color: #10b981;">$0.00</span>
                </div>
            </div>

            <!-- Main Content Area -->
            <div style="flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 24px;">
                
                <!-- Report Header -->
                <div style="border-left: 3px solid #38bdf8; padding-left: 16px; margin-bottom: 4px;">
                    <h2 style="margin: 0; font-size: 16px; font-weight: 700; color: #f8fafc; letter-spacing: -0.01em;">Test Execution Report</h2>
                    <div style="color: #38bdf8; font-size: 11px; font-weight: 700; text-transform: uppercase; margin: 4px 0 12px 0; letter-spacing: 0.05em;">Senior QA Expert Signature</div>
                    <p id="ag-mission-goal" style="margin: 0; color: #94a3b8; font-size: 13px; line-height: 1.6; white-space: pre-line;">Waiting for mission details...</p>
                </div>

                <!-- Progress Header -->
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 4px;">
                    <span style="font-weight: 700; font-size: 11px; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">Show steps</span>
                    <span style="color: #64748b;">▾</span>
                </div>

                <!-- Step Tree -->
                <div id="ag-step-list" style="display: flex; flex-direction: column; gap: 16px;">
                    <!-- Steps injected here -->
                </div>

                <!-- AI Thought Stream -->
                <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; margin-top: 8px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                        <span style="font-weight: 700; font-size: 11px; text-transform: uppercase; color: #38bdf8; letter-spacing: 0.05em;">AI Thought Stream</span>
                        <div style="display: flex; gap: 4px;">
                            <div style="width: 4px; height: 4px; background: #38bdf8; border-radius: 50%; animation: ag-pulse 1s infinite;"></div>
                        </div>
                    </div>
                    <div id="ag-thought-stream" style="display: flex; flex-direction: column; gap: 12px; max-height: 200px; overflow-y: auto;">
                        <!-- Thoughts injected here -->
                    </div>
                </div>

                <!-- Activity Log (Debug Only) -->
                <div id="ag-activity-log" style="display: none;"></div>
            </div>

            <!-- Footer / Chat -->
            <div style="padding: 20px; background: #1e293b; border-top: 1px solid #334155;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; color: #a78bfa; font-size: 11px; font-weight: 600;">
                    <span style="font-size: 14px;">⚡</span>
                    SHARING "SAUCE LABS"
                </div>
                <div style="position: relative;">
                    <input id="ag-chat-input" type="text" placeholder="Type @ to ask about a tab" 
                           style="width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 10px 40px 10px 12px; color: white; font-size: 13px; outline: none;">
                    <div style="position: absolute; right: 12px; top: 10px; display: flex; gap: 8px; color: #64748b;">
                        <span>Fast ▾</span>
                        <span style="font-size: 18px; line-height: 1;">⏹</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.container);
        this.stepList = this.container.querySelector('#ag-step-list');
        this.chatInput = this.container.querySelector('#ag-chat-input');
        this.cartCountEl = this.container.querySelector('#ag-cart-count');
        this.cartTotalEl = this.container.querySelector('#ag-cart-total');
        this.testIdEl = this.container.querySelector('#ag-test-id');
        this.thoughtStream = this.container.querySelector('#ag-thought-stream');

        this.initEventListeners();
        this.injectViewportBorder();
        this.injectTakeoverOverlay();
    }

    initEventListeners() {
        const pauseBtn = this.container.querySelector('#ag-btn-pause');
        pauseBtn.addEventListener('click', () => this.togglePause());

        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && this.onSendMessage) {
                this.onSendMessage(this.chatInput.value);
                this.chatInput.value = '';
            }
        });

        const collapseBtn = this.container.querySelector('#ag-btn-collapse');
        collapseBtn.addEventListener('click', () => this.remove());

        const downloadBtn = this.container.querySelector('#ag-btn-download');
        downloadBtn.addEventListener('click', () => {
            if (this.onDownloadLogs) this.onDownloadLogs();
        });
    }

    setMission(goal) {
        if (!this.container) this.create();
        const welcomeMsg = "Hi, I am Senior QA expert in eCommerce domain..";
        this.container.querySelector('#ag-mission-goal').textContent = `${welcomeMsg}\n\n${goal}`;
    }

    setTestId(id) {
        if (this.testIdEl) {
            this.testIdEl.textContent = id.substring(0, 10).toUpperCase();
        }
    }

    updateIndicators(count, total) {
        if (this.cartCountEl) this.cartCountEl.textContent = count || '-';
        if (this.cartTotalEl) this.cartTotalEl.textContent = total || '-';
    }

    addEntry(status, detail, phase, qaResult) {
        console.log(`[QA-SIDEBAR] LOG: ${status} | ${detail} (${phase || 'INFO'})`);
        // capturing general logs into a hidden container for debugging
        if (this.logContainer) {
            const entry = document.createElement('div');
            const ts = new Date().toLocaleTimeString();
            entry.textContent = `[${ts}] ${phase || 'INFO'} | ${status}: ${detail} ${qaResult ? `[${qaResult}]` : ''}`;
            this.logContainer.appendChild(entry);
        }
    }

    /**
     * Stream a thought/reasoning message to the UI
     * @param {string} text The reasoning text
     * @param {string} type 'reason' | 'discovery' | 'learning'
     */
    addThought(text, type = 'reason') {
        const icons = {
            'reason': '🧠',
            'discovery': '🔍',
            'learning': '💡'
        };
        const colors = {
            'reason': '#38bdf8',
            'discovery': '#a78bfa',
            'learning': '#10b981'
        };

        const thoughtEl = document.createElement('div');
        thoughtEl.style.cssText = `
            font-size: 12px;
            color: #94a3b8;
            line-height: 1.5;
            display: flex;
            gap: 10px;
            padding: 8px;
            background: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            transition: all 0.3s ease;
        `;

        thoughtEl.innerHTML = `
            <span style="font-size: 14px; color: ${colors[type]}">${icons[type]}</span>
            <div style="flex: 1;">${text}</div>
        `;

        if (this.thoughtStream) {
            this.thoughtStream.prepend(thoughtEl);
            // Keep only latest 10 thoughts
            while (this.thoughtStream.children.length > 10) {
                this.thoughtStream.lastChild.remove();
            }
        }
    }

    updateSteps(steps, currentStepIndex, currentInterimState) {
        if (!this.stepList) this.create();
        this.stepList.innerHTML = '';

        steps.forEach((step, index) => {
            const isCompleted = index < currentStepIndex;
            const isActive = index === currentStepIndex;
            const isPending = index > currentStepIndex;

            const stepEl = document.createElement('div');
            stepEl.style.cssText = `
                display: flex;
                gap: 12px;
                opacity: ${isPending ? '0.4' : '1'};
                transition: all 0.3s ease;
            `;

            let iconHtml = '';
            if (isCompleted) iconHtml = '<div style="color: #10b981; font-size: 14px;">✓</div>';
            else if (isActive) iconHtml = '<div style="width: 8px; height: 8px; background: #38bdf8; border-radius: 50%; margin: 4px; box-shadow: 0 0 8px #38bdf8; animation: ag-pulse 1.5s infinite;"></div>';
            else iconHtml = '<div style="width: 8px; height: 8px; border: 1px solid #475569; border-radius: 50%; margin: 4px;"></div>';

            stepEl.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center;">
                    ${iconHtml}
                    ${index < steps.length - 1 ? '<div style="width: 1px; flex: 1; background: #334155; margin-top: 4px;"></div>' : ''}
                </div>
                <div style="flex: 1;">
                    <div style="color: ${isActive ? '#f8fafc' : (isCompleted ? '#94a3b8' : '#64748b')}; font-weight: ${isActive ? '600' : '400'}; font-size: 13px;">
                        ${step.description}
                    </div>
                    ${isActive && currentInterimState ? `
                        <div style="background: #1e293b; border-radius: 6px; padding: 6px 12px; display: inline-flex; align-items: center; gap: 8px; margin-top: 8px; color: #94a3b8; font-size: 11px;">
                            <span style="font-size: 14px;">⌨</span>
                            ${currentInterimState}
                        </div>
                    ` : ''}
                </div>
            `;
            this.stepList.appendChild(stepEl);
        });
    }

    togglePause() {
        this.isPaused = !this.isPaused;
        const pauseBtn = this.container.querySelector('#ag-btn-pause');
        const overlay = document.getElementById('ag-takeover-overlay');
        const border = document.getElementById('ag-viewport-border');

        if (this.isPaused) {
            pauseBtn.textContent = 'Resume';
            pauseBtn.style.background = '#10b981';
            overlay.style.display = 'flex';
            border.style.borderColor = '#f59e0b'; // Amber for manual control
        } else {
            pauseBtn.textContent = 'Pause';
            pauseBtn.style.background = '#334155';
            overlay.style.display = 'none';
            border.style.borderColor = '#38bdf8'; // Blue for AI control
        }

        if (this.onPauseToggle) this.onPauseToggle(this.isPaused);
    }

    injectViewportBorder() {
        if (document.getElementById('ag-viewport-border')) return;
        const border = document.createElement('div');
        border.id = 'ag-viewport-border';
        border.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: ${this.width};
            bottom: 0;
            border: 3px solid #38bdf8;
            pointer-events: none;
            z-index: 2147483646;
            box-shadow: inset 0 0 20px rgba(56, 189, 248, 0.2);
            transition: border-color 0.3s ease;
        `;
        document.body.appendChild(border);
    }

    injectTakeoverOverlay() {
        if (document.getElementById('ag-takeover-overlay')) return;
        const overlay = document.createElement('div');
        overlay.id = 'ag-takeover-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(8px);
            border: 1px solid #f59e0b;
            border-radius: 30px;
            padding: 8px 24px;
            display: none;
            align-items: center;
            gap: 12px;
            z-index: 2147483647;
            color: #f59e0b;
            font-weight: 700;
            font-size: 13px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        `;
        overlay.innerHTML = `
            <span style="font-size: 16px;">⏸</span>
            Manual Override Active
            <button id="ag-btn-resume-top" style="background: #f59e0b; border: none; color: #0f172a; padding: 4px 12px; border-radius: 20px; cursor: pointer; font-size: 11px; font-weight: 800; margin-left: 8px;">Resume AI</button>
        `;
        document.body.appendChild(overlay);
        overlay.querySelector('#ag-btn-resume-top').addEventListener('click', () => this.togglePause());
    }

    remove() {
        if (this.container) {
            this.container.remove();
            document.getElementById('ag-viewport-border')?.remove();
            document.getElementById('ag-takeover-overlay')?.remove();
            this.container = null;
            this.shiftPage(false);
        }
    }

    shiftPage(active) {
        document.body.style.marginRight = active ? this.width : '0';
        document.body.style.transition = 'all 0.3s ease-in-out';
    }

    injectStyles() {
        if (document.getElementById('ag-sidebar-styles')) return;
        const styles = document.createElement('style');
        styles.id = 'ag-sidebar-styles';
        styles.textContent = `
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            @keyframes ag-pulse {
                0% { transform: scale(0.95); opacity: 0.5; }
                50% { transform: scale(1.05); opacity: 1; }
                100% { transform: scale(0.95); opacity: 0.5; }
            }
        `;
        document.head.appendChild(styles);
    }
}
