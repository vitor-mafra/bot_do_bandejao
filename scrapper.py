from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from environment import restaurantes
import environment
import time


# configurando o browser
chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = False # nao precisamos e nem queremos uma interface grafica
browser = webdriver.Chrome('/home/vitor/Downloads/chromedriver', options = chrome_options)


def acessa_site_fump(site_fump):

    #try:
    browser.get(environment.site_fump)
    #except expression as identifier:
    #   pass



def seleciona_caixa_de_selecao(restaurante):

    caixa_de_selecao = browser.find_element_by_id("contentPlaceHolder_drpRestaurante") # nome da caixa de selecao no site

    try:
        if restaurante == 'RU_SETORIAL_I':
            caixa_de_selecao.click()
            # como eh o segundo elemento da caixa de selecao, temos que enviar a
            # tecla "DOWN" uma vez
            caixa_de_selecao.send_keys(Keys.DOWN)
            caixa_de_selecao.send_keys(Keys.ENTER)

        elif restaurante == 'RU_SETORIAL_II':
            caixa_de_selecao.click()
            # terceiro elemento da caixa de selecao
            caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN)
            caixa_de_selecao.send_keys(Keys.ENTER)
                                                         
        elif restaurante == 'RU_SAUDE_E_DIREITO':         
            caixa_de_selecao.click()                     
            # quarto elemento da caixa de selecao
            caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN, Keys.DOWN)     
            caixa_de_selecao.send_keys(Keys.ENTER)
                                                        
        elif restaurante == 'RU_ICA':
            caixa_de_selecao.click()
            # quinto elemento da caixa de selecao
            caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN, Keys.DOWN,Keys.DOWN)
            caixa_de_selecao.send_keys(Keys.ENTER)

        time.sleep(2) #  tempo pra garantir que o cardapio do restaurante carregue
        #browser.close()

    except:
        print("Erro ao selecionar a caixa de selecao!\n")



def pega_cardapio(site_fump, restaurante):
    acessa_site_fump(environment.site_fump)
    seleciona_caixa_de_selecao(restaurante)


for restaurante in restaurantes:
    acessa_site_fump(environment.site_fump)
    seleciona_caixa_de_selecao(restaurante)
