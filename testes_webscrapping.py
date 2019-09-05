from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

site_fump = "http://www.fump.ufmg.br/cardapio.aspx"
RU_SETORIAL_I = 1
RU_SETORIAL_II = 2
RU_SAUDE_E_DIREITO = 3
RU_ICA = 4
#restaurantes = [RU_SETORIAL_I, RU_SETORIAL_II, RU_SAUDE_E_DIREITO, RU_ICA]

browser = webdriver.Firefox()
browser.get(site_fump)

def caixa_de_selecao(restaurante):
    caixa_de_selecao = browser.find_element_by_name("ctl00$contentPlaceHolder$drpRestaurante")

    if restaurante == RU_SETORIAL_I:
        caixa_de_selecao.click()
        caixa_de_selecao.click()
        caixa_de_selecao.send_keys(Keys.DOWN)

    elif restaurante == RU_SETORIAL_II:
        caixa_de_selecao.click()
        caixa_de_selecao.click()
        caixa_de_selecao.send_keys(Keys.DOWN)
        caixa_de_selecao.send_keys(Keys.DOWN)

    elif restaurante == RU_SAUDE_E_DIREITO:
        caixa_de_selecao.click()
        caixa_de_selecao.click()
        caixa_de_selecao.send_keys(Keys.DOWN)
        caixa_de_selecao.send_keys(Keys.DOWN)
        caixa_de_selecao.send_keys(Keys.DOWN)

    elif restaurante == RU_ICA:
        caixa_de_selecao.click()
        caixa_de_selecao.click()
        caixa_de_selecao.send_keys(Keys.DOWN)
        caixa_de_selecao.send_keys(Keys.DOWN)
        caixa_de_selecao.send_keys(Keys.DOWN)
        caixa_de_selecao.send_keys(Keys.DOWN)


restaurante = RU_ICA
caixa_de_selecao(restaurante)

#print(clique_caixa_de_selecao)
#caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN)


time.sleep(5)
browser.quit()


#def pega_cardapio(site_fump):
#    #tentando abrir o site da fump
#   try:
#        html = urlopen(site_fump)
#    except HTTPError as erro:
#        return None
#    
#    #procurando os itens cardapio
#    try:
#        soup = BeautifulSoup(html.read(), 'html.parser')
#        #cardapio = Select(browser.find_element_by_id(6))
#        cardapio = (soup.find('li')) #  <---------------------------  #
#    except AttributeError as erro:
#        return None
#
#    return cardapio



#cardapio = pega_cardapio(site_fump)



#if (cardapio == None):
#   print("Erro ao tentar encontrar o cardapio")
#else:
#    print(cardapio)
