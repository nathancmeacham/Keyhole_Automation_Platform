import os
import sys

# Set up paths dynamically
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")

# Ensure backend directory is in Python path
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

# Initialize memory system before running anything
from memory_manager import init_memory_collection

print("✅ Project initialized. All modules are now importable.")
