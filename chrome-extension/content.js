// Singleton guard to prevent multiple agent instances
if (window.agAgentLoaded) {
    console.log('[QA-AGENT] Agent already loaded, announcing readiness...');
    chrome.runtime.sendMessage({ type: 'CONTENT_READY' }).catch(() => { });
} else {
    window.agAgentLoaded = true;
    console.log('[QA-AGENT] Content script injected!');

    (async () => {
        try {
            const src = chrome.runtime.getURL('content.module.js');
            await import(src);
            console.log('[QA-AGENT] Content module loaded via dynamic import');
            chrome.runtime.sendMessage({ type: 'CONTENT_READY' });
        } catch (e) {
            console.error('[QA-AGENT] Failed to load content module:', e);
            chrome.runtime.sendMessage({ type: 'MODULE_ERROR', payload: e.toString() });
            window.agAgentLoaded = false; // Allow retry on error
        }
    })();
}
