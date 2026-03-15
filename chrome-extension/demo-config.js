/**
 * Expert Demo Scenarios
 * Pre-configured test cases for specific e-commerce platforms
 */

export const DEMO_SCENARIOS = {
    // SAUCEDEMO.COM (Standard Reference)
    'saucedemo.com': [
        {
            name: '✅ Happy Path Checkout',
            goal: 'Login as standard_user, add backpack & bike light to cart, and complete full checkout flow.',
            description: 'Verifies the core purchase funnel from login to order confirmation.'
        },
        {
            name: '🚫 Locked Out User',
            goal: 'Attempt login with username "locked_out_user" and password "secret_sauce". Verify error message contains "locked out".',
            description: 'Security test to ensure banned users are correctly blocked.'
        },
        {
            name: '💰 High Value Cart Audit',
            goal: 'Login, sort by Price (high to low), add the 2 most expensive items, and verify cart total matches sum of prices.',
            description: 'Complex financial validation combining sorting, selection, and math.'
        },
        {
            name: '🛒 Cart Persistence',
            goal: 'Login, add 1 item to cart. Logout. Login again. Verify cart is empty (or persistent depending on site logic).',
            description: 'Tests session state management and cart retention policies.'
        }
    ],

    // AUTOMATIONEXERCISE.COM (Complex Real-World)
    'automationexercise.com': [
        {
            name: '👗 Contact Us Form',
            goal: 'Navigate to Contact Us, fill name, email, subject, and message. Upload a file if possible. Submit and verify success message.',
            description: 'Tests form submission, file handling, and feedback systems.'
        },
        {
            name: '🔎 Product Search',
            goal: 'Navigate to Products. Search for "Jeans". Verify all displayed products contain "Jeans" in their title.',
            description: 'Validates search functionality and result relevance.'
        },
        {
            name: '📦 Subscription Check',
            goal: 'Scroll to footer. Enter email in subscription box. Click arrow. Verify success text "You have been successfully subscribed!"',
            description: 'Tests footer functionality and AJAX form submission.'
        }
    ],

    // GENERIC E-COMMERCE (Fallback)
    'generic': [
        {
            name: '🕵️ smoke Test: Add to Cart',
            goal: 'Find the first product on the page. Add it to cart. Verify cart count increases by 1.',
            description: 'Universal smoke test for any shop.'
        },
        {
            name: '📝 Guest Checkout Flow',
            goal: 'Add a product to cart. Proceed to checkout. Select "Guest Checkout" if available. Fill required shipping info.',
            description: 'Tests conversion flow without account creation.'
        },
        {
            name: '🔍 Search & Filter',
            goal: 'Search for a common item (e.g., "shirt"). Apply a price filter if available. Verify results update.',
            description: 'Tests discovery and filtering mechanisms.'
        }
    ]
};

export function getScenariosForUrl(url) {
    const hostname = new URL(url).hostname.replace('www.', '');
    return DEMO_SCENARIOS[hostname] || DEMO_SCENARIOS['generic'];
}
