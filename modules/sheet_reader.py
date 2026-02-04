import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config.config import (
    SPREADSHEET_NAME,
    WORKSHEET_NAME,
    CREDENTIALS_FILE
)


def get_participants():

    # 1️⃣ Define the API scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # 2️⃣ Authenticate using service account credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        scope
    )

    client = gspread.authorize(credentials)

    # 3️⃣ Open spreadsheet and worksheet
    spreadsheet = client.open(SPREADSHEET_NAME)
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    # 4️⃣ Fetch all records as list of dictionaries
    records = worksheet.get_all_records()

    participants = []

    # 5️⃣ Extract Name and Email from each row
    for row in records:
        name = row.get("Name")
        email = row.get("Email")

        # Skip incomplete rows
        if not name or not email:
            continue

        participants.append({
            "name": name.strip(),
            "email": email.strip()
        })

    return participants
