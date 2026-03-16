import sys
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from imap_tools import MailBox, AND, OR

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")

REMETENTES = [
    "newsletter@mail.techdrop.news",
]


since_date = (datetime.now() - timedelta(days=1)).date()

with MailBox("imap.gmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "INBOX") as mb:
    for msg in mb.fetch(
        AND(
            OR(from_=REMETENTES),
            date_gte=since_date
        )
    ):
        print(msg.subject, msg.date, msg.text)