import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import main
import scrapper
import tweet
import environment


class TestIntegration(unittest.TestCase):
    def test_processa_restaurante(self):
        restaurante = environment.restaurantes["RU_SETORIAL_I"]
        scrapper.pega_cardapio = lambda x: True  # Simula que o cardápio foi encontrado
        tweet.setup_for_tweet = (
            lambda x: None
        )  # Simula a configuração da API do Twitter

        with self.assertLogs() as log:
            main.processa_restaurante(restaurante)

        self.assertTrue("Tudo certo!" in log.output[0])

    def test_pega_cardapio(self):
        scrapper.browser.get(environment.site_fump)
        restaurante = environment.restaurantes["RU_SETORIAL_I"]

        with self.assertLogs() as log:
            scrapper.pega_cardapio(restaurante)

        self.assertTrue("Cardápio RU Setorial I" in log.output[0])


if __name__ == "__main__":
    unittest.main()
