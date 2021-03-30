#--
# prt1.py
# Implements solutions to sections 1 of the coursework on text mining
# @author: Adam Toner
# @created: 30 Mar 2021
#
#--

import os
import numpy as np
import pandas as pd

# Set the literals for the file
DEBUGGING = True
FILE_DIR = os.path.dirname(__file__)
OUT_DIR = FILE_DIR + '/../output/'
DATA_DIR = FILE_DIR + '/../data/text_data/'
DATA_FILE = 'Corona_NLP_train.csv'

######################## MAIN ########################
def load_tweets( tweet_file ):
    # read in tweets with pandas using the ISO-8859-1 encoding as UTF-8 was causing problems
    tweet_df = pd.read_csv( tweet_file, encoding = "ISO-8859-1" )
    return tweet_df
    
df = load_tweets( DATA_DIR + DATA_FILE )

if DEBUGGING: 
    print( len( df ))
    print( df.head())
    print( df.tail())

######################## SECTION 1.1 ########################
# Print the number of unique sentiments.
print( f'There are {len( df.Sentiment.unique())} possible sentiments that a tweet may have.' )

# Find the second most popular sentiment in the tweets.
print( f'The second most popular tweet sentiment is { df.Sentiment.value_counts().index[1] }.' )

# Find the date with the greates number of extremely positive tweets.
print( f'The day with the most extermely positive tweets was { df[( df.Sentiment == "Extremely Positive" )].TweetAt.value_counts().index[0] }.' )

# Clean the tweet text.
df[ 'OriginalTweet' ] = df[ 'OriginalTweet' ].str.lower() #convert to lower case
df[ 'OriginalTweet' ] = df[ 'OriginalTweet' ].str.replace( '[^a-zA-Z]', ' ' ) #remove no alphabetic characters
df[ 'OriginalTweet' ] = df[ 'OriginalTweet' ].str.replace( '\s\s+', ' ' ) #remove all but single spacing
if DEBUGGING: print( df[ 'OriginalTweet' ])

######################## SECTION 1.2 ########################



######################## SECTION 1.3 ########################



######################## SECTION 1.4 ########################

