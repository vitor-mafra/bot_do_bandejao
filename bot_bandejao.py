import tweepy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #apenas pra facilitar a leitura do codigo
import datetime
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
restaurantes_almoco_seg_sex = (RU_SETORIAL_I, RU_SETORIAL_II, RU_SAUDE_E_DIREITO, RU_ICA)
restaurantes_almoco_sab = (RU_SETORIAL_I, RU_SAUDE_E_DIREITO, RU_ICA)
restaurantes_jantar_seg_sab = (RU_SETORIAL_I, RU_SAUDE_E_DIREITO)
#restaurantes_jantar_seg_sab = (RU_ICA, RU_ICA)

    # variaveis relacionandas ao tempo
almoco = False
jantar = True
dia_da_semana = datetime.datetime.today().weekday() # Segunda = 0, Terca = 1 ... Domingo = 6

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
                cardapio_almoco_tratado += letra   # itea pela parte das sobremesas
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
                #count += 1
            if count > 18 and count < 23:
                cardapio_jantar_tratado += letra
            elif count == 29:
               cardapio_jantar_tratado += letra
        return cardapio_jantar_tratado

'''
def confere_cardapio(cardapio):
    count_caracteres = 0
    for letra in cardapio:
        count_caracteres += 1
    #confere se ele eh tuitavel, ie, tem menos de 280 caracteres
    if (count_caracteres <= 280):
        mais_280_caracteres = False
    else:
        mais_280_caracteres = True

    return mais_280_caracteres # a ideia eh definir outros tipos de possiveis erros aqui nessa funcao e retorna-los todos juntos
'''

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

    count_caracteres = 0
    for letra in tweet:
        count_caracteres += 1
    #confere se ele eh tuitavel, ie, tem menos de 280 caracteres
    if (count_caracteres <= 280): # nao tem problema tuitar
        mais_280_caracteres = False
    else:                          # nao eh tuitavel e por isso precisa ser dividido
        mais_280_caracteres = True
        
        count_linhas = 0
        cardapio_parte_1 = ''
        cardapio_parte_2 = ''
        for letra in tweet:
            if letra == '\n':
                count_linhas += 1
            if count_linhas < 7: # itera ate chegar a parte da guarnicao
                cardapio_parte_1 += letra # e guarda tudo isso em uma parte
            elif count_linhas == 7:  # itera ate a sobremesa
                cardapio_parte_2 += string_restaurante + cardapio[:6] +' (continuação)' + '\n\n'
                count_linhas += 1
            elif count_linhas >= 7 and count_linhas <= 11:   
                cardapio_parte_2 += letra # e guarda tudo isso em outra parte

        tweet_1 = cardapio_parte_1
        tweet_2 = cardapio_parte_2

    #verificacao se o cardapio esta pronto para ser tuitado
    if (cardapio == None):
        print("Erro ao tentar encontrar o cardapio\n")
        #tentar_novamente = True
        #return tentar_novamente
        #tweet = "Tive problemas ao acessar o cardapio, tentarei novamente mais tarde"
        #print(tweet)
    else:
        #finalmente tuitando
        try:
            if not mais_280_caracteres: 
                #api.update_status(tweet)
                print(tweet)
                print("\nTem mais de 280 caracteres = ", mais_280_caracteres)
                print("\nTweet publicado com sucesso!\n")
                print("*****************************\n")
                tweetou = True
            else:
                #tweet = api.update_status(tweet_1)
                #time.sleep(3) # espera um tempo para ter certeza de que o tweet foi publicado
                #api.update_status(tweet_2, in_reply_to_status_id = tweet.id_str)
                print(tweet_1)
                print("\n--------outro tweet--------\n")
                print(tweet_2)
                print("\nTem mais de 280 caracteres = ", mais_280_caracteres)
                tweetou = True
        except:
            if not tweetou:
                tweetou = False
                print("Erro ao tweetar!\n")
    return tweetou


