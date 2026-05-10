import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

from llm import resumir_todas_newsletters

class TestLLM(unittest.TestCase):
    @patch('llm.genai.Client')
    def test_resumir_todas_newsletters(self, mock_client):
        # Mock do cliente Gemini
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_response = MagicMock()
        mock_response.text = '<h1>Resumo Teste</h1><p>Conteúdo resumido.</p>'
        mock_instance.models.generate_content.return_value = mock_response

        # Texto de teste
        textos_teste = "Conteúdo de teste das newsletters."

        # Executa a função
        result = resumir_todas_newsletters(textos_teste)

        # Verificações
        self.assertIn('<h1>Resumo Teste</h1>', result)
        print("✅ Teste de resumir_todas_newsletters passou!")

if __name__ == '__main__':
    unittest.main()