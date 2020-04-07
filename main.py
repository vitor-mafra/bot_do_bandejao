import tweepy

import environment
import scrapper
import tweet


def main():

    for restaurante in environment.restaurantes:
        print(restaurante, ": ")
        encontrou_cardapio = scrapper.pega_cardapio(restaurante)

        if encontrou_cardapio:
            print("Tudo certo!\n")
            texto_tweet = tweet.elabora_tweet(
                restaurante,
                environment.cardapio,
                environment.almoco,
                environment.jantar,
            )

            api = tweet.setup_for_tweet(environment.keys)

            novo_tweet, mais_280_caracteres = tweet.confere_tweet(texto_tweet)

            if novo_tweet:
                texto_tweet = novo_tweet

            print(texto_tweet)

            tweet.tweeta(api, texto_tweet, mais_280_caracteres)

        else:
            print("Ops........")
            # tenta encontrar de novo, mais tarde

    scrapper.browser.close()


if __name__ == "__main__":
    main()
