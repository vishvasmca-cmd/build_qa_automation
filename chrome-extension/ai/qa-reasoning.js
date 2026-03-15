/**
 * QA Reasoning Engine
 * High-level test strategy and scenario planning
 */

export class QAReasoning {
    constructor(geminiClient) {
        this.gemini = geminiClient;
    }

    async generateTestPlan(goal, url, context) {
        console.log('[QA-REASONING] Generating discovery-driven test plan:', goal);

        // Use Gemini to create comprehensive test scenarios based on actual page context
        const testPlan = await this.gemini.generateTestPlan(goal, url, context);

        if (!testPlan || !testPlan.scenarios) {
            console.error('[QA-REASONING] Failed to generate valid test plan scenarios');
            return testPlan || { scenarios: [] };
        }

        // Enhance with domain knowledge
        testPlan.scenarios = this.enhanceWithDomainExpertise(testPlan.scenarios, url);

        return testPlan;
    }

    enhanceWithDomainExpertise(scenarios, url) {
        // Add standard e-commerce validations to each scenario
        const enhancedScenarios = scenarios.map(scenario => {
            const enhancedSteps = [...scenario.steps];

            // Auto-inject price validation after cart operations
            if (scenario.steps.some(s => s.action === 'click' && s.target?.includes('cart'))) {
                enhancedSteps.push({
                    action: 'validate',
                    target: 'cart_total',
                    description: 'Verifying cart total calculation accuracy',
                    validation_type: 'price_integrity'
                });
            }

            return {
                ...scenario,
                steps: enhancedSteps
            };
        });

        // Add domain-specific scenarios based on site detection
        if (url.includes('saucedemo')) {
            enhancedScenarios.push(this.createLockedUserScenario());
            enhancedScenarios.push(this.createCartPersistenceScenario());
        }

        return enhancedScenarios;
    }

    createLockedUserScenario() {
        return {
            name: 'Unauthorized Access Prevention',
            description: 'Verify locked_out_user cannot access the system',
            steps: [
                {
                    action: 'navigate',
                    target: 'https://www.saucedemo.com',
                    description: 'Navigating to login page'
                },
                {
                    action: 'fill',
                    target: 'username',
                    value: 'locked_out_user',
                    description: 'Entering locked username'
                },
                {
                    action: 'fill',
                    target: 'password',
                    value: 'secret_sauce',
                    description: 'Entering password'
                },
                {
                    action: 'click',
                    target: 'login',
                    description: 'Attempting unauthorized login'
                },
                {
                    action: 'validate',
                    target: 'error_message',
                    value: 'Sorry, this user has been locked out',
                    description: 'Confirming access denial message'
                }
            ],
            expected_outcome: 'User should be blocked with clear error message'
        };
    }

    createCartPersistenceScenario() {
        return {
            name: 'Shopping Cart Persistence',
            description: 'Verify cart items persist across navigation',
            steps: [
                {
                    action: 'click',
                    target: 'add_to_cart',
                    description: 'Adding product to cart'
                },
                {
                    action: 'validate',
                    target: 'cart_count',
                    value: '1',
                    description: 'Verifying cart badge shows 1 item'
                },
                {
                    action: 'navigate',
                    target: 'cart',
                    description: 'Navigating to different page'
                },
                {
                    action: 'navigate',
                    target: 'inventory',
                    description: 'Returning to product list'
                },
                {
                    action: 'validate',
                    target: 'cart_count',
                    value: '1',
                    description: 'Confirming cart persistence (still shows 1)'
                }
            ],
            expected_outcome: 'Cart count should remain at 1 after navigation'
        };
    }

    async reasonNextStep(goal, currentState, pageContext) {
        console.log('[QA-REASONING] Determining next step...');

        // Use Gemini to reason about the next action
        const nextAction = await this.gemini.reasonNextStep(goal, currentState, pageContext);

        // Apply safety checks
        if (nextAction.action === 'fill' && nextAction.target?.includes('credit')) {
            console.warn('[QA-REASONING] Blocking sensitive data input');
            nextAction.value = 'TEST_CARD_4111111111111111';
        }

        return nextAction;
    }
}
