from __future__ import division
import numpy as np
import pickle
from sys import stdout
import scipy.special as sp
try:
    from scipy.misc import logsumexp
except:
    from scipy.special import logsumexp
from libc.math cimport log,exp,sqrt
import os
#import integrals
cwd = os.getcwd()


cdef extern from "integrals.h":
    double integral_signal_1det(double g, double logfrac, int k, int N, double pv)
    double ch2_noise_1det(double g, int k, int N) 
    double integral_signal_2det(double g1, double g2, double logfrac, int k, int N, double pv)
    double integral_line_2det(double g1, double g2,  double logfrac, int k, int N, double pv)
    double ch2_noise_2det(double g1, double g2, int k, int N) 

def bayes_2det(g1,g2,logfrac,k,N,pvs,pvl,ratio):
    """
    calculate the bayes factor for signal noise and line
    args
    -----------
    g1: float
       power in det 1
    g2: float
       power in det 2
    logfrac: float
       fraction of duty cycle and noise in each detector
    k: int
       number of degrees of freedom
    N: int
       number of sfts summed over
    pvs: float
       width of prior on signal
    pvl: float
       width of prior on line
    ratio: float
       ratio of the prior on noise model vs line
    returns
    ---------
    b1: float
       bayes factor including all signal,line and noise
    sig_int: float
       marginalised likelihood for signal
    line_int:
       marginalised likelihood for line
    noise: float
       noise likelihood
    """
    cdef double sig_int
    cdef double line_int
    cdef double noise
    cdef double b1
    sig_int = integral_signal_2det(g1,g2,logfrac,k,N,pvs)
    line_int = integral_line_2det(g1,g2,logfrac,k,N,pvl)
    noise = ch2_noise_2det(g1,g2,k,N)
    b1 = sig_int/(ratio*line_int + noise)
    return [b1,sig_int,line_int,noise]

def bayes_1det(g,logfrac,k,N,pvs,pvl,ratio):
    """
    calculate the bayes factor for signal noise and line
    args
    -----------
    g1: float
       power in det 1
    g2: float
       power in det 2
    logfrac: float
       fraction of duty cycle and noise in each detector
    k: int
       number of degrees of freedom
    N: int
       number of sfts summed over
    pvs: float
       width of prior on signal
    pvl: float
       width of prior on line
    ratio: float
       ratio of the prior on noise model vs line
    returns
    ---------
    b1: float
       bayes factor including all signal,line and noise
    sig_int: float
       marginalised likelihood for signal
    line_int:
       marginalised likelihood for line
    noise: float
       noise likelihood
    """
    cdef double sig_int
    cdef double line_int
    cdef double noise
    cdef double b1
    sig_int = integral_signal_1det(g,logfrac,k,N,pvs)
    line_int = integral_signal_1det(g,logfrac,k,N,pvl)
    noise = ch2_noise_1det(g,k,N)
    b1 = sig_int/(ratio*line_int + noise)
    return [b1,sig_int,line_int,noise]

def gen_lookup_1det(x,int_type = 'chi2',pvs=1,pvl=1,ratio=1,k=2,N=48):
    """
    calculates the odds ratio for given values of power and ratio.
    args
    --------
    x: array
        array of the SFT power in detector 1
    n1: array
        array of the ratios of the duty cycle and noise psds, \frac{f_{1} S_{2}}{f_{2} S_{1}}
    int_type: string
        which statistic to use ("chi2" only option for now)
    pvs: float
        width on prior for signal model
    pvl: float
        width on prior for line model
    ratio: float
        ratio of the priors on the line and signal models
    k: int
        number of degrees of freedom
    N: int
        number of summed distributions, i.e. SFTs 
    returns
    ----------
    odds: array
       array of odd ratio with 3 models
    signal: array
       array of signal likelihoods
    line: array
       array of line likelihoods
    noise: array
       array of noise likelihoods
    """
    cdef int i
    cdef double[:] xc = x
    cdef double[:] odds = np.zeros((len(x)))
    cdef double[:] signal = np.zeros((len(x)))
    cdef double[:] line = np.zeros((len(x)))
    cdef double[:] noise = np.zeros((len(x)))
    cdef double n1 = 0.
    for i in range(len(x)):
        ig = bayes_1det(xc[i],n1,k,N,pvs,pvl,ratio)
        odds[i] = ig[0]
        signal[i] = ig[1]
        line[i] = ig[2]
        noise[i] = ig[3]

    return odds,signal,line,noise


