import argparse
import ast
import sys
from core.dsl.parser import DSLParser
from core.dsl.ast_builder import ASTBuilder

def main():
    parser = argparse.ArgumentParser(description="Antigravity DSL Compiler")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile DSL to Python')
    compile_parser.add_argument('input', help='Input YAML file')
    compile_parser.add_argument('--output', '-o', help='Output Python file')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate DSL schema only')
    validate_parser.add_argument('input', help='Input YAML file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    dsl_parser = DSLParser()
    
    try:
        # Step 1: Parse & Validate
        print(f"📖 Parsing {args.input}...")
        test_model = dsl_parser.parse_file(args.input)
        print(f"✅ Schema Validation Passed: {test_model.test_name}")
        
        if args.command == 'validate':
            sys.exit(0)
            
        # Step 2: Generate AST
        print("🏗️  Generating AST...")
        builder = ASTBuilder()
        module_ast = builder.build_module(test_model)
        
        # Step 3: Unparse to Source Code
        print("📝 Generating Python Code...")
        # ast.unparse requires Python 3.9+
        if sys.version_info < (3, 9):
            print("❌ Error: AST code generation requires Python 3.9+")
            sys.exit(1)
            
        source_code = ast.unparse(module_ast)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(source_code)
            print(f"💾 Saved to {args.output}")
        else:
            print("\n" + "="*40 + " GENERATED CODE " + "="*40)
            print(source_code)
            print("="*96 + "\n")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
