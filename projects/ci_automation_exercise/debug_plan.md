# Debug Plan: Fix Flow Divergence and Hallucinations

## Problem Diagnosis
The `DeepExplorerAgent` is diverging from the actual application flow.
1. **Hallucination:** It suggests actions like "click 'ALL PRODUCTS'" or "search 'Search Product'" which might not correspond to visible/valid elements.
2. **Loops:** It repeatedly suggests "click 'Products'" even after just doing so, likely because it doesn't wait for the page to stabilize or doesn't recognize the transition.
3. **Redundant Mining:** It re-enters mining loops for corrected steps that might not need deep mining if verified locators are provided by the AI planner.

## Proposed Strategy

### 1. Hardened "Next Step" Context
We must ground the AI's "Next Step" suggestions in reality.
- **Action:** Update `_ask_llm_next_step` prompting.
    - Explicitly list *just executed* actions (history).
    - **Constraint:** "Do not suggest {last_action} again unless it failed or is a form input."
    - **Constraint:** "Only suggest elements present in the Visible Elements list."

### 2. State Comparison (Deduping)
The current loop detection `_repeat_ai_counter` is too simple. It counts *sequential* identical suggestions.
- **Action:** Add a hash/signature of the `(url, visible_elements_summary)` to the `suggestion_history`.
- if `current_state_hash == last_state_hash` AND `suggestion == last_suggestion`, then we are definitely spinning. Abort/Break.

### 3. Locator Verification Flow
The user complaint "found one verified locator, then why are you trying couple of times?" suggests the flow doesn't exit cleanly.
- **Action:** In `_explore_scenario` mining loop:
    - If `found_stable_locator` is TRUE, break *immediately*.
    - Ensure `corrective execution` (inline navigation) *clears* the `candidates` list but *preserves* the loop if it needs to re-mine on the NEW page.
    - If inline navigation succeeds, do NOT re-suggest it.

## Implementation Steps

1. **Modify `core/agents/explorer.py`**:
    - Update `_ask_llm_next_step` prompt to include "Action History" and strict prohibitions.
    - Update `_explore_scenario` loop logic to ensure it respects `found_stable_locator` more aggressively.
    - Add `history_tracking` to `ExplorationContext` or passed args.

2. **Verify**:
    - Run the pipeline again.
    - Watch for "Skipping duplicate" messages.
    - Ensure flow is: Home -> Products -> Search (if visible) OR Home -> Products -> wait -> Search.

