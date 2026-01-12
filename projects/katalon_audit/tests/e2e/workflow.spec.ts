import { test, expect } from '@playwright/test';
import { HomePage } from '../../pages/HomePage';


test('Autonomous Workflow', async ({ page }) => {
    const homePage = new HomePage(page);
    await homePage.goto('https://katalon.com/');
    await homePage.verifyLoaded();
    await homePage.products_menu.click({ force: true });
});