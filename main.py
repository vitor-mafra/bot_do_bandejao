import tweepy

import environment
import scrapper
import tweet


def main():

    api = tweet.setup_for_tweet(environment.keys)

    #texto = "o/"
    #tweet.faz_tweet(api, texto)

main()