from typing import Dict, Any, List
import json
import yaml
from core.lib.locator_translator import LocatorTranslator
from core.dsl.schema import (
    DSLTest, 
    NavigateAction, 
    ClickAction, 
    FillAction, 
    SelectAction, 
    WaitAction,
    ActionType
)

class DSLGenerator:
    """
    Generates DSL YAML from execution traces.
    Acts as the bridge between Agent/Recorder and the DSL Compiler.
    """
    
    def __init__(self):
        self.locator_translator = LocatorTranslator()

    def generate_dsl(self, trace_data: Dict[str, Any], test_name: str = "generated_test") -> DSLTest:
        """
        Convert trace data to DSLTest model.
        """
        steps: List[ActionType] = []
        base_url = trace_data.get('target_url')
        
        trace_steps = trace_data.get('trace', [])
        
        for step in trace_steps:
            action = step.get('action')
            
            if action == 'navigate':
                # Navigate action
                url = step.get('value') or step.get('url')
                steps.append(NavigateAction(url=url))
                
            elif action in ['click', 'fill', 'select']:
                # Interaction actions
                # Use LocatorTranslator to get the best locator string
                # This might return "page.get_by_role(...)" or "page.locator(...)"
                # Our ASTBuilder now supports these raw expressions!
                raw_locator = self.locator_translator.translate(step)
                
                # Strip "page." prefix if it's a simple selector? 
                # No, LocatorTranslator creates robust calls like page.get_by_role
                # We interpret "page." as "Raw Expression" in ASTBuilder.
                # However, cleaner DSL preferred semantic names, but for auto-gen, strict is better.
                
                if action == 'click':
                    steps.append(ClickAction(locator=raw_locator))
                elif action == 'fill':
                    value = step.get('value', '')
                    # Auto-correct fill -> select for dropdowns
                    element_context = step.get('element_context', {})
                    if element_context.get('tag') == 'select':
                        steps.append(SelectAction(locator=raw_locator, value=value))
                    else:
                        steps.append(FillAction(locator=raw_locator, value=value))
                elif action == 'select':
                    value = step.get('value', '')
                    steps.append(SelectAction(locator=raw_locator, value=value))
                    
            elif action == 'wait':
                continue # implicit wait usually
        
        return DSLTest(
            test_name=test_name,
            base_url=base_url,
            steps=steps
        )

    def save_to_yaml(self, dsl_test: DSLTest, output_path: str):
        """Dump DSL to YAML file"""
        # Convert pydantic to dict, excluding defaults
        data = dsl_test.model_dump(exclude_none=True)
        
        # Custom dumper for cleaner YAML? 
        # For now, default safe_dump is fine.
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, sort_keys=False, indent=2)
