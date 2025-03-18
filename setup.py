import os
import subprocess
import sys

# Define project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(PROJECT_ROOT, ".venv")
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")

# Define critical directories
MCP_PATH = os.path.join(PROJECT_ROOT, "backend", "mcp")
VS_CODE_EXTENSION_PATH = os.path.join(PROJECT_ROOT, "frontend", "mcp_code_suggester")
UNIT_TESTS_PATH = os.path.join(PROJECT_ROOT, "scripts", "unit_tests")

def create_virtual_environment():
    """Creates a virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_PATH):
        print("🔧 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", VENV_PATH], check=True)
    else:
        print("✅ Virtual environment already exists.")

def install_requirements():
    """Installs dependencies from requirements.txt."""
    if not os.path.exists(REQUIREMENTS_FILE):
        print("❌ requirements.txt not found. Please create it first.")
        return

    print("📦 Installing dependencies from requirements.txt...")

    pip_path = os.path.join(VENV_PATH, "Scripts" if os.name == "nt" else "bin", "pip")
    subprocess.run([pip_path, "install", "-r", REQUIREMENTS_FILE], check=True)

    # Ensure pytest is installed
    subprocess.run([pip_path, "install", "pytest"], check=True)

    print("✅ Dependencies installed successfully.")

def ensure_directories_exist():
    """Creates missing directories for MCP and VS Code extension."""
    print("📂 Ensuring necessary directories exist...")
    os.makedirs(MCP_PATH, exist_ok=True)
    os.makedirs(VS_CODE_EXTENSION_PATH, exist_ok=True)
    print("✅ Required directories are set up.")

def setup_mcp():
    """Ensures the MCP module is correctly installed."""
    print("⚙️ Setting up MCP module...")
    if not os.path.exists(MCP_PATH):
        print(f"❌ MCP directory missing, creating it: {MCP_PATH}")
        os.makedirs(MCP_PATH, exist_ok=True)

    pip_path = os.path.join(VENV_PATH, "Scripts" if os.name == "nt" else "bin", "pip")
    subprocess.run([pip_path, "install", "-e", MCP_PATH], check=True)

    print("✅ MCP module is set up.")

def setup_vscode_extension():
    """Packages the VS Code extension for installation."""
    print("🖥️ Setting up VS Code extension...")

    if not os.path.exists(VS_CODE_EXTENSION_PATH):
        print(f"❌ VS Code extension directory missing, creating it: {VS_CODE_EXTENSION_PATH}")
        os.makedirs(VS_CODE_EXTENSION_PATH, exist_ok=True)

    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ npm is not installed. Please install Node.js and npm first.")
        return

    os.chdir(VS_CODE_EXTENSION_PATH)
    subprocess.run(["npm", "install"], check=True)
    subprocess.run(["vsce", "package"], check=True)

    print("✅ VS Code extension is packaged. Manually install the .vsix file in VS Code.")

def run_unit_tests():
    """Runs all unit tests to verify installation success."""
    print("🧪 Running unit tests...")

    if not os.path.exists(UNIT_TESTS_PATH):
        print(f"❌ Unit tests directory not found: {UNIT_TESTS_PATH}, creating it.")
        os.makedirs(UNIT_TESTS_PATH, exist_ok=True)

    pytest_path = os.path.join(VENV_PATH, "Scripts" if os.name == "nt" else "bin", "pytest")
    
    # Check if pytest exists before running
    if not os.path.exists(pytest_path):
        print("❌ pytest not found. Ensure it was installed correctly in the virtual environment.")
        return
    
    subprocess.run([pytest_path, UNIT_TESTS_PATH], check=False)

    print("✅ Unit tests completed.")

def main():
    create_virtual_environment()
    install_requirements()
    ensure_directories_exist()
    setup_mcp()
    setup_vscode_extension()
    run_unit_tests()

    print("🎉 Setup complete! To activate your environment:")
    if os.name == "nt":
        print(f"   .venv\\Scripts\\activate")
    else:
        print(f"   source .venv/bin/activate")

if __name__ == "__main__":
    main()
