import time
from datetime import datetime

# paginas web necessarias para buscar o cardapio
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"


# dicionario com as chaves que serao lidas de um arquivo .txt secreto
keys = {
    'CONSUMER_KEY' : '',
    'CONSUMER_SECRET' : '',
    'ACCESS_KEY' : '',
    'ACCESS_SECRET' : '',
    }

# informacoes relacionadas a tempo
agora = datetime.now()

if agora.hour <= 14:
    almoco = True
    jantar = False

else:
    almoco = False
    jantar = True

dia_da_semana = agora.weekday() # seg = 0, ter = 1, ... , dom = 6

# informacoes dos restaurantes e dos cardapios
if almoco:
    # busca pelo cardapio do almoco, que segue a forma:
    cardapio = {
        'proteina_1' : "",
        'proteina_2' : "",
        'proteina_3' : "",

        'guarnicao' : "",

        'acompanhamento_1' : "",
        'acompanhamento_2' : "",
        'acompanhamento_3' : "",

        'entrada_1' : "",
        'entrada_2' : "",
        'entrada_3' : "",

        'sobremesa_1' : "",
        'sobremesa_2' : "",

        'refresco' : "",
        'molho_salada' : "",
    }

    # como eh almoco, precisa-se determinar quais sao os restaurantes do dia
    if dia_da_semana < 5: # segunda a sexta 
        restaurantes = {
            'RU_SETORIAL_I' : 1,
            'RU_SETORIAL_II' : 2,
            'RU_SAUDE_E_DIREITO' : 3,
            'RU_ICA' : 4,
        }

    else: # sabado
        restaurantes = {
            'RU_SETORIAL_I' : 1,
            'RU_SAUDE_E_DIREITO' : 3,
            'RU_ICA' : 4,
        }

elif jantar:
    # busca pelo cardapio do jantar, que esta na seguinte forma
        cardapio = {
            'proteina_1' : "",
            'proteina_3' : "",

            'guarnicao' : "",

            'acompanhamento_1' : "",
            'acompanhamento_2' : "",
            'acompanhamento_3' : "",

            'entrada_1' : "",
            'entrada_2' : "",
            'entrada_3' : "",

            'sobremesa_1' : "",

            'refresco' : "",
            'molho_salada' : "",
        }
        
        # no jantar, os restaurantes nao mudam de acordo com o dia da semana
        restaurantes = {
            'RU_SETORIAL_I' : 1,
            'RU_SAUDE_E_DIREITO' : 3,
            'RU_ICA' : 4,
        }       
