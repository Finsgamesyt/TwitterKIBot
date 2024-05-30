import json
import tweepy
from ai import AIAPI
from twitterapiscraper import TwitterScraper
from time import sleep
import os

# Twitter API Login:
consumer_key = os.getenv("CONSUMER_KEY") # Your API/Consumer key
consumer_secret = os.getenv("CONSUMER_SECRET") # Your API/Consumer Secret Key
access_token = os.getenv("ACCESS_TOKEN") # Your Access token key
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET") # Your Access token Secret key
bearer_token = os.getenv("BEARER_TOKEN") # Your Bearer token

client = tweepy.Client(bearer_token=bearer_token, consumer_key = consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

ai = AIAPI("http://localhost:11434", "mixtral:8x7b", "deutsch") # AI wird definiert
# User (zum auslesen von Twitter)
email = os.getenv("MAIL")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
scraper = TwitterScraper(email=email, username=username, password=password) #scraper wird definiert

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
            newTweet = ai.prompt(prompt1).split('"') # Funktion ai.prompt ausführen, prompt als Parameter
            if len(newTweet) >= 2:  # '"' werden entfernt
                newTweet = newTweet[1].strip(" ")
            else: newTweet = newTweet[0].strip(" ")
            print(newTweet)
            if len(newTweet) > 261:
                print('Tweet ist zu lang!')
            print('Zufrieden? ')
            success = input('y or n: ')
        tweetInfo1 = client.create_tweet(text=newTweet) # Tweet wird erstellt
        print('TweetID: ')
        print(tweetInfo1)
        print(type(tweetInfo1))

    if program == '2':
        tweetid = input('Geben sie eine valide Tweetid ein: ')
        l = scraper.scrape(tweetid) #Funktion wird aufgerufen
        while True:
            count = 0
            sleep(60)
            for i in l[0]['children']: #"children" sind die Antworten auf den orginalen Tweet, demnach wird hier für jede Antwort das folgende Ausgeführt
                if count == 199:
                    sleep(15*60)
                if username not in [i['handle']]: #Wenn der Ersteller des Kommentar's nicht der Bot ist, ist die if Abfrage hier True
                    if username not in [j['handle'] for j in i['children']]: # i['children'] sind die Kommentare auf das Kommentar, demnach wird hier abgefragt, ob der Bot bereits auf das Kommentar kommentiert hat
                        t = i['text']# Inhalt des unkommentierten Tweets
                        id = i['id'] # tweetID des zu kommentierenden Kommentars
                        print(t)
                        print(id)
                        tweets = [l[0]['text'],t] #Die KI erhällt sowohl den orgialtweet, als auch das Kommentar, um den nötigen Kontext zu haben
                        print(tweets)
                        answer = ai.answer(*tweets)  # Funktion ai.answer ausführen. Der Parameter sind alle vorherigen Tweet/s.
                        print(answer)
                        posted = client.create_tweet(text=answer, in_reply_to_tweet_id=id)  # erstellt einen Tweet
                        print(posted.json()['id']) # gibt die tweetid der gegebenen Antwort
                count = count + 1


    if program == '3': # Siehe oben
        success = 'n'
        while success != 'y':
            prompt1 = input('Bitte geben sie ein Thema ein, um das sich der Tweet handeln soll: ')
            print('bitte Warten...')
            newTweet = ai.prompt(prompt1).split('"')
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
                if username not in [i['handle']]:
                    if username not in [j['handle'] for j in i['children']]:
                        t = i['text']
                        id = i['id']
                        print(t)
                        print(id)
                        tweets = [l[0]['text'], t]
                        print(tweets)
                        answer = ai.answer(
                            *tweets)
                        print(answer)
                        posted = client.create_tweet(text=answer, in_reply_to_tweet_id=id)
                count = count + 1
