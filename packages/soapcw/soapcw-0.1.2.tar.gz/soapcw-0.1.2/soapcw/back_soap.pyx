# cython: language_level=3
from __future__ import division
import numpy as np
import timeit
import itertools
import time
import pickle
import json
from sys import stdout
#import scipy.special as sp
#from scipy.misc import logsumexp
from libc.math cimport log,exp,sqrt 
from scipy.interpolate import interp2d,RectBivariateSpline
from scipy.special import logsumexp

class single_detector(object):
 
    def __init__(self, tr, obs, weight = None, prog = False,stat_t="sum",lookup_file=None):
        '''
        initialising viterbi class
        '''
        self.prog = prog
        
        # make sure input data of right type
        tr = np.array(tr).astype('double')
        obs = np.array(obs).astype('double')

        # make sure input data of right shape
        if len(np.shape(tr)) != 1:
            raise Exception("transition matrix wrong shape, should be Kx1 array")
        if len(np.shape(obs)) != 2:
            raise Exception("observation wrong shape, should be NxM array")
        if stat_t == "sum":
            self.run_sum(tr, obs)
        elif stat_t == "lookup":
            self.run_lookup(tr, obs,lookup_file)

        self.get_vitmap()

        
    #------------------------------------------------------------------------------------------------
    # Get Viterbi map
    #------------------------------------------------------------------------------------------------

    def get_vitmap(self,log=False):
        """
        normalise the viterbi output such that the sum of eah column is 1
        """
        path_m = []
        for i in self.V:
            sump = logsumexp(i)
            val = np.exp(i-sump)
            path_m.append(val)
        path_m = np.array(path_m)
        if log:
            path_m = np.log(path_m)

        self.vitmap = path_m


    
    
    #-------------------------------------------------------------------------------------------------
    # Basic Viterbi Algorithm
    #-------------------------------------------------------------------------------------------------

    
    def run_sum(self,double[:] tr, double[:, :] obs, double[:] weight = None):
        '''
        Run the viterbi algorithm for given single set of data and 3x1 transition matrix.
        This returns the track through the data which gives the largest sum of power.
        Args
        ------
        tr: array
            transition matrix of sixe Kx1
        obs: array
            observation data of size NxM
        Returns
        -------
        vit_track: array
            index of the viterbi path found in data
        max_end_prob: float
            maximum probability at end of path
        V: array
           viterbi matrix
        prev: array
            previous positions of paths for each bin
        '''
        
        # find shape of the observation and create empty array for citerbi matrix and previous track positions
        shape = np.shape(obs)
        cdef double[:, :] V = np.zeros(shape)
        cdef long[:, :] prev = np.zeros(shape,dtype=np.int)
        
        # defining variables
        cdef int t,i,j         # indexes
        cdef double pbar = 0   # progress bar
        cdef double pt
        
        # finding length and width of observation
        cdef int length = shape[0]#len(obs)
        cdef int width = shape[1]#len(obs[0])
        
        # find size of the transition matrix
        cdef int tr_length = len(tr)
        # find half width of transntion, i.e. number of bins up and down it can move
        cdef int tr_width = int((tr_length-1)/2 )
        
        # run for first time index, i.e. fill with observation
        for i in range(width):
            V[0][i] = obs[0][i]
            prev[0][i] = 1
        
        # apply a weight to each time segment
        wtrue = False
        if weight == None:
            wtrue = False
        else:
            wtrue = True
        
        # run iterative part of algorithm
        for t in range(1,length):
            pt = t/(length)*100
            for i in range(width):
                temp = -1e6
                for j in range(tr_length):
                    if i+j-tr_width>=0 and i+j-tr_width<=width-1:
                        if wtrue:
                            value =(obs[t][i]+tr[j]+V[t-1][i+j-tr_width] - weight[t]) #- obs[t][i+1] - obs[t][i-1]
                        else:
                            value = obs[t][i]+tr[j]+V[t-1][i+j-tr_width] #- obs[t][i+1] - obs[t][i-1]
                        if value>temp:
                            temp = value
                            V[t][i] = temp
                            prev[t][i] = i+j-tr_width
                        elif value == temp and j == int(tr_length/2.):
                            temp = value
                            V[t][i] = temp
                            prev[t][i] = i+j-tr_width
                            

            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./len(obs)
    
        cdef double max_end_prob = max(V[length-1][i] for i in range(width))
        cdef int previous
        cdef long[:] vit_track = np.zeros(length,dtype=np.int)
        
                        
        for i in range(width):
            if V[length-1][i] == max_end_prob:
                vit_track[length-1] = i # appends maximum path value from final step
                previous = prev[length-1][i]
                break

        for t in range(len(V)-2,-1,-1):
            vit_track[t] = previous # insert previous step
            previous = prev[t][previous]

        self.vit_track = np.array(vit_track)
        self.max_end_prob = max_end_prob
        self.V = np.array(V)
        self.prev = np.array(prev)
        
    def run_lookup(self,double[:] tr, double[:, :] obs, lookup_file = None):
        '''
        Run the viterbi algorithm for given single set of data and 3x1 transition matrix.
        This returns the track through the data which gives the largest sum of power.
        Args
        ------
        tr: array
            transition matrix of sixe Kx1
        obs: array
            observation data of size NxM
        Returns
        -------
        vit_track: array
            index of the viterbi path found in data
        max_end_prob: float
            maximum probability at end of path
        V: array
           viterbi matrix
        prev: array
            previous positions of paths for each bin
        '''
        
        # find shape of the observation and create empty array for citerbi matrix and previous track positions
        shape = np.shape(obs)
        cdef double[:, :] V = np.zeros(shape)
        cdef long[:, :] prev = np.zeros(shape,dtype=np.int)
        
        # defining variables
        cdef int t,i,j         # indexes
        cdef double pbar = 0   # progress bar
        cdef double pt
        
        # finding length and width of observation
        cdef int length = shape[0]#len(obs)
        cdef int width = shape[1]#len(obs[0])
        
        # find size of the transition matrix
        cdef int tr_length = len(tr)
        # find half width of transntion, i.e. number of bins up and down it can move
        cdef int tr_width = int((tr_length-1)/2 )
        
        
        with open(lookup_file,'r') as f1:
            line = f1.readline()
            line = line.rstrip('\n')
            l_vals_1d = [float(v) for v in line.split(" ")[1:]]
            likelihood_1d = np.loadtxt(f1)

        ranges_1d = np.linspace(l_vals_1d[0],l_vals_1d[1],int(l_vals_1d[2]))
        logarr_1d = likelihood_1d
        fact_1d = abs(1./(ranges_1d[0] - ranges_1d[1]))
        
        # run for first time index, i.e. fill with observation
        for i in range(width):
            V[0][i] = obs[0][i]
            prev[0][i] = 1
        
        
        # run iterative part of algorithm
        for t in range(1,length):
            pt = t/(length)*100
            for i in range(width):
                temp = -1e6
                for j in range(tr_length):
                    if i+j-tr_width>=0 and i+j-tr_width<=width-1:
                        value = obs[t][i]+tr[j]+V[t-1][i+j-tr_width] #- obs[t][i+1] - obs[t][i-1]
                        if value>temp:
                            temp = value
                            V[t][i] = temp
                            prev[t][i] = i+j-tr_width
                        elif value == temp and j == int(tr_length/2.):
                            temp = value
                            V[t][i] = temp
                            prev[t][i] = i+j-tr_width
                            

            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./len(obs)
    
        cdef double max_end_prob = max(V[length-1][i] for i in range(width))
        cdef int previous
        cdef long[:] vit_track = np.zeros(length,dtype=np.int)
        
                        
        for i in range(width):
            if V[length-1][i] == max_end_prob:
                vit_track[length-1] = i # appends maximum path value from final step
                previous = prev[length-1][i]
                break

        for t in range(len(V)-2,-1,-1):
            vit_track[t] = previous # insert previous step
            previous = prev[t][previous]

        self.vit_track = np.array(vit_track)
        self.max_end_prob = max_end_prob
        self.V = np.array(V)
        self.prev = np.array(prev)


