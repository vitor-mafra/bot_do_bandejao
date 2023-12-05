import unittest
from unittest.mock import patch, MagicMock
from tweet import (
    get_keys,
    set_API,
    setup_for_tweet,
    tweeta,
    elabora_tweet,
    confere_tweet,
)


class TestTwitterBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup initial environment, if needed
        pass

    def test_get_keys(self):
        # Mock the open function to return a predefined content
        with patch(
            "builtins.open", return_value=MagicMock(readline=lambda: "mock_key")
        ):
            environment = {"keys": {}}
            get_keys(environment)
            self.assertEqual(environment["keys"]["some_key"], "mock_key")

    def test_set_API(self):
        # Mock the tweepy.OAuthHandler and tweepy.API calls
        with patch("tweepy.OAuthHandler") as mock_oauth_handler, patch(
            "tweepy.API"
        ) as mock_api:
            environment = {
                "keys": {
                    "CONSUMER_KEY": "key1",
                    "CONSUMER_SECRET": "secret1",
                    "ACCESS_KEY": "key2",
                    "ACCESS_SECRET": "secret2",
                }
            }
            set_API(environment)
            mock_oauth_handler.assert_called_once_with("key1", "secret1")
            mock_oauth_handler.return_value.set_access_token.assert_called_once_with(
                "key2", "secret2"
            )
            mock_api.assert_called_once()

    def test_setup_for_tweet(self):
        # Test if setup_for_tweet calls get_keys and set_API
        with patch("your_script_file.get_keys") as mock_get_keys, patch(
            "your_script_file.set_API"
        ) as mock_set_API:
            environment = {"keys": {}}
            setup_for_tweet(environment)
            mock_get_keys.assert_called_once_with(environment)
            mock_set_API.assert_called_once_with(environment)

    def test_tweeta(self):
        # Mock the tweepy.API.update_status call
        with patch("tweepy.API") as mock_api:
            tweeta(mock_api, "Test tweet", False)
            mock_api.update_status.assert_called_once_with("Test tweet")

    def test_elabora_tweet(self):
        # Test if elabora_tweet generates the correct tweet
        cardapio = {
            "proteina_1": "Frango",
            "proteina_2": "Peixe",
            "guarnicao": "Arroz",
            "sobremesa_1": "Pudim",
            "sobremesa_2": "Gelatina",
        }
        tweet = elabora_tweet("RU_SETORIAL_I", cardapio, almoco=True, jantar=False)
        expected_tweet = "Cardápio RU Setorial I - Almoço\n\nFrango\nPeixe\nArroz\n\nPudim\nGelatina\n"
        self.assertEqual(tweet, expected_tweet)

    def test_confere_tweet(self):
        # Test if confere_tweet adds a warning emoji when necessary
        tweet = "Cardápio RU Setorial I - Almoço\n\nFrango\nPeixe\nArroz\n\nPudim\nGelatina\n"
        modified_tweet, over_280_chars = confere_tweet(tweet)
        expected_modified_tweet = "Cardápio RU Setorial I - Almoço ⚠️\n\nFrango\nPeixe\nArroz\n\nPudim\nGelatina\n"
        self.assertEqual(modified_tweet, expected_modified_tweet)
        self.assertFalse(over_280_chars)


if __name__ == "__main__":
    unittest.main()
