import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
    /**
     * The Katalon homepage aims to introduce users to the Katalon platform.
     * URL Pattern: https://katalon.com/
     */

    /** Dropdown menu for Katalon products. */
    get products_menu(): Locator {
        return this.smartLocator({
            role: ['button', { name: 'Products', exact: false }],
            text: 'Products',
        });
    }

    /** Dropdown menu for Katalon solutions. */
    get solutions_menu(): Locator {
        return this.smartLocator({
            role: ['button', { name: 'Solutions', exact: false }],
            text: 'Solutions',
        });
    }

    async verifyLoaded() {
        await expect(this.page).toHaveTitle(/.*HomePage.*/i);
    }
}