# 📌 Keyhole Automation Platform - Project Setup Guide

## 🚀 Overview
This document serves as a **comprehensive setup guide** for the **Keyhole Automation Platform**. It documents the major steps taken during the initial setup and deployment, ensuring that new developers and maintainers can quickly onboard and configure the system.

---

## 📂 Repository Structure

```
Keyhole_Automation_Platform/
├── backend/               # FastAPI & LangGraph backend
│   ├── main.py               # Core backend service
│   ├── tools.py              # Dynamic tool management
│   ├── embeddings.py         # Document embeddings & retrieval
│   ├── qdrant.py             # Vector DB integration
│   ├── langgraph.py          # LangGraph orchestration logic
│   ├── security.py           # Security & governance policies
│   ├── vonage_integration.py # Vonage API integration
│   ├── hubspot_integration.py# HubSpot API integration
│   ├── whatsapp_integration.py # WhatsApp API integration
│   ├── gmail_integration.py  # Gmail API integration
│   ├── hostgator_integration.py # HostGator API integration
│   ├── oracle_apex.py        # Oracle APEX integration
│   ├── mcp/                  # Master Control Program (MCP) integration
│   └── mcp_code_suggester/   # VS Code extension backend
│
├── frontend/              # VS Code integration & UI
│   ├── src/
│   ├── package.json          # VS Code extension metadata
│   └── extension.ts          # VS Code interactions
│
├── docs/                  # Documentation, logs & setup guides
│   ├── INIT.md               # Initialization instructions
│   ├── CHANGELOG.md          # Development updates
│   ├── README.md             # Project overview (this file)
│   ├── PROJECT_SETUP.md      # This document
│   └── mkdocs.yml            # MkDocs configuration
│
├── infrastructure/        # Infrastructure & CI/CD automation
│   ├── docker/               # Container configurations
│   ├── kubernetes/           # Kubernetes deployment configs
│   ├── ci_cd/                # GitHub Actions workflows
│   └── workflows/            # Automated workflows (e.g., documentation deployment)
│
└── scripts/               # Utility scripts & automation
    ├── initialize_chat.py    # Context loader for new sessions
    ├── update_changelog.py   # Automated changelog updater
    ├── unit_tests/           # Directory for unit tests
        ├── test_main.py      # Unit tests for main.py
        ├── test_tools.py     # Unit tests for tools.py
        ├── ...
```

---

## 🛠️ Initial Setup & Configuration

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/nathancmeacham/Keyhole_Automation_Platform.git
cd Keyhole_Automation_Platform
```

### 2️⃣ **Create & Activate a Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Initialize MCP & VS Code Extensions**
```bash
cd backend/mcp_code_suggester
vsce package
```
Then, install the `.vsix` file manually in VS Code.

### 5️⃣ **Run the Backend**
```bash
cd backend
uvicorn main:app --reload
```

---

## 📄 Documentation & MkDocs Setup

### ✅ **MkDocs Installation & Preview**
Ensure MkDocs is installed:
```bash
pip install mkdocs mkdocs-material mkdocs-autorefs mkdocs-mermaid2-plugin
```
Run a local server to preview:
```bash
mkdocs serve
```

### 🚀 **Deploy Documentation to GitHub Pages**
The documentation is deployed using GitHub Actions. It runs automatically when changes are pushed to the repository.

To manually deploy:
```bash
mkdocs gh-deploy --force
```

---

## 🧪 Running Tests
```bash
pytest scripts/unit_tests/
```

---

## 🎯 Additional Configurations
- **`.env` File:** Store API keys and secrets in `.env`
- **`.gitignore` Includes:** `.venv/`, `*.log`, `.env`, `__pycache__/`, `*.vsix`

---

## ✅ Next Steps
- Test integrations with **Oracle APEX, Vonage, HubSpot, WhatsApp, Gmail, and HostGator**
- Expand **MCP tool management**
- Document all API endpoints in MkDocs

---

📌 *This document will be updated as new features are added.*

