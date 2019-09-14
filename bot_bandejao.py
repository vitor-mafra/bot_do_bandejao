import tweepy
#from urllib.request import urlopen
#from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #apenas pra facilitar a leitura do codigo
import time


#"constantes" - bem, talvez nao exatamente
    #chaves geradas pelo app do twitter
CONSUMER_KEY = '**********************'
CONSUMER_SECRET = '*************************'
ACCESS_KEY = '************-**********************'
ACCESS_SECRET = '*************************'
    #paginas web necessarias para buscar o cardapio
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"
    #restaurantes
RU_SETORIAL_I = 1
RU_SETORIAL_II = 2
RU_SAUDE_E_DIREITO = 3
RU_ICA = 4
restaurantes = (RU_SETORIAL_I, RU_SETORIAL_II, RU_SAUDE_E_DIREITO, RU_ICA)

#setting webbrowser
browser = webdriver.Firefox()
    
#setting API (https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#comunicacao com a API do twitter para poder ler e escrever tweets
api = tweepy.API(auth)


def pega_cardapio(site_fump, restaurante):
    #tentando abrir o site da fump
    acessa_site_fump(site_fump)

    #tentando selecionar o restaurante da caixa de selecao
    seleciona_caixa_de_selecao(restaurante)

    #procurando os itens cardapio
    '''try:
        encontrando_cardapio()
    except:
        print("Erro ao encontrar o cardapio!")
    '''
    browser.quit()
    ####################return cardapio


def acessa_site_fump(site_fump):
    #tentando abrir o site da fump
    try:
        browser.get(site_fump)
    except:
        print("Erro ao tentar abrir o site da Fump!")


def seleciona_caixa_de_selecao(restaurante):
    caixa_de_selecao = browser.find_element_by_name("ctl00$contentPlaceHolder$drpRestaurante") #nome da caixa de selecao no site
    
    try:        
        if restaurante == RU_SETORIAL_I:
            caixa_de_selecao.click() 
            caixa_de_selecao.send_keys('r')             # Por algum motivo desconhecido, tentar enviar a tecla DOWN mais de uma
            caixa_de_selecao.send_keys(Keys.ENTER)      # vez nao estava funcionando. Nao sei se essa eh uma limitacao ou bug da
                                                        # biblioteca, ou se tem algo a ver com o site. Tentei navegar por esse 
        elif restaurante == RU_SETORIAL_II:             # select de todas as formas obvias e fazendo algumas variacoes. Por sorte
            caixa_de_selecao.click()                    # descobri que apertar a tecla R navegava pelo menu. Eh exatamente isso que
            caixa_de_selecao.send_keys('r', 'r')        # esta sendo feito aqui. Como todas as opcoes de restaurantes universitarios
            caixa_de_selecao.send_keys(Keys.ENTER)      # comecam com "RU", apertar a tecla R navega por cada uma dessas opcoes - da 
                                                        # primeira `a ultima. Muito obrigado ao @gnus e ao @jottagpg por terem me 
        elif restaurante == RU_SAUDE_E_DIREITO:         # explicado o que eu tinha feito e nao sabia muito bem como funcionava hahaha
            caixa_de_selecao.click()                     
            caixa_de_selecao.send_keys('r', 'r', 'r')     
            caixa_de_selecao.send_keys(Keys.ENTER)       
                                                        
        elif restaurante == RU_ICA:                     
            caixa_de_selecao.click()
            caixa_de_selecao.send_keys('r', 'r', 'r', 'r')
            caixa_de_selecao.send_keys(Keys.ENTER)

        time.sleep(5) #tempo pra garantir que o cardapio do restaurante carregue
    except:
        print("Erro ao selecionar a caixa de selecao!")
    

def encontra_cardapio():
    soup = BeautifulSoup(html.read(), 'html.parser')
    #cardapio = (soup.select('ul')) 

#tweetando (ou ao menos tentando)
def faz_tweet(restaurante, almoco_ou_jantar, cardapio):
    if restaurante ==  RU_SETORIAL_I:
        string_restaurante = "Cardapio RU Setorial I - "

    elif restaurante == RU_SETORIAL_II:
        string_restaurante = "Cardapio RU Setorial II - "

    elif restaurante == RU_SAUDE_E_DIREITO:
        string_restaurante = "Cardapio Saude e Direito - "
    
    elif restaurante == RU_ICA:
        string_restaurante = "Cardapio RU ICA - "

    tweet = string_restaurante + almoco_ou_jantar + '\n\n' + cardapio

    try:
        api.update_status(tweet)
        print("Tweet publicado com sucesso!")
    except:
        print("Erro ao tweetar!")
    



pega_cardapio(site_fump, RU_SETORIAL_I)

#acessando o cardapio do bandejao
'''almoco_ou_jantar = "almoco"
'''

#verificacao se o cardapio esta pronto para ser tweetado
'''if (cardapio == None):
   print("Erro ao tentar encontrar o cardapio")
   #tweet = "Tive problemas ao acessar o cardapio, tentarei novamente mais tarde"
else:
    print(cardapio)
    #tweet = cardapio
'''

'''for restaurante in restaurantes:
    cardapio = pega_cardapio(site_fump, restaurante)
    faz_tweet(restaurante, almoco_ou_jantar,cardapio)
'''










# get_text()    IMPORTANTE, LIMPA AS TAGS E PEGA SOMENTE O TEXTO