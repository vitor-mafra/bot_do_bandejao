from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import environment
import time


# configurando o browser
chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = True # nao queremos uma interface grafica
browser = webdriver.Chrome('/home/vitor/Downloads/chromedriver', \
                            options = chrome_options)


def seleciona_caixa_de_selecao(restaurante):
    '''
    Simula o clique de um usuario para selecionar o restaurante do cardapio que
    sera consultado. Faz a requisicao ao site da FUMP e, a partir desse ponto, 
    deixa as informacoes referentes ao cardapio no HTML da pagina
    '''
    caixa_de_selecao = browser.find_element_by_id(\
                                        "contentPlaceHolder_drpRestaurante")

    try:
        if restaurante == environment.restaurantes['RU_SETORIAL_I']:
            caixa_de_selecao.click()
            # como eh o segundo elemento da caixa de selecao, temos que enviar a
            # tecla "DOWN" uma vez
            caixa_de_selecao.send_keys(Keys.DOWN)

        elif restaurante == environment.restaurantes['RU_SETORIAL_II']:
            caixa_de_selecao.click()
            # terceiro elemento da caixa de selecao
            caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN)
                                                         
        elif restaurante == environment.restaurantes['RU_SAUDE_E_DIREITO']:         
            caixa_de_selecao.click()                     
            # quarto elemento da caixa de selecao
            caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN, Keys.DOWN)     
                                                        
        elif restaurante == environment.restaurantes['RU_ICA']:
            caixa_de_selecao.click()
            # quinto elemento da caixa de selecao
            caixa_de_selecao.send_keys(Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN)

        # enfim, confirma a selecao
        caixa_de_selecao.send_keys(Keys.ENTER)

    except:
        print("Erro ao selecionar a caixa de selecao!")


def encontra_cardapio():
    '''
    Procura no HTML da pagina pelo cardapio do restaurante e almoco em questao.
    Armazena a lista encontrada em um dicionario com cada um dos. Retorna um 
    booleano que indica se o cardapio foi ou nao encontrado
    '''
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # cardapio eh uma lista que esta dentro de uma tag <ul> cujo id eh "carte"
    carte = soup.find('ul', {'id' : 'carte'})
    cardapio = []

    if carte != None:
        # Porem, essa tag contem tb outras infos - portanto navegamos por 
        # outras tags internas (pois ja garantimos que o cardapio existe)
        
        if environment.almoco:
            carte = soup.find('ul', {'id' : 'carte'}).find('ul')

        elif environment.jantar:
            carte = soup.find('ul', {'id' : 'carte'}).\
                find('li', {'class' : 'marginTop10'}).find('ul')
            
        # armazenando o texto de "carte" na lista "cardapio" 
        for elemento in carte.find_all('li'):
            cardapio.append(elemento.get_text())

        # colocando o cardapio do restaurante (uma lista) dentro de cada um dos
        # itens do dicionario que armazena o cardapio
        environment.cardapio.update(dict(zip(environment.cardapio, cardapio)))

        encontrou_cardapio = True
    
    else:
        # Tuita erro ao encontrar o cardapio
        print("Cardapio inexistente!")

        # garante que o dicionario nao tera valores atribuidos (possivelmente
        # valores dos cardapios anteriores
        environment.cardapio = environment.cardapio.fromkeys(\
                                                    environment.cardapio, '')

        encontrou_cardapio = False

    return encontrou_cardapio


def pega_cardapio(restaurante):
    '''
    Junta todos os metodos necessarios para acessar a pagina da fump,
    selecionar os restaurantes e retirar os dados de cada cardapio
    '''
    browser.get(environment.site_fump)
    seleciona_caixa_de_selecao(restaurante)
    encontrou_cardapio = encontra_cardapio()
    print(environment.cardapio)
    
    return encontrou_cardapio