class two_detector(object):
 
    def __init__(self, tr1, obs11, obs21, beta=0, stat_t='sum', lookup_file_2det = None, lookup_file_1det = None, prog = False,fractions=None):
        '''
        viterbi algorithm for two detectors with an optional line veto statistic
        uses S = \frac{p(ss \mid x)}{p(nn \mid x)+p(ns \mid x)+p(sn \mid x)}
        if beta not set, default is no line veto statistic just sum of powers
        [currently configured for averaging over 48 SFT need to change to correctly use any]
        Args
        ---------
        tr1: array
            transition matrix
        obs11: array
            observation from detector 1
        obs21: array
            observation from detector 2 
        beta: float (optional)
            tuning parameter for line veto statistic, set to 0 as default i.e. no line veto statistic
        stat_t: string
            define which version of two detector search you want, 
            options = {"sum" : uses the sum of the fft power in each detector as statistic ,
                       "lookup" : uses a lookup table for 2d generated statistic ,
                       "lookupgaps" : uses two lookup tables where 2det one is used when there is data in both detectors, 1det used when only one detector data, 
                       "lookupnoise" : uses a 3 dimensional lookup table which takes into account the ratio of the amount of data and noise floor between detectors}
        lookup_file_1det: string (optional)
            filepath of lookup table for the one detector case
        lookup_file_2det: string ( optional)
            filepath of lookup table for the two detector case
        prog: bool (optional)
            show progress bar if True 
        fractions: array (optional)
            array of the ratio of the noise floor and amount of data between detectors
        returns
        -----------
        vit_track1: array
            path in detector 1
        vit_track2: array
            path in detector2
        vit_track_ref: array
            path in reference detector
        V: array
            viterbi values in reference detector
        prev: array
            previous positions before jump
        max_prob: double
            maximum end path probability

        '''
        self.prog = prog
        if stat_t == "sum":
            self.run_sum(tr1, obs11, obs21)
        elif stat_t == "lookup":
            self.run_lookup(tr1, obs11, obs21,lookup_file_2det)
        elif stat_t == "lookupgaps":
            self.run_lookup_gaps(tr1, obs11, obs21,lookup_file_1det=lookup_file_1det, lookup_file_2det=lookup_file_2det)
        elif stat_t == "lookupnoise":
            self.run_lookup_noise(tr1, obs11, obs21,lookup_file=lookup_file_2det,fractions=fractions)

        else:
            print("no type specified, running soap summing fft powers")
            self.run_sum(tr1, obs11, obs21)
            
        self.get_track()
        self.get_vitmap()

    #------------------------------------------------------------------------------------------------
    # Get Viterbi map
    #------------------------------------------------------------------------------------------------

    def get_vitmap(self,log=False):
        """
        normalise the viterbi output such that the sum of eah column is 1
        """
        path_m = []
        for i in self.V:
            sump = logsumexp(i)
            val = np.exp(i-sump)
            path_m.append(val)
        path_m = np.array(path_m)
        if log:
            path_m = np.log(path_m)

        self.vitmap = path_m


    #---------------------------------------------------------
    # Two detector viterbi
    #--------------------------------------------------------


    def run_lookup(self,tr1, obs11, obs21,lookup_file = None):
        """
        viterbi algorithm for two detectors with an lookup table for the line veto statistic
        Args
        ---------
        tr1: array
            transition matrix
        obs11: array
            observation from detector 1
        obs21: array
            observation from detector 2 
        lookup_file: float
            links to a file which contains a 2d lookup table
        returns
        -----------
        V: array
            viterbi values in reference detector
        prev: array
            previous positions before jump
        """
        
        cdef double[:, :, :] tr = tr1
        cdef double[:, :] obs1 = obs11
        cdef double[:, :] obs2 = obs21
        
        shape = np.shape(obs1)
        
        cdef int length = min(len(obs1),len(obs2))
        cdef int width = len(obs1[0])
        
        cdef double[:, :] val = np.ones(shape)*-1e6
        cdef long[:, :] prev = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det1 = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det2 = np.zeros(shape,dtype = np.int)
        
        cdef int tr_len = len(tr)
        cdef int sep_len = len(tr[0])
        cdef int tr_dist = int(len(tr)/2. - 0.5)
        cdef int sep_dist = int(len(tr)/2. - 0.5)
        
        cdef int i
        cdef int j
        cdef int k
        cdef int m
        cdef int t
        cdef int x

        
        cdef long max_pos
        cdef long[:] indicies
        cdef double max_val
        cdef double value
        cdef double temp
        cdef int edge_range = 0

        # currently set for sum of 48 sfts, will change to be a parameter dependent of summing 
        cdef double mean = 96.0
        cdef double sigma = 13.85

        cdef double[:,:] logarr
        cdef double fact 
        
        with open(lookup_file,'r') as f1:
            line = f1.readline()
            line = line.rstrip('\n')
            l_vals = [float(v) for v in line.split(" ")[1:]]
            likelihood = np.loadtxt(f1)

        ranges = np.linspace(l_vals[0],l_vals[1],int(l_vals[2]))
        logarr = likelihood
        fact = abs(1./(ranges[0] - ranges[1]))

        for i in range(width):
            temp = -1e6
            for k in range(sep_len): 
                if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                    for m in range(sep_len):
                        if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                            try:
                                value = tr[1][k][m] + logarr[int(obs1[0][i+k-sep_dist]*fact),int(obs2[0][i+m-sep_dist]*fact)]
                            except IndexError:
                                try:
                                    value = tr[1][k][m] + logarr[-1,int(obs2[0][i+m-sep_dist]*fact)]
                                except IndexError:
                                    try:
                                        value = tr[1][k][m] + logarr[int(obs1[0][i+k-sep_dist]*fact),-1]
                                    except IndexError:
                                        value = tr[1][k][m] + logarr[-1,-1]
                            if value > temp:
                                temp = value
                                val[0][i] = temp
                                prev[0][i] =  i
                                det1[0][i] =  i+k-1 
                                det2[0][i] =  i+m-1
                            else:
                                continue
    
        # i is current frequency position
        # j is transition in reference detector
        # k is separation of first detector
        # m is separation of second detector


        
        pbar = 0
        for t in range(1,length):
            pt = t/(float(length))*100.
            for i in range(width):
                temp = -np.inf
                for j in range(tr_len):
                    if i+j-tr_dist>=0 and i+j-tr_dist<width:
                       for k in range(sep_len):
                            if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                                for m in range(sep_len):
                                    if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                                        try:
                                            value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[int(obs1[t][i+k-sep_dist]*fact),int(obs2[t][i+m-sep_dist]*fact)]
                                        except IndexError:
                                            try:
                                                value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[-1,int(obs2[t][i+m-sep_dist]*fact)]
                                            except IndexError:
                                                try:
                                                    value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[int(obs1[t][i+k-sep_dist]*fact),-1]
                                                except IndexError:
                                                    value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[-1,-1]
                                        if value > temp:
                                            temp = value
                                            val[t][i] = temp
                                            prev[t][i] =  i+j-tr_dist
                                            det1[t][i] =  i+k-sep_dist
                                            det2[t][i] =  i+m-sep_dist
                                        else:
                                            continue
            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length

        self.V = np.array(val)
        self.prev = np.array(prev)
        self.det1 = np.array(det1)
        self.det2 = np.array(det2)
        self.width = width
        self.length = length

    def run_lookup_gaps(self,tr1, obs11, obs21,lookup_file_1det = None,lookup_file_2det = None):
        """
        viterbi algorithm for two detectors with an lookup table for the line veto statistic

        Where there is only one detectors data use the single detector search with the same statistic
        Args
        ---------
        tr1: array
            transition matrix
        obs11: array
            observation from detector 1
        obs21: array
            observation from detector 2 
        lookup_file: float
            links to a file which contains a 2d lookup table
        returns
        -----------
        V: array
            viterbi values in reference detector
        prev: array
            previous positions before jump
        """
        
        cdef double[:, :, :] tr = tr1
        cdef double[:, :] obs1 = obs11
        cdef double[:, :] obs2 = obs21
        
        shape = np.shape(obs1)
        
        cdef int length = min(len(obs1),len(obs2))
        cdef int width = len(obs1[0])
        
        cdef double[:, :] val = np.ones(shape)*-1e6
        cdef long[:, :] prev = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det1 = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det2 = np.zeros(shape,dtype = np.int)
        
        cdef int tr_len = len(tr)
        cdef int sep_len = len(tr[0])
        cdef int tr_dist = int(len(tr)/2. - 0.5)
        cdef int sep_dist = int(len(tr)/2. - 0.5)
        
        cdef int i
        cdef int j
        cdef int k
        cdef int m
        cdef int t
        cdef int x

        
        cdef long max_pos
        cdef long[:] indicies
        cdef double max_val
        cdef double value
        cdef double temp
        cdef int edge_range = 0

        # currently set for sum of 48 sfts, will change to be a parameter dependent of summing 
        cdef double mean = 96.0
        cdef double sigma = 13.85

        cdef double[:,:] logarr_2d
        cdef double[:] logarr_1d
        cdef double fact 
        
        with open(lookup_file_1det,'r') as f1:
            line = f1.readline()
            line = line.rstrip('\n')
            l_vals_1d = [float(v) for v in line.split(" ")[1:]]
            likelihood_1d = np.loadtxt(f1)

        with open(lookup_file_2det,'r') as f1:
            line = f1.readline()
            line = line.rstrip('\n')
            l_vals_2d = [float(v) for v in line.split(" ")[1:]]
            likelihood_2d = np.loadtxt(f1)

        ranges_1d = np.linspace(l_vals_1d[0],l_vals_1d[1],int(l_vals_1d[2]))
        logarr_1d = likelihood_1d
        fact_1d = abs(1./(ranges_1d[0] - ranges_1d[1]))

        ranges_2d = np.linspace(l_vals_2d[0],l_vals_2d[1],int(l_vals_2d[2]))
        logarr_2d = likelihood_2d
        fact_2d = abs(1./(ranges_2d[0] - ranges_2d[1]))

        f1det1 = False
        f2det2 = False
        if len(set(obs1[0])) == 1:
            f1det1 = True
        if len(set(obs2[0])) == 1:
            f1det2 = True
            
        for i in range(width):
            temp = -1e6
            for k in range(sep_len): 
                if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                    for m in range(sep_len):
                        if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                            o1 = obs1[0][i+k-sep_dist]
                            o2 = obs2[0][i+m-sep_dist]
                            if f1det1 == True and f1det2 == False:
                                try:
                                    value = tr[1][k][m] + logarr_1d[int(o1*fact_1d)]
                                except IndexError:
                                    value = tr[1][k][m] + logarr_1d[-1]
                            elif f1det2 == True and f1det1 == False:
                                try:
                                    value = tr[1][k][m] + logarr_1d[int(o2*fact_1d)]
                                except IndexError:
                                    value = tr[1][k][m] + logarr_1d[-1]

                            else:
                                try:
                                    value = tr[1][k][m] + logarr_2d[int(o1*fact_2d),int(o2*fact_2d)]
                                except IndexError:
                                    try:
                                        value = tr[1][k][m] + logarr_2d[-1,int(o2*fact_2d)]
                                    except IndexError:
                                        try:
                                            value = tr[1][k][m] + logarr_2d[int(o1*fact_2d),-1]
                                        except IndexError:
                                            value = tr[1][k][m] + logarr_2d[-1,-1]
                            if value > temp:
                                temp = value
                                val[0][i] = temp
                                prev[0][i] =  i
                                det1[0][i] =  i+k-1 
                                det2[0][i] =  i+m-1
                            else:
                                continue
    
        # i is current frequency position
        # j is transition in reference detector
        # k is separation of first detector
        # m is separation of second detector

        
        pbar = 0
        for t in range(1,length):
            pt = t/(float(length))*100.
            f1det1 = False
            f1det2 = False
            if len(set(obs1[t])) == 1:
                f1det1 = True
            if len(set(obs2[t])) == 1:
                f1det2 = True
            for i in range(width):
                temp = -np.inf
                for j in range(tr_len):
                    if i+j-tr_dist>=0 and i+j-tr_dist<width:
                       for k in range(sep_len):
                            if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                                for m in range(sep_len):
                                    if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                                        o1 = obs1[t][i+k-sep_dist]
                                        o2 = obs2[t][i+m-sep_dist]
                                        if f1det1 == True and f1det2 == False:
                                            try:
                                                value = tr[j][k][m] + logarr_1d[int(o1*fact_1d)] + val[t-1][i+j-tr_dist]
                                            except IndexError:
                                                value = tr[j][k][m] + logarr_1d[-1] + val[t-1][i+j-tr_dist]
                                        elif f1det2 == True and f1det1 == False:
                                            try:
                                                value = tr[j][k][m] + logarr_1d[int(o2*fact_1d)] + val[t-1][i+j-tr_dist]
                                            except IndexError:
                                                value = tr[j][k][m] + logarr_1d[-1] + val[t-1][i+j-tr_dist]
                                        else:
                                            try:
                                                value = tr[j][k][m] + logarr_2d[int(o1*fact_2d),int(o2*fact_2d)] + val[t-1][i+j-tr_dist]
                                            except IndexError:
                                                try:
                                                    value = tr[j][k][m] + logarr_2d[-1,int(o2*fact_2d)] + val[t-1][i+j-tr_dist]
                                                except IndexError:
                                                    try:
                                                        value = tr[j][k][m] + logarr_2d[int(o1*fact_2d),-1] + val[t-1][i+j-tr_dist]
                                                    except IndexError:
                                                        value = tr[j][k][m] + logarr_2d[-1,-1] + val[t-1][i+j-tr_dist]

                                        if value > temp:
                                            temp = value
                                            val[t][i] = temp
                                            prev[t][i] =  i+j-tr_dist
                                            det1[t][i] =  i+k-sep_dist
                                            det2[t][i] =  i+m-sep_dist
                                        else:
                                            continue

            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length

        self.V = np.array(val)
        self.prev = np.array(prev)
        self.det1 = np.array(det1)
        self.det2 = np.array(det2)
        self.width = width
        self.length = length

    def run_lookup_noise(self,tr1, obs11, obs21,lookup_file = None, fractions = None):
        """
        viterbi algorithm for two detectors with an lookup table for the line veto statistic
        Args
        ---------
        tr1: array
            transition matrix
        obs11: array
            observation from detector 1
        obs21: array
            observation from detector 2 
        lookup_file: float
            links to a file which contains a 2d lookup table
        returns
        -----------
        V: array
            viterbi values in reference detector
        prev: array
            previous positions before jump
        """
        print("start")
        cdef double[:, :, :] tr = tr1
        cdef double[:, :] obs1 = obs11
        cdef double[:, :] obs2 = obs21
        
        shape = np.shape(obs1)
        
        cdef int length = min(len(obs1),len(obs2))
        cdef int width = len(obs1[0])
        
        cdef double[:, :] val = np.ones(shape)*-1e6
        cdef long[:, :] prev = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det1 = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det2 = np.zeros(shape,dtype = np.int)
        
        cdef int tr_len = len(tr)
        cdef int sep_len = len(tr[0])
        cdef int tr_dist = int(len(tr)/2. - 0.5)
        cdef int sep_dist = int(len(tr)/2. - 0.5)
        
        cdef int i
        cdef int j
        cdef int k
        cdef int m
        cdef int t
        cdef int x

        
        cdef long max_pos
        cdef long[:] indicies
        cdef double max_val
        cdef double value
        cdef double temp
        cdef int edge_range = 0

        # currently set for sum of 48 sfts, will change to be a parameter dependent of summing 
        cdef double mean = 96.0
        cdef double sigma = 13.85

        cdef double[:,:,:,:] logarr
        cdef int[:,:] abbl
        cdef int[:,:] frac_ind
        cdef double fact
        cdef double fact_frac
        print("defs")
        
        # load the 3 dimensional lookup table
        with open(lookup_file,'r') as f1:
            l_vals,likelihood = json.load(f1)

        # get the range of powers which are used and convert to and index for the lookup table
        ranges = np.linspace(l_vals[0],l_vals[1],int(l_vals[2]))
        print("ranges")
        # define the likelihood as two array one which is the transpose of the other, such that the fractions of time one detector is on can calways be compared witha  value less than 1
        shp = np.shape(likelihood)
        logarr1 = np.zeros((2,shp[0],shp[1],shp[2]))
        logarr1[0] = likelihood
        logarr1[1] = ([np.array(lkl).T for lkl in likelihood])
        print("logarr1")
        logarr = logarr1
        print("likelihood")
        # factor to shift the power values by to be an index
        fact = abs(1./(ranges[0] - ranges[1]))

        # get the range for the fraction of data 
        frac_ranges = np.linspace(l_vals[3],l_vals[4],int(l_vals[5]))
        fact_frac = abs(1./(frac_ranges[0] - frac_ranges[1]))
        print("fact_frac")
        # if the fractions are above a value of 1, inverse the lookup table so that only values between 0 and 1 have to be generated.

        if len(np.shape(fractions)) == 1:
            fractions = np.array([np.ones(width)*i for i in fractions])
            
        abbl1 = np.ones(np.shape(fractions)).astype(np.int32)
        abbl1[fractions > 1] = int(1)
        abbl1[fractions <= 1] = int(0)
        abbl = abbl1
        print("abbl")
        
        fractions[fractions > 1] = 1./fractions[fractions > 1]
        # make sure the fractions are the same dimensions as the input data and convert into an index
        if len(np.shape(fractions)) == 1:
            frac_ind = np.array(np.array(np.round(fractions*fact_frac)) + int(l_vals[5]/2.)).astype(np.int32)
        else:
            frac_ind = np.array(np.array(np.round(fractions*fact_frac)) + int(l_vals[5]/2.)).astype(np.int32)
        print("frac")
        
        for i in range(width):
            temp = -1e6
            for k in range(sep_len): 
                if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                    for m in range(sep_len):
                        if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                            try:
                                value = tr[1][k][m] + logarr[abbl[0,i],frac_ind[0,i],int(obs1[0][i+k-sep_dist]*fact),int(obs2[0][i+m-sep_dist]*fact)]
                            except IndexError:
                                try:
                                    value = tr[1][k][m] + logarr[abbl[0,i],frac_ind[0,i],-1,int(obs2[0][i+m-sep_dist]*fact)]
                                except IndexError:
                                    try:
                                        value = tr[1][k][m] + logarr[abbl[0,i],frac_ind[0,i],int(obs1[0][i+k-sep_dist]*fact),-1]
                                    except IndexError:
                                        value = tr[1][k][m] + logarr[abbl[0,i],frac_ind[0,i],-1,-1]
                            if value > temp:
                                temp = value
                                val[0][i] = temp
                                prev[0][i] =  i
                                det1[0][i] =  i+k-1 
                                det2[0][i] =  i+m-1
                            else:
                                continue
        print("init")
        # i is current frequency position
        # j is transition in reference detector
        # k is separation of first detector
        # m is separation of second detector


        
        pbar = 0
        for t in range(1,length):
            pt = t/(float(length))*100.
            for i in range(width):
                temp = -np.inf
                for j in range(tr_len):
                    if i+j-tr_dist>=0 and i+j-tr_dist<width:
                       for k in range(sep_len):
                            if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                                for m in range(sep_len):
                                    if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                                        try:
                                            value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[abbl[t,i],frac_ind[t,i],int(obs1[t][i+k-sep_dist]*fact),int(obs2[t][i+m-sep_dist]*fact)]
                                        except IndexError:
                                            try:
                                                value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[abbl[t,i],frac_ind[t,i],-1,int(obs2[t][i+m-sep_dist]*fact)]
                                            except IndexError:
                                                try:
                                                    value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[abbl[t,i],frac_ind[t,i],int(obs1[t][i+k-sep_dist]*fact),-1]
                                                except IndexError:
                                                    value = tr[j][k][m] + val[t-1][i+j-tr_dist] + logarr[abbl[t,i],frac_ind[t,i],-1,-1]
                                        if value > temp:
                                            temp = value
                                            val[t][i] = temp
                                            prev[t][i] =  i+j-tr_dist
                                            det1[t][i] =  i+k-sep_dist
                                            det2[t][i] =  i+m-sep_dist
                                        else:
                                            continue
            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length

        self.V = np.array(val)
        self.prev = np.array(prev)
        self.det1 = np.array(det1)
        self.det2 = np.array(det2)
        self.width = width
        self.length = length


    def run_sum(self,tr1, obs11, obs21):
        """
        Viterbi for two detectors where just the sum of the powers in each detector is taken
        Args
        ---------
        tr1: array
            transition matrix
        obs11: array
            observation from detector 1
        obs21: array
            observation from detector 2 
        returns
        -----------
        V: array
            viterbi values in reference detector
        prev: array
            previous positions before jump
        """
        
        cdef double[:, :, :] tr = tr1
        cdef double[:, :] obs1 = obs11
        cdef double[:, :] obs2 = obs21
        
        shape = np.shape(obs1)
        
        cdef int length = min(len(obs1),len(obs2))
        cdef int width = len(obs1[0])
        
        cdef double[:, :] val = np.ones(shape)*-1e6
        cdef long[:, :] prev = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det1 = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det2 = np.zeros(shape,dtype = np.int)
        
        cdef int tr_len = len(tr)
        cdef int sep_len = len(tr[0])
        cdef int tr_dist = int(len(tr)/2. - 0.5)
        cdef int sep_dist = int(len(tr)/2. - 0.5)
        
        cdef int i
        cdef int j
        cdef int k
        cdef int m
        cdef int t
        cdef int x

        
        cdef long max_pos
        cdef double value
        cdef double temp
        cdef int edge_range = 0

        for i in range(width):
            temp = -1e6
            for k in range(sep_len): 
                if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                    for m in range(sep_len):
                        if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                            value = tr[1][k][m] + obs1[0][i+k-sep_dist] + obs2[0][i+m-sep_dist]
                            if value > temp:
                                temp = value
                                val[0][i] = temp
                                prev[0][i] =  i
                                det1[0][i] =  i+k-1 
                                det2[0][i] =  i+m-1
                            else:
                                continue
    
        # i is current frequency position
        # j is transition in reference detector
        # k is separation of first detector
        # m is separation of second detector


        
        pbar = 0
        for t in range(1,length):
            pt = t/(float(length))*100.
            for i in range(width):
                temp = -np.inf
                for j in range(tr_len):
                    if i+j-tr_dist>=0 and i+j-tr_dist<width:
                       for k in range(sep_len):
                            if i+k-sep_dist>=0+edge_range and i+k-sep_dist<width-edge_range:
                                for m in range(sep_len):
                                    if i+m-sep_dist>=0+edge_range and i+m-sep_dist<width-edge_range:
                                        value = tr[j][k][m] + val[t-1][i+j-tr_dist] + obs1[t][i+k-sep_dist] + obs2[t][i+m-sep_dist]
                                        if value > temp:
                                            temp = value
                                            val[t][i] = temp
                                            prev[t][i] =  i+j-tr_dist
                                            det1[t][i] =  i+k-sep_dist
                                            det2[t][i] =  i+m-sep_dist
                                        else:
                                            continue
            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length
        self.V = np.array(val)
        self.prev = np.array(prev)
        self.det1 = np.array(det1)
        self.det2 = np.array(det2)
        self.width = width
        self.length = length

        
    def get_track(self):
        """
        Takes in the viterbi data from a run and identifies the track thorugh whcih gives the maximum probability
        Returns
        -------------
        vit_track1 : array
           array of indicies for track in obs1
        vit_track2 : array
           array of indicies for track in obs2
        vit_track: array
           array of indicies for track in the "reference" detector
        max_end_prob: float
           value of maxmimum end statistic
        """
        cdef long previous = 1
        cdef long[:] vit_trackr = np.zeros(self.length).astype(int)
        cdef long[:] vit_track2 = np.zeros(self.length).astype(int)
        cdef long[:] vit_track1 = np.zeros(self.length).astype(int)
        
        cdef float max_prob = np.array([self.V[self.length-1][i] for i in range(self.width)]).max()
        cdef long max_prob_index = np.array([self.V[self.length-1][i] for i in range(self.width)]).argmax()
        
        vit_trackr[self.length-1] = max_prob_index
        vit_track1[self.length-1] = self.det1[self.length-1][max_prob_index]
        vit_track2[self.length-1] = self.det2[self.length-1][max_prob_index]
        previous = self.prev[self.length-1][max_prob_index]
        

        for t in range(self.length-2,-1,-1):
            vit_trackr[t] = previous # insert previous step
            vit_track1[t] = self.det1[t][previous]
            vit_track2[t] = self.det2[t][previous]
            previous = self.prev[t][previous]
    
        self.vit_track1 = np.array(vit_track1)
        self.vit_track2 = np.array(vit_track2)
        self.vit_track = np.array(vit_trackr)
        self.max_end_prob = max_prob
        
        #return np.array(vit_track1), np.array(vit_track2), np.array(vit_trackr), np.array(val),np.array(prev),max_prob

        
