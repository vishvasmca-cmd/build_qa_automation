/**
 * Ollama Local AI Client
 * Connects to local Ollama instance (default: http://localhost:11434)
 */

export class OllamaClient {
    constructor(model = 'llava') {
        this.model = model; // 'llava' is best for vision, 'llama3' for text
        this.baseURL = 'http://localhost:11434/api/generate';
        console.log(`[Ollama] Initialized with model: ${model}`);
    }

    async generateContent(prompt, images = []) {
        // Ollama expects explicit 'images' array in base64
        const body = {
            model: this.model,
            prompt: prompt,
            original_prompt: prompt, // Keep track for debugging
            stream: false,
            options: {
                temperature: 0.2, // Low temp for JSON stability
                num_ctx: 4096     // Context window
            }
        };

        if (images && images.length > 0) {
            body.images = images; // Array of base64 strings
        }

        try {
            const response = await fetch(this.baseURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                throw new Error(`Ollama Error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            return data.response;

        } catch (error) {
            console.error('[Ollama] Request failed:', error);
            // Friendly error for the UI
            if (error.message.includes('Failed to fetch')) {
                throw new Error('Connection failed. Is Ollama running? (run `ollama serve`)');
            }
            throw error;
        }
    }

    extractJSON(text) {
        // Reuse the logic from GeminiClient, or a simplified version
        if (!text) return null;
        let cleaned = text.trim();

        // Remove markdown fences
        const fenceMatch = cleaned.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
        if (fenceMatch) cleaned = fenceMatch[1];

        // Locate first '{'
        const firstBrace = cleaned.indexOf('{');
        const lastBrace = cleaned.lastIndexOf('}');

        if (firstBrace !== -1 && lastBrace !== -1) {
            cleaned = cleaned.substring(firstBrace, lastBrace + 1);
        }

        try {
            return JSON.parse(cleaned);
        } catch (e) {
            console.warn('[Ollama] JSON parse failed:', e);
            console.log('Raw output:', text);
            return null;
        }
    }
}