def gen_lookup_2det(x,y,int_type = 'chi2',pvs=1,pvl=1,ratio=1,k=2,N=48):
    """
    calculates the odds ratio for given values of power and ratio for two detectors.
    args
    --------
    x: array
        array of the SFT power in detector 1
    y: array
        array of SFT power in detector 2
    n1: array
        array of the ratios of the duty cycle and noise psds, \frac{f_{1} S_{2}}{f_{2} S_{1}}
    int_type: string
        which statistic to use ("chi2" only option for now)
    pvs: float
        width on prior for signal model
    pvl: float
        width on prior for line model
    ratio: float
        ratio of the priors on the line and signal models
    k: int
        number of degrees of freedom
    N: int
        number of summed distributions, i.e. SFTs 
    returns
    ----------
    odds: array
       array of odd ratio with 3 models
    signal: array
       array of signal likelihoods
    line: array
       array of line likelihoods
    noise: array
       array of noise likelihoods

    """
    cdef int i
    cdef int j
    cdef double[:] xc = x
    cdef double[:] yc = y
    cdef double[:, :] odds = np.zeros((len(x),len(y)))
    cdef double[:, :] signal = np.zeros((len(x),len(y)))
    cdef double[:, :] line = np.zeros((len(x),len(y)))
    cdef double[:, :] noise = np.zeros((len(x),len(y)))
    cdef double n1 = 0.
    for i in range(len(x)):
        for j in range(len(y)):
            ig = bayes_2det(xc[i],yc[j],n1,k,N,pvs,pvl,ratio)
            odds[i,j] = ig[0]
            signal[i,j] = ig[1]
            line[i,j] = ig[2]
            noise[i,j] = ig[3]

    return odds,signal,line,noise

def gen_lookup_noisefloor(x,y,n1,int_type = 'chi2',pvs=1,pvl=1,ratio=1,k=2,N=48):
    """
    calculates the odds ratio in ch_integrals_approx_noise for given values of power and ratio.
    args
    --------
    x: array
        array of the SFT power in detector 1
    y: array
        array of SFT power in detector 2
    n1: array
        array of the ratios of the duty cycle and noise psds, \frac{f_{1} S_{2}}{f_{2} S_{1}} (f is fraction of summed sfts which are real data, S is noise psd)
    int_type: string
        which statistic to use ("chi2" only option for now)
    approx: bool
        choose whether to use trapz or quad to complete integrals
    pvs: float
        width on prior for signal model
    pvl: float
        width on prior for line model
    ratio: float
        ratio of the priors on the line and signal models
    k: int
        number of degrees of freedom for chi2 dist (default = 2)
    N: int
        number of summed sfts (default = 48)
    returns
    ----------
    val: array
       array of odd ratio with 3 models
    val1: array
       array of odd ratio with signal/noise model
    val2: array
       array of odd ratio with signal/line model
    val3: array
       array of signal likelihoods
    val4: array
       array of noise likelihoods
    val: array
       array of line likelihoods
    """
    cdef int i
    cdef int j
    cdef int l
    cdef double[:] xc = x
    cdef double[:] yc = y
    cdef double[:] n1c = n1
    cdef double[:, :, :] odds = np.zeros((len(n1),len(x),len(y)))
    cdef double[:, :, :] signal = np.zeros((len(n1),len(x),len(y)))
    cdef double[:, :, :] line = np.zeros((len(n1),len(x),len(y)))
    cdef double[:, :, :] noise = np.zeros((len(n1),len(x),len(y)))
    #cdef double[:, :, :] val4 = np.zeros((len(x),len(y),len(n1)))
    #cdef double[:, :, :] val5 = np.zeros((len(x),len(y),len(n1)))
    for i in range(len(x)):
        for j in range(len(y)):
            for l in range(len(n1)):
                ig = bayes_2det(xc[i],yc[j],n1c[l],2,48,pvs,pvl,ratio)
                odds[l,i,j] = ig[0]
                signal[l,i,j] = ig[1]
                line[l,i,j] = ig[2]
                noise[l,i,j] = ig[3]
                #val4[i,j,k] = ig[4]
                #val5[i,j,k] = ig[5]
    return np.array(odds),np.array(signal),np.array(line),np.array(noise)#,val4,val5


    
    
