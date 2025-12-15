from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas, models
from .utils import save_upload_file

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/students/', response_model=schemas.StudentCreate)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.name == student.name).first()
    if existing:
        raise HTTPException(status_code=400, detail='Student already exists')
    s = models.Student(name=student.name)
    db.add(s)
    db.commit()
    db.refresh(s)
    return student

@router.post('/teachers/', response_model=schemas.TeacherCreate)
def register_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Teacher).filter(models.Teacher.name == teacher.name).first()
    if existing:
        raise HTTPException(status_code=400, detail='Teacher already exists')
    t = models.Teacher(name=teacher.name)
    db.add(t)
    db.commit()
    db.refresh(t)
    return teacher

@router.post('/assignments/')
async def submit_assignment(
    student_name: str = Form(...),
    subject: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    student = crud.get_or_create_student(db, student_name)
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
def add_comment(assignment_id: int, teacher_name: str = Form(...), comment: str = Form(...), db: Session = Depends(get_db)):
    assignment = crud.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail='Assignment not found')
    c = crud.add_comment(db, assignment, teacher_name, comment)
    return {'id': c.id, 'assignment_id': c.assignment_id, 'teacher_name': c.teacher_name, 'comment': c.comment}
