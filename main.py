import json
import os
import tempfile
import uuid

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

import cad_builder
import database
from models import Generation

app = FastAPI(title="Parametric Parts API", version="0.1.0")
database.init_db()

TMP = os.getenv("TMP_DIR", tempfile.gettempdir())


class GenerateRequest(BaseModel):
    part: str
    params: dict
    format: str = "step"  # step | stl


@app.get("/parts")
def list_parts():
    return {"parts": list(cad_builder.BUILDERS.keys())}


@app.post("/generate")
def generate(req: GenerateRequest, db: Session = Depends(database.get_db)):
    if req.format not in ("step", "stl"):
        raise HTTPException(400, "format must be 'step' or 'stl'")
    try:
        part = cad_builder.build(req.part, req.params)
    except Exception as exc:
        raise HTTPException(400, f"build failed: {exc}")

    suffix = req.format
    filename = f"part_{uuid.uuid4().hex}.{suffix}"
    path = os.path.join(TMP, filename)
    cad_builder.export(part, path)

    rec = Generation(part=req.part, params=json.dumps(req.params), filename=filename)
    db.add(rec)
    db.commit()

    return FileResponse(
        path,
        filename=f"{req.part}.{suffix}",
        media_type="application/octet-stream",
    )


@app.get("/history")
def history(db: Session = Depends(database.get_db), limit: int = 20):
    rows = (
        db.query(Generation)
        .order_by(Generation.id.desc())
        .limit(limit)
        .all()
    )
    return [r.to_dict() for r in rows]
