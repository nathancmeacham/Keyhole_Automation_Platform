ALLOWED_FILES = set([
    "example.py",
    "utils.py",
    # Add permitted filenames here
])

def is_file_allowed(filename: str) -> bool:
    return filename in ALLOWED_FILES
