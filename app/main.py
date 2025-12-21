from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from . import models
from .routes import router
from .config import BASE_DIR, UPLOAD_DIR

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Assignment Submission System')

app.include_router(router)

# Mount uploads for direct access
app.mount('/uploads', StaticFiles(directory=str(BASE_DIR / UPLOAD_DIR)), name='uploads')

@app.get('/')
def root():
    return {"message": "Assignment Submission System API - Use /students/register, /teachers/register for auth"}
