import tweepy
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#"constantes" - bem, talvez nao exatamente
    #chaves geradas pelo app do twitter
CONSUMER_KEY = '**********************'
CONSUMER_SECRET = '********************************************'
ACCESS_KEY = '**********************-**********************'
ACCESS_SECRET = '********************************************'
    #paginas web necessarias para buscar o cardapio
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"
    #restaurantes
RU_SETORIAL_I = 1
RU_SETORIAL_II = 2
RU_SAUDE_E_DIREITO = 3
RU_ICA = 4

restaurantes = (RU_SETORIAL_I, RU_SETORIAL_II, RU_SAUDE_E_DIREITO, RU_ICA)

#setting API (https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#comunicacao com a API do twitter para poder ler e escrever tweets
api = tweepy.API(auth)
#setting webbrowser
browser = webdriver.Firefox()


def pega_cardapio(site_fump, restaurante):
    #tentando abrir o site da fump
    acessa_site_fump()

    #tentando o restaurante da caixa de selecao
    try:
        seleciona_caixa_de_selecao(restaurante)
    except:
        print("Erro ao selecionar a caixa de selecao!")

    #procurando os itens cardapio
    try:
        encontrando_cardapio()
    except:
        print("Erro ao encontrar o cardapio!")
        
    return cardapio


def acessa_site_fump(site_fump):
    #tentando abrir o site da fump
    try:
        browser.get(site_fump)
    except:
        print("Erro ao tentar abrir o site da Fump!")


def seleciona_caixa_de_selecao(restaurante):
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


def encontrando_cardapio():
    soup = BeautifulSoup(html.read(), 'html.parser')
    #cardapio = (soup.select('ul')) 


#tweetando (ou ao menos tentando)
def faz_tweet(restaurante, almoco_ou_jantar, cardapio):
    if restaurante ==  RU_SETORIAL_I:
        string_restaurante = "Cardapio RU Setorial I"

    elif restaurante == RU_SETORIAL_II:
        string_restaurante = "Cardapio RU Setorial II"

    elif restaurante == RU_SAUDE_E_DIREITO:
        string_restaurante = "Cardapio Saude e Direito"
    
    elif restaurante == RU_ICA:
        string_restaurante = "Cardapio RU ICA"

    tweet = string_restaurante + almoco_ou_jantar + cardapio

    try:
        api.update_status(tweet)
        print("Tweet publicado com sucesso!")
    except AttributeError as erro:
        print("Erro ao tweetar!")
    

#acessando o cardapio do bandejao
almoco_ou_jantar = "almoco"

#verificacao se o cardapio esta pronto para ser tweetado
if (cardapio == None):
   print("Erro ao tentar encontrar o cardapio")
   #tweet = "Tive problemas ao acessar o cardapio, tentarei novamente mais tarde"
else:
    print(cardapio)
    #tweet = cardapio


for restaurante in restaurantes:
    cardapio = pega_cardapio(site_fump, restaurante)
    faz_tweet(restaurante, almoco_ou_jantar,cardapio)


#verificacao se o cardapio esta pronto para ser tweetado
if (cardapio == None):
   print("Erro ao tentar encontrar o cardapio")
   #tweet = "Tive problemas ao acessar o cardapio, tentarei novamente mais tarde"
else:
    print(cardapio)
    #tweet = cardapio



# get_text()    IMPORTANTE, LIMPA AS TAGS E PEGA SOMENTE O TEXTO