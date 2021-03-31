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

# Create a function to print the checkpoint times to see where the program can be improved
def time_check( cp ):
    if TIMING:
        print( f'\n## {cp}: { time.time() - start }' )

######################## SECTION 1.1 ########################
time_check( 'Start 1.1' )



# Print the number of unique sentiments.
print( f'There are {} possible sentiments that a tweet may have.' )
# Find the second most popular sentiment in the tweets.
print( f'The second most popular tweet sentiment is {  }.' )
# Find the date with the greates number of extremely positive tweets.
print( f'The day with the most extremely positive tweets was {  }.' )


# Using vectorized string methods to clean up the spacing
def clean_spacing( series ):
    series = series.str.replace( '\s\s+', ' ' ) #remove all but single spacing
    series = series.str.strip() #strip whitespace before tokenization to avoid counting whitespace as words
    return series

if DEBUGGING: 
    print( '\n\n Original Tweets:' )
    print( )
    print( '\n\n Altered Tweets:' )
    print( )

######################## SECTION 1.2 ########################
# Tokenize the tweets
time_check( 'Start 1.2' )

# Print the number of words in the corpus
print( f'With stop words, there are {} words total, {} of which are unique.' )
print( f'Without stop words, there are {} words total, {} of which are unique.' )
print( '\nThe ten most frequently used words are:')
print( f'With stop words: {}' )
print( f'Without stop words: {}' )

######################## SECTION 1.3 ########################
time_check( 'Start 1.3' )

######################## SECTION 1.4 ########################
time_check( 'Start 1.4' )
