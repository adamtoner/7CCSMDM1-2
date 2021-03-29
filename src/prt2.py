#--
# prt2.py
# Implements solutions to sections 2 of the coursework on clustering
# @author: Adam Toner
# @created: 17 Feb 2021
#
#--

from logging import error
import sys
import math
import os
import csv
import numpy as np
import sklearn.cluster as cluster
import matplotlib.pyplot as plt

# Set the literals for the file
DEBUGGING = False
FILE_DIR = os.path.dirname(__file__)
OUT_DIR = FILE_DIR + '/../output/'
DATA_DIR = FILE_DIR + '/../data/'
DATA_FILE = 'wholesale_customers.csv'
CLUSTER_MARKERS = [ 'co', 'rv', 'b^', 'g<', 'm>', 'ys', 'kp', 'w*', 'bD', 'cP' ]

################################################ MAIN ################################################

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

# Drop the 'CHANNEL' and 'REGION' attributes
for line in rawdata:
    del line[1]
    del line[0]

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

################################################ SECTION 2.1 ################################################

M = len( rawdata ) # number of instances
H = len( header ) # number of attributes

if DEBUGGING:
    print( 'number of instances: ' + str( M ))

# change the rawdata into a numpy array of ints
np_rawdata = np.zeros(( M, H ))
try:
    for i in range( M ): # iterate through each instance
        np_rawdata[i] = np.array( [int( v ) for v in rawdata[i]] ) # convert each value in the instance to an int and store it in a numpy.array
        if ( i == 2 and DEBUGGING ): print(np_rawdata)
# Handle any exceptions
except ValueError as ve:
    print( 'There was a value error: ' + str( ve ))
    sys.exit()
except TypeError as te:
    print( 'There was a value error: ' + str( te ))
    sys.exit()
except Exception as x:
    print( 'There was an error: ' + str( x ))
    sys.exit()
del rawdata

# Create the empty arrays to store the range and mean info
ranges = np.zeros(( H, 2 ), np.int )
means = np.zeros(( H ), np.float )
for i in range( H ):
    col = np_rawdata[ :, i ]
    ranges[i][0] = np.amin( col )
    ranges[i][1] = np.amax( col )
    means[i] = np.mean( col )

if DEBUGGING:
    print( ranges )
    print( means )

# Build the table for the report
section1_table = [None] * ( H + 1 ) # Create the empty array for the table
section1_table[0] = ('Attribute', 'Mean', 'Range') # Create the table headers
for i in range( H ): # Populate the array with the values caluculated above
    section1_table[i + 1] = ( str( header[i] ), str( np.round( means[i], 2 ) ), '[ ' + str( np.round( ranges[i][0] )) + ', ' + str( np.round( ranges[i][1] )) + ' ]' )

if DEBUGGING: print( section1_table )

del ranges, means, col

################################################ SECTION 2.2 ################################################
# Define a method for fitting a dataset to a given number of clusters. 
# Note: this always fits the given dataset and would need to be edited to work with other datasets.
# This is fine for the purposes of this coursework.

def fit_cluster( n_clusters ):
    km = cluster.KMeans( n_clusters )
    km.fit( np_rawdata )
    return km

K = 3
km = fit_cluster( K )

# print the cluster center locations when debugging
if DEBUGGING:
    print ('cluster centres:')
    for k in range( K ):
        print('c{} = [{}, {}, {}, {}, {}, {}]'.format( k, km.cluster_centers_[k][0], km.cluster_centers_[k][1], km.cluster_centers_[k][2], km.cluster_centers_[k][3], km.cluster_centers_[k][4], km.cluster_centers_[k][5] ))


