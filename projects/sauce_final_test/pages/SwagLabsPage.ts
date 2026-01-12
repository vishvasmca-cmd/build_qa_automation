import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class SwagLabsPage extends BasePage {
    /**
     * This is the login page for Swag Labs, where users can enter their credentials to access the inventory.
     * URL Pattern: https://www.saucedemo.com/
     */

    /** Input field for the username. */
    get username_input(): Locator {
        return this.smartLocator({
            text: 'id=user-name',
            css: 'input[placeholder=\'Username\']',
        });
    }

    /** Input field for the password. */
    get password_input(): Locator {
        return this.smartLocator({
            text: 'id=password',
            css: 'input[placeholder=\'Password\']',
        });
    }

    /** Button to submit the login form. */
    get login_button(): Locator {
        return this.smartLocator({
            role: ['button', { name: 'id=login-button' }],
            css: 'input[value=\'Login\']',
        });
    }

    /** Text indicating accepted usernames */
    get accepted_usernames_are_(): Locator {
        return this.smartLocator({
            text: 'text=Accepted usernames are:',
            text: 'css=div.login_credentials_wrap',
        });
    }

    /** Text indicating password for all users */
    get password_for_all_users_(): Locator {
        return this.smartLocator({
            text: 'text=Password for all users:',
            css: 'div.login_password',
        });
    }

    async verifyLoaded() {
        await expect(this.page).toHaveTitle(/.*SwagLabsPage.*/i);
        // Login button is present
        // Username input field is present
        // Password input field is present
    }
}