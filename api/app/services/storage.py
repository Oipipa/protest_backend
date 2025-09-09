import os
from uuid import uuid4
from datetime import datetime
from typing import List, Dict
from fastapi import UploadFile
from app.core.config import settings

async def save_uploads(files: List[UploadFile], subdir: str = "") -> List[Dict]:
    base = settings.upload_dir
    date_part = datetime.utcnow().strftime("%Y/%m/%d")
    rel_dir = os.path.join(subdir, date_part) if subdir else date_part
    abs_dir = os.path.join(base, rel_dir)
    os.makedirs(abs_dir, exist_ok=True)
    saved = []
    for f in files:
        if not f.content_type or not f.content_type.startswith("image/"):
            continue
        ext = os.path.splitext(f.filename or "")[1].lower() or ".bin"
        name = f"{uuid4().hex}{ext}"
        abs_path = os.path.join(abs_dir, name)
        size = 0
        with open(abs_path, "wb") as out:
            while True:
                chunk = await f.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                out.write(chunk)
        await f.close()
        url = f"/uploads/{rel_dir.replace(os.sep,'/')}/{name}"
        saved.append({"filename": name, "mime_type": f.content_type, "size": size, "url": url})
    return saved
