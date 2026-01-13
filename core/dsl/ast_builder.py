import ast
from typing import List, Union
from core.dsl.schema import DSLTest, ActionType, LoginAction, NavigateAction, ClickAction, FillAction, AssertAction

class ASTBuilder:
    """Builds Python AST from DSL actions"""

    def __init__(self):
        from core.dsl.locator_inference import LocatorInference
        self.inference = LocatorInference()

    def _build_imports(self) -> List[ast.stmt]:
        """
        from playwright.sync_api import Page, expect
        import re
        """
        playwright_import = ast.ImportFrom(
            module='playwright.sync_api',
            names=[
                ast.alias(name='Page', asname=None),
                ast.alias(name='expect', asname=None)
            ],
            level=0
        )
        re_import = ast.Import(names=[ast.alias(name='re', asname=None)])
        return [playwright_import, re_import]

    def build_module(self, test: DSLTest) -> ast.Module:
        """
        Build complete Python module with imports and test function.
        """
        imports = self._build_imports()
        test_func = self._build_test_function(test)
        
        body = []
        body.extend(imports)
        body.append(test_func)
        
        module = ast.Module(
            body=body,
            type_ignores=[]
        )
        ast.fix_missing_locations(module)
        return module

    def _build_test_function(self, test: DSLTest) -> ast.FunctionDef:
        """def test_name(page: Page): ..."""
        body = []
        
        # Initial navigation if base_url provided
        if test.base_url:
            body.append(self._create_goto(test.base_url))
        
        # Compile usage steps
        for step in test.steps:
             body.extend(self._compile_action(step))

        return ast.FunctionDef(
            name=f"test_{test.test_name}",
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg='page', annotation=ast.Name(id='Page', ctx=ast.Load()))],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=body,
            decorator_list=[],
            returns=None
        )

    def _compile_action(self, action: ActionType) -> List[ast.stmt]:
        """Dispatch to specific builder methods"""
        if isinstance(action, LoginAction):
            return self._build_login(action)
        elif isinstance(action, NavigateAction):
            return [self._create_goto(action.url)]
        elif isinstance(action, ClickAction):
            return self._build_click(action)
        elif isinstance(action, FillAction):
            return self._build_fill(action)
        elif isinstance(action, AssertAction):
            return self._build_assert(action)
        return []

    def _create_goto(self, url: str) -> ast.Expr:
        """page.goto('url', timeout=60000, wait_until='domcontentloaded')"""
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='page', ctx=ast.Load()),
                    attr='goto',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=url)],
                keywords=[
                    ast.keyword(arg='timeout', value=ast.Constant(value=60000)),
                    ast.keyword(arg='wait_until', value=ast.Constant(value='commit'))
                ]
            )
        )

    def _create_locator_call(self, selector: str) -> ast.AST:
        """
        Create locator AST node from string selector.
        Handles both CSS selectors and raw Playwright expressions.
        """
        if selector.startswith('page.') or selector.startswith('self.page.'):
             # It's a full Playwright expression (e.g. page.get_by_role(...))
             # Parse it into an AST node
             try:
                 clean_selector = selector.replace('self.page.', 'page.')
                 # ast.parse returns Module -> [Expr] -> value
                 return ast.parse(clean_selector, mode='eval').body
             except Exception:
                 # Fallback if parsing fails
                 pass
        
        # Default: page.locator("selector")
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='page', ctx=ast.Load()),
                attr='locator',
                ctx=ast.Load()
            ),
            args=[ast.Constant(value=selector)],
            keywords=[]
        )

    def _resolve_locator(self, locator_str: str) -> str:
        """Resolve potential semantic name to locator"""
        if self.inference.is_semantic_name(locator_str):
            return self.inference.infer(locator_str)
        return locator_str

    def _build_fill(self, action: FillAction) -> List[ast.stmt]:
        """page.locator(locator).fill(value)"""
        locator = self._resolve_locator(action.locator)
        return [ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=self._create_locator_call(locator),
                    attr='fill',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=action.value)],
                keywords=[]
            )
        )]

    def _build_click(self, action: ClickAction) -> List[ast.stmt]:
        """page.locator(locator).click()"""
        locator = self._resolve_locator(action.locator)
        return [ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=self._create_locator_call(locator),
                    attr='click',
                    ctx=ast.Load()
                ),
                args=[],
                keywords=[]
            )
        )]

    def _build_login(self, action: LoginAction) -> List[ast.stmt]:
        """Standard login sequence"""
        stmts = []
        
        # Username
        user_sel = action.username_selector or self.inference.infer('username')
        stmts.append(ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=self._create_locator_call(user_sel),
                    attr='fill',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=action.username)],
                keywords=[]
            )
        ))
        
        # Password
        pass_sel = action.password_selector or self.inference.infer('password')
        stmts.append(ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=self._create_locator_call(pass_sel),
                    attr='fill',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=action.password)],
                keywords=[]
            )
        ))
        
        # Submit
        submit_sel = action.submit_selector or self.inference.infer('submit')
        stmts.append(ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=self._create_locator_call(submit_sel),
                    attr='click',
                    ctx=ast.Load()
                ),
                args=[],
                keywords=[]
            )
        ))
        
        return stmts

    def _build_assert(self, action: AssertAction) -> List[ast.stmt]:
        """expect(page)... assertions"""
        if action.type == 'url_contains':
            # expect(page).to_have_url(re.compile(value))
            return [ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id='expect', ctx=ast.Load()),
                            args=[ast.Name(id='page', ctx=ast.Load())],
                            keywords=[]
                        ),
                        attr='to_have_url',
                        ctx=ast.Load()
                    ),
                    args=[ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='re', ctx=ast.Load()),
                            attr='compile',
                            ctx=ast.Load()
                        ),
                        args=[ast.Constant(value=action.value)],
                        keywords=[]
                    )], 
                    keywords=[]
                )
            )]
        elif action.type == 'text_visible':
            # expect(page.locator("body")).to_contain_text(value)
            return [ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id='expect', ctx=ast.Load()),
                            args=[ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id='page', ctx=ast.Load()),
                                    attr='locator',
                                    ctx=ast.Load()
                                ),
                                args=[ast.Constant(value="body")],
                                keywords=[]
                            )],
                            keywords=[]
                        ),
                        attr='to_contain_text',
                        ctx=ast.Load()
                    ),
                    args=[ast.Constant(value=action.value)],
                    keywords=[]
                )
            )]
        elif action.type == 'title_contains':
            # expect(page).to_have_title(re.compile(value))
            return [ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id='expect', ctx=ast.Load()),
                            args=[ast.Name(id='page', ctx=ast.Load())],
                            keywords=[]
                        ),
                        attr='to_have_title',
                        ctx=ast.Load()
                    ),
                    args=[ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='re', ctx=ast.Load()),
                            attr='compile',
                            ctx=ast.Load()
                        ),
                        args=[ast.Constant(value=action.value)],
                        keywords=[]
                    )], 
                    keywords=[]
                )
            )]
        elif action.type == 'element_visible':
            # expect(page.locator(locator)).to_be_visible()
            if not action.locator:
                return []
            return [ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id='expect', ctx=ast.Load()),
                            args=[self._create_locator_call(action.locator)],
                            keywords=[]
                        ),
                        attr='to_be_visible',
                        ctx=ast.Load()
                    ),
                    args=[],
                    keywords=[]
                )
            )]
        return []
