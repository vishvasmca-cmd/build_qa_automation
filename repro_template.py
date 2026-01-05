from core.template_engine import TestTemplateEngine

engine = TestTemplateEngine()
result = engine.generate_test("test_proj", "http://example.com", "    pass")
print("---START---")
print(result)
print("---END---")
