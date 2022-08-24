import tweepy
import pandas as pd
from datetime import *
import pymongo
import urllib


with open('authentication.txt') as f:
    lines = f.read().splitlines()


#twitter api info
api_key = lines[0]
api_secret = lines[1]
access_token = lines[2]
access_secret = lines[3]


#tweepy twitter authentication
auth = tweepy.OAuthHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)


#mongodb info
dbUser = urllib.parse.quote_plus(lines[4])
dbPass = urllib.parse.quote_plus(lines[5])
dbLink = lines[6]


#mongodb authentication
dbClient = ("mongodb+srv://{}:{}@{}.mongodb.net/"
            "?retryWrites=true&w=majority")
dbClient = dbClient.format(dbUser, dbPass, dbLink)
client = pymongo.MongoClient(dbClient)
db = client.test
Tweets = db["Tweets"]
twitterBot = Tweets["twitterBot"]


#gather and reverse tweets
def reverseTweet(user, limit):
    
    tweets = []
    ids = []

    for t in api.user_timeline(screen_name = user, count = limit,
     tweet_mode = 'extended', exclude_replies = True, include_rts = False):
        
        temp = t.full_text
        temp = temp[::-1]
        tweets.insert(0, temp)
        ids.insert(0, t.id)

    return tweets, ids


#consult mongodb to see if the tweets have been tweeted before
def dbCheck(statuses, idno):

    count = len(idno)
    for i in range(count):
        temp = {str(idno[i]):statuses[i]}
        if twitterBot.count_documents(temp) == 0:
            if len(statuses[i]) <= 280:
                api.update_status(status = statuses[i])
                twitterBot.insert_one(temp)
            else:
                print("Tweet too long")
        else:
            print("Duplicate Tweet")
            
    print("Task Complete")
    return


#define search terms
search = "Nadeshot"
num = 50


text, ids = reverseTweet(search, num)
dbCheck(text, ids)







client.close()