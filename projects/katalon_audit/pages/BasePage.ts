import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
    protected page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    /**
     * Navigation with stability guard.
     */
    async goto(url: string) {
        await this.page.goto(url, { waitUntil: 'domcontentloaded' });
        await this.waitStable();
    }

    /**
     * Safe click that waits for visibility and handles potential overlays.
     */
    async clickSafe(locator: Locator) {
        await locator.waitFor({ state: 'visible', timeout: 10000 });
        await locator.click();
    }

    /**
     * Wait for network idle and animations to settle.
     */
    async waitStable() {
        try {
            await this.page.waitForLoadState('networkidle', { timeout: 5000 });
        } catch (e) {
            // Network idle might time out on tracky sites, proceed anyway
        }
        await this.page.waitForTimeout(500); // Animation buffer
    }
}
