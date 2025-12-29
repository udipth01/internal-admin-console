# Internal Admin Console

Secure internal dashboard to view Supabase tables.

## Features
- Login with role-based access
- Dropdown table selector
- Read-only table viewer
- JWT secured
- Render deployable

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
