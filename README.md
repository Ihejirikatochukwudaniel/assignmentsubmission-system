# Assignment Submission System

Backend API built with FastAPI + SQLAlchemy for students to submit assignments and teachers to comment.

Quick start

1. Create a PostgreSQL database and set `DATABASE_URL` env var, e.g.:

```
export DATABASE_URL=postgresql://postgres:password@localhost:5432/assignments_db
```

On Windows (PowerShell):

```powershell
$env:DATABASE_URL = "postgresql://postgres:password@localhost:5432/assignments_db"
```

2. Install dependencies:

```bash
pip install -r "requirements.txt"
```

3. Run the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API Endpoints

- POST /students/ — register student (JSON {"name": "..."})
- POST /teachers/ — register teacher (JSON {"name": "..."})
- POST /assignments/ — submit assignment (form: `student_name`, `subject`, `description`, `file`)
- GET /assignments/ — list all assignments
- GET /students/{name}/assignments/ — assignments by student
- POST /assignments/{assignment_id}/comment — add comment (form: `teacher_name`, `comment`)

Uploaded files are stored in the `uploads/` directory by default.
