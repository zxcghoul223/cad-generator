import json
import logging
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("parts_api")

app = FastAPI(title="Parametric Parts API", version="0.1.0")
database.init_db()

TMP = os.getenv("TMP_DIR", tempfile.gettempdir())

# обязательные числовые параметры для каждой детали
REQUIRED_PARAMS = {
    "box": ["w", "h", "t"],
    "bracket": ["w", "h", "t", "hole_d"],
    "star": ["points", "r_out", "r_in", "t"],
}


class GenerateRequest(BaseModel):
    part: str
    params: dict
    format: str = "step"  # step | stl


@app.get("/parts")
def list_parts():
    return {"parts": list(cad_builder.BUILDERS.keys())}


def _validate_params(part: str, params: dict):
    """Семантическая валидация: ловим невалидные параметры до сборки геометрии."""
    required = REQUIRED_PARAMS.get(part)
    if required is None:
        raise HTTPException(400, f"unknown part: {part}")
    missing = [k for k in required if k not in params]
    if missing:
        raise HTTPException(400, f"missing parameters: {', '.join(missing)}")
    for key in required:
        value = params[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise HTTPException(400, f"parameter '{key}' must be a positive number, got {value!r}")


@app.post("/generate")
def generate(req: GenerateRequest, db: Session = Depends(database.get_db)):
    if req.format not in ("step", "stl"):
        raise HTTPException(400, "format must be 'step' or 'stl'")
    _validate_params(req.part, req.params)
    try:
        part = cad_builder.build(req.part, req.params)
    except Exception as exc:
        logger.exception("CadQuery build failed: part=%s params=%s", req.part, req.params)
        raise HTTPException(500, "geometry build failed, see server logs")

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
