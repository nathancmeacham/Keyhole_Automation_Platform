```
C:/Users/natha/Py_Coding_Projects/Keyhole_Automation_Platform/docs/internal/system_context.md
```

---

# 🧠 System Context: Keyhole Automation Platform

## 🔧 Project Structure Overview

```
Keyhole_Automation_Platform/
│
├── backend/
│   └── mcp/
│       ├── routes/            # FastAPI route files (auth, agent, dashboard)
│       ├── dependencies/      # JWT/role validation, auth dependencies
│       ├── memory/            # MemoryManager + Qdrant integration
│       ├── utils/             # email_utils, auth_utils, jwt_utils
│       ├── server.py          # Main FastAPI app entrypoint
│
├── frontend/
│   └── Keyhole-Solution-App/
│       └── app/
│           ├── screens/       # React Native screens
│           │   └── LoginScreen.tsx
│           └── utils/         # Shared frontend utility functions
│
├── tests/
│   └── backend/
│       └── mcp/
│           └── routes/        # Route-specific unit tests
│           └── utils/         # Email mocking tests
│
├── .env                      # Shared backend config (e.g. SMTP, TESTING)
├── requirements.txt          # Python dependencies
├── setup.bat                 # Unified local dev launcher
```

---

## 🔐 Authentication & Email Flow

### 🔁 Backend Flow (FastAPI)
1. **`/auth/register`**
   - Hashes and stores password
   - Stores default role `user`
   - Sends verification email using `send_email(...)`
   - Memory is stored in Qdrant under user-specific collection

2. **`/auth/verify-email`**
   - Parses the JWT token
   - Sets `email_verified = true` in memory

3. **`/auth/login`**
   - Validates email + password
   - Confirms `email_verified` is true
   - Issues new JWT if successful

4. **`/auth/logout`**
   - Stateless endpoint
   - Handled entirely via frontend

5. **MemoryManager (Qdrant)**
   - One Qdrant collection per user (`facts_<email>`)
   - All facts (password_hash, email_verified, etc.) stored as key-value vector records

---

## 💻 Frontend Integration (React Native)

### 📱 LoginScreen.tsx
- Collects email + password
- Sends to `/auth/login`
- Saves access token in async storage
- Navigates to secure screen if successful

### 🔒 Auth Flow
- Token stored in memory
- Sent on future requests via Authorization header
- Logged-out state clears token

---

## ✅ Testing Strategy

### 🧪 Unit Tests
- All `auth_*` endpoints have dedicated test files
- Email is mocked using `IS_TESTING=true` flag
- Tests use Qdrant collections prefixed with `facts_test_*`
- `pytest -s tests/backend/mcp/routes/test_auth_*.py` for backend testing
- React Native frontend tests go in `__tests__` next to screens

---

## 🧠 Agent Memory & Context

- Agents retrieve memory from Qdrant using MemoryManager
- Login is required to isolate user context
- Guest sessions are temporary and IP-tracked
- All authenticated users have persistent memory

---

## 🛡️ Security Features

- Role-based route protection (`user`, `guest`, `admin`)
- JWT validation via FastAPI Depends
- All emails sent through `security@keyholesolution.com`
- `passlib[bcrypt]` for password hashing
- `.env` centralizes config/secrets

---
