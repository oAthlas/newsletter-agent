import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório atual ao path para importar módulos locais
sys.path.insert(0, os.path.dirname(__file__))

from main import get_recent_newsletters

class TestMain(unittest.TestCase):
    @patch('main.load_dotenv')  # Mock load_dotenv para não sobrescrever environ
    @patch('main.MailBox')
    @patch.dict('os.environ', {
        'MAIL_USERNAME': 'test@gmail.com',
        'MAIL_PASSWORD': 'password',
        'NEWSLETTER_SENDERS': 'sender1@example.com, sender2@example.com'
    })
    def test_get_recent_newsletters(self, mock_mailbox, mock_load_dotenv):
        # Mock do MailBox e mensagens
        mock_mb = MagicMock()
        mock_mailbox.return_value.__enter__.return_value = mock_mb
        mock_msg = MagicMock()
        mock_msg.subject = 'Test Subject'
        mock_msg.date = '2023-01-01'
        mock_msg.html = '<p>Test HTML</p>'
        mock_mb.fetch.side_effect = lambda *args, **kwargs: [mock_msg]  # Sempre retorna a mensagem mockada

        # Executa a função
        result = get_recent_newsletters()

        # Verificações
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['subject'], 'Test Subject')
        print("✅ Teste de get_recent_newsletters passou!")

if __name__ == '__main__':
    unittest.main()