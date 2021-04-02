#--
# prt2.py
# Implements solutions to sections 2 of the coursework on image processing
# @author: Adam Toner
# @created: 30 Mar 2021
#
#--

from logging import error
import sys
import math
import os
import csv
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import skimage.color as color
import skimage.filters as filters
import skimage.util as util
import scipy.ndimage as ndi
import imageio
import matplotlib.pyplot as plt

# Set the literals for the file
DEBUGGING = True
FILE_DIR = os.path.dirname(__file__)
OUT_DIR = FILE_DIR + '/../output/'
DATA_DIR = FILE_DIR + '/../data/image_data/'
DATA_FILE = ''

######################## MAIN ########################
im_ave = imageio.imread( DATA_DIR + 'avengers_imdb.jpg' )
im_bhw = imageio.imread( DATA_DIR + 'bush_house_wikipedia.jpg' )
im_fcg = imageio.imread( DATA_DIR + 'forestry_commission_gov_uk.jpg' )
im_rgt = imageio.imread( DATA_DIR + 'rolland_garros_tv5monde.jpg' )

######################## SECTION 2.1 ########################
print( im_ave.shape )
im_ave_gray = color.rgb2gray( im_ave )
plt.imshow( im_ave_gray, cmap="gray" )
plt.savefig( OUT_DIR + 'avengers_imdb_grayscale.png' )

threshold = filters.threshold_otsu( im_ave_gray )
binary_img = im_ave_gray > threshold
plt.imshow( binary_img, cmap=plt.cm.gray, interpolation='nearest' )
plt.savefig( OUT_DIR + 'avengers_imdb_bw.png' )

######################## SECTION 2.2 ########################
im_bhw_noise = util.random_noise( im_bhw, mode = 'gaussian', seed = None, clip = True, var = 0.1 )
plt.imshow( im_bhw_noise )
plt.savefig( OUT_DIR + 'im_bhw_noise.png' )

im_bhw_gfilter = filters.gaussian( im_bhw_noise, sigma = 1 )
plt.imshow( im_bhw_gfilter )
plt.savefig( OUT_DIR + 'im_bhw_gfilter.png' )

im_bhw_ufilter = ndi.uniform_filter( im_bhw_noise, size = 9 )
plt.imshow( im_bhw_ufilter )
plt.savefig( OUT_DIR + 'im_bhw_ufilter.png' )

im_bhw_bfilter = ndi.uniform_filter( im_bhw_gfilter, size = 9 )
plt.imshow( im_bhw_bfilter )
plt.savefig( OUT_DIR + 'im_bhw_bfilter.png' )

######################## SECTION 2.3 ########################



######################## SECTION 2.4 ########################
