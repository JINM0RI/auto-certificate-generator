from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from pathlib import Path

from app.services.sheet_service import read_participants
from app.services.certificate_service import generate_certificate

app = FastAPI()

# ---------- BASE DIR ----------
BASE_DIR = Path(__file__).resolve().parent

# ---------- DIRECTORIES ----------
UPLOADS_DIR = BASE_DIR / "uploads"
TEMPLATE_DIR = UPLOADS_DIR / "templates"
SHEET_DIR = UPLOADS_DIR / "sheets"
GENERATED_DIR = BASE_DIR / "generated_certificates"

TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
SHEET_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# ---------- STATIC MOUNTS ----------
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_DIR),
    name="uploads"
)

app.mount(
    "/generated",
    StaticFiles(directory=GENERATED_DIR),
    name="generated"
)

# ---------- GLOBAL POSITION STORE ----------
position_config = {
    "x": 300,
    "y": 300,
    "font_size": 48
}

# ---------- APIs ----------

@app.post("/upload-sheet")
async def upload_sheet(file: UploadFile = File(...)):
    path = SHEET_DIR / file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    participants = read_participants(path)
    return {
        "message": "Sheet uploaded",
        "count": len(participants)
    }


@app.post("/upload-template")
async def upload_template(file: UploadFile = File(...)):
    path = TEMPLATE_DIR / file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {
        "message": "Template uploaded",
        "template_url": f"/uploads/templates/{file.filename}"
    }


@app.post("/preview")
def preview(name: str, template_name: str):
    template_path = TEMPLATE_DIR / template_name
    preview_path = UPLOADS_DIR / "preview.jpg"

    generate_certificate(
        name=name,
        template_path=template_path,
        output_path=preview_path,
        x=position_config["x"],
        y=position_config["y"],
        font_size=position_config["font_size"]
    )

    return FileResponse(preview_path)


@app.post("/save-position")
def save_position(data: dict):
    position_config["x"] = data["x"]
    position_config["y"] = data["y"]
    position_config["font_size"] = data.get("font_size", 48)

    return {
        "status": "saved",
        "position": position_config
    }


@app.post("/generate-certificates")
def generate_all(template_name: str):
    template_path = TEMPLATE_DIR / template_name

    sheet_files = list(SHEET_DIR.iterdir())
    if not sheet_files:
        return {"error": "No sheet uploaded"}

    sheet_path = sheet_files[-1]
    participants = read_participants(sheet_path)

    for p in participants:
        output_path = GENERATED_DIR / f"{p['name'].replace(' ', '_')}.pdf"

        generate_certificate(
            name=p["name"],
            template_path=template_path,
            output_path=output_path,
            x=position_config["x"],
            y=position_config["y"],
            font_size=position_config["font_size"]
        )

    return {
        "message": "Certificates generated",
        "count": len(participants),
        "download_url": "/generated/"
    }
