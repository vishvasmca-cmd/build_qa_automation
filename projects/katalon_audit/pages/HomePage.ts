import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
    /**
     * The Katalon homepage aims to introduce users to the Katalon platform and its various testing solutions, encouraging them to explore the products and download the studio.
     * URL Pattern: https://katalon.com/
     */

    /** Link to return to the homepage. */
    get katalon_logo(): Locator {
        return this.page.locator('//a[@aria-label='Katalon']').or(this.page.locator('css=a[aria-label='Katalon']'));
    }

    /** Dropdown menu for Katalon products. */
    get products_menu(): Locator {
        return this.page.locator('//button[contains(text(),'Products')]').or(this.page.getByText('css=button:contains('Products')'));
    }

    /** Dropdown menu for Katalon solutions. */
    get solutions_menu(): Locator {
        return this.page.locator('//button[contains(text(),'Solutions')]').or(this.page.getByText('css=button:contains('Solutions')'));
    }

    /** Link to the Katalon pricing page. */
    get katalon_pricing(): Locator {
        return this.page.locator('//a[contains(text(),'Katalon Pricing')]').or(this.page.getByText('css=a:contains('Katalon Pricing')'));
    }

    /** Dropdown menu for Katalon resources. */
    get resources_menu(): Locator {
        return this.page.locator('//button[contains(text(),'Resources')]').or(this.page.getByText('css=button:contains('Resources')'));
    }

    /** Button to view a demo of Katalon. */
    get view_demo_button(): Locator {
        return this.page.locator('//a[contains(text(),'View Demo')]').or(this.page.getByText('css=a:contains('View Demo')'));
    }

    /** Button to download Katalon Studio. */
    get download_studio_button(): Locator {
        return this.page.locator('//a[contains(text(),'Download Studio')]').or(this.page.getByText('css=a:contains('Download Studio')'));
    }

    /** Button to learn more about Katalon Studio. */
    get learn_more_button(): Locator {
        return this.page.locator('//a[contains(text(),'Learn more')]').or(this.page.getByText('css=a:contains('Learn more')'));
    }

    /** Button to explore Katalon Studio integrations. */
    get integrations_button(): Locator {
        return this.page.locator('//a[contains(text(),'Integrations')]').or(this.page.getByText('css=a:contains('Integrations')'));
    }

    /** Button to accept all cookies. */
    get accept_all_cookies(): Locator {
        return this.page.locator('//button[contains(text(),'Accept All Cookies')]').or(this.page.getByText('css=button:contains('Accept All Cookies')'));
    }

    async verifyLoaded() {
        await expect(this.page).toHaveTitle(/.*Katalon.*/i);
        // Verify the presence of the 'Katalon Studio' header
        // Verify the presence of the 'Download Studio' button
        // Verify the presence of the 'Learn more' button
    }
}