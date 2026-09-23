# VideoMind Backend

## Early access endpoint

URL:

```http
POST /api/early-access
```

Request body:

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

Expected successful response:

```json
{
  "success": true,
  "message": "Early access registration received."
}
```

Duplicate-email response:

```json
{
  "success": true,
  "message": "This email is already registered for early access."
}
```

Validation errors return HTTP 422 automatically when:

- name is empty or whitespace-only
- name length is less than 2 or greater than 100 characters
- email is invalid or empty

Local testing command:

```bash
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Example request with curl:

```bash
curl -X POST http://localhost:8000/api/early-access \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Johnson","email":"alice@example.com"}'
```

Example request with PowerShell:

```powershell
$body = '{"name":"Alice Johnson","email":"alice@example.com"}'
Invoke-RestMethod -Uri 'http://localhost:8000/api/early-access' -Method Post -ContentType 'application/json' -Body $body
```