class three_detector(object):
 
    def __init__(self, tr, obs1, obs2, obs3, prog = False):
        '''
        initialising viterbi class
        '''
        self.prog = prog
        self.tracks = self.run(tr, obs1, obs2, obs3)

    

    #---------------------------------------------------------
    # Three detector viterbi
    #--------------------------------------------------------

    def run(self,tr1, obs11, obs21, obs31):
        """
        viterbi algorithm for multiple detectors 2 at the moment
        Args
        ---------
        tr1: array
            transition matrix
        obs11: array
            observation from detector 1
        obs21: array
            observation from detector 2
        returns
        -----------
        vit_track1: array
            path in det 1
        vit_track2: array
            path in 2
        vit_trackr: array
            path in reference detector
        val: array
            values in reference detector
        prev: array
            previous positions
        det1: array
            det1 data
        det2: array
            det 2 data
        """
        #tr_len = np.arange(len(tr))-len(tr)/2
        #range_tr = np.arange(3)
        
    
        cdef double[:, :, :, :] tr = tr1
        cdef double[:, :] obs1 = obs11
        cdef double[:, :] obs2 = obs21
        cdef double[:, :] obs3 = obs31

        shape = np.shape(obs1)
        
        cdef int length = min(len(obs1),len(obs2),len(obs3))
        cdef int width = len(obs1[0])
        
        cdef double[:, :] val = np.ones(shape)*-1e6
        cdef long[:, :] prev = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det1 = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det2 = np.zeros(shape,dtype = np.int)
        cdef long[:, :] det3 = np.zeros(shape,dtype = np.int)
        
        cdef int tr_len = len(tr)
        
        cdef int i
        cdef int j
        cdef int k
        cdef int m
        cdef int t
        cdef int x
        
        cdef long max_pos
        cdef long[:] indicies
        cdef double max_val
        cdef double value
        cdef double temp
        #cdef double[:] max_vals
    
        for i in range(width):
            
            temp = -1e6
            for k in range(tr_len): 
                if i+k-1>=0 and i+k-1<width:
                    for m in range(tr_len):
                        if i+m-1>=0 and i+m-1<width:
                            for l in range(tr_len):
                                if i+l-1>=0 and i+l-1<width:
                                    value = obs1[0][i+k-1] + obs2[0][i+m-1] + obs3[0][i+l-1] + tr[1][k][m][l]
                                if value > temp:
                                    temp = value
                                    val[0][i] = temp
                                    prev[0][i] =  i
                                    det1[0][i] =  i+k-1 
                                    det2[0][i] =  i+m-1
                                    det3[0][i] =  i+l-1
                                else:
                                    continue

    
        # i is current frequency position
        # j is transition in reference detector
        # k is separation from other detector
        
        pbar = 0
        for t in range(1,length):
            pt = t/(float(length))*100.
            for i in range(width):
                
                temp = -1e6
                for j in range(tr_len):
                    if i+j-1>=0 and i+j-1<width:
                       for k in range(tr_len):
                            if i+k-1>=0 and i+k-1<width:
                                for m in range(tr_len):
                                     if i+m-1>=0 and i+m-1<width:
                                         for l in range(tr_len):
                                             if i+l-1>=0 and i+l-1<width:
                                                 value = obs1[t][i+k-1] + obs2[t][i+m-1] + obs3[t][i+l-1] + tr[j][k][m][l] + val[t-1][i+j-1]
                                                 if value > temp:
                                                     temp = value
                                                     val[t][i] = temp
                                                     prev[t][i] =  i+j-1
                                                     det1[t][i] =  i+k-1 
                                                     det2[t][i] =  i+m-1
                                                     det3[0][i] =  i+l-1
                                                 else:
                                                     continue
            
            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length

        
    
        cdef long previous = 1
        cdef long[:] vit_trackr = np.zeros(length).astype(int)
        cdef long[:] vit_track1 = np.zeros(length).astype(int)
        cdef long[:] vit_track2 = np.zeros(length).astype(int)
        cdef long[:] vit_track3 = np.zeros(length).astype(int)
        
        cdef float max_prob = np.array([val[length-1][i] for i in range(width)]).max()
        cdef long max_prob_index = np.array([val[length-1][i] for i in range(width)]).argmax()
        
        vit_trackr[length-1] = max_prob_index
        vit_track1[length-1] = det1[length-1][max_prob_index]
        vit_track2[length-1] = det2[length-1][max_prob_index]
        vit_track3[length-1] = det3[length-1][max_prob_index]
        previous = prev[length-1][max_prob_index]
        

        for t in range(length-2,-1,-1):
            vit_trackr[t] = previous # insert previous step
            vit_track1[t] = det1[t][previous]
            vit_track2[t] = det2[t][previous]
            vit_track3[t] = det3[t][previous]
            previous = prev[t][previous]
    
        self.vit_track1    = np.array(vit_track1)
        self.vit_track2    = np.array(vit_track2)
        self.vit_track3    = np.array(vit_track3)
        self.vit_track = np.array(vit_trackr)
        self.V            = np.array(val)
        self.prev         = np.array(prev)
        self.max_end_prob = max_prob
    
        #return np.array(vit_track1), np.array(vit_track2), np.array(vit_track3), np.array(vit_trackr), np.array(val),np.array(prev), max_prob

