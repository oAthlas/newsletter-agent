from app import get_recent_newsletters
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Lendo o arquivo de texto
with open("teste.txt", "r", encoding="utf-8") as f:
    teste_llm = f.read()

def resumir_newsletter(texto):
    # O Client do genai puxa automaticamente a variável GEMINI_API_KEY do seu .env
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash", # ou gemini-1.5-flash caso dê erro de modelo não encontrado
        contents="Resuma este texto:\n" + texto,
    )

    print(response.text)

if __name__ == "__main__":
    resumir_newsletter(teste_llm)
