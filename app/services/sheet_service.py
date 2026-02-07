from pathlib import Path
import pandas as pd

def read_participants(file_path: Path):
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")

    # 🔹 Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 🔹 Map possible column names
    name_column = None
    email_column = None

    for col in df.columns:
        if col in ["name", "full_name", "participant_name"]:
            name_column = col
        if col in ["email", "email_address", "e_mail"]:
            email_column = col

    if not name_column or not email_column:
        raise ValueError("Sheet must contain name and email columns")

    participants = []
    for _, row in df.iterrows():
        participants.append({
            "name": str(row[name_column]).strip(),
            "email": str(row[email_column]).strip()
        })

    return participants
