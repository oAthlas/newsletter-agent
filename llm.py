from main import get_recent_newsletters
import os
from dotenv import load_dotenv
from google import genai
import smtplib
from email.message import EmailMessage
from datetime import datetime

load_dotenv()

newsletters = get_recent_newsletters()

def resumir_todas_newsletters(textos_combinados):
    client = genai.Client()

    prompt = (
        "Aqui estão várias newsletters originais (em HTML ou texto) recebidas hoje. "
        "Leia todas elas e crie um único resumo massivo, consolidando todos os tópicos e notícias mais importantes de forma organizada. "
        "Agrupe por temas ou tópicos com uma boa narrativa, em vez de apenas listar o que cada newsletter disse, para uma leitura fluida e rica. "
        "Entregue o resultado EM PORTUGUÊS-BR, puramente formatado em HTML "
        "(use tags como <h1>, <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em> para estruturar bem; não use ```html no início ou fim). "
        "Retorne EXATAMENTE APENAS O CÓDIGO HTML limpo e pronto para renderização no corpo de um e-mail:\\n\\n"
        f"{textos_combinados}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text

if __name__ == "__main__":
    
    # -----------------------= SEND MODULE =------------------------
    
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
    
    if not newsletters:
        print("Nenhuma newsletter encontrada para resumir hoje.")
    else:
        try:
            print(f"Combinando {len(newsletters)} newsletters para resumo massivo...")
            textos_combinados = ""
            for news in newsletters:
                textos_combinados += f"\\n\\n--- INÍCIO DA NEWSLETTER: {news['subject']} ---\\n"
                textos_combinados += news["text"]
                textos_combinados += f"\\n--- FIM DA NEWSLETTER: {news['subject']} ---\\n"
                
            print("Enviando conteúdo para o Gemini gerar o resumo centralizado...")
            resumo_geral = resumir_todas_newsletters(textos_combinados)
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                
                msg = EmailMessage()
                hoje = datetime.now().strftime("%d/%m/%Y")
                msg["Subject"] = f"[RESUMO LLM] Todas as Newsletters de {hoje}"
                msg["From"] = MAIL_USERNAME
                msg["To"] = MAIL_ADDRESS
                
                msg.set_content("Seu cliente de e-mail não suporta exibição de HTML. O resumo foi gerado, mas precisa ser lido num formato compatível.")
                
                msg.add_alternative(resumo_geral, subtype='html')
                
                print("Enviando e-mail consolidado...")
                smtp.send_message(msg)
                print("✅ E-mail de resumo massivo enviado com sucesso!\\n")
                    
        except Exception as e:
            print(f"Ocorreu um erro ao processar/enviar os e-mails: {e}")
