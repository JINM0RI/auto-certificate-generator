from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil
import os
from pathlib import Path
import random
from fastapi.responses import FileResponse, JSONResponse
from app.services.email_service import send_certificates
from fastapi import Body
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.services.sheet_service import read_participants
from app.services.certificate_service import generate_certificate
from fastapi.staticfiles import StaticFiles




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
app.mount("/static", StaticFiles(directory="app/static"), name="static")
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

@app.get("/preview-generated")
def preview_generated_certificate():
    pdf_files = list(GENERATED_DIR.glob("*.pdf"))

    if not pdf_files:
        return JSONResponse(
            status_code=404,
            content={"error": "No certificates generated yet"}
        )

    preview_pdf = pdf_files[0]  # any one certificate

    return FileResponse(
        path=preview_pdf,
        media_type="application/pdf",
        filename=preview_pdf.name
    )


@app.post("/send-emails")
def send_emails(
    subject: str = Body(...),
    body: str = Body(...)
):
    sheet_files = list(SHEET_DIR.glob("*"))

    if not sheet_files:
        return JSONResponse(
            status_code=400,
            content={"error": "No participant sheet uploaded"}
        )

    participants = read_participants(sheet_files[-1])

    send_certificates(
        participants=participants,
        subject=subject,
        body=body,
        certificates_dir=GENERATED_DIR
    )

    # AUTO RESET AFTER SUCCESS
    for folder in [TEMPLATE_DIR, SHEET_DIR, GENERATED_DIR]:
        for file in folder.iterdir():
            file.unlink()

    return {
        "message": "Emails sent & system reset",
        "count": len(participants)
    }



templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/reset")
def reset_app_state():
    global position_config

    # Reset position
    position_config = {
        "x": 300,
        "y": 300,
        "font_size": 48
    }

    # Clear uploaded templates & sheets
    for folder in [TEMPLATE_DIR, SHEET_DIR]:
        for file in folder.iterdir():
            file.unlink()

    # Clear generated certificates (PDFs)
    for file in GENERATED_DIR.iterdir():
        file.unlink()

    return {"status": "reset_complete"}
