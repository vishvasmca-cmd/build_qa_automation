/**
 * Gemini AI Client
 * Wrapper for Google's Generative AI JavaScript SDK
 */

export class GeminiClient {
    constructor(apiKey, model = 'gemini-2.0-flash') {
        this.apiKey = apiKey;
        this.model = model;
        console.log(`[Gemini] Initialized with model: ${model}`); // Debug log
        this.baseURL = 'https://generativelanguage.googleapis.com/v1beta';
    }

    async generateContent(prompt, options = {}) {
        const endpoint = `${this.baseURL}/models/${this.model}:generateContent?key=${this.apiKey}`;
        const maxRetries = 5;
        let retryCount = 0;

        const body = {
            contents: [{
                parts: [{
                    text: prompt
                }]
            }],
            generationConfig: {
                temperature: options.temperature || 0.2,
                topK: options.topK || 40,
                topP: options.topP || 0.95,
                maxOutputTokens: options.maxOutputTokens || 8192,
            }
        };

        while (retryCount <= maxRetries) {
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(body)
                });

                if (response.status === 429) {
                    if (retryCount === maxRetries) {
                        throw new Error('Gemini API Error: Resource exhausted after multiple retries.');
                    }
                    // Exponential backoff with jitter: (2^retry * 5s) + random(0-1000ms)
                    const waitTime = (Math.pow(2, retryCount) * 5000) + (Math.random() * 1000);
                    console.warn(`[Gemini] Quota hit (429). Retrying in ${Math.round(waitTime)}ms (Attempt ${retryCount + 1}/${maxRetries})...`);
                    await new Promise(r => setTimeout(r, waitTime));
                    retryCount++;
                    continue;
                }

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(`Gemini API Error: ${error.error?.message || response.statusText}`);
                }

                const data = await response.json();
                const text = data.candidates?.[0]?.content?.parts?.[0]?.text;

                if (!text) {
                    throw new Error('No response from Gemini');
                }

                return text;
            } catch (error) {
                const isQuotaError = error.message.includes('429') || error.message.includes('Resource exhausted');
                if (retryCount === maxRetries || !isQuotaError) {
                    console.error('[Gemini] Error:', error);
                    throw error;
                }

                // For other potential 429s caught in catch block
                const waitTime = (Math.pow(2, retryCount) * 5000) + (Math.random() * 1000);
                console.warn(`[Gemini] Error caught (likely quota). Retrying in ${Math.round(waitTime)}ms...`);
                await new Promise(r => setTimeout(r, waitTime));
                retryCount++;
            }
        }
    }

    extractJSON(text) {
        if (!text) return null;

        // 1. Try to find JSON block between code fences
        let cleaned = text.trim();
        const fenceMatch = cleaned.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
        if (fenceMatch) {
            cleaned = fenceMatch[1];
        }

        try {
            // 2. Direct Parse of cleaned/fenced content
            return JSON.parse(cleaned);
        } catch (error) {
            // 3. Ultra-Robust Extraction: Find first '{' and use stack-based matching
            console.warn('[Gemini] Simple parse failed, attempting stack-based extraction...', error.message);

            const firstBrace = text.indexOf('{');
            if (firstBrace === -1) {
                console.error('[Gemini] No JSON found in response:', text);
                throw new Error('No JSON object found in AI response');
            }

            // Stack-based bracket matcher to find the matching closing brace
            let stack = 0;
            let found = false;
            let lastBrace = -1;

            for (let i = firstBrace; i < text.length; i++) {
                if (text[i] === '{') stack++;
                if (text[i] === '}') stack--;

                if (stack === 0) {
                    lastBrace = i;
                    found = true;
                    break;
                }
            }

            if (found) {
                const jsonStr = text.substring(firstBrace, lastBrace + 1);
                try {
                    return JSON.parse(jsonStr);
                } catch (innerError) {
                    // One last attempt: Strip common issues (like trailing commas) if it's simple
                    const sanitized = jsonStr.replace(/,\s*([\]}])/g, '$1');
                    try {
                        return JSON.parse(sanitized);
                    } catch (finalError) {
                        console.error('[Gemini] All extraction attempts failed. Segment:', jsonStr);
                    }
                }
            }

            console.error('[Gemini] JSON parse error. Raw response:', text);
            throw new Error(`Failed to parse JSON: ${error.message}`);
        }
    }

    async reasonNextStep(goal, currentState, pageContext) {
        const prompt = `
You are an Unstoppable Senior eCommerce SDET. A step in your mission has either failed or you are detecting an "off-track" state. You must find the optimal path to reach the goal.

GOAL: ${goal}
CURRENT URL: ${currentState.url}
PAGE TYPE: ${currentState.pageType} (Logged In: ${currentState.isLoggedIn ? 'YES' : 'NO'})
HISTORY: ${JSON.stringify(currentState.history)}
RECENT FAILURES: ${currentState.recentFailures}
PAGE ELEMENTS:
${JSON.stringify(pageContext.interactiveElements)}

DECISION RULES:
1. ANTI-LOOP: If Logged In is YES or Page Type is "inventory", NEVER suggest "Login". You are already past that.
2. SUCCESS: If you see "THANK YOU FOR YOUR ORDER" or "CHECKOUT: COMPLETE", return {"action": "complete"}.
3. VISION FIRST: Use visual landmarks (headers, buttons, footer) to determine page state. DO NOT predict technical fields like 'username' if you are already on a product page.
4. NO HIDDEN CHECKS: Do not validate tokens, cookies, or session storage. Look for visible proof of success (e.g., "Logout" link present means logged in).
5. RECOVERY: If a button was missing, suggest a logical navigation, search, or click a parent container.
6. UNSTOPPABLE: Do not give up. Even if failures are high, suggest the next most logical exploratory action.

Respond in JSON:
{
  "action": "click|fill|navigate|validate|complete",
  "target": "element description",
  "value": "value if needed",
  "reason": "Explain why this action recovers the mission or reaches the goal"
}

IMPORTANT: Respond ONLY with a valid JSON object. No preamble.
`;

        const response = await this.generateContent(prompt);
        return this.extractJSON(response);
    }

    async generateTestPlan(goal, url, context) {
        const prompt = `
You are a Senior SDET creating a granular e-commerce test plan based strictly on CURRENT PAGE EVIDENCE.

GOAL: ${goal}
TARGET URL: ${url}
PAGE ELEMENTS (DISCOVERED):
${JSON.stringify(context?.interactiveElements || [], null, 2)}

CRITICAL INSTRUCTIONS:
1. DISCOVERY-ONLY: Construct steps based ONLY on the provided PAGE ELEMENTS. Do not guess selectors, IDs, or classes that are not in the list.
2. VISION-FIRST: Prioritize visual UI proof. VALIDATE VISUALS (success messages, icon changes, text updates). 
3. NO TECHNICALS: DO NOT validate hidden technical states (tokens, storage, cookies). If it's not in the PAGE ELEMENTS list, don't try to validate it.
4. BE GRANULAR: Do not skip steps. If the goal is "Add to cart" and you see it, click it. If you need to login first and see login inputs, include those steps.
5. NO PREDICTIONS: If an element is missing, hypothesize the next logical navigation step to find it, but do not pretend the element exists on this page.
6. DATA-DRIVEN: Use specific item names (e.g., "Sauce Labs Backpack") if mentioned in the goal.

Respond in JSON:
{
  "scenarios": [
    {
      "name": "Scenario name",
      "steps": [
        {
          "action": "navigate|click|fill|validate",
          "target": "element description from provided list",
          "value": "value if needed",
          "description": "Granular step description"
        }
      ]
    }
  ]
}

IMPORTANT: Respond ONLY with a valid JSON object. No preamble, no explanation.
`;

        const response = await this.generateContent(prompt);
        return this.extractJSON(response);
    }
}
