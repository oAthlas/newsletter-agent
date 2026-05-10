from main import get_recent_newsletters
import os
from dotenv import load_dotenv
from google import genai
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Carrega as variáveis de ambiente
load_dotenv()

# Coleta as newsletters recentes (apenas quando executado diretamente)
if __name__ == "__main__":
    newsletters = get_recent_newsletters()

def resumir_todas_newsletters(textos_combinados):
    # Inicializa o cliente do Google Gemini para geração de conteúdo
    client = genai.Client()

    prompt = (
        "Aqui estão várias newsletters recebidas hoje. "
        "Crie um resumo conceitual e visual, focando nos insights principais, tópicos chave e tendências. "
        "Estruture em HTML puro com: "
        "- Headings curtos e descritivos (<h1>, <h2>). "
        "- Listas com bullets (<ul>, <li>) para pontos-chave. "
        "- Emojis para destacar seções (ex.: 📈 para tendências, 📰 para notícias). "
        "- Mantenha conciso: máximo 8-10 tópicos principais, evitando texto excessivo. "
        "- Use CSS inline ou <style> para aumentar o tamanho da fonte (ex.: body { font-size: 18px; line-height: 1.6; }). "
        "Agrupe por temas lógicos para uma leitura rápida e impactante. "
        "Entregue em português-BR, apenas HTML limpo e pronto para e-mail (sem ```html). "
        f"Conteúdo das newsletters:\n{textos_combinados}"
    )

    # Envia o prompt para o modelo Gemini e obtém a resposta
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text

if __name__ == "__main__":
    
    # -----------------------= SEND MODULE =------------------------
    
    # Obtém as credenciais de e-mail das variáveis de ambiente
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
    
    if not newsletters:
        print("❌ Nenhuma newsletter encontrada para resumir hoje.")
    else:
        try:
            print(f"🔄 Combinando {len(newsletters)} newsletters para resumo massivo...")
            textos_combinados = ""
            for news in newsletters:
                textos_combinados += f"\\n\\n--- INÍCIO DA NEWSLETTER: {news['subject']} ---\\n"
                textos_combinados += news["text"]
                textos_combinados += f"\\n--- FIM DA NEWSLETTER: {news['subject']} ---\\n"
                
            print("🤖 Enviando conteúdo para o Gemini gerar o resumo centralizado...")
            resumo_geral = resumir_todas_newsletters(textos_combinados)
            print("✅ Resumo gerado com sucesso pelo Gemini.")
            
            # Conecta ao servidor SMTP do Gmail para envio
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                print("📤 Conectado ao SMTP. Preparando e-mail...")
                
                msg = EmailMessage()
                hoje = datetime.now().strftime("%d/%m/%Y")
                msg["Subject"] = f"[Resumo Diário] Newsletters de {hoje}"
                msg["From"] = MAIL_USERNAME
                msg["To"] = MAIL_ADDRESS
                
                # Define o corpo alternativo para clientes que não suportam HTML
                msg.set_content("Seu cliente de e-mail não suporta exibição de HTML. O resumo foi gerado, mas precisa ser lido num formato compatível.")
                
                # Adiciona o resumo em HTML como alternativa principal
                msg.add_alternative(resumo_geral, subtype='html')
                
                print("📧 Enviando e-mail consolidado...")
                smtp.send_message(msg)
                print("✅ E-mail de resumo enviado com sucesso!\\n")
                    
        except Exception as e:
            print(f"❌ Ocorreu um erro ao processar/enviar os e-mails: {e}")
