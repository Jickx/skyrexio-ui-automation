INVALID_PASSWORD_CASES = [
    ("short_password", "123"),
    ("long_password", "a" * 129),
    ("special_chars_only", "!@#$%^&*()_+-=[]{}|;':\",.<>/?"),
    ("spaces_only", "     "),
]
