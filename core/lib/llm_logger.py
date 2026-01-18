"""
LLM Interaction Logger - Tracks all LLM calls for debugging
"""

import json
import os
from datetime import datetime
from termcolor import colored

class LLMLogger:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.interactions = []
        self.log_file = os.path.join(output_dir, 'llm_interactions.json')
    
    def log_request(self, step, system_prompt, user_prompt, context):
        """Log an LLM request"""
        interaction = {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "type": "request",
            "system_prompt": system_prompt[:200] + "...",  #Truncate for readability
            "user_prompt": user_prompt[:500] + "...",
            "context_summary": {
                "num_elements": len(context.get('elements', [])),
                "last_error": context.get('last_action_error'),
                "loop_warning": context.get('loop_warning'),
                "history_length": len(context.get('history', []))
            }
        }
        
        self.interactions.append(interaction)
        self._save()
        
        # Print to console
        print(colored(f"\n📤 LLM REQUEST (Step {step}):", "cyan", attrs=['bold']))
        print(colored(f"   Elements: {len(context.get('elements', []))}", "grey"))
        print(colored(f"   Last Error: {context.get('last_action_error', 'None')}", "yellow"))
        if context.get('loop_warning'):
            print(colored(f"   ⚠️  Loop Warning: {context.get('loop_warning')[:80]}...", "red"))
    
    def log_response(self, step, raw_response, parsed_decision):
        """Log an LLM response"""
        interaction = {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "type": "response",
            "raw_response": raw_response[:500] + "...",
            "decision": {
                "thought": parsed_decision.get('thought', 'N/A')[:200] if parsed_decision else 'PARSE_ERROR',
                "tool": parsed_decision.get('tool') if parsed_decision else None,
                "arguments": str(parsed_decision.get('arguments', {}))[:200] if parsed_decision else None,
                "expected_outcome": parsed_decision.get('expected_outcome', 'N/A')[:100] if parsed_decision else None
            }
        }
        
        self.interactions.append(interaction)
        self._save()
        
        # Print to console
        if parsed_decision:
            print(colored(f"\n📥 LLM RESPONSE (Step {step}):", "green", attrs=['bold']))
            print(colored(f"   Thought: {parsed_decision.get('thought', 'N/A')[:100]}...", "yellow"))
            print(colored(f"   Tool: {parsed_decision.get('tool', 'N/A')}", "cyan"))
            print(colored(f"   Args: {parsed_decision.get('arguments', {})}\n", "grey"))
        else:
            print(colored(f"\n📥 LLM RESPONSE (Step {step}): ❌ PARSE ERROR", "red", attrs=['bold']))
    
    def _save(self):
        """Save to JSON file"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.interactions, f, indent=2)
    
    def generate_summary(self):
        """Generate a human-readable summary"""
        summary_path = os.path.join(self.output_dir, 'llm_summary.md')
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# LLM Interaction Summary\n\n")
            
            for i in range(0, len(self.interactions), 2):
                if i+1 < len(self.interactions):
                    req = self.interactions[i]
                    resp = self.interactions[i+1]
                    
                    f.write(f"## Step {req['step']}\n\n")
                    f.write(f"**Request ({req['timestamp']}):**\n")
                    f.write(f"- Elements: {req['context_summary']['num_elements']}\n")
                    f.write(f"- Last Error: {req['context_summary']['last_error']}\n")
                    if req['context_summary']['loop_warning']:
                        f.write(f"- ⚠️ Loop Warning: {req['context_summary']['loop_warning']}\n")
                    
                    f.write(f"\n**Response ({resp['timestamp']}):**\n")
                    f.write(f"- Thought: {resp['decision']['thought']}\n")
                    f.write(f"- Tool: `{resp['decision']['tool']}`\n")
                    f.write(f"- Arguments: `{resp['decision']['arguments']}`\n")
                    f.write(f"- Expected: {resp['decision']['expected_outcome']}\n\n")
                    f.write("---\n\n")
        
        print(colored(f"📊 Generated LLM summary: {summary_path}", "cyan"))
