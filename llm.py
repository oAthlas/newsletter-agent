from app import get_recent_newsletters
import os
from dotenv import load_dotenv
from google import genai
import smtplib
from email.message import EmailMessage

load_dotenv()

newsletters = get_recent_newsletters()

def resumir_newsletter(texto):
    # O Client do genai puxa automaticamente a variável GEMINI_API_KEY do seu .env
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash", # ou gemini-1.5-flash caso dê erro de modelo não encontrado
        contents="Resuma este texto. Entregue o resultado EM PORTUGUÊS-BR, puramente formatado usando tags em HTML (como <h2>, <p>, <ul>, <li>, <strong>, <em>, <br>), organizando bem a leitura de forma amigável, com o tom do texto. Retorne EXATAMENTE APENAS O CÓDIGO HTML sem os delimitadores de código markdown (```html):\n" + texto,
    )

    return response.text

if __name__ == "__main__":
    
    # -----------------------= SEND MODULE =------------------------
    
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
    
    # Inicia a conexão segura com o servidor do Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            
            # Para CADA newsletter encontrada, vamos gerar um resumo e mandar um e-mail
            for news in newsletters:
                print(f"[{news['date']}] Processando e resumindo: {news['subject']}...")
                
                # 1. Extraímos apenas a parte do texto (news["text"]) e mandamos para a IA
                resumo = resumir_newsletter(news["text"])
                
                # 2. Montamos o e-mail
                msg = EmailMessage()
                msg["Subject"] = f"[RESUMO LLM] {news['subject']}"
                msg["From"] = MAIL_USERNAME
                msg["To"] = MAIL_ADDRESS
                
                # Definimos um fallback em texto plano
                msg.set_content("Seu cliente de e-mail não suporta exibição de HTML. O resumo foi gerado, mas precisa ser lido num formato compatível.")
                
                # Injetamos o render HTML criado pela LLM
                msg.add_alternative(resumo, subtype='html')
                
                # 3. Disparamos o e-mail
                smtp.send_message(msg)
                print(f"✅ E-mail de resumo enviado para '{news['subject']}'!\n")
                
    except Exception as e:
        print(f"Ocorreu um erro ao enviar os e-mails: {e}")
