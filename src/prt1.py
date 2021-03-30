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
import nltk.tokenize as tknz
from collections import Counter

start = time.time() #start the timer

# Set the literals for the file
DEBUGGING = False
FILE_DIR = os.path.dirname(__file__)
OUT_DIR = FILE_DIR + '/../output/'
DATA_DIR = FILE_DIR + '/../data/text_data/'
DATA_FILE = 'Corona_NLP_train.csv'

######################## MAIN ########################
df = pd.read_csv( DATA_DIR + DATA_FILE, encoding = "ISO-8859-1" )

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
df[ 'AlteredTweet' ] = df[ 'OriginalTweet' ].str.lower() #convert to lower case
df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.replace( '[^a-zA-Z]', ' ' ) #remove no alphabetic characters
df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.replace( '\s\s+', ' ' ) #remove all but single spacing
if DEBUGGING: 
    print( df[ 'OriginalTweet' ])
    print( df[ 'AlteredTweet' ])

######################## SECTION 1.2 ########################
# Tokenize the tweets

# Using a Tokenizer.
# start = time.time()
# df[ 'TokenizedTweet' ] = df[ 'AlteredTweet' ].apply( tknz.word_tokenize )
# if DEBUGGING: print( time.time() - start )

# Using vectorized string methods
df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.strip() #strip whitespace before tokenization to avoid counting whitespace as words
df[ 'TokenizedTweet' ] = np.array( df[ 'AlteredTweet' ].str.split( ' ' )) #tokenize the tweets

if DEBUGGING: 
    print( time.time() - start )
    print( df[ 'AlteredTweet' ])
    print( df[ 'TokenizedTweet' ])

words = np.concatenate( df[ 'TokenizedTweet' ])
print( f'There are {len( words )} words total in the corpus, {len( np.unique( words ))} of which are unique.' )
c = Counter(words)
print( 'Here are a list of the 10 most frequently used words:' )
mcw = c.most_common( 10 )
for i in range( 10 ):
    print( f'({i+1}) {mcw[i][0]}' )

df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.replace( r'\b\w{1,2}\b', '', regex = True ) #remove stop words
df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.replace( '\s\s+', ' ' ) #remove all but single spacing again
df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.strip() #strip whitespace before tokenization to avoid counting whitespace as words
df[ 'TokenizedTweet' ] = np.array( df[ 'AlteredTweet' ].str.split( ' ' )) #tokenize the tweets
words = np.concatenate( df[ 'TokenizedTweet' ])
print( f'After removing stop words, there are {len( words )} words total in the corpus, {len( np.unique( words ))} of which are unique.' )
print( 'Here are a list of the 10 most frequently used words:' )
c = Counter(words)
mcw = c.most_common( 10 )
for i in range( 10 ):
    print( f'({i+1}) {mcw[i][0]}' )

if DEBUGGING: 
    print( df[ 'AlteredTweet' ])
    print( df[ 'TokenizedTweet' ])

######################## SECTION 1.3 ########################
print( f'Start 1.3: {time.time() - start}' )



######################## SECTION 1.4 ########################