# plot clusters for each pair of attributes
plt.figure()
ind = 0
for i in range( H ): # iterate through the attributes
    for j in range( i+1, H ): # iterate through the remaining attributes
        for k in range( M ): # plot each datapoint with the correct colour according to clustering
            plt.plot( np_rawdata[k][i], np_rawdata[k][j], CLUSTER_MARKERS[km.labels_[k]], markersize=5 )
        # set the plot metadata
        plt.title( f'{header[i]} vs {header[j]}' )
        plt.xlabel( str( header[i] ) )
        plt.ylabel( str( header[j] ) )
        plt.savefig( OUT_DIR + 'prt2-' + str( ind ) + '.png' )
        ind += 1 # increment the naming index
#plt.show()
plt.close()

del K, km, ind

################################################ SECTION 2.3 ################################################

# Define a method for calculating the between score of the clusters
def bc_score( km ):
    k = km.n_clusters # number of clusters
    between = np.zeros(( k ))
    for i in range( k ): # loop through each cluster
        between[i] = 0.0
        for l in range( i+1, k ): # for each cluster, iterate through any remaining clusters for which the distance has not been added already
            # for each cluster, calculate the distance from the cluster center to each remaining cluster center
            between[i] += ( math.pow(( km.cluster_centers_[i][0]-km.cluster_centers_[l][0] ), 2 ) + math.pow(( km.cluster_centers_[i][1]-km.cluster_centers_[l][1] ), 2 ))
    return np.sum( between ) # sum all the distances and return

# Define a method for calculating the within score of the clusters
def wc_score( km, members ):
    k = km.n_clusters # number of clusters
    within = np.zeros(( k )) # initialise empty array to store the sum of distances to each center from their cluster members
    for i in range( k ): # iterate through each cluster
        within[i] = 0.0 
        for j in members[i]: # for each cluster, calculate the distance from the cluster center to each point and add it to the total
            within[i] += ( np.square( np_rawdata[j,0]-km.cluster_centers_[i][0] ) + np.square( np_rawdata[j,1]-km.cluster_centers_[i][1] ))
    return np.sum( within ) # sum all the distances and return


K = [3, 5, 10]
BC = np.zeros(( 3 ))
WC = np.zeros(( 3 ))
BC_WC = np.zeros(( 3 ))

for i in range( len( K )):
    # fit the dataset to K[i] clusters
    km = fit_cluster( K[i] )

    # work out the members of each cluster based on the label list
    members = [[] for j in range( K[i] )]
    for j in range( M ):
        members[ km.labels_[j] ].append( j )

    if i != 0:
        # Plot a graph for one of the attribute pairs for each value of K
        plt.figure()
        for k in range( M ): # plot each datapoint with the correct colour according to clustering
            plt.plot( np_rawdata[k][0], np_rawdata[k][1], CLUSTER_MARKERS[km.labels_[k]], markersize=5 )
        # set the plot metadata
        plt.title( f'Fresh vs Grocery ( k = { K[i] } )' )
        plt.xlabel( 'Fresh' )
        plt.ylabel( 'Grocery' )
        plt.savefig( OUT_DIR + 'prt2-k' + str( K[i] ) + '.png' )
        #plt.show()
        plt.close()

    # calculate the between score, within score and the ratio
    b = bc_score( km )
    w = wc_score( km, members )
    BC[i] = np.round( b, 1 ) # rounded to 1dp
    WC[i] = np.round( w, 1 ) # rounded to 1dp
    BC_WC[i] = np.round( b / w, 5 ) # rounded to 5dp

# Draw the table from the problem sheet
section3_table = [None] * 4 # Create the empty array for the table
section3_table[0] = ('', 'k = 3', 'k = 5', 'k = 10') # Create the table headers
def create_row_4_wide( heading, list ):
    return (heading, str( list[0] ), str( list[1] ), str( list[2] ))
section3_table[1] = create_row_4_wide( 'BC', BC )
section3_table[2] = create_row_4_wide( 'WC', WC )
section3_table[3] = create_row_4_wide( 'BC/WC', BC_WC )
# This is a bit clunky but format preserving of the given table.
del K, BC, WC, BC_WC, km, members