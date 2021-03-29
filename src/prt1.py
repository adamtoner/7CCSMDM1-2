#--
# prt1.py
# Implements solutions to sections 1 of the coursework on classification
# @author: Adam Toner
# @created: 17 Feb 2021
#
#--

import sys
import os
import csv
import numpy as np
import sklearn.model_selection as model_select
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from collections import Counter

# Set the constants for the file
DEBUGGING = False
FILE_DIR = os.path.dirname(__file__)
OUT_DIR = FILE_DIR + '/../output/'
DATA_DIR = FILE_DIR + '/../data/'
DOT_FILE = OUT_DIR + 'decision-tree.dot'
DATA_FILE = 'adult.csv'

######################## MAIN ########################

# Get the data from the csv file
try:
    f = open( DATA_DIR + DATA_FILE, 'rt' )
    rawdata0 = csv.reader(f)
    rawdata = [rec for rec in rawdata0]
# Handle the exceptions
except IOError as iox:
    print( 'there was an I/O error trying to open the data file: ' + str(iox) )
    sys.exit()
except Exception as x:
    print( 'there was an error: ' + str(x) )
    sys.exit

# Drop the fnlwgt attribute
for line in rawdata:
    del line[2]

# Save the header and remove it from the dataset
header = rawdata[0]
del rawdata[0]

if DEBUGGING:
    print( f'number of fields = { len ( header )}' )
    print( 'fields:' )
    i = 0
    for field in header:
        print( f'i={i} field={field}' )
        i = i + 1

del f, rawdata0

######################## SECTION 1.1 ########################

M = len( rawdata ) # number of instances
H = len( header ) # number of attributes

# Find number of missing values
num_missing = 0
incomplete_instances = []
# cycle through each instance to check for missing values
for i in range( M ):
    missing = False # reset for each instance
    # check each attribute
    for j in range( H ):
        if ( rawdata[i][j] == '' ):
            missing = True
            num_missing += 1
    # add the index of the instance with missing values to our list
    if missing: incomplete_instances.append( i ) 
        
N = len( incomplete_instances ) # number of instances with missing values

# split the dataset into complete and incomplete instances
split_data = [ [], [] ] # [ [no missing values], [missing values] ]
for i in range( M ):
    split_data[1].append( rawdata[i] ) if i in incomplete_instances else split_data[0].append( rawdata[i] )

# Calculate the fraction of missing values and incomplete instances    
frac_missing = num_missing / ( M * H)
frac_incomplete = N / M

section1_table = [('Number of Instances', str( M )), ('Number of Missing Values', str( num_missing )), ('Fraction of Missing Values', str( frac_missing )), ('Fraction of Incomplete Instances', str( frac_incomplete ))]

# print the values before creating the table and the pdf when debugging
if DEBUGGING:
    print( num_missing )
    print( len( incomplete_instances ))
    print( frac_missing )
    print( frac_incomplete )

del num_missing, incomplete_instances, frac_incomplete, frac_missing, missing, rawdata

######################## SECTION 1.2 ########################
# Convert all attributes into nominal using Scikit-learn LabelEncoder
com_encdata = np.array( split_data[0][:] ) # list of all complete instances to be encoded
pos_values = [] # list of all possible values for each attribute
section2_table = [('Attribute', 'Possible Values')] # table for displaying possible values in report
# iterate through each column and encode all of the values
for i in range( H ):
    le = LabelEncoder()
    com_encdata[:, i] = le.fit_transform( com_encdata[:, i] )
    pos_values.append( le.classes_ )
    section2_table.append(( str( header[i] ), str( pos_values[i] )[1:-1] )) # add row to report table
    if DEBUGGING:
        print( 'The possible values for \'' + str( header[i] ) + '\' are:')
        print( pos_values[i] )

del le

######################## SECTION 1.3 ########################
# Build a Decision Tree for classifying an individual
# split the data into training and test sets
x_train, x_test, y_train, y_test = model_select.train_test_split( com_encdata[:, :-1], com_encdata[:, -1], random_state=0 )

def build_tree(x_train_set, x_test_set, y_train_set, y_test_set, min_weight = 0.001, dot_file = ''):
    M_train = len( x_train_set )
    M_test = len( x_test_set )
    if DEBUGGING:
        print('number of training instances = ' + str( M_train ))
        print('number of test instances = ' + str( M_test ))

    # initialise the decision tree and fit it to the training data
    clf = tree.DecisionTreeClassifier( random_state = 0, min_weight_fraction_leaf = min_weight )
    clf.fit( x_train_set, y_train_set )

    # Calculate the resubstitution error
    # predict the labels for the training set and count the correct predictions
    y_hat = clf.predict( x_train_set )
    count = 0.0
    for i in range( M_train ):
        if y_hat[i] == y_train_set[i] : count += 1 
    resub_error = 1 - ( count / M_train ) # resub error calculation

    # Calculate the test error
    # predict the labels for the test set and count the correct predictions
    y_hat = clf.predict( x_test_set )
    count = 0.0
    for i in range( M_test ):
        if y_hat[i] == y_test_set[i] : count += 1
    test_error = 1 - ( count / M_test ) # test error calculation

    if DEBUGGING:
        # print error rates
        print( 'Resubstitution error: ' + str( resub_error ))
        print( 'Test error: ' + str( test_error ))

    # output the tree to dot format if file location is provided
    if ( dot_file != '' ):
        tree.export_graphviz( clf, out_file = dot_file, class_names=pos_values[-1], impurity=True )
        if DEBUGGING: print('Output dot file written to: ', dot_file)
    
    return([resub_error, test_error])

