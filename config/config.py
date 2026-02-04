# ==============================
# Google Sheets Configuration
# ==============================

# Name or ID of the Google Spreadsheet
SPREADSHEET_NAME = "participants"

# Worksheet (tab) name inside the spreadsheet
WORKSHEET_NAME = "Form Responses 1"

# Path to Google service account credentials
CREDENTIALS_FILE = "credentials/service_account.json"


# ==============================
# Certificate Template Settings
# ==============================

# Certificate template image path
CERTIFICATE_TEMPLATE_PATH = "templates/certificate_template.png"

# Output directories
OUTPUT_IMAGE_DIR = "output/images"
OUTPUT_PDF_DIR = "output/pdfs"

# Font settings
FONT_PATH = "fonts/font.ttf"
FONT_SIZE = 60


# ==============================
# Name Placement Settings
# ==============================

# Coordinates where participant name will be placed
NAME_POSITION_X = 500
NAME_POSITION_Y = 600

# Text color (RGB)
NAME_TEXT_COLOR = (0, 0, 0)


# ==============================
# Email Configuration (No passwords here!)
# ==============================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "youremail@gmail.com"
EMAIL_SUBJECT = "Your Participation Certificate"
EMAIL_BODY = """
Dear Participant,

Thank you for participating in our event.
Please find your certificate attached.

Best regards,
Event Team
"""


# ==============================
# General Settings
# ==============================

DEBUG = True
