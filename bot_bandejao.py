import tweepy
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

#chaves geradas pelo app do twitter
CONSUMER_KEY = '*****************************************'
CONSUMER_SECRET = '*****************************************'
ACCESS_KEY = '*****************************************'
ACCESS_SECRET = '*****************************************'

#site da fump
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"

def pega_cardapio(site_fump):
    #tentando abrir o site da fump
    try:
        html = urlopen(site_fump)
    except HTTPError as error:
        return None

    #procurando os itens cardapio
    try:
        soup = BeautifulSoup(html.read(), 'html.parser')
        cardapio = (soup.body.a)
    except AttributeError as error:
        return None

    return cardapio
    

#setting API (https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

#comunicacao com a API do twitter para poder ler e escrever tweets
api = tweepy.API(auth)

#acessando e imprimindo o titulo da pagina do cardapio do bandejao
cardapio = pega_cardapio(site_fump)

#verificacao se o cardapio esta pronto para ser tweetado
if cardapio == None:
    print("Erro ao tentar encontrar o cardapio")
else:
    print(cardapio)
    #tweetando (ou ao menos tentando)
    try:
        api.update_status()
        print("Tweet publicado com sucesso!")
    except: 
        print("Erro ao tweetar!")


#print(soup.find_all('li'))