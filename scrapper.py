from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import environment
import time


# configurando o browser
chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = True  # nao queremos uma interface grafica
browser = webdriver.Chrome("/home/vitor/Downloads/chromedriver", options=chrome_options)


def seleciona_caixa_de_selecao(restaurante):
    """
    Simula o clique de um usuário para selecionar o restaurante do cardápio que
    será consultado. Faz a requisição ao site da FUMP e, a partir desse ponto,
    deixa as informações referentes ao cardápio no HTML da página
    """
    caixa_de_selecao = browser.find_element_by_id("contentPlaceHolder_drpRestaurante")

    try:
        teclas_down = environment.restaurantes[restaurante]
        caixa_de_selecao.click()

        for _ in range(teclas_down):
            caixa_de_selecao.send_keys(Keys.DOWN)

        caixa_de_selecao.send_keys(Keys.ENTER)

    except Exception as e:
        print(f"Erro ao selecionar a caixa de seleção: {e}")


def encontra_cardapio():
    """
    Procura no HTML da página pelo cardápio do restaurante e almoço em questão.
    Armazena a lista encontrada em um dicionário com cada um dos itens.
    Retorna um booleano que indica se o cardápio foi ou não encontrado
    """
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Cardápio é uma lista que está dentro de uma tag <ul> cujo id é "carte"
    carte = soup.find("ul", {"id": "carte"})
    cardapio = []

    if carte:
        # A tag <ul> contém outras informações, navegamos por outras tags internas

        if environment.almoco:
            carte = soup.find("ul", {"id": "carte"}).find("ul")
        elif environment.jantar:
            carte = (
                soup.find("ul", {"id": "carte"})
                .find("li", {"class": "marginTop10"})
                .find("ul")
            )

        # Armazenando o texto de "carte" na lista "cardapio"
        cardapio = [elemento.get_text() for elemento in carte.find_all("li")]

        # Atualizando o dicionário de cardápio
        environment.cardapio.update(dict(zip(environment.cardapio, cardapio)))

        encontrou_cardapio = True
    else:
        print("Cardápio inexistente!")
        # Reinicializando o dicionário para evitar valores de cardápios anteriores
        environment.cardapio = environment.cardapio.fromkeys(environment.cardapio, "")
        encontrou_cardapio = False

    return encontrou_cardapio


def pega_cardapio(restaurante):
    """
    Junta todos os métodos necessários para acessar a página da FUMP,
    selecionar os restaurantes e retirar os dados de cada cardápio
    """
    try:
        browser.get(environment.site_fump)
        seleciona_caixa_de_selecao(restaurante)
        encontrou_cardapio = encontra_cardapio()
        print(environment.cardapio)

        return encontrou_cardapio
    except Exception as e:
        print(f"Erro ao processar restaurante {restaurante}: {e}")
        return False
