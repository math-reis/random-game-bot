import os
import re
import tweepy
import random

from urllib.request import Request, urlopen

####################################################################
######################## API AUTHENTICATION ########################
####################################################################

api_keys = os.environ.get('api_keys')
api_keys_secret = os.environ.get('api_keys_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')
bearer_token = os.environ.get('bearer_token')

auth = tweepy.OAuthHandler(api_keys, api_keys_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)

client = tweepy.Client(bearer_token = bearer_token)

####################################################################
########################## UPDATE STATUS ###########################
####################################################################

pageNumber = random.randint(0, 192)

url = f'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page={pageNumber}'

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read()

html = webpage.decode("utf-8")

index = random.randint(0, 99)

if pageNumber == 192:
    index = random.randint(0, 30)

gameName = re.findall('class="title"><h3>(.*)</h3>', html)[index]

gameDate = re.findall('<span>(.*)</span>', html)[index]

gameScore = (re.findall('<div class="metascore_w large game(.*)</div>', html)[index])[-2:]

partialURL = re.findall('<a href="(.*)" class="title">', html)[index]

gameURL = "https://www.metacritic.com" + partialURL

partialPlataform = re.findall('game/(.*)/', partialURL)[0]

gamePlataform = (partialPlataform.replace('-', ' ')).title()

if gamePlataform == 'Pc':
    gamePlataform = 'PC'

if gamePlataform == 'Psp':
    gamePlataform = 'PSP'

if gamePlataform == 'Ds':
    gamePlataform = 'DS'

str1 = gameName
str2 = 'Plataform: ' + gamePlataform
str3 = gameDate
str4 = 'Metascore: ' + gameScore
str5 = 'Link: ' + gameURL

tweet = f"{str1}\n\n{str2}\n{str3}\n{str4}\n\n{str5}"

api.update_status(tweet)

####################################################################
######################## CREATE FRIENDSHIP #########################
####################################################################

query = 'Playstation OR Xbox OR Wii OR Nintendo'

response = client.search_recent_tweets(query, max_results = 15, tweet_fields = ['author_id'])

for tweet in response.data:
    list = [tweet.author_id]

    for author in list:
        api.create_friendship(user_id=author)
        print(author)
