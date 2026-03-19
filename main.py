import sys
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from imap_tools import MailBox, AND, OR

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
def get_recent_newsletters():
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    REMETENTES = [
        "newsletter@mail.techdrop.news",
        "contato@thenewscc.com.br",
        "news@alphasignal.ai",
    ]

    since_date = (datetime.now() - timedelta(days=1)).date()
    
    newsletters = []

    with MailBox("imap.gmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "INBOX") as mb:
        for msg in mb.fetch(
            AND(
                OR(from_=REMETENTES),
                date_gte=since_date
            )
        ):
            newsletters.append({
                "subject": msg.subject,
                "date": msg.date,
                "text": msg.text
            })
            
    return newsletters

if __name__ == "__main__":
    emails = get_recent_newsletters()
    for email in emails:
        print(f"Encontrado: {email['subject']} ({email['date']})")
    
    print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
    print("MAIL_PASSWORD existe?", os.getenv("MAIL_PASSWORD") is not None)