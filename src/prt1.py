#--
# prt1.py
# Implements solutions to sections 1 of the coursework on text mining
# @author: Adam Toner
# @created: 30 Mar 2021
#
#--

import os
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import collections

start = time.time() #start the timer

# Set the literals for the file
DEBUGGING = False
TIMING = True
FILE_DIR = os.path.dirname(__file__)
OUT_DIR = FILE_DIR + '/../output/'
DATA_DIR = FILE_DIR + '/../data/text_data/'
DATA_FILE = 'Corona_NLP_train.csv'

######################## MAIN ########################
tdf = pd.read_csv( DATA_DIR + DATA_FILE, encoding = "ISO-8859-1" )

# Create a function to print the checkpoint times to see where the program can be improved
def time_check( cp ):
    if TIMING:
        print( f'\n## { cp }: { time.time() - start }' )

def cp_time( id ):
    if TIMING:
        print( f'\n## checkpoint: { time.time() - start }' )
    return time.time()

######################## SECTION 1.1 ########################
time_check( 'Start 1.1' )

# Print the number of unique sentiments.
print( f'There are { len( tdf.Sentiment.value_counts() ) } possible sentiments that a tweet may have.' )
# Find the second most popular sentiment in the tweets.
print( f'The second most popular tweet sentiment is { tdf.Sentiment.value_counts().index[1] }.' )
# Find the date with the greates number of extremely positive tweets.
print( f'The day with the most extremely positive tweets was { tdf[tdf[ "Sentiment" ] == "Extremely Positive"].TweetAt.value_counts().index[0] }.' )

tdf[ 'Tweet' ] = tdf[ 'OriginalTweet' ].str.lower()
tdf[ 'Tweet' ] = tdf[ 'Tweet' ].str.replace( '[^a-zA-Z]', ' ' )

# Using vectorized string methods to clean up the spacing
def clean_spacing( series ):
    series = series.str.replace( '\s\s+', ' ' ) #remove all but single spacing
    series = series.str.strip() #strip whitespace before tokenization to avoid counting whitespace as words
    return series

tdf[ 'Tweet' ] = clean_spacing( tdf[ 'Tweet' ])

if DEBUGGING: 
    print( '\n\n Original Tweets:' )
    print( tdf[ 'OriginalTweet' ])
    print( '\n\n Altered Tweets:' )
    print( tdf[ 'Tweet' ])

######################## SECTION 1.2 ########################
# Tokenize the tweets
time_check( 'Start 1.2' )

checkpoint = time.time()
tdf[ 'Tokens' ] = tdf.Tweet.str.split()
checkpoint = cp_time( checkpoint )
corpus = pd.Series( ' '.join(tdf[ 'Tweet' ]).split() )
checkpoint = cp_time( checkpoint )

# Print the number of words in the corpus
print( f'\nWith stop words, there are { len( corpus ) } words total, { len( corpus.unique() ) } of which are unique.' )
print( f'The ten most frequently used words are: { ", ".join(corpus.value_counts()[:10].index.tolist()) }')

# Remove the stop words from the corpus
corpus = corpus[(corpus.str.len() > 2)]
print( f'\nWithout stop words, there are { len( corpus.unique() ) } words total, { len( corpus.unique() ) } of which are unique.' )
print( f'The ten most frequently used (non-stop) words are: { ", ".join(corpus.value_counts()[:10].index.tolist()) }')

######################## SECTION 1.3 ########################
time_check( 'Start 1.3' )

######################## SECTION 1.4 ########################
time_check( 'Start 1.4' )
