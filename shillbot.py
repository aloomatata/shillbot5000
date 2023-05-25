## Customizing? Go to line 10

import tweepy
import requests
import json
from dotenv import load_dotenv
import os
import random

## EDIT THE QUERIES AND POSSIBLE REPLIES
## ONE PER LINE, MUST MEET TWITTER'S CHARACTER LIMIT

queries = [
    "wallstreetbets",
    "wall street bets",
    "wsb",
    "$wsb",
    "#wsb"
]

possible_replies = [
    'Check out $WSBC @thewsbclassic - community owned!',
    'Buy the dip, a-hole. $WSBC @thewsbclassic',
    'We print tendies so we can eat tendies. $WSBC @thewsbclassic'
]

## DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING
load_dotenv()

PATH_TO_BOT = os.environ['PATH_TO_BOT']

FILE_NAME = PATH_TO_BOT + "last.txt"

def get_tweet_text():
    tweet_text = random.choice(messages)

def reply_to_tweet(api, tweet_id):
    tweet_text = random.choice(possible_replies)
    confirmation = api.update_status(tweet_text, in_reply_to_status_id = tweet_id, auto_populate_reply_metadata=True)
    confirmationID = confirmation.id_str
    print('Tweet ID %s: ' % confirmationID)
    print(tweet_text)
    print('response to Tweet ID # %s' % tweet_id)

def read_last_seen():
    try:
        file_read = open(FILE_NAME, 'r')
        last_seen_id = int(file_read.read().strip())
        file_read.close()
        return last_seen_id
    except:
        return 0

def store_last_seen(last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

tweets_per_query  = 100

lastId = read_last_seen()
for tweet in tweepy.Cursor(api.search, q=queries, tweet_mode="extended", since_id=lastId).items(tweets_per_query):
    isRetweet = False
    try:
        text = tweet.retweeted_status.full_text.lower()
        isRetweet = True
    except:
        text = tweet.full_text.lower()
    
    if not isRetweet:
        if not tweet.retweeted:
            try:
                reply_to_tweet(api, tweet.id)
            except tweepy.TweepError as e:
                print('cannot reply to tweet %s' % str(tweet.id))

store_last_seen(lastId)