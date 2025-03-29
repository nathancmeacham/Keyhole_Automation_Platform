import os
import sys

# Define folders to exclude from crawling
EXCLUDED_FOLDERS = ['.expo', '.vscode', 'android', 'assets', 'node_modules']

def should_crawl_folder(folder_path):
    """Check if the folder should be crawled."""
    folder_name = os.path.basename(folder_path)
    return folder_name not in EXCLUDED_FOLDERS

def crawl_directory(directory):
    """Recursively crawl the directory and print file contents."""
    for root, dirs, files in os.walk(directory):
        # Remove excluded folders from the list of directories to crawl
        dirs[:] = [d for d in dirs if should_crawl_folder(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f"Contents of {file_path}:")
                    print(f.read())
                    print("-" * 40)
            except (UnicodeDecodeError, PermissionError):
                # Skip files that cannot be read (e.g., binary files or permission issues)
                print(f"Skipping {file_path} (unreadable or binary file)")

# Set sys.stdout encoding to utf-8 to handle Unicode characters
sys.stdout.reconfigure(encoding='utf-8')

# Start crawling from the specified root directory
root_directory = r'C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform\frontend'
crawl_directory(root_directory)