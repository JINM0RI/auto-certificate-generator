from pathlib import Path
import pandas as pd

def read_participants(file_path: Path):
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")

    return df.to_dict(orient="records")
