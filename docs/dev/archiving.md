# 🔒 Archiving Code and Tests

In the Keyhole Automation Platform, deprecated code and tests are moved to the `archive/` directory to preserve past work while keeping the active codebase clean and efficient.

---

## 📁 Archive Folder Structure

Archived files mirror their original directory structure, like so:

**Original location:**
C:. +---backend | qdrant.py | ---tests ---backend test_qdrant.py


**Archived version:**
C:. ---archive +---backend | qdrant.py ➜ renamed to qdrant_raw.py | ---tests ---backend test_qdrant.py


---

## 🏷️ File Annotations

Archived files include clear headers to indicate their status and usage:

### 🔹 Archived Module Example
```python
# Keyhole_Automation_Platform\archive\backend\qdrant_raw.py
# 🔒 ARCHIVED MODULE - NOT RUN IN PRODUCTION
# This file was deprecated and moved from backend/qdrant.py.
# Retained for reference or future reuse.
