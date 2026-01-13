import yaml
import os
from typing import Dict, Any, Union
from pydantic import ValidationError
from core.dsl.schema import DSLTest, ActionType

class DSLParser:
    """Parses YAML test specifications into validated DSL objects"""
    
    def parse_file(self, file_path: str) -> DSLTest:
        """
        Load and validate a YAML DSL file.
        
        Args:
            file_path: Path to .yaml file
            
        Returns:
            Validated DSLTest object
            
        Raises:
            ValueError: If file not found or invalid YAML
            ValidationError: If schema validation fails
        """
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML syntax in {file_path}: {e}")
            
        if not data:
            raise ValueError("Empty DSL file")

        # Validate against schema
        try:
            # Polymorphic parsing: Pydantic will try to match each item in 'steps'
            # to one of the ActionType union members based on the 'action' field.
            return DSLTest(**data)
        except ValidationError as e:
            # Format error nicely
            error_msg = self._format_validation_error(e)
            raise ValidationError(error_msg, model=DSLTest) 

    def _format_validation_error(self, e: ValidationError) -> str:
        """Create human-readable error message from Pydantic error"""
        errors = e.errors()
        messages = []
        for err in errors:
            loc = " -> ".join(str(l) for l in err['loc'])
            msg = err['msg']
            messages.append(f"[{loc}]: {msg}")
        return "\n".join(messages)

if __name__ == '__main__':
    # Quick test
    import sys
    if len(sys.argv) > 1:
        parser = DSLParser()
        try:
            test = parser.parse_file(sys.argv[1])
            print(f"✅ Successfully parsed test: {test.test_name}")
            for i, step in enumerate(test.steps):
                print(f"  Step {i+1}: {step.action} -> {step}")
        except Exception as e:
            print(f"❌ Failed to parse: {e}")