class single_detector_mem_n(object):
 
    def __init__(self, tr, obs, prog = False):
        '''
        
        Find single detector algorithm with a memory, uses the summed pixel power as statistic

        initialising viterbi class
        '''
        self.prog = prog
        self.tracks = self.run(tr, obs)

    
    #--------------------------------------------------------------------------
    # n dimensional memory viterbi
    #------------------------------------------------------------------------

    def run(self, tr, obs):
        ''' Run viterbi algroithm with memory of n
        the amount of memory is determined by the transition matrix
        args
        -------
        tr : array
            transition matrix, any dimension greater that 1 - type: array
        obs: array
            observation - type: array
        
        returns
        -------
        vit_track: array
            optimum path through data
        val: array
            values of viterbi
        prev: array
            previous positions of viterbi
        '''
        
        if len(np.shape(tr))<=1:
            raise Exception("ERROR: Please use a transition matrix with dimensions larger than one")
        
        #np.insert(obs,0,-1e6,axis=1)
        #np.insert(obs,len(obs[0]),-1e6,axis=1)

        #cdef double[:] tr = tr1
        #cdef double[:, :] obs = obs1
        
        range_tr = np.arange(len(tr))
        cdef int n = len(tr)
        shape = np.shape(tr)
        cdef int length = len(shape)
        
        dimensions = (len(obs),len(obs[0]))
        dimensions = list(dimensions)
        
        cdef int length_t = dimensions[0]
        cdef int width = dimensions[1]
        
        cdef int i
        cdef int t
        cdef int k
        cdef int c
        
        cdef double value
        cdef double temp
        
        for i in range(len(shape)-1):
            dimensions.append(n)
        
        dimensions = tuple(dimensions)

        val    = np.ones(dimensions)*-1e6
        prev   = np.ones(dimensions)
    
        range_j = list(itertools.product(range(n),repeat=length-1))
    
        for i in range(width):
            for j in range_j:
                val[0][i][j]    = obs[0][i]
                prev[0][i][j]   = np.nan
    
        cdef float pbar = 0
        for t in range(1,length_t):
            obst = obs[t]
            valt = val[t-1]
            pt = t/float(length_t)*100.
            for i in range(width): 
                for j in range_j:
                    cond = True
                    for c in range(1,len(j)+1):
                        b = i+np.sum(j[:c])-len(j[:c])
                        if b >= 0 and b<width: 
                            continue
                        else:
                            cond = False
                            break
                    if cond:
                        temp = -1e6
                        for k in range(n):
                            m = list(j[1:])
                            m.append(k)
                            if t<length:
                                for n1 in range(len(m)):
                                    if n1>=t-1:
                                        m[n1] = 1
                            m = tuple(m)
                            value = obst[i] + tr[j[0]][m] + valt[i+j[0]-1][m]
    
                        
                            if value>temp:
                                temp = value
                                val[t][i][j] = temp
                                prev[t][i][j] = k

            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length_t

        cdef int previous   = 1
        previous_1 = None
        vit_track   = [0]

        #cdef double max_end_prob = max(val[length-1][i] for i in range(width))

        temp = -1e6
        for i in range(width):
            for j in range_j:
                value = val[-1][i][j]
                if value>temp:
                    temp = value
                    vit_track[0] = i
                    previous = i
                    previous_1 = j
                    previous_2 = int(prev[-1][i][j])
    
                
        for t in range(length_t-2,-1,-1):
            vit_track.append(previous+previous_1[0]-1)
            previous += previous_1[0]-1
            previous_1 = list(previous_1[1:])
            previous_1.append(int(previous_2))
            previous_1 = tuple(previous_1)
            previous_2 = prev[t][previous][previous_1]
        
        vit_track = vit_track[::-1]

        self.vit_track = np.array(vit_track)
        self.V = np.array(val)
        self.prev = np.array(prev)
        self.max_end_prob = None # needs to be fixed
        
        #return (vit_track,val,prev)

