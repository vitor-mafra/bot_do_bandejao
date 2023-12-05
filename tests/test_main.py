import unittest
from unittest.mock import patch, Mock
from main import main, processa_restaurante


class TestMain(unittest.TestCase):
    @patch("scrapper.browser.close")
    @patch("scrapper.pega_cardapio", return_value=True)
    @patch("tweet.elabora_tweet", return_value="Texto do Tweet")
    @patch("tweet.setup_for_tweet", return_value=Mock())
    @patch("tweet.confere_tweet", return_value=("Texto do Tweet modificado", False))
    @patch("tweet.tweeta")
    def test_main_successful_tweet(
        self,
        mock_tweeta,
        mock_confere_tweet,
        mock_setup_for_tweet,
        mock_elabora_tweet,
        mock_pega_cardapio,
        mock_browser_close,
    ):
        environment = {
            "restaurantes": ["Restaurante1"],
            "cardapio": "Cardapio",
            "almoco": "Almoco",
            "jantar": "Jantar",
            "keys": "Keys",
        }
        with patch.dict("environment.__dict__", environment):
            main()

        mock_pega_cardapio.assert_called_once_with("Restaurante1")
        mock_elabora_tweet.assert_called_once_with(
            "Restaurante1", "Cardapio", "Almoco", "Jantar"
        )
        mock_setup_for_tweet.assert_called_once_with("Keys")
        mock_confere_tweet.assert_called_once_with("Texto do Tweet")
        mock_tweeta.assert_called_once_with(
            mock_setup_for_tweet.return_value, "Texto do Tweet", False
        )
        mock_browser_close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
