# 📚 Student Assignment Submission System

A comprehensive FastAPI-based backend system for managing student assignment submissions with teacher feedback capabilities.

## 🎯 Features

- Student and teacher registration
- Assignment submission with file uploads
- View all assignments or filter by student
- Teacher commenting system on assignments
- PostgreSQL database with SQLAlchemy ORM
- File storage for assignment attachments

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Python Version:** 3.8+
- **Additional Libraries:** python-multipart, psycopg2-binary

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd student-assignment-system
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Database Setup

#### Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [PostgreSQL Official Website](https://www.postgresql.org/download/windows/)

#### Create Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE assignment_system;
CREATE USER assignment_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE assignment_system TO assignment_user;
\q
```

### 5. Environment Variables Setup

Create a `.env` file in the project root directory:

```bash
# Database Configuration
DATABASE_URL=postgresql://assignment_user:your_secure_password@localhost:5432/assignment_system

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=True

# File Upload Configuration
UPLOAD_DIRECTORY=./uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

**Important:** Add `.env` to your `.gitignore` file to keep credentials secure.

### 6. Create Uploads Directory

```bash
mkdir uploads
```

## 📁 Project Structure

```
student-assignment-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # Database operations
│   └── routers/
│       ├── __init__.py
│       ├── students.py      # Student endpoints
│       ├── teachers.py      # Teacher endpoints
│       └── assignments.py   # Assignment endpoints
├── uploads/                 # File storage directory
├── .env                     # Environment variables (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🗄️ Database Models

### Student
- `id` (Primary Key)
- `name` (Unique)
- `email`
- `created_at`

### Teacher
- `id` (Primary Key)
- `name` (Unique)
- `email`
- `created_at`

### Assignment
- `id` (Primary Key)
- `student_id` (Foreign Key)
- `student_name`
- `subject`
- `description`
- `file_path`
- `submitted_at`

### Comment
- `id` (Primary Key)
- `assignment_id` (Foreign Key)
- `teacher_id` (Foreign Key)
- `teacher_name`
- `comment`
- `created_at`

## 🔌 API Endpoints

### Student Management

#### Register Student
```http
POST /students/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Teacher Management

#### Register Teacher
```http
POST /teachers/
Content-Type: application/json

{
  "name": "Dr. Smith",
  "email": "smith@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Dr. Smith",
  "email": "smith@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Assignment Management

#### Submit Assignment
```http
POST /assignments/
Content-Type: multipart/form-data

student_name: John Doe
subject: Mathematics
description: Chapter 5 homework
file: [binary file data]
```

**Response:**
```json
{
  "id": 1,
  "student_name": "John Doe",
  "subject": "Mathematics",
  "description": "Chapter 5 homework",
  "file_path": "uploads/assignment_1_mathematics.pdf",
  "submitted_at": "2024-01-15T14:30:00"
}
```

#### List All Assignments
```http
GET /assignments/
```

**Response:**
```json
[
  {
    "id": 1,
    "student_name": "John Doe",
    "subject": "Mathematics",
    "description": "Chapter 5 homework",
    "file_path": "uploads/assignment_1_mathematics.pdf",
    "submitted_at": "2024-01-15T14:30:00",
    "comments": []
  }
]
```

#### Get Student's Assignments
```http
GET /students/{student_name}/assignments/
```

**Response:**
```json
[
  {
    "id": 1,
    "student_name": "John Doe",
    "subject": "Mathematics",
    "description": "Chapter 5 homework",
    "file_path": "uploads/assignment_1_mathematics.pdf",
    "submitted_at": "2024-01-15T14:30:00",
    "comments": []
  }
]
```

#### Add Comment to Assignment
```http
POST /assignments/{assignment_id}/comment
Content-Type: multipart/form-data

teacher_name: Dr. Smith
comment: Good work! Consider reviewing theorem 3.2
```

**Response:**
```json
{
  "id": 1,
  "assignment_id": 1,
  "teacher_name": "Dr. Smith",
  "comment": "Good work! Consider reviewing theorem 3.2",
  "created_at": "2024-01-15T16:00:00"
}
```

## 🏃 Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## 📝 Testing the API

### Using cURL

```bash
# Register a student
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# Submit an assignment
curl -X POST "http://localhost:8000/assignments/" \
  -F "student_name=John Doe" \
  -F "subject=Mathematics" \
  -F "description=Homework Chapter 5" \
  -F "file=@/path/to/assignment.pdf"

# List all assignments
curl -X GET "http://localhost:8000/assignments/"
```

### Using Python Requests

```python
import requests

# Register student
response = requests.post(
    "http://localhost:8000/students/",
    json={"name": "John Doe", "email": "john@example.com"}
)
print(response.json())

# Submit assignment
files = {"file": open("assignment.pdf", "rb")}
data = {
    "student_name": "John Doe",
    "subject": "Mathematics",
    "description": "Homework"
}
response = requests.post(
    "http://localhost:8000/assignments/",
    files=files,
    data=data
)
print(response.json())
```

## 🔒 Security Considerations

1. **Environment Variables:** Never commit `.env` file to version control
2. **File Validation:** Implement file type and size validation
3. **SQL Injection:** SQLAlchemy ORM provides protection
4. **CORS:** Configure CORS for production deployment
5. **Authentication:** Consider adding JWT authentication for production

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Verify database exists
psql -U assignment_user -d assignment_system -h localhost
```

### Import Errors

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Verify Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### File Upload Issues

```bash
# Check uploads directory permissions
chmod 755 uploads

# Verify directory exists
mkdir -p uploads
```

## 📦 Dependencies (requirements.txt)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

## 🤝 Team Collaboration

### Suggested Roles

1. **Backend Developer 1:** Student/Teacher registration endpoints
2. **Backend Developer 2:** Assignment submission with file handling
3. **Backend Developer 3:** Assignment listing and filtering
4. **Backend Developer 4:** Commenting system and relationships

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/student-registration

# Make changes and commit
git add .
git commit -m "Add student registration endpoint"

# Push and create PR
git push origin feature/student-registration
```

## 📈 Future Enhancements

- [ ] User authentication with JWT tokens
- [ ] Assignment grading system
- [ ] Email notifications
- [ ] Assignment due dates
- [ ] File download endpoints
- [ ] Pagination for large datasets
- [ ] Search and advanced filtering
- [ ] Assignment status tracking (submitted, graded, returned)
- [ ] Multiple file uploads per assignment
- [ ] Docker containerization

## 📄 License

This project is licensed under the MIT License.