class two_detector_mem_n(object):
 
    def __init__(self, tr, obs1, obs2, prog = False):
        '''
        initialising viterbi class
        '''
        self.prog = prog
        self.tracks = self.run(tr, obs1, obs2)

    
    #------------------------------------------------------------------------
    # Multi viterbi vit n dimensional memory
    #-----------------------------------------------------------------------
    

    def run(self, tr, obs11, obs22):
        ''' Run viterbi algroithm with memory of n
        the amount of memory is determined by the transition matrix
        args
        -------
        tr : transition matrix, any dimension greater that 1 - type: array
        obs: observation - type: array
        
        returns
        -------
        vit_track: optimum path through data
        '''
        
        if len(np.shape(tr))<=1:
            raise Exception("ERROR: Please use a transition matrix with dimensions larger than one")
        
        range_tr = np.arange(len(tr))
        
        cdef double[:, :] obs1 = obs11
        cdef double[:, :] obs2 = obs22
        
        cdef int n      = len(tr)
        shape           = np.shape(tr)
        cdef int length = len(shape)
        
        dimensions = (min(len(obs1),len(obs2)),min(len(obs1[0]),len(obs2[0])))
        dimensions = list(dimensions)
        
        cdef int length_t = dimensions[0]
        cdef int width = dimensions[1]
        
        cdef int i
        cdef int k
        cdef int m
        cdef int j1
        cdef int n1
        cdef int b
        cdef int t
        cdef double value
        cdef double temp

        
        for i in range(len(shape)-3):
            dimensions.append(n)
        
        dimensions = tuple(dimensions)

        val    = np.ones(dimensions)*-1e6
        prev   = np.ones(dimensions)
        pos1   = np.ones(dimensions)
        pos2   = np.ones(dimensions)
        
    
        range_j = list(itertools.product(range(n),repeat=length-3))
    
        for i in range(width):
            for j in range_j:
                temp = -1e6
                for k in range(n):
                    if i+k-1>=0 and i+k-1<width:
                        for m in range(n):
                            if i+m-1>=0 and i+m-1<width:
                                value = obs1[0][i+k-1] + obs2[0][i+m-1] + tr[tuple(np.ones(len(shape)-2).astype('int'))][k][m]
                                if value>temp:
                                    temp = value
                                    val[0][i][j]    = value
                                    prev[0][i][j]   = np.nan
                                    pos1[0][i][j]   = k
                                    pos2[0][i][j]   = m
    
        pbar = 0
        for t in range(1,length_t):
            obs1t = obs1[t]
            obs2t = obs2[t]
            valt = val[t-1]
            pt = t/float(length_t)*100.
            for i in range(width): 
                for j in range_j:
                    cond = True
                    for c in range(1,len(j)+1):
                        b = i+np.sum(j[:c])-len(j[:c])
                        if b >= 0 and b<width: 
                            continue
                        else:
                            cond = False
                            break
                    if cond:
                        temp = -1e6
                        for j1 in range(n):
                            a = list(j[1:])
                            a.append(j1)
                            if t<length:
                                for n1 in range(len(a)):
                                    if n1>=t-1:
                                        a[n1] = 1
                            a = tuple(a)
                            for k in range(n):
                                if i+k-1>=0 and i+k-1<width:
                                    for m in range(n):
                                        if i+m-1>=0 and i+m-1<width:
                                            value = obs1t[i+k-1] + obs2t[i+m-1] + tr[j][j1][k][m] + valt[i+j[0]-1][a]
                                            if value > temp:
                                                temp = value
                                                val[t][i][j]  = temp
                                                prev[t][i][j] = j1
                                                pos1[t][i][j] = k
                                                pos2[t][i][j] = m
                        """
                        for k in range(length):
                            m = list(j[1:])
                            m.append(k)x
                            if t<length:
                                for n1 in range(len(m)):
                                    if n1>=t-1:
                                        m[n1] = 1
                            m = tuple(m)
                            value = obst[i] + tr[j[0]][m] + valt[i+j[0]-1][m]
                            if value>temp:
                                temp = value
                                val[t][i][j] = temp
                                prev[t][i][j] = k
                        """
                    
            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length_t

        previous   = 1
        previous_1 = None
        vit_track1  = [0]
        vit_track2  = [0]
        vit_trackr  = [0]

        temp = -1e6
        for i in range(width):
            for j in range_j:
                value = val[-1][i][j]
                if value>temp:
                    temp = value
                    vit_trackr[0] = i
                    vit_track1[0] = i+pos1[-1][i][j]-1
                    vit_track2[0] = i+pos2[-1][i][j]-1
                    previous = i
                    previous_1 = j
                    previous_2 = int(prev[-1][i][j])
    
        
        for t in range(length_t-2,-1,-1):
            vit_trackr.append(previous+previous_1[0]-1)
            previous += previous_1[0]-1
            previous_1 = list(previous_1[1:])
            previous_1.append(int(previous_2))
            previous_1 = tuple(previous_1)
            vit_track1.append(previous+pos1[t][previous][previous_1]-1)
            vit_track2.append(previous+pos2[t][previous][previous_1]-1)
            previous_2 = prev[t][previous][previous_1]
        
        vit_trackr = vit_trackr[::-1]   
        vit_track1 = vit_track1[::-1] 
        vit_track2 = vit_track2[::-1]

        self.vit_track1 = np.array(vit_track1)
        self.vit_track2 = np.array(vit_track2)
        self.vit_track = np.array(vit_trackr)
        self.V = np.array(val)
        self.prev = np.array(prev)
        
        #return (vit_track1,vit_track2,vit_trackr,val,prev)


