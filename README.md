# Task Tracker Backend

A lightweight FastAPI backend for tracking tasks, built as a simple monolithic
application for learning purposes. It uses direct SQLite access with minimal
layering instead of an ORM, prioritizing clarity and fast iteration over
enterprise-style architecture.

## Setup

### 1. Create a virtual environment and install dependencies

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and adjust values if needed:

**Linux/macOS:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

### 3. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 4. Test the health endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{"status": "ok", "timestamp": "2026-07-05T12:34:56.789012+00:00"}
```# tasks-tracker
# tasks-tracker
