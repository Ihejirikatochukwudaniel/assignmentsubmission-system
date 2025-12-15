from sqlalchemy.orm import Session
from . import models

def get_or_create_student(db: Session, name: str):
    student = db.query(models.Student).filter(models.Student.name == name).first()
    if student:
        return student
    student = models.Student(name=name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def create_teacher(db: Session, name: str):
    teacher = db.query(models.Teacher).filter(models.Teacher.name == name).first()
    if teacher:
        return teacher
    teacher = models.Teacher(name=name)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

def create_assignment(db: Session, student: models.Student, subject: str, description: str, file_path: str):
    assignment = models.Assignment(student_id=student.id, subject=subject, description=description, file_path=file_path)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def list_assignments(db: Session):
    return db.query(models.Assignment).order_by(models.Assignment.created_at.desc()).all()

def get_assignments_by_student(db: Session, student_name: str):
    return db.query(models.Assignment).join(models.Student).filter(models.Student.name == student_name).all()

def add_comment(db: Session, assignment: models.Assignment, teacher_name: str, comment_text: str):
    teacher = db.query(models.Teacher).filter(models.Teacher.name == teacher_name).first()
    if not teacher:
        teacher = models.Teacher(name=teacher_name)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
    comment = models.Comment(assignment_id=assignment.id, teacher_id=teacher.id, teacher_name=teacher.name, comment=comment_text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_assignment(db: Session, assignment_id: int):
    return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
