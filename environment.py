import time

# paginas web necessarias para buscar o cardapio
site_fump = "http://www.fump.ufmg.br/cardapio.aspx"


# dicionario com as chaves que serao lidas de um arquivo .txt secreto
keys = {
    'CONSUMER_KEY' : '',
    'CONSUMER_SECRET' : '',
    'ACCESS_KEY' : '',
    'ACCESS_SECRET' : '',
    }

# informacoes dos restaurantes
restaurantes = {
    'RU_SETORIAL_I' : 1,
    'RU_SETORIAL_II' : 2,
    'RU_SAUDE_E_DIREITO' : 3,
    'RU_ICA' : 4,
    }

almoco_seg_sex = (
    restaurantes['RU_SETORIAL_I'], 
    restaurantes['RU_SETORIAL_II'],
    restaurantes['RU_SAUDE_E_DIREITO'],
    restaurantes['RU_ICA'],
    )

almoco_sab = (
    restaurantes['RU_SETORIAL_I'], 
    restaurantes['RU_SAUDE_E_DIREITO'],
    restaurantes['RU_ICA'],
    )

jantar_seg_sab = (
    restaurantes['RU_SETORIAL_I'], 
    restaurantes['RU_SAUDE_E_DIREITO'],
    restaurantes['RU_ICA'],
    )
