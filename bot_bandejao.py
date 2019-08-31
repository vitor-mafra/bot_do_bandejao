import tweepy
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

#"constantes" - bem, talvez nao exatamente
    #chaves geradas pelo app do twitter
CONSUMER_KEY = '7AhJo1deDf791kzPaYi2oATAN'
CONSUMER_SECRET = 'rxG8gFspxJ7TRYua4ARr6iQggYmA2lht3x4cU4uj2cf5TxkHa6'
ACCESS_KEY = '1166732818363428864-mQYEY9FXAtm1cyCxVvgFNjyDpDPzK1'
ACCESS_SECRET = 'kiGvXlPXunSZs4LJpTeYA9Oao1wFdgCZM5vMANoAqgg44'
    #paginas web necessarias para buscar o cardapio
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"


#def seleciona_opcoes_cardapio_site_fump(site_fump):


def pega_cardapio(site_fump):
    #tentando abrir o site da fump
    try:
        html = urlopen(site_fump)
    except HTTPError as erro:
        return None

    #procurando os itens cardapio
    try:
        soup = BeautifulSoup(html.read(), 'html.parser')
        cardapio = (soup.find(id = 'carte'))
        cardapio = soup.find('body')
    except AttributeError as erro:
        return None

    return cardapio


#tweetando (ou ao menos tentando)
def faz_tweet(tweet):
        api.update_status(tweet)
        print("Tweet publicado com sucesso!")
    

#setting API (https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#comunicacao com a API do twitter para poder ler e escrever tweets
api = tweepy.API(auth)


#acessando o cardapio do bandejao
###cardapio = pega_cardapio(site_fump)

#verificacao se o cardapio esta pronto para ser tweetado
##if (cardapio == None):
##   print("Erro ao tentar encontrar o cardapio")
##else:
##    print(cardapio.get_text())

tweet = "Como funciono?\
\
🐍\
 Fui programado em Python e o repositório com o meu código se encontra na descrição desse perfil\
\
🤖\
 Busco os cardápios no site da Fump\
\
⛔\
 Fui desenvolvido por um aluno da UFMG e, portanto, não possuo nenhum vínculo oficial com a universidade ou seus órgãos"
faz_tweet(tweet)


#print(soup.findAll('li'))


# get_text()    IMPORTANTE, LIMPA AS TAGS E PEGA SOMENTE O TEXTO