#!/usr/bin/env python
# coding: utf-8

from twitterscraper.query import query_tweets_from_user
import time
import re
import sys
import pyphen
from twython import Twython
import json
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
    penultimate_tweet = list_of_tweets[1].text

    print("current tweet:", current_tweet, "\n")
    print("penultimate tweet:", penultimate_tweet, "\n")
    tweet_state = 'tweet_output.json'

    #print the retrieved tweets to the screen:
    #for single_tweet in list_of_tweets:
    #print(single_tweet.text, single_tweet.timestamp, "\n")

    former_tweet_zero = ""
    former_tweet_one = ""
    try:
        with open(tweet_state) as json_file:
            former_tweets = json.load(json_file)
            for t in former_tweets['tweets']:
                print('former tweets:','\n')
                former_tweet_zero = t['tweet_zero']
                former_tweet_one = t['tweet_one']
    except:
        print('error in opening former tweets in', tweet_state)
    finally:
        print('tweet[0]:', former_tweet_zero, "\n")
        print('tweet[1]:', former_tweet_one, "\n")


def quacked(tweet):
    split_tweet = tweet.split()
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

        # handle weblinks
        if 'http' in word:
            quacked_word = " " + word

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
    return quacked_tweet


def tweet(text):
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
    message = text

    if len(text) > 280:
        tweet_textA = '1/2 ' + message[0:131] + '...'
        tweet_textB = '2/2 ...' + message[131:]
        twitter.update_status(status=tweet_textA)
        time.sleep(7)
        twitter.update_status(status=tweet_textB)
        print('message too long: split into two tweets:\nTweet Text A: ' + tweet_textA + '\nTweet Text B: ', tweet_textB)

    else:
        twitter.update_status(status=message)
        print("Message tweeted: %s" % message)


if (current_tweet == former_tweet_zero) & (penultimate_tweet == former_tweet_one):
        print("no change")
        print('exit program')
        pass
elif (current_tweet == former_tweet_zero) & (penultimate_tweet != former_tweet_one):
    print("change detected in penultimate tweet, pinned tweet likely")

        #send tweet
    quacked_tweet = quacked(penultimate_tweet)
    tweet(quacked_tweet)

        #save new tweet to persistent storage:
    current_tweets_object = {}
    current_tweets_object['tweets'] = []
    current_tweets_object['tweets'].append({
        'tweet_zero': current_tweet,
        'tweet_one': penultimate_tweet
    })
    try:
        with open(tweet_state, 'w') as json_file:
            #file.write(current_tweet)
            json.dump(current_tweets_object, json_file)
            print("current tweets saved: Current tweet: ", current_tweet, "\nPenultimate tweet: ", penultimate_tweet)
    except:
        print('error saving ', tweet_state)
else:
    print("Change detected")

        #send tweet
    quacked_tweet = quacked(current_tweet)
    tweet(quacked_tweet)

        #save new tweet to persistent storage:
    current_tweets_object = {}
    current_tweets_object['tweets'] = []
    current_tweets_object['tweets'].append({
        'tweet_zero': current_tweet,
        'tweet_one': penultimate_tweet
    })
    try:
        with open(tweet_state, 'w') as json_file:
            json.dump(current_tweets_object, json_file)
            print("Current tweets saved: Current tweet: ", current_tweet, "\nPenultimate tweet: ", penultimate_tweet)
    except:
        print('error saving ', tweet_state)
print('End Program')
