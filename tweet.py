import tweepy
import environment


def get_keys(keys):
    '''
    Le em um arquivo cada uma das chaves/tokens de autenticacao fornecidos
    pelo Twitter para publicar na conta do bot e armazana esses dados em
    um dicionario 
    '''
    with open("secret_user_keys.txt", "r") as user_keys:
            for key in environment.keys:
                environment.keys[key] = str(user_keys.readline().rstrip())

            user_keys.close()


def set_API(keys):
    '''
    Utiliza as chaves de autenticacao nas funcoes da biblioteca tweepy,
    configurando assim todo o codigo necessario para publicar os tweets
    no perfil @bot_RU_UFMG

    Para uma introducao facil e amigavel a essa biblioteca, veja:
    https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy
    '''
    auth = tweepy.OAuthHandler(environment.keys['CONSUMER_KEY'], \
        environment.keys['CONSUMER_SECRET'])

    auth.set_access_token(environment.keys['ACCESS_KEY'], \
        environment.keys['ACCESS_SECRET'])

    api = tweepy.API(auth)

    return api


def setup_for_tweet(keys):
    '''
    Funcao que chamam todas as funcoes necessarias para deixar tudo pronto
    para a postagem dos tweets
    '''
    get_keys(keys)
    return set_API(keys)


def tweeta(api, texto_tweet, mais_280_caracteres):
    '''
    Publica o tweet no perfil do bot (@bot_RU_UFMG)
    '''
    if not mais_280_caracteres:
        api.update_status(texto_tweet)

    elif mais_280_caracteres:
        #tweet_1 = texto_tweet
        print("erro, mais de 280 carac")

    print("Tweet publicado com sucesso!")


def elabora_tweet(restaurante, cardapio, almoco, jantar):
    '''
    '''
    if restaurante == environment.restaurantes['RU_SETORIAL_I']:
        texto_restaurante = "Cardápio RU Setorial I"

    elif restaurante == environment.restaurantes['RU_SETORIAL_II']:
        texto_restaurante = "Cardápio RU Setorial II"

    elif restaurante == environment.restaurantes['RU_SAUDE_E_DIREITO']:
        texto_restaurante = "Cardápio Saúde e Direito"

    elif restaurante == environment.restaurantes['RU_ICA']:
        texto_restaurante = "Cardápio RU ICA"

    # variavel para armazenar somente a parte do cardapio que eh usada no tweet
    cardapio_tweet = ""

    # lista que determina quais partes do cardapio fazem parte do tweet
    partes_tweetaveis = []

    if almoco:
        partes_tweetaveis = ['proteina_1', 'proteina_2','proteina_3', \
                            'guarnicao', 'sobremesa_1', 'sobremesa_2']
        
        almoco_ou_jantar = "Almoço"

    elif jantar:
        partes_tweetaveis = ['proteina_1', 'proteina_3', 'guarnicao', \
                                                        'sobremesa_1']
        almoco_ou_jantar = "Jantar"

    for elemento in partes_tweetaveis:
        cardapio_tweet += cardapio[elemento]
        cardapio_tweet += "\n" # pula para a proxima linha
        if elemento == 'guarnicao':
            cardapio_tweet += "\n" # pula mais uma linha para separar as partes
                                   # do cardapio

    tweet = texto_restaurante + " - " + almoco_ou_jantar + "\n\n"  + \
        cardapio_tweet

    return tweet


def confere_tweet(tweet):
    '''
    Busca pelo texto das tags que indicam os tipos  de prato do cardapio, que
    sempre deveriam estar presentes. Caso algum desses tipos nao seja 
    encontrado, adiciona um emoji (⚠️) no tweet para indicar que possivelmente
    aquele cardapio pode ter algum dos itens em falta. Depois disso, confere 
    se o texto original tem mais de 280 caracteres (limite maximo que um tweet
    pode ter). Retorna um booleano que indica isso
    '''

    if environment.almoco:   
        termos_obrigatorios = ["Prato protéico 1", "Prato protéico 2", \
            "Prato protéico 3", "Guarnição", "Sobremesa (uma porção)", \
                 "Sobremesa 2"]

    elif environment.jantar:
        termos_obrigatorios = ["Prato protéico 1", "Prato protéico 3", \
            "Guarnição", "Sobremesa (uma porção)"]

    cardapio_completo = True

    for termo_obrigatorio in termos_obrigatorios:
        if termo_obrigatorio in tweet:
            cardapio_completo = cardapio_completo and True
        else:
            # se um dos elementos nao esta no cardapio, ele ja esta errado
            cardapio_completo = cardapio_completo and False

    if not cardapio_completo:
        print("cardapio incompleto!")
        if environment.almoco:
            novo_tweet = tweet[:tweet.find("Almoço") + len("Almoço")] + " ⚠️" \
             + tweet[tweet.find("Almoço") + len("Almoço"):]

        elif environment.jantar:
            novo_tweet = tweet[:tweet.find("Jantar") + len("Jantar")] + " ⚠️" \
             + tweet[tweet.find("Jantar") + len("Jantar"):]

    else:
        novo_tweet = None

    if len(tweet) > 282:
        mais_280_caracteres = True

    else:
        mais_280_caracteres = False

    return novo_tweet, mais_280_caracteres

'''
TO DO:

[] funcao que tenta buscar o cardapio de novo, caso ele nao tenha sido encontrado

[] dividir o tweet em 2, caso ele tenha mais de 280 caracteres

[] screenshot da pagina se o cardapio nao foi encontrado???
'''