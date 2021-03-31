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
from numpy.lib.arraysetops import unique
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

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

if DEBUGGING: 
    print( len( tdf ))
    print( tdf.head())
    print( tdf.tail())

def time_check( cp ):
    if TIMING:
        print( f'\n## {cp}: { time.time() - start }' )

######################## SECTION 1.1 ########################
time_check( 'Start 1.1' )

# Print the number of unique sentiments.
print( f'There are {len( tdf.Sentiment.unique())} possible sentiments that a tweet may have.' )

# Find the second most popular sentiment in the tweets.
print( f'The second most popular tweet sentiment is { tdf.Sentiment.value_counts().index[1] }.' )

# Find the date with the greates number of extremely positive tweets.
print( f'The day with the most extremely positive tweets was { tdf[( tdf.Sentiment == "Extremely Positive" )].TweetAt.value_counts().index[0] }.' )


# Using vectorized string methods to clean up the spacing
def clean_spacing( series ):
    series = series.str.replace( '\s\s+', ' ' ) #remove all but single spacing
    series = series.str.strip() #strip whitespace before tokenization to avoid counting whitespace as words
    return series

# Clean the tweet text.
tdf[ 'CTweet' ] = tdf[ 'OriginalTweet' ].str.lower() #convert to lower case
tdf[ 'CTweet' ] = tdf[ 'CTweet' ].str.replace( '[^a-zA-Z]', ' ' ) #remove no alphabetic characters
tdf[ 'CTweet' ] = clean_spacing( tdf[ 'CTweet' ] ) # clean up the spacing

if DEBUGGING: 
    print( '\n\n Original Tweets:' )
    print( tdf[ 'OriginalTweet' ])
    print( '\n\n Altered Tweets:' )
    print( tdf[ 'CTweet' ])

######################## SECTION 1.2 ########################
# Tokenize the tweets
time_check( 'Start 1.2' )

# Make a custom tokenize function which uses vecotrization as the .apply with prebuilt tokenizers is slow.
def tokenize( series, split = ' ' ): #default split value is a space
    return np.array( series.str.split( split ) )

tdf[ 'TokenizedTweet' ] = tokenize( tdf[ 'CTweet' ] ) #tokenize the tweets by splitting at the spaces (regularized above by clean_spacing())

# Create a dataframe to store data about the words
wdf = pd.Series(np.concatenate( tdf[ 'TokenizedTweet' ]))
nwdf = wdf[( wdf.str.len() > 2 )]

# Print the number of words in the corpus
print( f'With stop words, there are {len( wdf )} words total, {len( wdf.unique())} of which are unique.' )
print( f'Without stop words, there are {len( nwdf )} words total, {len( nwdf.unique() )} of which are unique.' )
print( '\nThe ten most frequently used words are:')
print( f'With stop words: {wdf.value_counts()[:10].index.tolist()}' )
print( f'Without stop words: {nwdf.value_counts()[:10].index.tolist()}' )

######################## SECTION 1.3 ########################
time_check( 'Start 1.3' )

vec = CountVectorizer()
X = vec.fit_transform( tdf.CTweet )

print(X)

def get_frequency( word ):
    return tkdf.isin( [word] ).any(axis=1).value_counts()[ True ]

#word = 'to'
#print( len( tdf[( tdf.CTweet.str.contains( r'\b' + word + r'\b' ) )] ) )
#freq = []
#uws.apply(lambda x: print( tdf[( tdf.CTweet.str.contains( r'\b' + x + r'\b' ) )] ))
#print(  )
    
#freq = tkdf.isin( [uws] ).any(axis=1).value_counts()[ True ]

#if DEBUGGING:
#    j=0
#    for i in range( len( df[ 'OriginalTweet' ])):
#        if ( 'the' in tdfdf[ 'TokenizedTweet' ][i] ): j += 1
#    print(j)
#    print( len( tdf[( tdf[ 'CTweet' ].str.contains( r'\bthe\b' ))]))
#    print( len( tdf[( tdf[ 'TokenizedTweet' ].apply( lambda x: 'the' in x ))]))

#print( freq ) 

#freqdf = pd.DataFrame({ 'Word': words, 'DocCount': 0 })
#
#def get_doc_count( word ):
#    return len( df[( df[ 'CTweet' ].str.contains( r'\b' + word + r'\b' ))])
#
#print(freqdf.Word.apply(  ))
#
#freqdf[ 'DocCount' ] = freqdf.apply( lambda row: get_doc_count( row[ 'Word' ], 'AlteredTweet', df ) )
#
#print( f'Runtime: {time.time() - checkpoint}' )
#
#def count( x ):
#    
#    return frequencies
#
#freq = uwdf.apply( count )

######################## SECTION 1.4 ########################
time_check( 'Start 1.4' )
