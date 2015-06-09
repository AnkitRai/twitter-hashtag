#!/usr/bin/python
# Contact at rai5@illinois.edu for any queries
# Adapted by Mining the Social Web by Mathew A. Russell

from __future__ import print_function
import re
import twitter
import pandas as pd
import os
import pickle
from pytagcloud import create_tag_image, make_tags

def search_twitter(twitter_api, q, search_size = 100, stop_count = 1000):
    '''
    
    Parameters:
      twitter_api: Use twitter.Twitter to create twitter.api.Twitter object.
      q (str): search query (e.g. #green infrastructure)
      search_size: default 100.
      stop_count: stops search when the total size of tweets exceeds stop_count.
    '''
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q = q, count = search_size)
    statuses = search_results['statuses']

    # Iterate through results by following the cursor until we hit the count number
    while stop_count > len(statuses):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
        
        next_results = twitter_api.search.tweets(**kwargs)
        statuses += next_results['statuses']
        print(len(statuses), 'tweets fetched...')
        
    return statuses

def clean_statuses(statuses):
    '''
    Takes a list of dictionaries of tweet metadata returned from
    search_twitter() function, and returns a list with all lowercase words
    (no words with #, @, http, or non-alphabetical characters).

    Parameters:
      statuses: a list of dictionaries of tweet metadata returned from
                search_twitter() function.
    '''
    status_texts = [status['text'] for status in statuses]
    status_texts = [text.encode('ascii', 'ignore') for text in status_texts]

    clean_tweets = []
    clean_tweets = [w for t in status_texts
                        for w in t.split()]

    
    
    return clean_tweets

def get_counts(words):
    '''
    Takes a list of strings and returns a dictionary of {string: frequency}.

    Parameters:
      words: a list of strings

    Examples:
    >>> get_counts(['a', 'a', 'b', 'b', 'b', 'c'])
    [('b', 3), ('a', 2), ('c', 1)]
    '''

    
    counts = dict()
    for item in counts:
        if item not in counts:
            counts[item] = 1
        else:
            counts[item] += 1
    
    return counts


def main():
    
    # https://dev.twitter.com/docs/auth/oauth for more information 
    # on Twitter's OAuth implementation.
    CONSUMER_KEY = '7J6ZlYXjP1xOwimtaiADtvUD1'
    CONSUMER_SECRET = 'wPLHMfPqss9UXMHWd5wnbMk6lXWS5FSHxwGeOc7nzHDbqYzxBg'
    OAUTH_TOKEN = '410357936-hSdUGLvx8Lv3PNebvxx6gyeJX6q9n2C9vCnQ9Go4'
    OAUTH_TOKEN_SECRET = 'hWbOZQTCtheoiAR7c5JEBZ9hKb7tZfq4cGUKbgUs7ZmQo'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth = auth)

    # Search query, try your own.
    q = '#green infrastructure' # try different hash tag examples

    # calling search_twitter too often will lock you out for 1 hour.
    # we will call search twitter once and save the result in a file.
    if not os.path.isfile('{0}.p'.format(q)):
        results = search_twitter(twitter_api, q)
        pickle.dump(results, open('{0}.p'.format(q), 'wb'))

    # load saved pickle file
    results = pickle.load(open('{0}.p'.format(q), 'rb'))
    # clean the tweets and extract the words we want
    clean_tweets = clean_statuses(results)
    # calculate the frequency of each word
    word_count = get_counts(clean_tweets)

    # use PyTagCloud to create a tag cloud
    tags  = make_tags(word_count, maxsize = 120)
    # the image is store in 'cloud.png'
    create_tag_image(tags, 'cloud.png', size = (900, 600), fontname = 'Lobster')
    
if __name__ == '__main__':

    main()
