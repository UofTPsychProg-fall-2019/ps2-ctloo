#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#

##assumes the wd is /ps2-ctloo
##this currently fails as the files were created during testing
testingrooms = ['A','B','C']
for room in testingrooms:
    shutil.copy('testingroom' + room + '/experiment_data.csv', 'rawdata')
    os.rename('rawdata/experiment_data.csv', 'rawdata/experiment_data_' + room + '.csv')



#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
    tmp = sp.loadtxt('rawdata/experiment_data_' + room + '.csv', delimiter = ',')
    data = np.vstack([data,tmp])



#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.average(data[:,3])   # 91.48%
mrt_avg = np.average(data[:,4])   # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#

#initialize containers
#word_acc_sum = 0
#word_rt_sum = 0
#word_count = 0
#face_acc_sum = 0
#face_rt_sum = 0
#face_count = 0

#for i in range(len(data)):
#    if data[i,1] == 1:
#        word_acc_sum += data[i,3]
#        word_rt_sum += data[i,4]
#    else:
#        word_count += 1
#        face_acc_sum += data[i,3]
#        face_rt_sum += data[i,4]
#        face_count += 1


#word_acc_avg = word_acc_sum/word_count
#word_mrt_avg = word_rt_sum/word_count
#face_acc_avg = face_acc_sum/face_count
#face_mrt_avg = face_rt_sum/face_count
# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms

#one line version
word_acc_avg = np.mean(data[data[:,1]==1,3])
word_mrt_avg = np.mean(data[data[:,1]==1,4])
face_acc_avg = np.mean(data[data[:,1]==2,3])
face_mrt_avg = np.mean(data[data[:,1]==2,4])

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#

# using logical indexing to select all the rows
acc_wp = np.mean(data[data[:,2] == 1, 3])  # 94.0%
acc_bp = np.mean(data[data[:,2] == 2, 3])  # 88.9%
mrt_wp = np.mean(data[data[:,2] == 1, 4])  # 469.6ms
mrt_bp = np.mean(data[data[:,2] == 2, 4])  # 485.1ms

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#


# splitting the data into separate arrays for words and faces using logical indexing
# words == 1, faces == 2
data_word = data[data[:,1]==1,:]
data_face = data[data[:,1]==2,:]

# using np.mean to calculate the mean rt of all the rows seleceted with logical indexing
# white/pleasant == 1, black/pleasant == 2
mrt_word_wp = np.mean(data_word[data_word[:,2] ==1, 4])
mrt_word_bp = np.mean(data_word[data_word[:,2] ==2, 4])
mrt_face_wp = np.mean(data_face[data_face[:,2] ==1, 4])
mrt_face_bp = np.mean(data_face[data_face[:,2] ==2, 4])

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats


ttest_word = scipy.stats.ttest_rel(data_word[data_word[:,2]==1,4], data_word[data_word[:,2]==2,4])
ttest_face = scipy.stats.ttest_rel(data_face[data_face[:,2]==1,4], data_face[data_face[:,2]==2,4])
# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
#print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))

print('\nOn blocks in which words were categorized, the average median response time for black/pleasant pairings ({:.1f} ms) was significantly greater than the average median response time for white/pleasant pairings ({:.1f} ms), t = {:.2f}, p < .001.'.format(mrt_word_bp, mrt_word_wp, ttest_word[0]))

print('\nOn blocks in which faces were categorized, the average median response time for black/pleasant pairings ({:.1f} ms) was significantly greater than the average median response time for white/pleasant pairings ({:.1f} ms), t = {:.2f}, p < .05.'.format(mrt_face_bp, mrt_face_wp, ttest_face[0]))

#other averages
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORD STIMULI: {:.2f}%, {:.1f} ms'.format(100*word_acc_avg,word_mrt_avg))
print('\nFACE STIMULI: {:.2f}%, {:.1f} ms'.format(100*face_acc_avg,face_mrt_avg))
print('\nCONGRUENCY (WHITE/PLEASANT): {:.2f}%, {:.1f} ms'.format(100*acc_wp,mrt_wp))
print('\nCONGRUENCY (BLACK/PLEASANT): {:.2f}%, {:.1f} ms'.format(100*acc_bp,mrt_bp))
