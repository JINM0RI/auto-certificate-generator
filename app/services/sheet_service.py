import pandas as pd

def read_participants(file_path: str):
    # Read based on file type
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    if "name" not in df.columns or "email" not in df.columns:
        raise ValueError("Sheet must contain 'name' and 'email' columns")

    participants = []
    for _, row in df.iterrows():
        participants.append({
            "name": str(row["name"]).strip(),
            "email": str(row["email"]).strip()
        })

    return participants