section3_error = build_tree( x_train, x_test, y_train, y_test, dot_file=DOT_FILE)
section3_table = [( 'Resubstitution error:', str( section3_error[0] )), ( 'Test error:', str( section3_error[1] ))]

del com_encdata, x_train, x_test, y_train, y_test, section3_error

######################## SECTION 1.4 ########################
# select at random the same number of complete instances as incomplete instances
tmp1 = np.random.choice( range( M - N ), N, replace = False ) # list of selected indices
if DEBUGGING: print(f'tmp1: {len( tmp1 )}')
d_split = [ [], [] ] # [ [training set], [test set] ]
for i in range( M-N ):
    d_split[0].append( split_data[0][i] ) if i in tmp1 else d_split[1].append( split_data[0][i] )

# Note: d_split[1] is the test set containing all (complete) instances not in the test set
# combine the list of incomplete and complete instances
d_prime = np.concatenate(( split_data[1], d_split[0] ))
d_test = np.array( d_split[1] )
del tmp1, d_split
if DEBUGGING: print(f'd_prime: { len( d_prime[0] )} x { len( d_prime )} \n d_test: { len( d_test[0] )} x { len( d_test )}')

# create new value 'missing' for any missing values
def fill_missing_missing(L):
    for i in range( len( L )):
        for j in range( len( L[0] )):
            if ( L[i][j] == '' ):
                L[i][j] = 'missing'
    return L

def fill_missing_popular(L):
    # create a list to store the most popular value for each attribute
    for i in range( len( L[0] )):
        # find the most popular value for the attribute which isn't missing
        pop = Counter( L[:, i] )
        pop_value = [pop.most_common()[0][0], pop.most_common()[1][0]][pop.most_common()[0][0] == '']
        if DEBUGGING: print( f'popular value: { pop_value }')
        # fill in the most popular value for any missing value
        for j in range( len ( L )):
            if ( L[j][i] == '' ): L[j][i] = pop_value
    return L
    

# create two copies of d_prime and d_test
# fill the missing values and get ready for encoding
d_prime1 = fill_missing_missing(np.array([rec for rec in d_prime])) # use rec for rec to create a copy and prevent referencing confusion
d_prime2 = fill_missing_popular(np.array([rec for rec in d_prime]))
del d_prime
d_test1 = np.empty(( M - 2 * N, H ), np.str)
d_test2 = np.empty(( M - 2 * N, H ), np.str)

# Convert training set 1 and test set 1 to nominal
for i in range( len( header )):
    le = LabelEncoder()
    d_prime1[:, i] = le.fit_transform( d_prime1[:, i] )
    d_test1[:, i] = le.fit_transform([rec for rec in d_test[:, i]])
del le

# Convert training set 2 and test set 2 to nominal
for i in range( len( header )):
    le = LabelEncoder()
    d_prime2[:, i] = le.fit_transform( d_prime2[:, i] )
    d_test2[:, i] = le.fit_transform([rec for rec in d_test[:, i]])
del le

if DEBUGGING:
    print(f'd_prime1: { len( d_prime1[0] )} x { len( d_prime1 )} \n d_test1: { len( d_test1[0] )} x { len( d_test1 )}')
    print(f'd_prime2: { len( d_prime2[0] )} x { len( d_prime2 )} \n d_test2: { len( d_test2[0] )} x { len( d_test2 )}')


# Build the decision trees
if DEBUGGING:
    print( '\n Method 1:' )
method1_error = build_tree(d_prime1[:, :-1], d_test1[:, :-1], d_prime1[:, -1], d_test1[:, -1], 0.006, OUT_DIR + 'prt1-method1.dot')
method1_table = [( 'Resubstitution error:', str( method1_error[0] )), ( 'Test error:', str( method1_error[1] ))]
if DEBUGGING:
    print( '\n Method 2:' )
method2_error = build_tree(d_prime2[:, :-1], d_test2[:, :-1], d_prime2[:, -1], d_test2[:, -1], 0.006, OUT_DIR + 'prt1-method2.dot')
method2_table = [( 'Resubstitution error:', str( method2_error[0] )), ( 'Test error:', str( method2_error[1] ))]