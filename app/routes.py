from datetime import timedelta
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_student,
    get_current_teacher,
    get_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from .utils import save_upload_file

router = APIRouter()

@router.post('/students/register', response_model=schemas.Token)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = crud.get_student_by_name(db, student.name)
    if existing:
        raise HTTPException(status_code=400, detail='Student already exists')
    hashed = get_password_hash(student.password)
    s = crud.create_student(db, student.name, hashed)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": s.name, "type": "student"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/students/login', response_model=schemas.Token)
def login_student(name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    student = crud.get_student_by_name(db, name)
    if not student or not verify_password(password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student.name, "type": "student"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/teachers/register', response_model=schemas.Token)
def register_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    existing = crud.get_teacher_by_name(db, teacher.name)
    if existing:
        raise HTTPException(status_code=400, detail='Teacher already exists')
    hashed = get_password_hash(teacher.password)
    t = crud.create_teacher(db, teacher.name, hashed)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": t.name, "type": "teacher"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/teachers/login', response_model=schemas.Token)
def login_teacher(name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    teacher = crud.get_teacher_by_name(db, name)
    if not teacher or not verify_password(password, teacher.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": teacher.name, "type": "teacher"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/assignments/')
async def submit_assignment(
    subject: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    token: str = Form(None),
    db: Session = Depends(get_db),
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    student = await get_current_student(token, db)
    saved = await save_upload_file(file)
    assignment = crud.create_assignment(db, student, subject, description, saved)
    return {'id': assignment.id, 'subject': assignment.subject, 'file_path': assignment.file_path}

@router.get('/assignments/')
def list_all_assignments(db: Session = Depends(get_db)):
    items = crud.list_assignments(db)
    out = []
    for a in items:
        out.append({
            'id': a.id,
            'subject': a.subject,
            'description': a.description,
            'file_path': a.file_path,
            'created_at': a.created_at,
            'student_name': a.student.name if a.student else None,
            'comments': [{'id': c.id, 'teacher_name': c.teacher_name, 'comment': c.comment, 'created_at': c.created_at} for c in a.comments]
        })
    return out

@router.get('/students/{name}/assignments/')
def assignments_by_student(name: str, db: Session = Depends(get_db)):
    items = crud.get_assignments_by_student(db, name)
    return [{'id': a.id, 'subject': a.subject, 'description': a.description, 'file_path': a.file_path, 'created_at': a.created_at, 'comments': [{'id': c.id, 'teacher_name': c.teacher_name, 'comment': c.comment, 'created_at': c.created_at} for c in a.comments]} for a in items]

@router.post('/assignments/{assignment_id}/comment')
async def add_comment(
    assignment_id: int,
    comment: str = Form(...),
    token: str = Form(None),
    db: Session = Depends(get_db),
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    teacher = await get_current_teacher(token, db)
    assignment = crud.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail='Assignment not found')
    c = crud.add_comment(db, assignment, teacher, comment)
    return {'id': c.id, 'assignment_id': c.assignment_id, 'teacher_name': c.teacher_name, 'comment': c.comment}
