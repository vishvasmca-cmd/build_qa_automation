from enum import Enum

class ErrorType(Enum):
    ELEMENT_NOT_FOUND = "element_not_found"
    ELEMENT_NOT_VISIBLE = "element_not_visible"
    ELEMENT_NOT_ENABLED = "element_not_enabled"
    ELEMENT_BLOCKED = "element_blocked_by_overlay"
    TIMEOUT = "timeout"
    NETWORK_ERROR = "network_error"
    ASSERTION_FAILED = "assertion_failed"
    UNKNOWN = "unknown"

class ErrorHandler:
    @staticmethod
    def categorize(error: Exception) -> ErrorType:
        err_msg = str(error).lower()
        
        if "timeout" in err_msg:
            if "waiting for locator" in err_msg or "not found" in err_msg:
                return ErrorType.ELEMENT_NOT_FOUND
            return ErrorType.TIMEOUT
            
        if "not visible" in err_msg or "hidden" in err_msg:
            return ErrorType.ELEMENT_NOT_VISIBLE
            
        if "not enabled" in err_msg or "disabled" in err_msg:
            return ErrorType.ELEMENT_NOT_ENABLED
            
        if "intercepted" in err_msg or "overlay" in err_msg:
            return ErrorType.ELEMENT_BLOCKED
            
        if "expect" in err_msg or "assertion" in err_msg:
            return ErrorType.ASSERTION_FAILED
            
        return ErrorType.UNKNOWN

    @staticmethod
    def get_healing_strategies(error_type: ErrorType) -> list:
        strategies = {
            ErrorType.ELEMENT_NOT_FOUND: ["wait_and_retry", "scroll_page", "ai_heal"],
            ErrorType.ELEMENT_NOT_VISIBLE: ["scroll_into_view", "dismiss_overlay", "wait_for_visible"],
            ErrorType.ELEMENT_BLOCKED: ["dismiss_overlay", "press_escape", "wait_for_idle"],
            ErrorType.TIMEOUT: ["increase_timeout", "reload_page"],
            ErrorType.ASSERTION_FAILED: ["log_and_fail"]
        }
        return strategies.get(error_type, ["retry"])
