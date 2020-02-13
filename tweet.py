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
                        environment.keys[key] = user_keys.readline().rstrip()

        user_keys.close()
        print(environment.keys)


def set_API(keys):
        '''
        Utiliza as chaves de autenticacao nas funcoes da biblioteca tweepy,
        configurando assim todo o codigo necessario para publicar os tweets
        no perfil @bot_RU_UFMG

        Para uma introducao facil e amigavel a essa biblioteca, veja:
        https://tweepy.readthedocs.io/en/latest/getting_started.html#hello-tweepy
        '''
        auth = tweepy.OAuthHandler(str(environment.keys['CONSUMER_KEY']), str(environment.keys['CONSUMER_SECRET']))
        auth.set_access_token(str(environment.keys['ACCESS_KEY']), str(environment.keys['ACCESS_SECRET']))

        api = tweepy.API(auth)

        return api



def setup_for_tweet(keys):
        '''
        Funcao que chamam todas as funcoes necessarias para deixar tudo pronto
        para a postagem dos tweets
        '''
        get_keys(keys)
        return set_API(keys)


def faz_tweet(api, texto):
        '''
        Publica o tweet no perfil do bot (@bot_RU_UFMG)
        '''
        api.update_status(texto)
        print("Tweet publicado com sucesso!")
