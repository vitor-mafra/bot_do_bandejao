import unittest
from unittest.mock import patch
from tweet import (
    get_keys,
    set_API,
    tweeta,
    elabora_tweet,
    confere_tweet,
)


class TestTweetModule(unittest.TestCase):
    @patch("builtins.open", create=True)
    def test_get_keys(self):
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readline.side_effect = [
                "CONSUMER_KEY\n",
                "CONSUMER_SECRET\n",
                "ACCESS_KEY\n",
                "ACCESS_SECRET\n",
            ]

            keys = {}
            get_keys(keys)

            expected_keys = {
                "CONSUMER_KEY": "CONSUMER_KEY",
                "CONSUMER_SECRET": "CONSUMER_SECRET",
                "ACCESS_KEY": "ACCESS_KEY",
                "ACCESS_SECRET": "ACCESS_SECRET",
            }

            self.assertDictEqual(keys, expected_keys)

    def test_set_API(self):
        # Testa se a função set_API configura corretamente a API do tweepy
        keys = {
            "CONSUMER_KEY": "test_consumer_key",
            "CONSUMER_SECRET": "test_consumer_secret",
            "ACCESS_KEY": "test_access_key",
            "ACCESS_SECRET": "test_access_secret",
        }
        api = set_API(keys)

        self.assertIsNotNone(api)

    def test_tweeta(self):
        # Testa se a função tweeta publica o tweet corretamente
        api = unittest.mock.Mock()
        texto_tweet = "Testando a função tweeta"
        mais_280_caracteres = False

        with patch("builtins.print") as mock_print:
            tweeta(api, texto_tweet, mais_280_caracteres)
            mock_print.assert_called_with("Tweet publicado com sucesso!")

        api.update_status.assert_called_once_with(texto_tweet)

    def test_elabora_tweet(self):
        # Testa se a função elabora_tweet gera o tweet esperado
        restaurante = "RU_SETORIAL_I"
        cardapio = {
            "proteina_1": "Frango",
            "proteina_2": "Peixe",
            "guarnicao": "Arroz",
            "sobremesa_1": "Pudim",
            "sobremesa_2": "Frutas",
        }
        almoco = True
        jantar = False

        tweet = elabora_tweet(restaurante, cardapio, almoco, jantar)

        expected_tweet = (
            "Cardápio RU Setorial I - Almoço\n\n"
            "Frango\nPeixe\n\n"
            "Arroz\n\n"
            "Pudim\nFrutas\n"
        )
        self.assertEqual(tweet, expected_tweet)

    def test_confere_tweet(self):
        tweet = "Cardápio RU Setorial I - Almoço\n\nFrango\nPeixe\n\nArroz\n\nPudim\nFrutas\n"
        novo_tweet, mais_280_caracteres = confere_tweet(tweet)

        expected_novo_tweet = "Cardápio RU Setorial I - Almoço ⚠️\n\nFrango\nPeixe\n\nArroz\n\nPudim\nFrutas\n"
        self.assertEqual(novo_tweet, expected_novo_tweet)
        self.assertTrue(mais_280_caracteres)


if __name__ == "__main__":
    unittest.main()