### -----------------------------------------------------------------

## Single detector algorithm where data can include large gaps 

### ----------------------------------------------------------------

class single_detector_gaps(object):

    def __init__(self, tr, obs,times,tsft):
        """
        single detector viterbi algorithm where the data can include large gaps in data
        NOTE: This is for large gaps in data, the single_detector algorithm works faster if gaps are filled with the mean of data

        Parameters
        -----------------
        tr: list
            transition matrix elements
        obs: array
            an array of the sfts
        times: list
            times corresponding to each of the sfts
        tsft: float
            the length of each sfts in s
        Returns
        -------------------
        self.vit_track: list
            optimum path through dataset
        self.vit_track_times: list
            list of the times corresponding to each of the path elements
        """
        self.vits, self.sts, self.gps = self.vit_gaps(obs, times, tr=tr, tsft=tsft)
        self.vit_track, self.vit_track_times = self.get_track(self.vits, self.sts, self.gps,tsft=tsft)
        self.max_end_prob = max(self.vits[-1].V[-1])
        
    def max_track(self,tr,length,diff,bnd,ind,band_width):
        tr_val = np.arange(len(tr)).astype(int) - np.floor(len(tr)/2).astype(int)
        result = [seq for seq in itertools.combinations_with_replacement(tr_val, length) if sum(seq) == diff]
        max_seq = None
        thresh = -np.inf
        thresh2 = -np.inf
        #print ind,bnd, diff, [np.cumsum(s)+ind for s in result]
        for seq in result:
            #print seq
            abspath = np.array(np.cumsum(seq) + ind)
            if np.any(abspath < 0) == True or np.any(abspath >= band_width) == True:
                continue
            else:
                s = sum([tr[elem+1] for elem in seq]) 
                l = len(np.where(np.array(seq) == 0)[0])
                if s > thresh:
                    max_seq = np.insert(abspath,0,ind)[:-1] 
                    thresh = s
                elif s == thresh and l > thresh2:
                    max_seq = np.insert(abspath,0,ind)[:-1] 
                    thresh = s
                    thresh2 = l

        return max_seq,s

    def gap_run(self,viterbi, band_width, diff, tsft, tr):
        length = diff - 1
        max_vals = np.zeros(band_width)
        max_paths = np.zeros((band_width,length))
        #print band_width, length
        for bnd in range(band_width):
            low = bnd - length
            high = bnd + length + 1
            if low < 0:
                low = 0
            if high >= band_width:
                high = band_width
            thres = 0
            vend = viterbi.V[-1,low:high]
        
            val = 0
            ind = 0
            for j in range(len(vend)):
                if vend[j] > thres:
                    val = vend[j]
                    ind = low + j
                    thres = vend[j] 
            diff_ind = bnd-ind
            gaptrack = self.max_track(tr,length,diff_ind,bnd,ind,band_width)
            #print bnd,ind,low,high,diff_ind,length,gaptrack
        
            max_paths[bnd] = np.array(gaptrack[0])
            max_vals[bnd] = gaptrack[1] + val + length*2
    
        return max_vals, max_paths

    def find_path(self,prev,end_ind):
        length = len(prev)
        previous = prev[-1][end_ind]
        vit_track =  np.zeros(length,dtype=np.int)
        vit_track[-1] = end_ind
        for t in range(length-2,-1,-1):
            vit_track[t] = previous # insert previous step
            previous = prev[t][previous]
        
        return vit_track
        

    def vit_gaps(self,data1,epochs1,tr,tsft):

        band_width = len(data1[0])
        vit = []
        starts = []
        gappaths = []
        gapend = 0
        vitstart = epochs1[0]
        max_vals = None
    

        data = []
        epochs = []
        for i,idx in enumerate(epochs1):
            if i == 0 or i == len(epochs1)-1:
                data.append(data1[i])
                epochs.append(idx)
            elif i > 0 and i != len(epochs1)-1:
                diff = epochs1[i]-epochs1[i-1]
                if diff == 2:
                    data.append(np.ones(band_width)*2)
                    epochs.append(idx-tsft)
                    data.append(data1[i])
                    epochs.append(idx)
                else:
                    data.append(data1[i])
                    epochs.append(idx)
        data = np.array(data)
        epochs = np.array(epochs)
    
        for i,idx in enumerate(epochs):
            if i == 0 :
                pass
            elif i > 0:# and i != len(epochs)-1:
                diff = epochs[i]-epochs[i-1]
                diff_ind = int(diff/tsft)
                if diff_ind >= 2 and diff_ind < band_width + 1:
                    if max_vals is not None:
                        viterbi = single_detector(tr, np.vstack([max_vals,data[gapend:i]]))
                        starts.append(np.arange(len(viterbi.vit_track))*tsft + vitstart - tsft)
                        vitstart = idx 
                    else:
                        viterbi = single_detector(tr, data[gapend:i])
                        starts.append(np.arange(len(viterbi.vit_track))*tsft + vitstart)
                        vitstart = idx 
        
                    vit.append(viterbi)
                    gapend = i
                    max_vals, max_paths = self.gap_run(viterbi, band_width, diff_ind, tsft, tr)
                    #print max_vals, max_paths
                    gappaths.append(max_paths)
                    if i == len(epochs)-1:
                        viterbi = single_detector(tr, np.vstack([max_vals,data[gapend:]]))
                        starts.append(np.arange(len(viterbi.vit_track))*tsft + idx - tsft)
                        vit.append(viterbi)
            
                elif diff_ind >= band_width + 1:
                
                    diff1 = band_width + 1
                    if max_vals is not None:
                        viterbi = single_detector(tr, np.vstack([max_vals,data[gapend:i]]))
                        starts.append(np.arange(len(viterbi.vit_track))*tsft + vitstart - tsft)
                        vitstart = idx 
                    else:
                        viterbi = single_detector(tr, data[gapend:i])
                        starts.append(np.arange(len(viterbi.vit_track))*tsft + vitstart)
                        vitstart = idx
        

                    vit.append(viterbi)
                    gapend = i
                    max_vals, max_paths = self.gap_run(viterbi, band_width , diff1, tsft, tr)
                    #print max_vals, max_paths
                    gappaths.append(max_paths) 
                    if i == len(epochs)-1:
                        viterbi = single_detector(tr, np.vstack([max_vals,data[gapend:]]))
                        starts.append(np.arange(len(viterbi.vit_track))*tsft + idx - tsft)
                        vit.append(viterbi)
                  
                else:
                    continue
                
        return vit,starts, gappaths

    def get_track(self,vit,starts,gappaths,tsft=1):
        vit_track = []
        vit_track_time = []
        gpb = False
        gp = None
        if len(starts) > 1:
            for v in range(len(starts))[::-1]:
                if gpb:
                    p1 = self.find_path(vit[v].prev,int(vit_track[-1]))[::-1]
                    vit_track.extend(p1[1:])
                    vit_track_time.extend(starts[v][::-1][1:])
                else:
                    p1 = vit[v].vit_track[::-1]
                    vit_track.extend(p1)
                    vit_track_time.extend(starts[v][::-1])
                st = vit_track[-1]
                if v-1 >= 0:
                    gp = gappaths[v-1][st][::-1]
                    vit_track.extend(gp)
                    vit_track_time.extend(np.array(np.arange(len(gp))*tsft + starts[v-1][-1])[::-1])#+np.array(range(len(gp))[::-1]))
                    #vit_track_time.extend(range(len(gp))[::-1])
                    gpb = True
                else:
                    gpb = False
        else:
            vit_track = vit[0].vit_track
        return vit_track[::-1], vit_track_time[::-1]




