"""Shared test helper functions."""


def validate_cpp_braces(code):
    """Validate C/C++ code has balanced braces with proper nesting.

    Checks that braces are balanced AND that nesting depth never goes
    negative (which would indicate closing before opening).
    """
    depth = 0
    for ch in code:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and code.count("{") > 0
