import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./assignments.db')
UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
