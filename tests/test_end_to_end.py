import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import main
import scrapper
import tweet
import environment


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("/home/vitor/Downloads/chromedriver")

    def tearDown(self):
        self.browser.quit()

    def test_tweet_integration(self):
        # Este teste verifica se o processo de tweet é bem-sucedido até o fim
        restaurante = environment.restaurantes["RU_SETORIAL_I"]
        scrapper.pega_cardapio = lambda x: True  # Simula que o cardápio foi encontrado
        tweet.setup_for_tweet = lambda x: tweet.set_API(
            environment.keys
        )  # Simula a configuração da API do Twitter

        with self.assertLogs() as log:
            main.processa_restaurante(restaurante)

        self.assertTrue("Tweet publicado com sucesso!" in log.output[0])


if __name__ == "__main__":
    unittest.main()
