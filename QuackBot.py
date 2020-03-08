#!/usr/bin/env python
# coding: utf-8

from twitterscraper.query import query_tweets_from_user
import time
import re
import sys
import pandas as pd
import pyphen
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


if __name__ == '__main__':
    target_user = 'hankgreen'
    list_of_tweets = query_tweets_from_user(target_user, 10)
    current_tweet = list_of_tweets[0].text

    print("current tweet:", current_tweet, "\n")
    tweet_state = 'tweet_output.txt'

    # uncomment for debugging by printing retrieved tweets:
    #for tweet in list_of_tweets:
    #    print(tweet.text, tweet.timestamp)

    with open(tweet_state, 'r') as file:
        former_tweet = file.read()
        # uncomment for debugging by printing saved tweet file
        #print('former tweet:', former_tweet, "\n")


def quacked(tweet):
    split_tweet = tweet.split()
    #uncomment for debugging
    #print(split_tweet)
    quacked_tweet_array = []

    pyphen.language_fallback('nl_NL_variant1')
    dic = pyphen.Pyphen(lang='nl_NL')

    #iterate over each word in tweet
    for word in split_tweet:
        punctuation = ''
        punctuation_split = re.findall(r"[\w']+|[.,!?;]", word)
        #print(punctuation_split)
        quacked_word = dic.inserted(word)

        # remove weblinks
        if 'http' in word:
            quacked_word = ''
            #print('weblink removed')

        elif len(punctuation_split) > 1:
            word = punctuation_split[0]
            punctuation = punctuation_split[1:]
            punctuation = "".join(punctuation)
            if word.isupper():
                quacked_word = 'Quack'
            else:
                quacked_word = 'quack'
            #print('punctuation separated')

      #if words are multi-syllabic, replace the first syllable
        elif '-' in quacked_word:
            quacked_split_word = quacked_word.split("-")
            if quacked_split_word[0][0].isupper():
                quacked_split_word[0] = 'Quack'
            else:
                quacked_split_word[0] = 'quack'
            quacked_word = "".join(quacked_split_word)
        else:
            if quacked_word[0].isupper():
                quacked_word = 'Quack'
            else:
                quacked_word = 'quack'

        # add quacked word to new array
        if punctuation != '':
            quacked_word = quacked_word + punctuation
        #print(word)
        #print(quacked_word)
        if quacked_word != '':
            quacked_tweet_array.append(quacked_word)
        #print(quacked_tweet_array)

    #join array to make new string
    quacked_tweet = " ".join(quacked_tweet_array)

    # language parser/syllable logic
    return quacked_tweet

def tweet(text):
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
    message = text
    print(message)
    #twitter.update_status(status=message)
    print("Tweeted: %s" % message)
    #print(twitter)

    # if tweet is too long, split into two messages:
    if len(text) > 280:
        tweet_textA = '1/2 ' + message[0:131] + '...'
        tweet_textB = '2/2 ...' + message[131:]
        twitter.update_status(status=tweet_textA)
        time.sleep(7)
        twitter.update_status(status=tweet_textB)
        print('message too long: split into two tweets: ' + tweet_textA + '\n', tweet_textB)

    else:
        twitter.update_status(status=message)
        print('message tweeted: ', message)


quacked_tweet = quacked(current_tweet)
#print(current_tweet)
#print(quacked_tweet)

if current_tweet == former_tweet:
        print("no change")
        pass
elif current_tweet != former_tweet:
    print("change")
        #send tweet
    quacked(current_tweet)
    tweet(quacked_tweet)
    #save new tweet to persistent storage:
    with open(tweet_state, 'w') as file:
        file.write(current_tweet)
        file.close()
        print("current tweet saved:", current_tweet)
else:
    print('exit program')

print('End Program')
