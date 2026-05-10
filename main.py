import sys
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from imap_tools import MailBox, AND, OR

# Configura a codificação de saída para UTF-8, evitando problemas com caracteres especiais
sys.stdout.reconfigure(encoding='utf-8')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_recent_newsletters():
    # Obtém as credenciais de e-mail das variáveis de ambiente
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    # Carrega a lista de remetentes das newsletters da variável de ambiente, separada por vírgula
    REMETENTES_STR = os.getenv("NEWSLETTER_SENDERS", "")
    REMETENTES = [sender.strip() for sender in REMETENTES_STR.split(",") if sender.strip()]

    # Define a data de início como ontem (últimas 24 horas)
    since_date = (datetime.now() - timedelta(days=1)).date()
    
    print(f"🔍 Iniciando busca de newsletters desde {since_date} de remetentes: {REMETENTES}")
    
    newsletters = []

    # Conecta ao servidor IMAP do Gmail e busca mensagens
    with MailBox("imap.gmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "INBOX") as mb:
        print("📧 Conectado ao IMAP. Buscando mensagens...")
        for msg in mb.fetch(
            AND(
                OR(from_=REMETENTES),
                date_gte=since_date
            )
        ):
            print(f"✅ Encontrada newsletter: {msg.subject} ({msg.date})")
            newsletters.append({
                "subject": msg.subject,
                "date": msg.date,
                "text": msg.html if msg.html else msg.text
            })
    
    print(f"📋 Total de newsletters coletadas: {len(newsletters)}")
    return newsletters

if __name__ == "__main__":
    emails = get_recent_newsletters()
    for email in emails:
        print(f"Encontrado: {email['subject']} ({email['date']})")
    
    print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
    print("MAIL_PASSWORD existe?", os.getenv("MAIL_PASSWORD") is not None)