import json
import tweepy
from ai import AIAPI
from twitterapiscraper import TwitterScraper
from time import sleep
import os

#Twitter API Login:
consumer_key = os.getenv("CONSUMER_KEY") #Your API/Consumer key
consumer_secret = os.getenv("CONSUMER_SECRET") #Your API/Consumer Secret Key
access_token = os.getenv("ACCESS_TOKEN") #Your Access token key
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET") #Your Access token Secret key
bearer_token = os.getenv("BEARER_TOKEN")

client = tweepy.Client(bearer_token=bearer_token, consumer_key = consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

ai = AIAPI("http://localhost:11434", "mixtral:8x7b", "deutsch") #Klasse AIAPI aufrufen, Parameter eingeben
#User (zum auslesen von Twitter)
email = os.getenv("MAIL")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
scraper = TwitterScraper(email=email, username=username, password=password)

while True:

    print('Wollen sie:')
    print('1 Einen neuen Tweet erstellen lassen')
    print('2 Einen bisherigen Tweet vom Bot überwachen lassen')
    print('3 Einen neuen Tweet erstellen lassen und diesen überwachen lassen')
    program = input('Bitte geben sie 1, 2 oder 3 ein: ')


    if program == '1':
        success = 'n'
        while success != 'y':
            prompt1 = input('Bitte geben sie ein Thema ein, um das sich der Tweet handeln soll: ')
            print('bitte warten...')
            #still testing: !!!
            newTweet = ai.prompt(prompt1).split('"') # Funktion ai.promt ausführen, prompt als Parameter
            if len(newTweet) >= 2:
                newTweet = newTweet[1].strip(" ")
            else: newTweet = newTweet[0].strip(" ")
            print(newTweet)
            if len(newTweet) > 261:
                print('Tweet ist zu lang!')
            print('Zufrieden? ')
            success = input('y or n: ')
        tweetInfo1 = client.create_tweet(text=newTweet)
        print('TweetID: ')
        print(tweetInfo1)
        print(type(tweetInfo1))



    #print(l)
    #print(TwitterScraper.clean_tree_to_yaml(l))
    if program == '2':
        tweetid = input('Geben sie eine valide Tweetid ein: ')
        l = scraper.scrape(tweetid)
        while True:
            count = 0
            sleep(60)
            for i in l[0]['children']:
                if count == 199:
                    sleep(15*60)
                if 'botor276' not in [i['handle']]:
                    if 'botor276' not in [j['handle'] for j in i['children']]:
                        t = i['text']
                        id = i['id']
                        print(t)
                        print(id)
                        tweets = [l[0]['text'],t]
                        print(tweets)
                        answer = ai.answer(*tweets)  # Funktion ai.answer ausführen. Der Parameter sind alle vorherigen Tweet/s.
                        print(answer)
                        posted = client.create_tweet(text=answer, in_reply_to_tweet_id=id)  # erstellt einen Tweet
                        print(posted.json()['id'])
                count = count + 1


    if program == '3':
        success = 'n'
        while success != 'y':
            prompt1 = input('Bitte geben sie ein Thema ein, um das sich der Tweet handeln soll: ')
            print('bitte Warten...')
            newTweet = ai.prompt(prompt1).split('"')  # Funktion ai.promt ausführen, prompt als Parameter
            if len(newTweet) >= 2:
                newTweet = newTweet[1].strip(" ")
            else: newTweet = newTweet[0].strip(" ")
            print(newTweet)
            if len(newTweet) > 261:
                print('Tweet ist zu lang!')
            print('Zufrieden? ')
            success = input('y or n: ')
        tweetInfo3 = client.create_tweet(text=newTweet)
        print('TweetID: ')
        print(tweetInfo3.json['id'])
        l = scraper.scrape(tweetInfo3.json()['id'])
        while True:
            count = 0
            sleep(60)
            for i in l[0]['children']:
                if count >= 199:
                    sleep(15 * 60)
                if 'botor276' not in [i['handle']]:
                    if 'botor276' not in [j['handle'] for j in i['children']]:
                        t = i['text']
                        id = i['id']
                        print(t)
                        print(id)
                        tweets = [l[0]['text'], t]
                        print(tweets)
                        answer = ai.answer(
                            *tweets)  # Funktion ai.answer ausführen. Der Parameter sind alle vorherigen Tweet/s.
                        print(answer)
                        posted = client.create_tweet(text=answer, in_reply_to_tweet_id=id)  # erstellt einen Tweet
                count = count + 1