'''

class N_detector(object):
 
    def __init__(self, tr, obs):
        """
        UNTESTED: DO NOT USE
        initialising viterbi class
        """
        self.prog = prog
        self.tracks = self.run(tr, obs)

    
    #------------------------------------------------------------------------
    # Viterbi with N detectors
    #-----------------------------------------------------------------------
    

    def run(self, tr, mobs):
        """

        Run viterbi algroithm with memory of n
        the amount of memory is determined by the transition matrix
        args
        -------
        tr : transition matrix, any dimension greater that 1 - type: array
        obs: observation - type: array
        
        returns
        -------
        vit_track: optimum path through data
        """
        
        if len(np.shape(tr))<=1:
            raise Exception("ERROR: Please use a transition matrix with dimensions larger than one")
        
        range_tr = np.arange(len(tr))
        
        n_detectors = len(mobs)

        cdef double[:, :, :] obs_list = mobs
        
        cdef int n      = len(tr)
        shape           = np.shape(tr)
        cdef int length = len(shape)
        
        min_len1 = np.inf
        min_len2 = np.inf
        for obs in obs_list:
            if len(obs) < min_len1:
                min_len1 = len(obs)
            if len(obs[0]) < min_len2:
                min_len2 = len(obs[0])
            
        dimensions = (min_len1, min_len2)
        dimensions = list(dimensions)
        
        cdef int length_t = dimensions[0]
        cdef int width = dimensions[1]
        
        cdef int i
        cdef int k
        cdef int m
        cdef int j1
        cdef int n1
        cdef int b
        cdef int t
        cdef double value
        cdef double temp

        
        for i in range(len(shape)-3):
            dimensions.append(n)
        
        dimensions = tuple(dimensions)

        val    = np.ones(dimensions)*-1e6
        prev   = np.ones(dimensions)
        pos1   = np.ones(dimensions)
        pos2   = np.ones(dimensions)
        
    
        range_j = list(itertools.product(range(n),repeat=n_detectors))
    
        for i in range(width):
            temp = -1e6
            for k in range(n):
                if i+k-1>=0 and i+k-1<width:
                    for m in range(n):
                        if i+m-1>=0 and i+m-1<width:
                            value = obs1[0][i+k-1] + obs2[0][i+m-1] + tr[tuple(np.ones(len(shape)-2).astype('int'))][k][m]
                            if value>temp:
                                temp = value
                                val[0][i]    = value
                                prev[0][i]   = np.nan
                                pos1[0][i]   = k
                                pos2[0][i]   = m
    
        pbar = 0
        for t in range(1,length_t):
            obs1t = obs1[t]
            obs2t = obs2[t]
            valt = val[t-1]
            pt = t/float(length_t)*100.
            for i in range(width): 
                for j in range_j:
                    cond = True
                    for c in range(1,len(j)+1):
                        b = i+np.sum(j[:c])-len(j[:c])
                        if b >= 0 and b<width: 
                            continue
                        else:
                            cond = False
                            break
                    if cond:
                        temp = -1e6
                        for j1 in range(n):
                            a = list(j[1:])
                            a.append(j1)
                            if t<length:
                                for n1 in range(len(a)):
                                    if n1>=t-1:
                                        a[n1] = 1
                            a = tuple(a)
                            for k in range(n):
                                if i+k-1>=0 and i+k-1<width:
                                    for m in range(n):
                                        if i+m-1>=0 and i+m-1<width:
                                            value = obs1t[i+k-1] + obs2t[i+m-1] + tr[j][j1][k][m] + valt[i+j[0]-1][a]
                                            if value > temp:
                                                temp = value
                                                val[t][i][j]  = temp
                                                prev[t][i][j] = j1
                                                pos1[t][i][j] = k
                                                pos2[t][i][j] = m
                        """
                        for k in range(length):
                            m = list(j[1:])
                            m.append(k)x
                            if t<length:
                                for n1 in range(len(m)):
                                    if n1>=t-1:
                                        m[n1] = 1
                            m = tuple(m)
                            value = obst[i] + tr[j[0]][m] + valt[i+j[0]-1][m]
                            if value>temp:
                                temp = value
                                val[t][i][j] = temp
                                prev[t][i][j] = k
                        """
                    
            if self.prog == True:
                if pt>pbar:
                    stdout.write('\r{} %'.format(round(pt)))
                    stdout.flush()
                    pbar+=100./length_t

        previous   = 1
        previous_1 = None
        vit_track1  = [0]
        vit_track2  = [0]
        vit_trackr  = [0]

        temp = -1e6
        for i in range(width):
            for j in range_j:
                value = val[-1][i][j]
                if value>temp:
                    temp = value
                    vit_trackr[0] = i
                    vit_track1[0] = i+pos1[-1][i][j]-1
                    vit_track2[0] = i+pos2[-1][i][j]-1
                    previous = i
                    previous_1 = j
                    previous_2 = int(prev[-1][i][j])
    
        
        for t in range(length_t-2,-1,-1):
            vit_trackr.append(previous+previous_1[0]-1)
            previous += previous_1[0]-1
            previous_1 = list(previous_1[1:])
            previous_1.append(int(previous_2))
            previous_1 = tuple(previous_1)
            vit_track1.append(previous+pos1[t][previous][previous_1]-1)
            vit_track2.append(previous+pos2[t][previous][previous_1]-1)
            previous_2 = prev[t][previous][previous_1]
        
        vit_trackr = vit_trackr[::-1]   
        vit_track1 = vit_track1[::-1] 
        vit_track2 = vit_track2[::-1]

        self.vit_track1 = np.array(vit_track1)
        self.vit_track2 = np.array(vit_track2)
        self.vit_track = np.array(vit_trackr)
        self.V = np.array(val)
        self.prev = np.array(prev)
        
        #return (vit_track1,vit_track2,vit_trackr,val,prev)

'''

    
