import tweepy


# dicionario com as chaves que serao lidas de um arquivo .txt secreto
keys = {'CONSUMER_KEY' : '',
        'CONSUMER_SECRET' : '',
        'ACCESS_KEY' : '',
        'ACCESS_SECRET' : ''
        }

with open("secret_user_keys.txt", "r") as user_keys:
        for key in keys:
            keys[key] = user_keys.readline().rstrip()

user_keys.close()
print(keys)