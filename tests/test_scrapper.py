import unittest
from unittest.mock import patch
from selenium import webdriver
from bs4 import BeautifulSoup
import environment
import scrapper


class TestScrapper(unittest.TestCase):
    def setUp(self):
        # Configuração inicial do ambiente de teste
        self.mock_browser = webdriver.Chrome()
        self.mock_browser.page_source = "<html><body></body></html>"

        # Substitui o browser real pelo browser simulado nos testes
        scrapper.browser = self.mock_browser

    def tearDown(self):
        # Restaura o browser original após os testes
        scrapper.browser = webdriver.Chrome("/home/vitor/Downloads/chromedriver")

    @patch("scrapper.seleciona_caixa_de_selecao")
    def test_seleciona_caixa_de_selecao(self, mock_selecao):
        # Testa se a função de seleção da caixa de seleção é chamada corretamente
        scrapper.seleciona_caixa_de_selecao("restaurante_teste")
        mock_selecao.assert_called_once_with("restaurante_teste")

    @patch("scrapper.encontra_cardapio")
    def test_pega_cardapio(self, mock_encontra_cardapio):
        # Testa se a função de pegar cardápio é chamada corretamente
        scrapper.pega_cardapio("restaurante_teste")
        mock_encontra_cardapio.assert_called_once()

    def test_encontra_cardapio(self):
        # Testa o comportamento da função quando o cardápio é encontrado
        self.mock_browser.page_source = '<html><body><ul id="carte"><li>Item 1</li><li>Item 2</li></ul></body></html>'
        self.assertTrue(scrapper.encontra_cardapio())

        # Testa o comportamento da função quando o cardápio não é encontrado
        self.mock_browser.page_source = "<html><body></body></html>"
        self.assertFalse(scrapper.encontra_cardapio())

    def test_pega_cardapio_exception(self):
        # Testa se a função lida corretamente com exceções
        with patch("scrapper.browser.get", side_effect=Exception("Teste de exceção")):
            result = scrapper.pega_cardapio("restaurante_teste")
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
