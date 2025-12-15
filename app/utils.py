import uuid
from pathlib import Path
from fastapi import UploadFile

from .config import BASE_DIR, UPLOAD_DIR

UPLOAD_PATH = Path(BASE_DIR) / UPLOAD_DIR
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    ext = Path(upload_file.filename).suffix
    name = f"{uuid.uuid4().hex}{ext}"
    dest = UPLOAD_PATH / name
    with dest.open('wb') as f:
        content = await upload_file.read()
        f.write(content)
    return str(dest.relative_to(Path(BASE_DIR)))
