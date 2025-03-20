# Keyhole_Automation_Platform\__init__.py
import os
import sys

# Set up paths dynamically
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")
MCP_PATH = os.path.join(PROJECT_ROOT, "backend", "mcp")
SRC_PATH = os.path.join(PROJECT_ROOT, "backend", "mcp", "src")

# Ensure backend paths are in Python path
for path in [BACKEND_PATH, MCP_PATH, SRC_PATH]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Initialize memory system before running anything
try:
    from memory_manager import init_memory_collection
    init_memory_collection()
except ImportError:
    print("⚠️ Warning: memory_manager module not found. Skipping memory initialization.")

print("✅ Project initialized. All modules are now importable.")
