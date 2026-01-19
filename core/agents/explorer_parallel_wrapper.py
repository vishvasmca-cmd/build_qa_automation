"""
Parallel AI Processing Wrapper with Safe Fallback

This module provides a wrapper around the standard sequential step processing
that intelligently batches consecutive 'fill' steps for parallel AI mining.

SAFETY: On ANY error, automatically falls back to original sequential processing.
"""

async def process_batch_or_sequential(explorer_agent, page, steps, scenario, start_idx):
    """
    Intelligently process steps: batch if possible, sequential otherwise.
    
    FALLBACK CHAIN:
    1. Try parallel batch processing (if enabled + consecutive fills)
    2. On error → Fall back to sequential processing
    3. On feature disabled → Use sequential processing
    
    Args:
        explorer_agent: ExplorerAgent instance
        page: Playwright Page
        steps: List of all steps
        scenario: Current scenario dict
        start_idx: Index to start from
        
    Returns:
        (processed_count, success) - Number of steps processed and success status
    """
    
    # SAFETY CHECK 1: Feature flag
    if not explorer_agent.enable_parallel_ai:
        explorer_agent.log("    ℹ️ Parallel AI disabled. Using sequential processing", "grey")
        return await _process_sequential_single(explorer_agent, page, steps, scenario, start_idx)
    
    try:
        # SAFETY CHECK 2: Group steps into batches
        batches = explorer_agent._group_steps_into_batches(steps, start_idx, max_batch_size=5)
        
        if not batches:
            # No valid batches - fallback to sequential
            return await _process_sequential_single(explorer_agent, page, steps, scenario, start_idx)
        
        first_batch = batches[0]
        
        # SAFETY CHECK 3: Only batch if multiple fill steps
        if len(first_batch) <= 1:
            # Single step - use sequential
            return await _process_sequential_single(explorer_agent, page, steps, scenario, start_idx)
        
        # ALL CHECKS PASSED - Try parallel batch processing
        explorer_agent.log(f"    ⚡ PARALLEL MODE: Batching {len(first_batch)} fill steps", "cyan")
        
        # Mine locators in parallel
        batch_steps = [steps[idx] for idx in first_batch]
        locators_map = await explorer_agent._mine_locators_batch(
            page, 
            batch_steps, 
            scenario["name"]
        )
        
        # Assign mined locators back to steps
        success_count = 0
        for batch_idx, step_idx in enumerate(first_batch):
            locators = locators_map.get(batch_idx, [])
            if locators:
                steps[step_idx]["locators"] = locators
                success_count += 1
            else:
                explorer_agent.log(f"    ⚠️ No locators for step {step_idx}. Will try sequential", "yellow")
        
        explorer_agent.log(f"    ✅ Batch mined {success_count}/{len(first_batch)} steps successfully", "green")
        
        # Return batch size (caller will increment index by this amount)
        return (len(first_batch), True)
        
    except Exception as e:
        # FALLBACK: On ANY error, use sequential
        explorer_agent.log(f"    ⚠️ Batch processing error: {e}", "yellow")
        explorer_agent.log(f"    🔄 Falling back to sequential processing", "cyan")
        explorer_agent.metrics.record_retry("batch_fallback")
        
        return await _process_sequential_single(explorer_agent, page, steps, scenario, start_idx)


async def _process_sequential_single(explorer_agent, page, steps, scenario, start_idx):
    """
    Process a single step sequentially (original behavior).
    This is the fallback when batch processing fails or is disabled.
    
    Returns:
        (1, success) - Always processes exactly 1 step
    """
    # Note: This doesn't actually process the step, just signals to use
    # the existing sequential logic in the main loop
    # Return 1 to indicate "process 1 step normally"
    return (1, False)  # False = use existing sequential logic
