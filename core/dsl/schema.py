from typing import List, Optional, Union, Dict, Any, Literal
from pydantic import BaseModel, Field, validator

class BaseAction(BaseModel):
    """Base class for all DSL actions"""
    action: str
    description: Optional[str] = None

class LoginAction(BaseAction):
    """
    High-level login action.
    Abstraction: "Login as X"
    """
    action: Literal["login"] = "login"
    username: str
    password: str
    # Optional because knowledge bank might know the URL
    login_url: Optional[str] = None 
    # Optional selector overrides
    username_selector: Optional[str] = None
    password_selector: Optional[str] = None
    submit_selector: Optional[str] = None
    
    expect_redirect: Optional[str] = None

class NavigateAction(BaseAction):
    """Simple navigation"""
    action: Literal["navigate"] = "navigate"
    url: str

class ClickAction(BaseAction):
    """
    Click an element.
    """
    action: Literal["click"] = "click"
    locator: str
    # Context: Is this opening a new tab?
    expects_new_tab: bool = False
    wait_for: Literal["visible", "attached", "stable"] = "visible"

class FillAction(BaseAction):
    """
    Fill a form field.
    """
    action: Literal["fill"] = "fill"
    locator: str
    value: str
    # Validation: Is this a sensitive field?
    is_secret: bool = False

class SelectAction(BaseAction):
    """Select option from dropdown"""
    action: Literal["select"] = "select"
    locator: str
    value: str # Option value or label

class AssertAction(BaseAction):
    """
    Assertions / Verifications.
    """
    action: Literal["assert"] = "assert"
    type: Literal[
        "url_contains", 
        "text_visible", 
        "element_visible", 
        "title_contains",
        "redirected_to"
    ]
    value: str
    locator: Optional[str] = None # Required for element_visible

class WaitAction(BaseAction):
    """Explicit waits (use sparingly)"""
    action: Literal["wait"]
    type: Literal["time", "selector_visible", "url"]
    value: Union[str, int]

# Union of all possible actions
ActionType = Union[
    LoginAction, 
    NavigateAction, 
    ClickAction, 
    FillAction, 
    SelectAction, 
    AssertAction, 
    WaitAction
]

class DSLStep(BaseModel):
    """A single logical step in the test"""
    step_name: Optional[str] = None
    actions: List[ActionType]

class DSLTest(BaseModel):
    """Complete Test Specification"""
    test_name: str
    base_url: str
    # Metadata
    author: str = "Antigravity"
    version: str = "1.0"
    
    steps: List[ActionType] # Flattened list of actions for now
