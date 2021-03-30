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
import matplotlib.pyplot as plt

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
print( f'Start 1.1: {time.time() - start}' )

# Print the number of unique sentiments.
print( f'There are {len( df.Sentiment.unique())} possible sentiments that a tweet may have.' )

# Find the second most popular sentiment in the tweets.
print( f'The second most popular tweet sentiment is { df.Sentiment.value_counts().index[1] }.' )

# Find the date with the greates number of extremely positive tweets.
print( f'The day with the most extermely positive tweets was { df[( df.Sentiment == "Extremely Positive" )].TweetAt.value_counts().index[0] }.' )


# Using vectorized string methods to clean up the spacing
def clean_spacing( series ):
    series = series.str.replace( '\s\s+', ' ' ) #remove all but single spacing
    series = series.str.strip() #strip whitespace before tokenization to avoid counting whitespace as words
    return series

# Clean the tweet text.
df[ 'AlteredTweet' ] = df[ 'OriginalTweet' ].str.lower() #convert to lower case
df[ 'AlteredTweet' ] = df[ 'AlteredTweet' ].str.replace( '[^a-zA-Z]', ' ' ) #remove no alphabetic characters
df[ 'AlteredTweet' ] = clean_spacing( df[ 'AlteredTweet' ] ) # clean up the spacing

if DEBUGGING: 
    print( df[ 'OriginalTweet' ])
    print( df[ 'AlteredTweet' ])

######################## SECTION 1.2 ########################
# Tokenize the tweets
print( f'Start 1.2: {time.time() - start}' )

# Using a Tokenizer was too slow so this was deprecated and sthe split method was used instead.
# start = time.time()
# df[ 'TokenizedTweet' ] = df[ 'AlteredTweet' ].apply( tknz.word_tokenize )
# if DEBUGGING: print( time.time() - start )

# Make a custom tokenize function which uses vecotrization as the .apply with prebuilt tokenizers is slow.
def tokenize( series, split = ' ' ): #default split value is a space
    return np.array( series.str.split( split ) )

df[ 'TokenizedTweet' ] = tokenize( df[ 'AlteredTweet' ] ) #tokenize the tweets by splitting at the spaces (regularized above by clean_spacing())

# Remove all the stop words
df[ 'NoStopWords' ] = df[ 'AlteredTweet' ].str.replace( r'\b\w{1,2}\b', '', regex = True ) #remove stop words
df[ 'NoStopWords' ] = clean_spacing( df[ 'NoStopWords' ])
df[ 'NoStopTokenizedTweet' ] = tokenize( df[ 'NoStopWords' ])

# Concatenate the lists of words with and without stop words
words = np.concatenate( df[ 'TokenizedTweet' ]) # combine all tokenized words into one list
nostopwords = np.concatenate( df[ 'NoStopTokenizedTweet' ]) # combine all tokenized words into one list

# Print the number of words in the corpus
print( f'There are {len( words )} words total in the corpus, {len( np.unique( words ))} of which are unique.' )
print( f'Without stop words, there are {len( words )} words total in the corpus, {len( np.unique( words ))} of which are unique.' )

# Create the word counters
wc = Counter( words )
nswc = Counter( nostopwords )

print( 'Here are a list of the 10 most frequently used words, before and after removing the stop words:' )
mcw = wc.most_common( 10 )
mcnsw = nswc.most_common ( 10 )

print( '\n     | Original   | After Stop Word Removal' )
print( '--------------------------------------------' )
for i in range( 10 ):
    print( f'({i+1:2}) | {mcw[i][0]:10} | {mcnsw[i][0]:10}' )

#if DEBUGGING: 
#    print( df[ 'AlteredTweet' ])
#    print( df[ 'TokenizedTweet' ])

######################## SECTION 1.3 ########################
print( f'Start 1.3: {time.time() - start}' )

print( df[( df[ 'AlteredTweet' ].str.contains( 'the' ))].count() )

#freqdf = pd.DataFrame({ 'Word': words, 'DocCount':  })

#width = 1
#plt.bar(indexes, values, width)
#plt.show()

######################## SECTION 1.4 ########################

