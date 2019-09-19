import tweepy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #apenas pra facilitar a leitura do codigo
import time
import datetime


#"constantes" - bem, talvez nao exatamente
    #chaves geradas pelo app do twitter
CONSUMER_KEY = '******************'
CONSUMER_SECRET = '************************************'
ACCESS_KEY = '******************-******************'
ACCESS_SECRET = '************************************'
    #paginas web necessarias para buscar o cardapio
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"
    #restaurantes
RU_SETORIAL_I = 1
RU_SETORIAL_II = 2
RU_SAUDE_E_DIREITO = 3
RU_ICA = 4
restaurantes_almoco_seg_sex = (RU_SETORIAL_I, RU_SETORIAL_II, RU_SAUDE_E_DIREITO, RU_ICA)
restaurantes_almoco_sab = (RU_SETORIAL_I, RU_SAUDE_E_DIREITO, RU_ICA)
restaurantes_jantar_seg_sab = (RU_SETORIAL_I, RU_SAUDE_E_DIREITO, RU_ICA)

#setting webbrowser
browser = webdriver.Firefox()
    
#setting API (https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#comunicacao com a API do twitter para poder ler e escrever tweets
api = tweepy.API(auth)


def pega_cardapio(site_fump, restaurante, almoco, jantar):
    #tentando abrir o site da fump
    acessa_site_fump(site_fump)

    #tentando selecionar o restaurante da caixa de selecao
    seleciona_caixa_de_selecao(restaurante)

    #procurando os itens cardapio
    cardapio = encontra_cardapio(almoco, jantar)
        
    return cardapio


def acessa_site_fump(site_fump):
    #tentando abrir o site da fump
    try:
        browser.get(site_fump)
    except:
        print("Erro ao tentar abrir o site da Fump!\n")


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
        print("Erro ao selecionar a caixa de selecao!\n")
    

def encontra_cardapio(almoco, jantar):

    cardapio_completo = browser.find_element_by_id('carte').text
    
    cardapio_lista = []

    for letra in cardapio_completo:
        cardapio_lista.append(letra)
    
    #print(cardapio_completo)
    
    count = 0
    cardapio_almoco_tratado = ''
    cardapio_jantar_tratado = ''

    if almoco:
        for letra in cardapio_lista:
            if letra == '\n':
                count += 1
            if count == 1 or count == 6:        # valores onde uma linha deve ser pulada para facilitar a separacao entre
                cardapio_almoco_tratado += '\n' # o titulo, proteinas + guarnicao, sobremesas
                count += 1
            if count < 7:              # itera ate a primeira parte do cardapio (titulo + proteinas + guarnicao)
                cardapio_almoco_tratado += letra 
            elif (count > 12) and (count <= 14):   # pula as partes que sao parte fixa do cardapio
                cardapio_almoco_tratado += letra   # itera pela parte das sobremesas
        return cardapio_almoco_tratado

    elif jantar:
        for letra in cardapio_lista:
            if letra == '\n':
                count += 1
            if count == 22:
                cardapio_jantar_tratado += '\n'
                count += 1
            if count == 17:                           # se pegar a string original fica "\nJantar", fiz isso provisoriamente
                cardapio_jantar_tratado += 'Jantar\n' # arrumar depois
            if count > 18 and count < 23:
                cardapio_jantar_tratado += letra
            elif count == 29:
               cardapio_jantar_tratado += letra
        return cardapio_jantar_tratado

#tweetando (ou ao menos tentando)
def faz_tweet(restaurante, cardapio):
    if restaurante ==  RU_SETORIAL_I:
        string_restaurante = "Cardapio RU Setorial I - "

    elif restaurante == RU_SETORIAL_II:
        string_restaurante = "Cardapio RU Setorial II - "
        
    elif restaurante == RU_SAUDE_E_DIREITO:
        string_restaurante = "Cardapio Saúde e Direito - "
    
    elif restaurante == RU_ICA:
        string_restaurante = "Cardapio RU ICA - "

    tweet = string_restaurante + cardapio
    print(tweet)
    
    #verificacao se o cardapio esta pronto para ser tweetado
    if (cardapio == None):
        print("Erro ao tentar encontrar o cardapio\n")
        tentar_novamente = True
        return tentar_novamente
        #tweet = "Tive problemas ao acessar o cardapio, tentarei novamente mais tarde"
    else:
        try:
            api.update_status(tweet)
            print("\n**********************\n")
            print("Tweet publicado com sucesso!\n")
        except:
            print("Erro ao tweetar!\n")
        
def vai_bot(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab):
    if almoco:
        for restaurante in restaurantes_almoco_seg_sex:
            cardapio = pega_cardapio(site_fump, restaurante, almoco, jantar)
            faz_tweet(restaurante, cardapio)
            #postou = True
    elif jantar:
        for restaurante in restaurantes_jantar_seg_sab:
            cardapio = pega_cardapio(site_fump, restaurante, almoco, jantar)
            faz_tweet(restaurante, cardapio)
            #postou = True
    
'''
seconds = time.time()
hora_local = time.ctime(seconds) 
print(hora_local)
'''
'''
agora = datetime.datetime.now()
horario_postagem_almoco = datetime.datetime.now.replace(hour = 9, minute = 0, second = 0, microsecond = 0)
horario_postagem_jantar = datetime.datetime.now.replace(hour = 17, minute = 0, second = 0, microsecond = 0)

if (agora >= horario_postagem_almoco) and (agora < horario_postagem_jantar):
    almoco = True
    jantar = False
    print("Almoco!")
elif (agora >= horario_postagem_jantar):
    almoco = False
    jantar = True
    print('Jantar!')
'''
almoco = True
jantar = False

#tentar_novamente = False
#count_tentativas = 0


vai_bot(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)

browser.quit()

'''
if tentar_novamente: #tentou e nao conseguiu achar o cardapio
    #tweet =
    #if count_tentativas = 1 
    #tweet
    time.sleep(900) #espera 15 min
    count_tentativas += 1

    if count_tentativas < 3: #so tenta acessar o cardapio 2 vezes (30 min de espera total)
        vai_bot(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)
        

browser.quit()

 get_text()    IMPORTANTE, LIMPA AS TAGS E PEGA SOMENTE O TEXTO
'''