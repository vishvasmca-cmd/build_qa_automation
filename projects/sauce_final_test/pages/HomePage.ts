import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
    /**
     * This is the login page for the Swag Labs e-commerce website. Users can enter their username and password to access the product catalog.
     * URL Pattern: https://www.saucedemo.com/
     */

    /** Input field for the username. */
    get username_input(): Locator {
        return this.smartLocator({
            css: '[data-test=\'username\']',
            css: 'input#user-name',
        });
    }

    /** Input field for the password. */
    get password_input(): Locator {
        return this.smartLocator({
            css: '[data-test=\'password\']',
            css: 'input#password',
        });
    }

    /** Button to submit the login form. */
    get login_button(): Locator {
        return this.smartLocator({
            role: ['button', { name: '[data-test='login-button']' }],
            role: ['button', { name: 'input#login-button' }],
        });
    }

    /** Text displaying accepted usernames */
    get accepted_usernames_are_(): Locator {
        return this.smartLocator({
            text: 'text=Accepted usernames are:',
            text: 'div.login_credentials_wrap',
        });
    }

    /** Text displaying password for all users */
    get password_for_all_users_(): Locator {
        return this.smartLocator({
            text: 'text=Password for all users:',
            text: 'div.login_password',
        });
    }

    async verifyLoaded() {
        await expect(this.page).toHaveTitle(/.*HomePage.*/i);
        // Login button is present
        // Username input field is present
        // Password input field is present
    }
}