# backwardsBot

This is a python script that gathers a specified user's 50 latest tweets, 
then it removes retweets and replies and proceeds to reverse the text in every tweet and repost it to @backward_bot 
on twitter. It uses Tweepy along with the twitter api to handle gathering and posting tweets and I used pymongo 
to consult a mongodb collection to ensure that no duplicate tweets would be made.

It is currently set to reverse @Nadeshot's tweets; however, this can be easily adjusted.