def acessa_e_tweeta(almoco, jantar, dia_da_semana, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab):
    if almoco:
        if dia_da_semana < 5: # se nao eh fim de semana
            for restaurante in restaurantes_almoco_seg_sex:
                cardapio = pega_cardapio(site_fump, restaurante, almoco, jantar)
                tweetou = faz_tweet(restaurante, cardapio)
                if not tweetou: # se nao tiver tweetado, guarda o nome desse restaurante em uma lista para tentar novamente depois
                    restaurantes_nao_tweetados = []
                    restaurantes_nao_tweetados.append(restaurante)
                    return restaurantes_nao_tweetados


        elif dia_da_semana == 5: # se eh sabado
            for restaurante in restaurantes_almoco_sab:
                cardapio = pega_cardapio(site_fump, restaurante, almoco, jantar)
                tweetou = faz_tweet(restaurante, cardapio)
                if not tweetou: # se nao tiver tweetado, guarda o nome desse restaurante em uma lista para tentar novamente depois
                    restaurantes_nao_tweetados = []
                    restaurantes_nao_tweetados.append(restaurante)
                    return restaurantes_nao_tweetados

    elif jantar:
        if dia_da_semana < 6: # se nao eh domingo
            for restaurante in restaurantes_jantar_seg_sab:
                cardapio = pega_cardapio(site_fump, restaurante, almoco, jantar)
                tweetou = faz_tweet(restaurante, cardapio)
                if not tweetou: # se nao tiver tweetado, guarda o nome desse restaurante em uma lista para tentar novamente depois
                    restaurantes_nao_tweetados = []
                    restaurantes_nao_tweetados.append(restaurante)
                    return restaurantes_nao_tweetados

'''
# definindo o horario de postagem do cardapio
agora_almoco = datetime.datetime.now()
horario_postagem_almoco = agora_almoco.replace(hour=9, minute=0, second=0, microsecond=0)
agora_limite_almoco = datetime.datetime.now()
horario_limite_postagem_almoco = agora_limite_almoco.replace(hour=9, minute=5, second=0, microsecond=0)

agora_jantar = datetime.datetime.now()
horario_postagem_jantar = agora_jantar.replace(hour=17, minute=0, second=0, microsecond=0)
agora_limite_jantar = datetime.datetime.now()
horario_limite_postagem_jantar = agora_limite_jantar.replace(hour=17, minute=5, second=0, microsecond=0)

agora_3 = datetime.datetime.now()
meia_noite = agora_3.replace(hour=0, minute=0, second=1, microsecond=0)


horario_atual = datetime.datetime.now()

while True:
    
    while horario_atual > horario_postagem_jantar: #como meia noite eh 0h, ele espera virar o dia pra comecar a comparar 
        time.sleep(60)                              # de novo ate postar o cardapio do almoco
        horario_atual = datetime.datetime.now() #update hora atual                                                                                                          
    
    while horario_atual < horario_limite_postagem_almoco: 
        time.sleep(60) # confere, minuto a minuto a hora
        horario_atual = datetime.datetime.now() #update hora atual
        if horario_atual >= horario_postagem_almoco:
            almoco = True
            jantar = False
            restaurantes_nao_tweetados = acessa_e_tweeta(almoco, jantar, dia_da_semana, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)

    while horario_atual < horario_limite_postagem_almoco: 
        time.sleep(60) # confere, minuto a minuto a hora
        horario_atual = datetime.datetime.now() #update hora atual
        if horario_atual >= horario_postagem_almoco:
            almoco = True
            jantar = False
            restaurantes_nao_tweetados = acessa_e_tweeta(almoco, jantar, dia_da_semana, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)


    while(horario_atual > horario_postagem_almoco and horario_atual < horario_postagem_jantar):
        time.sleep(60)
        horario_atual = datetime.datetime.now()
        print(horario_atual)
        print("Espera")
        print("FOI!")   
'''

restaurantes_nao_tweetados = acessa_e_tweeta(almoco, jantar, dia_da_semana, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)
browser.quit() # fecha as abas abertas no navegador



'''
if len(restaurantes_nao_tweetados) > 0: # sei que essa forma de comparacao nao eh Pythonic, mas achei assim melhor fazer essa checagem de forma explicita
    for restaurante in restaurantes_nao_tweetados:
        count_tentativas = 0
        tweet_falhou = "Não consegui encontrar o cardápio do {}. Tentarei novamente em 15 minutos".format(str(restaurante))
        api.update_status(tweet_falhou)

        #if count_tentativas = 1 
        #tweet
        time.sleep(900) #espera 15 min
        count_tentativas += 1

        if count_tentativas <= 4: #so tenta acessar o cardapio 4 vezes (uma a cada 15 min)
            if almoco:
                if dia_da_semana < 5:
                    restaurantes_almoco_seg_sex = restaurantes_nao_tweetados 
                    acessa_e_tweeta(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)

                elif dia_da_semana == 5:
                    restaurantes_almoco_sab = restaurantes_nao_tweetados
                    acessa_e_tweeta(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)

            elif jantar:
                restaurantes_jantar_seg_sab = restaurantes_nao_tweetados
                acessa_e_tweeta(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)
'''


'''
seconds = time.time()
hora_local = time.ctime(seconds) 
print(hora_local)


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


#tentar_novamente = False
#count_tentativas = 0


#vai_bot(almoco, jantar, restaurantes_almoco_seg_sex, restaurantes_almoco_sab, restaurantes_jantar_seg_sab)
'''