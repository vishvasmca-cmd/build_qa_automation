import { Page, Locator, expect } from '@playwright/test';

export interface SmartLocatorConfig {
    role?: [string, any];
    text?: string;
    testId?: string;
    label?: string;
    placeholder?: string;
    css?: string;
    xpath?: string;
    iframe?: string;
}

/**
 * BasePage provides the Foundation for all Page Objects, 
 * including Resilient Locators and Agentic Execution.
 */
export class BasePage {
    readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async goto(url: string) {
        await this.page.goto(url);
        await this.dismissPopups();
        await this.page.waitForTimeout(2000); // Let layout settle after popups
    }

    /**
     * Resilient Smart Locator: Chained strategies with .or()
     */
    protected smartLocator(config: SmartLocatorConfig): Locator {
        let root = this.page as any;
        if (config.iframe) {
            root = this.page.frameLocator(config.iframe);
        }

        let locator: Locator | undefined;

        if (config.testId) {
            locator = root.getByTestId(config.testId).filter({ visible: true }).first();
        }

        if (config.role) {
            const [roleName, options] = config.role;
            const l = root.getByRole(roleName as any, options).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }

        if (config.label) {
            const l = root.getByLabel(config.label).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }

        if (config.text) {
             // Use RegExp for flexible text matching (handles spacers, icons, etc)
             const l = root.getByText(new RegExp(config.text, "i")).filter({ visible: true }).first();
             locator = locator ? locator.or(l) : l;
        }

        if (config.css) {
            const l = root.locator(config.css).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }
        if (config.xpath) {
            const l = root.locator(config.xpath).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }

        if (!locator) {
            throw new Error("SmartLocator must have at least one strategy defined.");
        }

        return locator;
    }

    /**
     * Agent Mode: Execute a high-level task using AI Planning.
     * Transitions from "Command Execution" (how) to "Strategic Goal" (what).
     */
    async agentExecute(goal: string) {
        console.log(`

[🤖 AGENT] Planning strategically for goal: "${goal}"`);
        
        // 1. Snapshot the state for the Planner
        const state = {
            url: this.page.url(),
            title: await this.page.title(),
            viewport: this.page.viewportSize(),
        };
        
        console.log(`[🤖 AGENT] Current URL: ${state.url}`);
        
        // 2. Resilience Loop: Handle unpredictable obstacles
        await this.dismissPopups();
        
        // 3. Strategic Execution (Placeholder for live LLM bridge)
        // In a full integration, this would call a local agent API to get the next step.
        // For now, it provides the hook for the Orchestrator to monitor and assist.
        console.log(`[🤖 AGENT] Strategy mapped. Executing interaction...`);
        
        await this.page.waitForLoadState('networkidle');
    }

    /**
     * Internal: Handle generic page obstacles (Overlays, Modals, Cookie Banners)
     */
    protected async dismissPopups() {
        const triggers = [
            'button:has-text("Accept")', 
            'button:has-text("Reject")',
            'button:has-text("Got it")',
            'button:has-text("Agree")',
            '#onetrust-accept-btn-handler',
            '.cookie-accept',
            '[aria-label="Close"]', 
            '.close-button', 
            '#dismiss'
        ];
        for (const selector of triggers) {
            try {
                const el = this.page.locator(selector).first();
                if (await el.isVisible({ timeout: 2000 })) {
                    console.log(`[🤖 AGENT] Clearing obstacle: ${selector}`);
                    await el.click({ force: true });
                }
            } catch (e) {}
        }
    }
}
