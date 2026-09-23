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

## Production Deployment

Run the backend from the `backend/` directory. The deployment environment must
provide a PostgreSQL connection string and may override the other settings:

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/video_ai
CORS_ORIGINS=https://videomind.in,http://localhost:5173
PORT=8000
SUPADATA_API_KEY=your-server-side-provider-key
```

`SUPADATA_API_KEY` configures the server-side YouTube transcript provider. It
does not contain YouTube account credentials or cookies. When it is absent,
local development falls back to `youtube-transcript-api`; production should
configure the provider key because cloud-provider IPs may be blocked by
YouTube. Optional settings include `SUPADATA_TIMEOUT_SECONDS`, `UPLOAD_DIR`,
`FRAMES_DIR`, `TESSERACT_PATH`, `YOLO_MODEL_PATH`, and the existing smart-sampling settings. `TESSERACT_PATH`
should be omitted when the `tesseract` executable is on the Linux `PATH`.

Install the backend dependencies with:

```bash
python -m pip install -r requirements.txt
```

Start the service with the platform-provided port:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

On PowerShell, use `--port $env:PORT`. The service exposes `GET /health`,
which returns `{"status":"ok","database":"ok"}` when the database is
reachable, and `GET /docs` for the OpenAPI documentation.

The application uses SQLAlchemy with PostgreSQL and calls
`Base.metadata.create_all()` during startup. This creates missing tables without
dropping existing tables or data. There is currently no migration system, so
schema changes will require a future migration process.

For verification, check `/health`, `/docs`, `POST /api/early-access`, a YouTube
analysis request, and `GET /videos/{id}/steps`. Set `CORS_ORIGINS` to a
comma-separated list of exact allowed origins; do not use `*` in production.

Uploads and generated frames are runtime files and require writable storage.
They are not suitable for ephemeral storage when uploaded-video analysis must
survive restarts. The transcript-based YouTube guide endpoint does not download
the video or require local video files. Full uploaded-video analysis additionally
requires OpenCV, Tesseract, and the YOLO weights configured by
`YOLO_MODEL_PATH`; the model file is not downloaded automatically.

Do not commit `.env` files, credentials, generated media, frames, or model
weights. Configure `VITE_API_BASE_URL` in the frontend deployment with the
public backend URL, for example `https://YOUR-BACKEND-DOMAIN`.
