import matplotlib
matplotlib.use('Agg')
from matplotlib import rc
from matplotlib import mlab
from mpl_toolkits.axes_grid1 import make_axes_locatable


from streamlines import streamplot
from streamlines import fstreamplot
#rc('verbose', level='debug')
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('mathtext',fontset='cm')
#rc('mathtext',rm='stix')
#rc('text', usetex=True)

#from pylab import figure, axes, plot, xlabel, ylabel, title, grid, savefig, show

import gc
import numpy as np
import array
import scipy as sp
from scipy.interpolate import griddata
from scipy.interpolate import interp1d
#from scipy.interpolate import Rbf
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from matplotlib import mpl
from matplotlib import cm
from numpy import ma
import matplotlib.colors as colors
import os,glob
import pylab
import sys
import streamlines
from matplotlib.patches import Ellipse

import re
#import sorting

from datetime import datetime

#from scipy import *
#import scipy.io.array_import
#from scipy import gplt
from scipy import fftpack

#from matplotlib.pyplot import *
#from numpy import *
#from mpl_toolkits.axisartist import *

#global rho, ug, vu, uu, B, CS
#global nx,ny,nz,_dx1,_dx2,_dx3,ti,tj,tk,x1,x2,x3,r,h,ph,gdet,conn,gn3,gv3,ck,dxdxp

# http://www.scipy.org/scipy_Example_List
# http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html
# http://mail.scipy.org/pipermail/scipy-user/2011-April/029172.html
def leastsqexample1():
    ## Parametric function: 'v' is the parameter vector, 'x' the independent varible
    fp = lambda v, x: v[0]/(x**v[1])*sin(v[2]*x)

    ## Noisy function (used to generate data to fit)
    v_real = [1.5, 0.1, 2.]
    fn = lambda x: fp(v_real, x)

    ## Error function
    e = lambda v, x, y: (fp(v,x)-y)

    ## Generating noisy data to fit
    n = 30
    xmin = 0.1
    xmax = 5
    x = linspace(xmin,xmax,n)
    y = fn(x) + rand(len(x))*0.2*(fn(x).max()-fn(x).min())

    ## Initial parameter value
    v0 = [3., 1, 4.]

    ## Fitting
    v, success = leastsq(e, v0, args=(x,y), maxfev=10000)

    ## Plot
    def plot_fit():
        print 'Estimater parameters: ', v
        print 'Real parameters: ', v_real
        X = linspace(xmin,xmax,n*5)
        plot(x,y,'ro', X, fp(v,X))

    plot_fit()
    show()




#newx=array([ 0.99367893 , 1.01687336 , 1.04006779 , 1.06326234 , 1.08645678 , 1.10965121, 1.13284564 , 1.15604019 , 1.17923462 , 1.20242906 , 1.22562349 , 1.24881804, 1.27201247 , 1.2952069 ,  1.31840146 , 1.34159589 , 1.36479032 , 1.38798475, 1.4111793 ,  1.43437374 , 1.45756817 , 1.48076272 , 1.50395703 , 1.52715158, 1.55034602 , 1.57354057 , 1.596735 , 1.61992943 , 1.64312387 , 1.66631842 , 1.68951285 , 1.71270728 , 1.73590171 , 1.75909626 , 1.7822907 ,  1.80548513 , 1.82867956 , 1.85187411 , 1.87506855 , 1.89826298 , 1.92145741 , 1.94465196])
#newy=array([-0.91355157, -0.91705036, -0.9185347, -0.92136014, -0.92199862, -0.92411357 , -0.92464483, -0.92716295, -0.92769766, -0.92856294, -0.92812204, -0.92825502 , -0.92767322, -0.9278236, -0.9260515, -0.92504358, -0.92273855, -0.92095131 , -0.91915423, -0.91806215, -0.91925704, -0.92391104, -0.93056518, -0.93906242 , -0.95015585, -0.96284544, -0.9774726, -0.99415284, -1.01308155, -1.03264165 , -1.05143404, -1.06892014, -1.08700919, -1.10795486, -1.12901759, -1.14929163 , -1.17080712, -1.19166636, -1.21111584, -1.22679734, -1.2373203, -1.24849439])




#  http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
def curvfitexample1():
    def func(x, a, b, c):
        return a*np.exp(-b*x) + c
    #
    x = np.linspace(0,4,50)
    y = func(x, 2.5, 1.3, 0.5)
    yn = y + 0.2*np.random.normal(size=len(x))
    #
    popt, pcov = curve_fit(func, x, yn)
    print("test curvfit")
    print(popt)
    print(pcov)
    #
    return(popt,pcov)

def jonpolyfit(x,y,degree,dologx=1,dology=1,doabs=1,badfit=0,num=0):
    #
    newx=np.copy(x)
    newy=np.copy(y)
    #
    if doabs==1:
        newx=np.fabs(newx)
        newy=np.fabs(newy)
    #
    # assume if do log, ok to take abs
    if dologx==1:
        newx=np.log10(np.fabs(newx)+1E-20)
    # assume x can't be a problem for inf or nan
    #
    if dology==1:
        newy=np.log10(np.fabs(newy)+1E-20)
        newy[np.isnan(newy)==1]=-20
        newy[np.isinf(newy)==1]=-20
    else:
        newy[np.isnan(newy)==1]=1E-20
        newy[np.isinf(newy)==1]=1E-20
    #
    xavg=np.average(newx)
    yavg=np.average(newy)
    #
    # remove average for simple interpretation of sigma and results for plotting
    newx=newx-xavg
    newy=newy-yavg
    #
    # make float64 so avoids silly errors or no actual calculation and inf for pcov and only returned popt=v0
    newx=np.asarray(newx,dtype=np.float64)
    newy=np.asarray(newy,dtype=np.float64)
    #
    ###############################################
    # get fit
    (fity)=np.polyfit(newx,newy,degree)
    #
    # get fit vs. newx
    # recall: y = x^n fity[d-n] for n=0..d inclusive of n=d
    fityvsx=np.copy(newy)
    for degiter in np.arange(0,degree+1):
        fityvsx=fityvsx + newx**(degree-degiter)*fity[degiter]
    #
    # goodness of overall fit
    sigmaoverall=np.std(fityvsx-newy)
    #
    # get covariance matrix (NOT for estimating variance of parameters!)
    covy=np.cov(newx,newy)
    #
    #
    # truefity[a,b] is fit to a*x + b
    # fity[ap,bp] is fit to ap*xp + bp
    # just changes average value, not slope
    truefity=np.copy(fity)
    truefity[1]=yavg - truefity[0]*xavg + truefity[1]
    #
    print("polyfit fity=") ; sys.stdout.flush()
    print(fity) ; sys.stdout.flush()
    print(truefity) ; sys.stdout.flush()
    #print(covy) ; sys.stdout.flush()
    #
    # determine if fit is significant using variance of parameter
    ###################################
    ## Parametric function: 'v' is the parameter vector, 'x' the independent varible
    fp = lambda v, x: v[0]*x + v[1]

    ## Noisy function (used to generate data to fit)
    #v_real = [1.5, 0.1, 2.]
    #fn = lambda x: fp(v_real, x)

    ## Error function
    e = lambda v, x, y: (fp(v,x)-y)

    ## Generating noisy data to fit
    #n = 30
    #xmin = 0.1
    #xmax = 5
    #x = linspace(xmin,xmax,n)
    #y = fn(x) + rand(len(x))*0.2*(fn(x).max()-fn(x).min())

    ## Initial parameter value
    v0 = [fity[0],fity[1]]

    ## Fitting
    (fitlsq, covlsq, infodict, mesg, ier) = leastsq(e, v0, args=(newx,newy), maxfev=10000,full_output=1)
    truefitlsq=np.copy(fitlsq)
    truefitlsq[1]=truefitlsq[1] + truefitlsq[0]*xavg + yavg
    #
    print("Least Square results") ; sys.stdout.flush()
    print(fitlsq) ; sys.stdout.flush()
    print(truefitlsq) ; sys.stdout.flush()
    print(covlsq) ; sys.stdout.flush()
    print(infodict) ; sys.stdout.flush()
    print(mesg) ; sys.stdout.flush()
    print(ier) ; sys.stdout.flush()
    print("Done least square results") ; sys.stdout.flush()
    #
    ################################
    # DEBUG:
    #curvfitexample1()
    #
    ################################
    #
    #
    # so measure deviations from the average, not from (x,y)=(0,0)
    def func(x, a, b):
        return a*x + b
    #
    # go ahead and put in good guess
    v0 = [fity[0],fity[1]]
    #
    # get fit
    # apparently pcov diagonals are variance of each parameter *independently* as if other parameter not fit for
    (popt, pcov) = curve_fit(func, newx, newy,p0=v0)
    truepopt=np.copy(popt)
    truepopt[1]=truepopt[1] + truepopt[0]*xavg + yavg
    #
    #print("curve_fit newx newy") ; sys.stdout.flush()
    #print("newx") ; sys.stdout.flush()
    #print(newx) ; sys.stdout.flush()
    #print("newy") ; sys.stdout.flush()
    #print(newy) ; sys.stdout.flush()
    #
    print("curve_fit results") ; sys.stdout.flush()
    print(popt) ; sys.stdout.flush()
    print(truepopt) ; sys.stdout.flush()
    print(pcov) ; sys.stdout.flush()
    print("done curve_fit results") ; sys.stdout.flush()
    #
    ################################
    # error analysis
    #
    sigma=np.copy(fity)
    goodfit=np.copy(fity)
    #
    # pcov should be array unless failed.
    if type(pcov) is float:
        badpcov=1
    else:
        badpcov=0
    #
    #pcov[0]!=np.inf: # then can estimate error
    #len(pcov)==degree
    #
    if badpcov==0:
        #  or 
        #
        # get sigma for each coefficient and check goodness of fit for each coefficient
        # http://en.wikipedia.org/wiki/Standard_deviation
        # 2sigma~95%
        if modelname=="runlocaldipole3dfiducial":
            numsigma=3.0
        else:
            numsigma=3.0 # only by sigma=4 does it appear I would say both power-law and reasonable looking fit
        #
        for degiter in np.arange(0,degree+1):
            sigma[degiter]=numsigma*np.sqrt(np.fabs(pcov[degiter,degiter]))
            #
            if 1==1:
                if (fity[degiter]>0.0 and (fity[degiter]-sigma[degiter]<0.0)) or (fity[degiter]<0.0 and (fity[degiter]+sigma[degiter]>0.0)):
                    goodfit[degiter]=0
                else:
                    goodfit[degiter]=1
                #
                # override for n~0.  Just because crosses zero doesn't mean bad fit -- not a correlation where no correlation means no result.  Rather, no correlation here means flat distribution and that's meaningful to report.
                # choose n=0.25 as cut-off since don't expect |n|<<0.25 to be meaningfully different from n=0
                # cutting n=0.25 with sigma=0.25 also matches zero-crossing, so n=0.26 not treated unfairly compared to n=0.25 -- smoothly |n|<0.25 allows broader condition than just zero-crossing.
                if degree==1 and degiter==0 and np.fabs(fity[degiter])<0.25 and np.fabs(sigma[degiter])<0.25:
                    goodfit[degiter]=1
                #
            elif 0==1:
                if 1==0:
                    # only bad fit if sigma too large -- define as deviating by 32% or whatever % one wants to use
                    conflimit=0.32
                    diffsigma=max(np.fabs(fity[degiter])-np.fabs(sigma[degiter]),0.0)
                    sumsigma=np.fabs(fity[degiter])+np.fabs(sigma[degiter])
                    # diffsigma/sumsigma varies from 1 (perfect fit) to 0 (bad fit).  This catches 0-crossings as bad fits, but is more restrictive for far-from-zero power-laws
                    if(diffsigma/sumsigma<conflimit):
                        goodfit[degiter]=0
                    else:
                        goodfit[degiter]=1
                    #                
                elif 1==0:
                    # only bad fit if sigma too large
                    conflimit1=0.25
                    conflimit2=0.5
                    conflimit3=1.0
                    conflimit4=2.0
                    cond1=(np.fabs(fity[degiter])<0.5 and np.fabs(sigma[degiter])>conflimit1)
                    cond2=(np.fabs(fity[degiter])>0.5 and np.fabs(fity[degiter])<1.0 and np.fabs(sigma[degiter])>conflimit2)
                    cond3=(np.fabs(fity[degiter])>1.0 and np.fabs(fity[degiter])<2.0 and np.fabs(sigma[degiter])>conflimit3)
                    cond4=(np.fabs(fity[degiter])>2.0 and np.fabs(fity[degiter])<3.0 and np.fabs(sigma[degiter])>conflimit4)
                    if cond1 or cond2:

                        goodfit[degiter]=0
                    else:
                        goodfit[degiter]=1
                    #                
        #
    else:
        # assume "good" if no pcov, which means only had (e.g.) 2 points for fitting
        print("NO PCOV")
        for degiter in np.arange(0,degree+1):
            sigma[degiter]=0
            goodfit[degiter]=1
    #
    # check if can even say if fit was good or not -- need enough points
    if len(newx)<6:
        print("not enough points: len(newx)=%d" % len(newx))
        for degiter in np.arange(0,degree+1):
            goodfit[degiter]=0
    #
    if badfit==1:
        print("bad fit assumed in sense that not enough radial dynamic range even if good fit over small range")
        for degiter in np.arange(0,degree+1):
            goodfit[degiter]=0
    #
    ############
    print("jonpolyfits sigma") ; sys.stdout.flush()
    print(sigma) ; sys.stdout.flush()
    print("jonpolyfits goodfit") ; sys.stdout.flush()
    print(goodfit) ; sys.stdout.flush()
    print("sigmaoverall=%g" % (sigmaoverall)) ; sys.stdout.flush()
    #
    # DEBUG:
    if avoidplotsglobal==0:
        #
        # for fil in `ls fitplot*.png | sort -V` ; do echo $fil ; display $fil ; done
        #
        # montage:
        # files=`ls -rt fitplot*.png` ; montage -geometry 100x100 $files montage_fitplot.png ; display montage_fitplot.png
        #
        #
        newX = np.linspace(min(newx),max(newx),len(newx)*5)
        fitlsqdevdn=np.copy(fitlsq)
        fitlsqdevdn[0]=fitlsq[0] - sigma[0]
        fitlsqdevup=np.copy(fitlsq)
        fitlsqdevup[0]=fitlsq[0] + sigma[0]
        #
        print("sigma")
        print(sigma)
        print("fitlsq")
        print(fitlsq)
        print("fitlsqdevdn")
        print(fitlsqdevdn)
        print("fitlsqdevup")
        print(fitlsqdevup)
        #
        plt.figure(992)
        plt.clf()
        plt.plot(newx,newy,'ro', newX, fp(fitlsq,newX),'b', newX, fp(fitlsqdevdn,newX),'g', newX, fp(fitlsqdevup,newX))
        plt.savefig("fitplot%d.png" % (num) )
        #show()
    #
    return(truefity,sigma,goodfit)



def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    np.hanning, np.hamming, np.bartlett, np.blackman, np.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s=x
    spacer=np.zeros(window_len/2,dtype=x.dtype)
    #leftbc=x[0]
    #leftbc=leftbc+spacer*0
    #rightbc=x[-1]
    #rightbc=rightbc+spacer*0
    ##s=np.r_[x[window_len/2-1:-1:-1],x,x[-1:-window_len/2:-1]]
    #s=np.r_[leftbc,x,rightbc]
    ##s=[spacer,x,spacer]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    #y=np.convolve(w/w.sum(),s,mode='valid')
    #y=np.convolve(w/w.sum(),s,mode='full')
    y=np.convolve(w/w.sum(),s,mode='same')
    print("smooth sizes: lenx=%d spacer=%d lens=%d lenw=%d leny=%d" % (len(x),len(spacer),len(s),len(w),len(y))) ; sys.stdout.flush()
    return y







def make_legend_axes(ax):
    divider = make_axes_locatable(ax)
    legend_ax = divider.append_axes('right', 0.4, pad=0.2)
    return legend_ax

def extrema(x, max = True, min = True, strict = False, withendi = False, withendf = False):
    """
    This function will index the extrema of a given array x.
    
    Options:
        max        If true, will index maxima
        min        If true, will index minima
        strict        If true, will not index changes to zero gradient
        withend(i/f) If true, always include x[0] and x[-1]
    
    This function will return a tuple of extrema indexies and values
    """
    
    # This is the gradient
    from numpy import zeros
    dx = zeros(len(x))
    from numpy import diff
    dx[1:] = diff(x)
    dx[0] = dx[1]
    
    # Clean up the gradient in order to pick out any change of sign
    from numpy import sign
    dx = sign(dx)
    
    # define the threshold for whether to pick out changes to zero gradient
    threshold = 0
    if strict:
        threshold = 1
        
    # Second order diff to pick out the spikes
    d2x = diff(dx)
    
    if max and min:
        d2x = abs(d2x)
    elif max:
        d2x = -d2x
    
    # Take care of the two ends
    if withendi:
        d2x[0] = 2
    if withendf:
        d2x[-1] = 2
    
    # Sift out the list of extremas
    from numpy import nonzero
    ind = nonzero(d2x > threshold)[0]
    
    return ind, x[ind]


# sign function
#http://fnielsen.posterous.com/where-is-the-sign-function-in-python

def divideavoidinf(x):
    SMALL=1E-30
    y=1.0*np.sign(x)/(np.fabs(x)+SMALL)
    return(y)

def round_to_n(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
    return "%.*e" % (n-1, x)

def roundto2fitold(x,goodness):
    if goodness==1:
        y="%.*e" % (2-1, x)
        z=float(y)
        y="%g" % (z)
    else:
        y="-"
    return(y)

def roundto2fit(x,sigma,goodness):
    #
    if goodness==1:
        # no point in showing second digit if sigma>1
        if (np.fabs(sigma)>=1.0 and np.fabs(x)<10.0) or (np.fabs(sigma)>=0.1 and np.fabs(x)<1.0) or (np.fabs(sigma)>=0.01 and np.fabs(x)<0.1):
            y="%.*e" % (1-1, x)
        else:
            y="%.*e" % (2-1, x)
        #
        z=float(y)
        y1="%g" % (z)
        ys="%.*e" % (1-1, sigma)
        zs=float(ys)
        y2="_{\\pm{}%g}" % (zs)
        y="$"+"{"+y1+"}"+y2+"$"
    else:
        y="-"
    #
    return(y)



def roundto2_rq2mri1(x,rcutdn,rcutup):
    #rq21cutdn=rcutdn
    #iq21cutdn=iofr(rq21cutdn)
    #rq21cutup=rcutup
    #iq21cutup=iofr(rq21cutup)
    #if x<=1.001*r[iq21cutdn,ny/2,0]:
    if x<=1.001*rcutdn:
        y="-"
        return(y)
    #elif x>=0.999*r[iq21cutup,ny/2,0]:
    elif x>=0.999*rcutup:
        y="%.*e" % (2-1, rcutup)
        z=float(y)
        y="$>%d$" % (z)
        return y
    else:
        y="%.*e" % (2-1, x)
        z=float(y)
        y="%d" % (z)
        return y
    #

def roundto2(x):
    y="%.*e" % (2-1, x)
    #y=y.replace('e+02',00
    z=float(y)
    return z


def roundto2forupsilon(x):
    # only more significant digits for >=0.1
    if x>=0.1:
        y="%.*e" % (2-1, x)
    else:
        y="%.*e" % (1-1, x)
    #y=y.replace('e+02',00
    z=float(y)
    return z

def roundto2forphi(x):
    # only more significant digits for <100.0
    if x<100.0:
        y="%.*e" % (2-1, x)
    else:
        y="%.*e" % (1-1, x)
    #y=y.replace('e+02',00
    z=float(y)
    z=z*1.0+1E-10*z
    return z

def roundto2forphistring(x):
    # only more significant digits for <100.0
    if x<100.0:
        y="%.*e" % (2-1, x)
        z=float(y)
        y="%g" % z
    else:
        y="%.*e" % (1-1, x)
    #y=y.replace('e+02',00
    return y

def roundto3(x):
    y="%.*e" % (3-1, x)
    #y=y.replace('e+02',00
    z=float(y)
    return z

def roundto3forl(x):
    if np.fabs(x)<0.01:
        y="%.*e" % (1-1, x)
    elif np.fabs(x)<0.1:
        y="%.*e" % (2-1, x)
    else:
        y="%.*e" % (3-1, x)
    #
    #y=y.replace('e+02',00
    z=float(y)
    # don't resolve better than 1%, so zero-out such small values since overall not significant digits
    #if np.fabs(z)<0.01:
    #    z=0
    return z


def roundto3foreta(x):
    if np.fabs(x)<0.01:
        y="%.*e" % (1-1, x)
    elif np.fabs(x)<0.1:
        y="%.*e" % (2-1, x)
    else:
        y="%.*e" % (3-1, x)
    #
    #y=y.replace('e+02',00
    z=float(y)
    # don't resolve better than 1%, so zero-out such small values since overall not significant digits
    #if np.fabs(z)<0.1:
    #if np.fabs(z)<0.01:
    #    z=0
    return z


def get2davg(usedefault=0,whichgroup=-1,whichgroups=-1,whichgroupe=-1,itemspergroup=20):
    if whichgroup >= 0:
        whichgroups = whichgroup
        whichgroupe = whichgroup + 1
    elif whichgroupe < 0:
        whichgroupe = whichgroups + 1
    #check values for sanity
    if usedefault == 0 and (whichgroups < 0 or whichgroupe < 0 or whichgroups >= whichgroupe or itemspergroup <= 0):
        print( "whichgroups = %d, whichgroupe = %d, itemspergroup = %d not allowed" 
               % (whichgroups, whichgroupe, itemspergroup) );sys.stdout.flush()
        sys.stdout.flush()
        return None
    #
    if usedefault:
        fname = "avg2d.npy"
    else:
        fname = "avg2d%02d_%04d_%04d.npy" % (itemspergroup, whichgroups, whichgroupe)
    #
    print("gdet2davg(): checking for fname=%s" % (fname)) ; sys.stdout.flush()
    #
    if os.path.isfile( fname ):
        print( "File %s exists, loading from file..." % fname );sys.stdout.flush()
        avgtot=np.load( fname )
        return( avgtot )
    #####################
    defaultfti,defaultftf=getdefaulttimes()
    avgfti = defaultfti
    avgftf = defaultftf
    ######################
    print("whichgroups=%d whichgroupe=%d" % (whichgroups,whichgroupe)) ; sys.stdout.flush()
    ######################
    n2avg = 0
    nitems = 0
    myrange = np.arange(whichgroups,whichgroupe)
    numrange = myrange.shape[0]
    firstavgone=1
    firstavgoneused=1
    # defaults for ts,tf
    ts=0
    tf=0
    for (i,g) in enumerate(myrange):
        print("i=%d g=%d" % (i,g)) ; sys.stdout.flush()
        avgone=get2davgone( whichgroup = g, itemspergroup = itemspergroup )
        if avgone == None:
            continue
        if firstavgone==1:
            avgtot = np.zeros_like(avgone)
            firstavgone=0
        tstry=avgone[0,0,0]
        tftry=avgone[0,1,0]
        # use avg data if either start or finish of time used for averaging is within average period
        didntuse=1
        if numrange>1:
            # then assume merging
            if tftry!=0 and tstry!=0: # only include if no inital dump (in case small set of files happens to have tf late but ti=0
                if (tstry>avgfti and tstry<avgftf) or ((tftry>avgfti and tftry<avgftf)):
                    if firstavgoneused==1:
                        ts=avgone[0,0,0]
                        firstavgoneused=0
                    tf=avgone[0,1,0]
                    #
                    avgtot += avgone
                    nitems += avgone[0,2,0]
                    n2avg += 1
                    print("USING: During merge: ts=%g tf=%g tstry=%g tftry=%g n2avg=%d" % (ts,tf,tstry,tftry,n2avg));sys.stdout.flush()
                    didntuse=0
                    #
            # end if within averaging period of time
            if didntuse==1:
                print("NOTUSING: During merge: tstry=%g tftry=%g n2avg=%d" % (tstry,tftry,n2avg));sys.stdout.flush()
        else:
            # then not merging, normal assignments no matter what the time
            ts=avgone[0,0,0]
            tf=avgone[0,1,0]
            avgtot += avgone
            nitems += avgone[0,2,0]
            n2avg += 1
            print("During NONmerge: ts=%g tf=%g tstry=%g tftry=%g n2avg=%d" % (ts,tf,tstry,tftry,n2avg));sys.stdout.flush()
    # end for loop over whichgroups->whichgroupe
    #
    # set final avg file times and number of items
    avgtot[0,0,0] = ts
    avgtot[0,1,0] = tf
    avgtot[0,2,0] = nitems
    print("Final avg_ts=%g avg_te=%g nitems=%d" % (avgtot[0,0,0],avgtot[0,1,0],avgtot[0,2,0]));sys.stdout.flush()
    #get the average
    if n2avg == 0:
        print( "0 total files, so no data generated." ) ; sys.stdout.flush()
        return( None )
    #avoid renormalizing the header
    avgtot[1:] /= n2avg
    #only save if more than 1 dump was to be processed (indicating merge)
    if numrange > 1:
        print( "Saving data to file: n2avg=%d ..." % (n2avg) );sys.stdout.flush()
        np.save( fname, avgtot )
    return( avgtot )
    


def assignavg2dvars(avgmem):
    global avg_ts,avg_te,avg_nitems
    global avg_rho,avg_ug,avg_bsq,avg_unb
    global avg_uu,avg_bu,avg_ud,avg_bd,avg_B,avg_gdetB,avg_omegaf2,avg_omegaf2b,avg_omegaf1,avg_omegaf1b,avg_rhouu,avg_rhobu,avg_rhoud,avg_rhobd
    global avg_absuu,avg_absbu,avg_absud,avg_absbd
    global avg_absomegaf2,avg_absomegaf2b,avg_absomegaf1,avg_absomegaf1b
    global avg_absrhouu,avg_absfdd
    global avg_uguu,avg_ugud,avg_Tud,avg_fdd,avg_rhouuud,avg_uguuud,avg_bsquuud,avg_bubd,avg_uuud
    global avg_TudEM, avg_TudMA, avg_mu, avg_sigma, avg_bsqorho, avg_absB, avg_absgdetB, avg_psisq
    global avg_TudPA, avg_TudIE
    global avg_gamma,avg_pg,avg_pb,avg_beta
    #avg defs
    i=0
    # 1
    # uses fake 2D space for some single numbers
    avg_ts=avgmem[i,0,:];
    avg_te=avgmem[i,1,:];
    print( "assignavg2dvars: avg_ts=%d avg_te=%d" % (avg_ts[0],avg_te[0])) ; sys.stdout.flush()
    avg_nitems=avgmem[i,2,:];i+=1
    #quantities
    # 4
    avg_rho=avgmem[i,:,:,None];i+=1
    avg_ug=avgmem[i,:,:,None];i+=1
    avg_bsq=avgmem[i,:,:,None];i+=1
    avg_unb=avgmem[i,:,:,None];i+=1
    # 4*4=16
    n=4
    avg_uu=avgmem[i:i+n,:,:,None];i+=n
    avg_bu=avgmem[i:i+n,:,:,None];i+=n
    avg_ud=avgmem[i:i+n,:,:,None];i+=n
    avg_bd=avgmem[i:i+n,:,:,None];i+=n
    # 4*4=16
    n=4
    avg_absuu=avgmem[i:i+n,:,:,None];i+=n
    avg_absbu=avgmem[i:i+n,:,:,None];i+=n
    avg_absud=avgmem[i:i+n,:,:,None];i+=n
    avg_absbd=avgmem[i:i+n,:,:,None];i+=n
    #cell-centered magnetic field components
    # 3*2=6
    n=3;
    avg_B=avgmem[i:i+n,:,:,None];i+=n
    avg_gdetB=avgmem[i:i+n,:,:,None];i+=n
    # 3*2=6
    n=3
    avg_absB=avgmem[i:i+n,:,:,None];i+=n
    avg_absgdetB=avgmem[i:i+n,:,:,None];i+=n
    # 4
    avg_omegaf2=avgmem[i,:,:,None];i+=1
    avg_omegaf2b=avgmem[i,:,:,None];i+=1
    avg_omegaf1=avgmem[i,:,:,None];i+=1
    avg_omegaf1b=avgmem[i,:,:,None];i+=1
    #
    # 4
    avg_absomegaf2=avgmem[i,:,:,None];i+=1
    avg_absomegaf2b=avgmem[i,:,:,None];i+=1
    avg_absomegaf1=avgmem[i,:,:,None];i+=1
    avg_absomegaf1b=avgmem[i,:,:,None];i+=1
    #
    # 6*4=24
    n=4
    avg_rhouu=avgmem[i:i+n,:,:,None];i+=n
    avg_rhobu=avgmem[i:i+n,:,:,None];i+=n
    avg_rhoud=avgmem[i:i+n,:,:,None];i+=n
    avg_rhobd=avgmem[i:i+n,:,:,None];i+=n
    avg_uguu=avgmem[i:i+n,:,:,None];i+=n
    avg_ugud=avgmem[i:i+n,:,:,None];i+=n
    #
    # 1*4=4
    n=4
    avg_absrhouu=avgmem[i:i+n,:,:,None];i+=n
    #
    # 2*16=32
    n=16
    #energy fluxes and faraday
    avg_Tud=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    avg_fdd=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # 1*16=16
    n=16
    # faraday
    avg_absfdd=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # 5*16=80
    # part1: rho u^m u_l
    avg_rhouuud=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # part2: u u^m u_l
    avg_uguuud=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # part3: b^2 u^m u_l
    avg_bsquuud=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # part6: b^m b_l
    avg_bubd=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # u^m u_l
    #print( "i = %d, avgmem.shape[0] = %d " % (i, avgmem.shape[0]) )
    #sys.stdout.flush()
    avg_uuud=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # 2*16=32
    n=16
    #EM/MA
    avg_TudEM=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    avg_TudMA=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # 2*16=32
    n=16
    #P/IE
    avg_TudPA=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    avg_TudIE=avgmem[i:i+n,:,:,None].reshape((4,4,nx,ny,1));i+=n
    # 3
    #mu,sigma
    n=1
    avg_mu=avgmem[i,:,:,None];i+=n
    avg_sigma=avgmem[i,:,:,None];i+=n
    avg_bsqorho=avgmem[i,:,:,None];i+=n
    # 1
    n=1
    avg_psisq=avgmem[i,:,:,None];i+=n
    #
    # number of full 2D quantities
    nqtyavg=i
    global navg
    navg=getnqtyavg()
    if nqtyavg!=navg:
        print("nqtyavg=%d while navg=%d" % (nqtyavg,navg)) ; sys.stdout.flush()
    #
    #
    ##########################
    #derived quantities
    avg_gamma=avg_uu[0]/(-gn3[0,0])**0.5
    avg_pg=((gam-1)*avg_ug)
    avg_pb=avg_bsq*0.5
    avg_beta=avg_pg/avg_pb


# http://stackoverflow.com/questions/4265284/how-to-do-sort-v-in-osx
# http://blog.pobblelabs.org/2007/12/11/exception-handling-slow/
# http://nedbatchelder.com/blog/200712/human_sorting.html#comments
# http://www.python-forum.org/pythonforum/viewtopic.php?f=3&t=22908
# http://www.python-forum.org/pythonforum/viewtopic.php?f=3&t=24328

def tryint(s):
    try:
        return int(s)
    except:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


def getnqtyavg():
    # was 206 before with Sasha's code, but apparently should have been 207
    #value=1 + 4 + 16 + 6 + 4 + 24 + 32 + 80 + 32 + 32 + 3 + 6 + 1
    # added&moved abs versions
    value=1 + 4 + 16*2 + 6*2 + 4*2 + 24+4 + 32+16 + 80 + 32 + 32 + 3 + 1
    return(value)


# even for average 2D data, clean-out floor already because some of the below involves multiplication or division that cannot be removed after averaging
# also, since region where bsqorho<maxbsqorho moves around, leakage occurs if only cutting based upon time-phi-averaged bsqorho
def getrhouclean(rho,ug,uu):
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        maxbsqorhohigh=45
        maxbsqorhonear=30
        maxbsqorhofar=20 # needs to appy at r=9 out to rjet\sim 50
        maxuu0high=50
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        maxbsqorhohigh=50
        maxbsqorhonear=40 # could make much higher for a=0.99 model and some other models
        maxbsqorhofar=30 # assumed at r=9 and outward including rjet\sim 50
        maxuu0high=50
    else: # thick disk models
        maxbsqorhohigh=40 # should be near limit on bsqorho
        maxbsqorhonear=30 # was 30, but want to cut closer to limit so rho vs. \phi plots are better represented # should include all of disk near horizon
        maxbsqorhofar=10 # should include part of jet far away, while maxbsqorhonear might be too restrictive at large radii so no jet would be included
        maxuu0high=50
    #
    #
    len3rho=len(rho[0,0,:])
    #
    if len3rho==1 and nz>1:
        # assume 2D averages involved where last dimension is 1.  Need to keep consistent with how used on other things.
        print("rho wasn't nz in size, so assume 2D avg with only nz=1 effectively") ; sys.stdout.flush()
    #
    #
    # generic reformatting of r to fit nz changes (assumes r doesn't vary with phi)
    faker=np.zeros((nx,ny,len3rho),dtype=r.dtype)
    for kk in np.arange(0,len3rho):
        faker[:,:,kk] = r[:,:,0]
    #
    rinterp=(faker-9.0)*(1.0-0.0)/(0.0-9.0) # gives 0 for use near 9   gives 1 for use near 0
    rinterp[rinterp>1.0]=1.0
    rinterp[rinterp<0.0]=0.0
    #
    condmaxbsqorhorhs=rinterp*maxbsqorhonear + (1.0-rinterp)*maxbsqorhofar
    condmaxbsqorho=(bsq/rho < condmaxbsqorhorhs) # used as spatial conditional to replace single value of maxbsqorho 
    #
    print("t=%g" % (t))
    print("r")
    print(r[:,ny/2,0])
    print("condmaxbsqorhorhs along r")
    print(condmaxbsqorhorhs[:,ny/2,0])
    print("condmaxbsqorho along eq")
    print(condmaxbsqorho[0,:,0])
    #
    bsqorho=bsq/rho # want this to be using original rho
    #
    rhoclean = np.copy(rho)
    rhoclean[bsqorho>maxbsqorhonear]=1E-30
    rhoclean[condmaxbsqorho==0]=1E-30
    #
    ugclean = np.copy(ug)
    ugclean[bsqorho>maxbsqorhonear]=1E-30
    ugclean[condmaxbsqorho==0]=1E-30
    #
    douuclean=0 # choose (decided to keep original uu3 values even if floor messes them up, because otherwise have to modify uu3 at all radii in way that has \Omega_F constant along field lines.  Can't just modify near horizon since then energy flux not conserved.  Otherwise, worked well.)
    uuclean = np.copy(uu)
    #
    if douuclean==1:
        #
        #
        #############
        # force omegaf to be close to stationary/axisymmetric solution where floor dominates
        rh = 1+(1-a**2)**0.5
        omegah=a/(2.0*rh)
        #
        # only correct uu3 if close to limit of bsqorho where sensitive uu3 can be messed-up by floor still -- like near the pole
        # relevant for very close to horizon
        # do this at each time, because doing it after the fact (e.g. in SM) after averaging leads to artifacts and questionable cut-off values for bsqorho
        #
        # assumes dxdxp already defined
        newdxdxp33=dxdxp[3,3]
        if(len(dxdxp[3,3][0,0,:])!=nz):
            newdxdxp33=np.zeros((nx,ny,nz),dtype=rho.dtype)
            for kk in np.arange(0,nz):
                newdxdxp33[:,:,kk]=dxdxp[3,3][:,:,0]
        #
        print("shapes") ; sys.stdout.flush()
        print(rho.shape) ; sys.stdout.flush()
        print(bsq.shape) ; sys.stdout.flush()
        print(bsqorho.shape) ; sys.stdout.flush()
        print(uu.shape) ; sys.stdout.flush()
        print(newdxdxp33.shape) ; sys.stdout.flush()
        #
        # setup parabolic \Omega_F
        # Interpolate to parabola form so closer to what real solution would allow so less likely to go outside light cone (Check that somehow)
        # This is valid in sense that solution inside pure magnetosphere agrees with para solution for \Omega_F, far from monopole.  So assume rest of magnetosphere near limits of numerical validity and near floor is close to para.
        condhupper=(h>np.pi*0.5)
        hbz=np.copy(h)
        hbz[condhupper]=(np.pi-h[condhupper])
        omegafpara=(0.25*np.sin(hbz)**2*(1+np.log(1+np.cos(hbz))))/(4.0*np.log(2.0)+np.sin(hbz)**2+(np.sin(hbz)**2-2*(1.0+np.cos(hbz)))*np.log(1.0+np.cos(hbz)))
        omegafohpara=omegafpara/(1.0/(2.0*2.0))
        #
        typeomegaf=1 # 0=mono 1=para
        if typeomegaf==0:
            newomegaf=omegah*0.5/newdxdxp33
        else:
            newomegaf=omegafohpara*omegah/newdxdxp33
        #
        # RHS restriction is just to match arrays
        cond=np.fabs(B[1]*np.sqrt(gv3[1,1]))<np.fabs(B[2]*np.sqrt(gv3[2,2]))
        numcond=np.sum(cond)
        cond2=(bsqorho>maxbsqorhohigh)
        numcond2=np.sum(cond2)
        print("numcond=%d numcond2=%d" % (numcond,numcond2)); sys.stdout.flush()
        #
        maxiter=5
        for iter in np.arange(0,maxiter):
            #
            # define new uu3 assuming stationary-axisymmetric flow
            newuu3a=newomegaf*uuclean[0] + (uuclean[1]/B[1])*B[3]
            newuu3b=newomegaf*uuclean[0] + (uuclean[2]/B[2])*B[3]
            newuu3=newuu3a
            newuu3[cond]=newuu3b[cond]
            #
            # use cleaned-up uu3 in high bsqorho region only
            uuclean[3][cond2]=newuu3[cond2]
            #
            # fix uu0 so u.u=-1 is enforced.  Not doing this leads to completely wrong solutions for (e.g.) T^r_t and T^r_\phi
            # Can't change uu[3] without changing uu[0] for consistency.
            if 1==0:
                # fix using 3-vel (changes u^r too much so T^r_t and T^r_\phi change too much)
                # Also, can't just convert to 3-vel since may go outside light cone even if that's what's required to choose that omegaf.
                vunew = np.zeros_like(uuclean)
                vunew[0]=0
                vunew[1]=uuclean[1]/uuclean[0]
                vunew[2]=uuclean[2]/uuclean[0]
                vunew[3]=uuclean[3]/uuclean[0]
                #
                vdnew = mdot(gv3,vunew) ; vdnew[0]=0
                vsq = mdot(vdnew,vunew)
                uu0sqnew=1.0/ ( -gv3[0,0] - vsq - 2.0*mdot(vunew,gv3[0,:]) )
                condbaduu0=(uu0sqnew<1E-20)
                condbaduu0=condbaduu0+(uu0sqnew>maxuu0high**2)
                numcondbaduu0=np.sum(condbaduu0>0)
                print("iter=%d numcondbaduu0=%d pickuu0sqnew=%g\n",iter,numcondbaduu0,uu0sqnew[condbaduu0]) ; sys.stdout.flush()
                uu0new = np.sqrt(uu0sqnew)
                # set new clean solution, but don't fix if new uu0 became bad (i.e. u^t<0) even if satisfies bsqorho condition
                uuclean[0][condbaduu0==0]=uu0new[condbaduu0==0]
                uuclean[1][condbaduu0==0]=vunew[1][condbaduu0==0]*uu0new[condbaduu0==0]
                uuclean[2][condbaduu0==0]=vunew[2][condbaduu0==0]*uu0new[condbaduu0==0]
                uuclean[3][condbaduu0==0]=vunew[3][condbaduu0==0]*uu0new[condbaduu0==0]
            else:
                # fix using 4-vel (ensures u^r is the same, so that b^2 u^r u_t is as close as possible to same, so that T^r_t and T^r_\phi are close to original
                uunew = np.zeros_like(uuclean)
                uunew[1]=uu[1] # remains the same!
                uunew[2]=uu[2] # remains the same!
                uunew[3]=uuclean[3] # set using new v^3 but with old u^t
                #
                # get uunew[0]:
                AA=gv3[0,0]
                tempuunew=np.copy(uunew)
                tempuunew[0]=0*tempuunew[0]
                BB=2.0*mdot(tempuunew,gv3[0,:])
                tempudnew = mdot(gv3,tempuunew) ; tempudnew[0]=0
                usq=mdot(tempudnew,tempuunew)
                CC=1.0 + usq
                disc=BB**2 - 4.0*AA*CC
                uu0newa=(-BB + np.sqrt(disc))/(2.0*AA)
                uu0newb=(-BB - np.sqrt(disc))/(2.0*AA)
                uunew[0]=np.copy(uuclean[0])
                #
                # avoid changing if makes it a bad solution
                condbaduu0=(disc<0.0)
                condbaduu0=condbaduu0+(uu0newa<1E-10)
                condbaduu0=condbaduu0+(uu0newa>maxuu0high)
                numcondbaduu0=np.sum(condbaduu0>0)
                #
                pickeduu0new=np.copy(uuclean[0])
                # pick b solution if actually closer uu0 to original uu0 value
                condpickuu0=(np.fabs(uu0newb-pickeduu0new)<np.fabs(uu0newa-pickeduu0new))
                sumcondpickuu0=np.sum(condpickuu0)
                pickeduu0new[condpickuu0]=uu0newb[condpickuu0]
                #
                # avoid final assignment if bad uu0 solution
                uunew[0][condbaduu0==0]=pickeduu0new[condbaduu0==0]
                #
                print("iter=%d numcondbaduu0=%d sumcondpickuu0=%d uu0newabad=%g uu0newbbad=%g\n",iter,numcondbaduu0,sumcondpickuu0,uu0newa[condbaduu0],uu0newb[condbaduu0]) ; sys.stdout.flush()
                #
                uuclean[0]=uunew[0]
                uuclean[1]=uunew[1]
                uuclean[2]=uunew[2]
                uuclean[3]=uunew[3]
            #
            #
            # but now vu3 won't be quite right, so have to iterate a few times so uu0 converges with desired vu3
            cond2pick=cond2[5,:,0]
            uu0pick=uuclean[0][5,:,0][cond2pick]
            print("iter=%d uuclean[0]=%g\n",iter,uu0pick) ; sys.stdout.flush()
        #
        #udnew = mdot(gv3,uunew)
        #
        #
        #
        # test result
        omegaftest=uuclean[3]/uu[0] - (uu[1]/uu[0]/B[1])*B[3]
        omegatest=omegaftest*newdxdxp33
        omegarattest=omegatest[5,:,0]/omegah
        chosenomegaf=newomegaf[5,:,0]*newdxdxp33[5,:,0]/omegah
        print("chosenomegaf=%g omegarattest=%g ",chosenomegaf,omegarattest) ; sys.stdout.flush()
    #
    return(rhoclean,ugclean,uuclean,maxbsqorhonear,maxbsqorhofar,condmaxbsqorho,condmaxbsqorhorhs,rinterp)



def get2davgone(whichgroup=-1,itemspergroup=20):
    """
    """
    global avg_ts,avg_te,avg_nitems,avg_rho,avg_ug,avg_bsq,avg_unb,avg_uu,avg_bu,avg_ud,avg_bd,avg_B,avg_gdetB,avg_omegaf2,avg_omegaf2b,avg_omegaf1,avg_omegaf1b,avg_rhouu,avg_rhobu,avg_rhoud,avg_rhobd,avg_uguu,avg_ugud,avg_Tud,avg_fdd,avg_rhouuud,avg_uguuud,avg_bsquuud,avg_bubd,avg_uuud
    global avg_TudEM, avg_TudMA, avg_mu, avg_sigma, avg_bsqorho, avg_absB, avg_absgdetB, avg_psisq
    global avg_TudPA, avg_TudIE
    global avg_absuu,avg_absbu,avg_absud,avg_absbd
    global avg_absomegaf2,avg_absomegaf2b,avg_absomegaf1,avg_absomegaf1b
    global avg_absrhouu,avg_absfdd
    global firstfieldlinefile
    #
    if whichgroup < 0 or itemspergroup <= 0:
        print( "whichgroup = %d, itemspergroup = %d not allowed" % (whichgroup, itemspergroup) ) ; sys.stdout.flush()
        return None
    #
    fname = "avg2d%02d_%02d.npy" % (itemspergroup, whichgroup)
    if os.path.isfile( fname ):
        print( "File %s exists, loading from file..." % fname ) ; sys.stdout.flush()
        avgmem=np.load( fname )
        return( avgmem )
    tiny=np.finfo(rho.dtype).tiny
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    firstfieldlinefile=flist[0]
    #flist.sort()
    #
    #print "Number of time slices: %d" % flist.shape[0] ; sys.stdout.flush()
    #store 2D data
    global navg
    navg=getnqtyavg()
    avgmem=np.zeros((navg,nx,ny),dtype=np.float32)
    assignavg2dvars(avgmem)
    ##
    ######################################
    ##
    ## NEED TO ADD vmin/vmax VELOCITY COMPONENTS
    ##
    ######################################
    ##
    #
    #
    #
    #print "Total number of quantities: %d" % (i)
    print "Doing %d-th group of %d items" % (whichgroup, itemspergroup) ; sys.stdout.flush()
    #end avg defs
    for fldindex, fldname in enumerate(flist):
        if( whichgroup >=0 and itemspergroup > 0 ):
            if( fldindex / itemspergroup != whichgroup ):
                continue
        #
        print( "Reading " + fldname + " ..." ) ; sys.stdout.flush()
        rfd("../"+fldname)
        #
        print( "Computing get2davgone:" + fldname + " ..." ) ;  sys.stdout.flush()
        cvel()
        #
        #
        # which is *accepted* condition for non-jet part that's not floor contaminated.  So which==1 means ok to pass into averaging.  So use which==0 to clean-up things
        Tcalcud(maxbsqorho=maxbsqorhonear,which=condmaxbsqorho)
        faraday()
        #
        bsqo2rho = bsq/(2.0*rhounclean)
        bsqorho = bsq/(rhounclean)
        #
        #
        ##########################
        #if first item in group
        if fldindex == itemspergroup * whichgroup:
            avg_ts[0]=t
        #if last item in group
        # NO, number of files may not be evenly divisible by itemspergroup, so just always save te as when merging
        #if fldindex == itemspergroup * whichgroup + (itemspergroup - 1):
        avg_te[0]=t
        #
        # 1
        avg_nitems[0]+=1
        #
        ###################
        #quantities
        # 4
        avg_rho+=rhoclean.sum(-1)[:,:,None]
        avg_ug+=ugclean.sum(-1)[:,:,None]
        avg_bsq+=bsq.sum(-1)[:,:,None]
        enth=1+ugclean*gam/rhoclean
        avg_unb+=(enth*ud[0]).sum(-1)[:,:,None]
        # 16
        avg_uu+=uu.sum(-1)[:,:,:,None]
        avg_bu+=bu.sum(-1)[:,:,:,None]
        avg_ud+=ud.sum(-1)[:,:,:,None]
        avg_bd+=bd.sum(-1)[:,:,:,None]
        # 16
        avg_absuu+=(np.fabs(uu)).sum(-1)[:,:,:,None]
        avg_absbu+=(np.fabs(bu)).sum(-1)[:,:,:,None]
        avg_absud+=(np.fabs(ud)).sum(-1)[:,:,:,None]
        avg_absbd+=(np.fabs(bd)).sum(-1)[:,:,:,None]
        #cell-centered magnetic field components
        # 3+3=6
        n=3;
        avg_B+=B[1:4].sum(-1)[:,:,:,None]
        avg_gdetB+=gdetB[1:4].sum(-1)[:,:,:,None]
        # 6
        n=3
        avg_absB += np.abs(B[1:4]).sum(-1)[:,:,:,None]
        avg_absgdetB += np.abs(gdetB[1:4]).sum(-1)[:,:,:,None]
        #
        # 4
        # omega has to be cleaned because of effects of floor near pole where effect on omegaf alot despite dynamically insignificance, but do it elsewhere
        avg_omegaf2+=omegaf2.sum(-1)[:,:,None]
        avg_omegaf2b+=omegaf2b.sum(-1)[:,:,None]
        avg_omegaf1+=omegaf1.sum(-1)[:,:,None]
        avg_omegaf1b+=omegaf1b.sum(-1)[:,:,None]
        # 4
        # omega has to be cleaned because of effects of floor near pole where effect on omegaf alot despite dynamically insignificance, but do it elsewhere
        avg_absomegaf2+=(np.fabs(omegaf2)).sum(-1)[:,:,None]
        avg_absomegaf2b+=(np.fabs(omegaf2b)).sum(-1)[:,:,None]
        avg_absomegaf1+=(np.fabs(omegaf1)).sum(-1)[:,:,None]
        avg_absomegaf1b+=(np.fabs(omegaf1b)).sum(-1)[:,:,None]
        #
        # 6*4=24
        n=4
        avg_rhouu+=(rhoclean*uu).sum(-1)[:,:,:,None]
        avg_rhobu+=(rhoclean*bu).sum(-1)[:,:,:,None]
        avg_rhoud+=(rhoclean*ud).sum(-1)[:,:,:,None]
        avg_rhobd+=(rhoclean*bd).sum(-1)[:,:,:,None]
        avg_uguu+=(ugclean*uu).sum(-1)[:,:,:,None]
        avg_ugud+=(ugclean*ud).sum(-1)[:,:,:,None]
        #
        # 1*4=4
        n=4
        avg_absrhouu+=(np.fabs(rhoclean*uu)).sum(-1)[:,:,:,None]
        #
        # 16*2=32
        n=16
        #energy fluxes and faraday
        avg_Tud+=Tud.sum(-1)[:,:,:,:,None]
        avg_fdd+=((fdd)).sum(-1)[:,:,:,:,None]
        #
        # 16*1=16
        n=16
        # faraday
        avg_absfdd+=(np.fabs(fdd)).sum(-1)[:,:,:,:,None] # take absolute value since oscillate around 0 near equator and would cancel out and give noise in fdd/fdd type calculations, such as for omegaf
        #
        # 
        uuud=odot(uu,ud).sum(-1)[:,:,:,:,None]
        #
        # 16*5=80
        # part1: rho u^m u_l
        avg_rhouuud+=rhoclean.sum(-1)[:,:,None]*uuud
        # part2: u u^m u_l
        avg_uguuud+=ugclean.sum(-1)[:,:,None]*uuud
        # part3: b^2 u^m u_l
        avg_bsquuud+=bsq.sum(-1)[:,:,None]*uuud
        # part6: b^m b_l
        avg_bubd+=odot(bu,bd)[:,:,:,:,None].sum(-1)
        # u^m u_l
        avg_uuud+=uuud
        #
        # 16*2=32
        #EM/MA
        avg_TudEM+=TudEM.sum(-1)[:,:,:,:,None]
        avg_TudMA+=TudMA.sum(-1)[:,:,:,:,None]
        # 16*2=32
        #PA/IE (EM is B) -- for gammie plot
        avg_TudPA+=TudPA.sum(-1)[:,:,:,:,None]
        avg_TudIE+=TudIE.sum(-1)[:,:,:,:,None]
        #
        # 3
        #mu,sigma
        avg_mu += (-Tud[1,0]/(rhoclean*uu[1])).sum(-1)[:,:,None]
        avg_sigma += (-TudEM[1,0]/TudMA[1,0]).sum(-1)[:,:,None]
        avg_bsqorho += (bsq/rhounclean).sum(-1)[:,:,None] # keep as unclean since want to know what bsqorho is
        #
        #
        # 1
        n=1
        aphi = fieldcalcface()
        avg_psisq += ((_dx3*aphi.sum(-1))**2)[:,:,None]
        #
    #
    if avg_nitems[0] == 0:
        print( "No files found" ) ; sys.stdout.flush()
        return None
    #
    #
    ######################
    #divide all lines but the header line [which holds (ts,te,nitems)]
    #by the number of elements to get time averages
    avgmem[1:]/=(np.float32(avg_nitems[0])*np.float32(nz))
    #
    print( "Saving to file..." ) ; sys.stdout.flush()
    np.save( fname, avgmem )
    #
    print( "Done avgmem!" ) ; sys.stdout.flush()
    #
    return(avgmem)



def extractlena():
    #along field lines 0.5,0.8,0.99
    cvel()
    Tcalcud()
    faraday()
    psi=fieldcalctoth()/dxdxp[3][3][:,:,0]
    #
    Br = dxdxp[1,1]*B[1]+dxdxp[1,2]*B[2]
    Bh = dxdxp[2,1]*B[1]+dxdxp[2,2]*B[2]
    Bp = B[3]*dxdxp[3,3]
    #
    Brnorm=Br
    Bhnorm=Bh*np.abs(r)
    Bpnorm=Bp*np.abs(r*np.sin(h))
    #
    Bznorm=Brnorm*np.cos(h)-Bhnorm*np.sin(h)
    BRnorm=Brnorm*np.sin(h)+Bhnorm*np.cos(h)
    #
    eta=rho*uu[1]/B[1]
    #
    z = -r*np.cos(h)
    R = r*np.sin(h)
    #
    uur = dxdxp[1,1]*uu[1]+dxdxp[1,2]*uu[2]
    uuh = dxdxp[2,1]*uu[1]+dxdxp[2,2]*uu[2]
    uup = uu[3] * dxdxp[3,3]
    #
    uurnorm = uur
    uuhnorm=uuh*np.abs(r)
    uupnorm=uup*np.abs(r*np.sin(h))
    #
    #(cpsi, cr, ch, cR, cz, cBr, cBtheta, cBphi, ceta, crho, cuur, cuutheta, cuuphi, cgamma, comegaf, cmu, csigma, cbsq) = cvals

    vals = (psi, r, h, R, z, -Brnorm, -Bhnorm, -Bpnorm, -eta, rho, uurnorm, uuhnorm, uupnorm, gamma, omegaf2*dxdxp[3][3], mu, sigma, bsq)
    nu = 1.0
    om0 = 0.75

    for psi0 in (0.2, 0.4, 0.6, 0.8, 0.9, 0.99, 1.0):
        #FIELDLINE: psi = psi0
        fname = "fieldline_nu%0.3g_om%0.2g_psi%0.3g.dat" % (nu, om0, psi0)
        print( "Doing psi = %0.3g, fname = %s" % (psi0, fname) )
        sys.stdout.flush()
        cvals = findroot2d(psi-psi0, vals, axis = 0 )
        fp = open( fname, "wt" )
        fp.write( "#psi, r, \\theta, R, z, B^r, B^\\theta, B^\\phi, \\eta, rho, u^r, u^\\theta, u^\\phi, \\gamma, \\Omega_F, \\mu, \\sigma, b^2 = B^2-E^2\n" )
        fp.flush()
        os.fsync(fp.fileno())
        np.savetxt( fp, np.array(cvals,dtype=np.float64).transpose(), fmt='%21.15g' )
        fp.close()

    for z0 in (10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 5e10):
        #FIELDLINE: psi = psi0
        fname = "fieldline_nu%0.3g_om%0.3g_z%0.3g.dat" % (nu, om0, z0)
        print( "Doing z0 = %0.3g, fname = %s" % (z0, fname) )
        sys.stdout.flush()
        cvals = findroot2d(z-z0, vals, axis = 1 )
        fp = open( fname, "wt" )
        fp.write( "#psi, r, \\theta, R, z, B^r, B^\\theta, B^\\phi, \\eta, rho, u^r, u^\\theta, u^\\phi, \\gamma, \\Omega_F, \\mu, \\sigma, b^2 = B^2-E^2\n" )
        fp.flush()
        os.fsync(fp.fileno())
        np.savetxt( fp, np.array(cvals,dtype=np.float64).transpose(), fmt='%21.15g' )
        fp.close()

def readlena(fname):
    global cpsi, cr, ch, cR, cz, cBr, cBtheta, cBphi, ceta, crho, cuur, cuutheta, cuuphi, cgamma, comegaf, cmu, csigma, cbsq
    cvals = np.loadtxt( fname, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True )
    cpsi, cr, ch, cR, cz, cBr, cBtheta, cBphi, ceta, crho, cuur, cuutheta, cuuphi, cgamma, comegaf, cmu, csigma, cbsq = cvals    
    return(cvals)

def findroot2d( fin, xin, isleft=True, nbnd = 1, axis = 0, fallback = 0, fallbackval = 0 ):
    """ returns roots, y(x), so that f(x,y(x)) = 0 (here axis = 0)
        (axis selects independent variable)
    """
    if fin.ndim == 3:
        fin = fin[:,:,0]
    if fin.ndim != 2:
        raise( ValueError( "fin.ndim = %d, should be 2" % fin.ndim ) )
    if axis == 1:
        f = fin.transpose()
    else:
        f = fin
    if not isinstance(xin,tuple):
        xtuple = (xin,)
    else:
        xtuple = xin
    xout = ()
    for (j, x) in enumerate(xtuple):
        if x.ndim == 3:
            x = x[:,:,0]
        if x.ndim != 2:
            raise( ValueError( "x[%d].ndim = %d, should be 2" % (j, x.ndim) ) )
        n = f.shape[0]
        if axis == 1:
            x = x.transpose()
        if f.shape != x.shape:
            raise( ValueError( "f and x have different shapes" ) )
        xsol = np.empty((n),dtype=f.dtype)
        for i in np.arange(0,n):
            xsol[i] = findroot1d( f[i], x[i], isleft, nbnd, fallback, fallbackval )
        xout += (xsol,)
    if len(xout) == 1:
        return( xout[0] )
    else:
        return( xout )
        
    
def findroot1d( f, x, isleft=True, nbnd = 1, fallback = 0, fallbackval = 0 ):
    """ find a 1-D root """
    #fallback=1
    if isleft==True:
        ind=0
        dir=1
    else:
        ind=-1
        dir=-1
    if f[ind] > 0:
        coef = 1
    else:
        coef = -1
    #multiplies the final function so f is increasing
    #otherwise scipy gives an error
    if isleft == False:
        interpcoef = coef
    else:
        interpcoef = -coef
    n = x.shape[0]
    ilist = np.arange(0,n)
    indexlist = f*coef<0
    if( not indexlist.any() ):
        if not fallback:
            return( float('nan') )
        else:
            return( fallbackval )
    i0 = ilist[indexlist][ind]
    if f[i0]*f[i0-dir] > 0:
        raise( ValueError("Could not bracket root") )
    ir = i0 + nbnd*dir
    il = i0 - (nbnd+1)*dir
    #limit il, ir to be between 0 and n-1:
    ir = max(0,min(ir,n-1))
    il = max(0,min(il,n-1))
    #order them
    istart = min(il,ir)
    iend = max(il,ir)
    kind = 'linear'
    x2interp = x[istart:iend+1]
    f2interp = interpcoef*f[istart:iend+1]
    #
    if f2interp.shape[0] < 4 or (f2interp[:-1]>=f2interp[1:]).any():
        #too few elements or non-monotonic behavior
        ir = i0 
        il = i0 - dir
        #limit il, ir to be between 0 and n-1:
        ir = max(0,min(ir,n-1))
        il = max(0,min(il,n-1))
        #order them
        istart = min(il,ir)
        iend = max(il,ir)
        kind = 'linear'
        x2interp = x[istart:iend+1]
        f2interp = interpcoef*f[istart:iend+1]
    #
    if f2interp.shape[0]==1:
        #too few elements
        kind='nearest'
        raise( "Too few entries" )
        xinterp = interp1d( f2interp, x2interp, kind=kind, copy = False )
    else:
        xinterp = interp1d( f2interp, x2interp, kind=kind, copy = False )
    ans = xinterp(0.0)
    #if ans < min(x[i0],x[i0-dir]) or ans > max(x[i0],x[i0-dir]):
    #    raise( ValueError("ans = %g out of bounds, (%g,%g)" % (ans,x[i0-dir],x[i0])) )
    return( ans )


def getdefaulttimes():
    #
    (defaultfti,defaultftf)=getdefaulttimes1()
    #(defaultfti,defaultftf)=getdefaulttimes2()
    #(defaultfti,defaultftf)=getdefaulttimes3()
    #
    #
    # GODMARK: For testing to see what initial conditions look like -- use 3 fieldline files at least.
    #defaultfti=0.0
    #defaultftf=10.0
    #
    #
    return defaultfti,defaultftf


# get averaging times if know the model type
# defaultfti and defaultftf: averaging for tables and frame averages
# default2fti and default2ftf: averaging for 
def getdefaulttimes1():
    #
    #defaultftf=1e6
    # not sure how thickdisk5 went further than 13000
    if modelname=="thickdisk7":
        defaultfti=8000
        defaultftf=17000 # because field flips later and becomes very different
    elif modelname=="thickdisk8":
        defaultfti=8000
        #defaultftf=11000
        defaultftf=1e6
    elif modelname=="thickdisk11":
        defaultfti=8000
        defaultftf=12000
        #defaultftf=1e6
    elif modelname=="thickdisk12":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdisk13":
        defaultfti=9000
        defaultftf=1e6
    elif modelname=="run.like8":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdiskrr2":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="run.liker2butbeta40":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="run.liker2":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdisk16":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdisk5":
        defaultfti=8000
        defaultftf=13000
    elif modelname=="thickdisk14":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdiskr1":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="run.liker1":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdiskr2":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdisk9":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="thickdiskr3":
        defaultfti=30000
        defaultftf=1e6
    elif modelname=="thickdisk17":
        defaultfti=40000
        defaultftf=1e6
    elif modelname=="thickdisk10":
        defaultfti=30000
        defaultftf=1e6
    elif modelname=="thickdisk15":
        defaultfti=35000
        defaultftf=1e6
    elif modelname=="thickdiskr15":
        defaultfti=80000
        defaultftf=1e6
    elif modelname=="thickdisk2":
        defaultfti=35000 # not good enough, and avoiding this run
        defaultftf=1e6
    elif modelname=="thickdisk3":
        defaultfti=35000
        defaultftf=1e6
    elif modelname=="thickdiskhr3": # probably want to be same as for "thickdisk3"
        defaultfti=35000
        defaultftf=1e6
    elif modelname=="runlocaldipole3dfiducial":
        # limited over range for disk turbulence to have not decayed much, but sufficiently long so see phibh/phia\sim 1
        defaultfti=2000
        defaultftf=3000
    elif modelname=="blandford3d_new":
        defaultfti=1500
        defaultftf=1e6
    elif modelname=="sasham9":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasham9full2pi":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasham5":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha0":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha1":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha2":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha5":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha9b25":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha9b50":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha9b100":
        defaultfti=8000
        defaultftf=1e6
    elif modelname=="sasha9b200":
        defaultfti=16000
        defaultftf=1e6
    elif modelname=="sasha99":
        defaultfti=8000
        defaultftf=1e6
    else:
        defaultfti=1000
        defaultftf=1e6
    #
    return defaultfti,defaultftf

# get averaging times if know the model type
# averaging for some plots where want to show during period of uniform flux in disk rather than when field has been removed mostly
def getdefaulttimes2():
    #
    (defaultfti,defaultftf)=getdefaulttimes1()
    #
    # now correct only for field flip models
    if modelname=="thickdisk7":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk8":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk11":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk12":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk13":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="run.like8":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdiskrr2":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="run.liker2butbeta40":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="run.liker2":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk16":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk5":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdisk14":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdiskr1":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="run.liker1":
        defaultfti=9000
        defaultftf=12000
    elif modelname=="thickdiskr2":
        defaultfti=9000
        defaultftf=12000
    #
    return defaultfti,defaultftf

# get averaging times if know the model type
# averaging for some plots where want to show during period of uniform flux in disk rather than when field has been removed mostly
def getdefaulttimes3():
    #
    (defaultfti,defaultftf)=getdefaulttimes1()
    #
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    lastfieldlinefile=flist[-1]
    rfdheaderonly(lastfieldlinefile)
    truetf=t
    print("truetf=%g" % (truetf))
    #
    defaultfti=truetf*0.7

    #
    return defaultfti,defaultftf




# get qty t,r(h,m) data and related calculations
def getbasicqtystuff(whichplot=None):
    rhor=1+(1-a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    #
    defaultfti,defaultftf=getdefaulttimes()
    #
    qtymem=getqtyvstime(ihor)
    #
    # assume original default's were used for average range, so plotqty computations should be computed using that same range, not some odd avg_ts/te markers
    fti = defaultfti
    ftf = defaultftf
    if 1==0:
        if avg_ts[0] != 0:
            fti = avg_ts[0]
        if avg_te[0] != 0:
            ftf = avg_te[0]
        #
    #
    print( "getbasicqtystuff: Using: ti = %g, tf = %g" % (fti,ftf) ) ; sys.stdout.flush()
    if whichplot==-1:
        md, ftot, fsqtot, f30, fsq30, pjemtot  = plotqtyvstime(qtymem,fullresultsoutput=0,whichplot=whichplot,fti=fti,ftf=ftf)
        return(md, ftot, fsqtot, f30, fsq30, pjemtot)
    else:
        hoverr_jet_vsr = plotqtyvstime(qtymem,fullresultsoutput=0,whichplot=whichplot,fti=fti,ftf=ftf)
        return(hoverr_jet_vsr)
    #




def plot2davg(dosq=True,whichplot=-1):
    global eout1, eout2, eout, avg_aphi,avg_aphi2,powjetwind,powjet,jminjet,jmaxjet,jminwind,jmaxwind,mymu,maxaphibh
    #use ratio of averages since more stable definition:
    #
    md, ftot, fsqtot, f30, fsq30, pjemtot = getbasicqtystuff(whichplot=-1)
    #
    etad = np.zeros_like(uu)
    etad[0] = -1/(-gn3[0,0])**0.5
    avg_mu = -avg_Tud[1,0] / avg_rhouu[1]
    avg_bsqo2rho = avg_bsqorho*0.5
    avg_unb = avg_TudMA[1,0] / avg_rhouu[1]
    #sum away from theta = 0
    muminwind= 1. #1./(1.-0.1**2)**0.5
    muminjet=2.0
    unbcutoff=0 #1./(1.-0.1**2)**0.5-1
    #
    #
    avg_aphi = scaletofullwedge(nz*_dx3*fieldcalc(gdetB1=avg_gdetB[0]))
    avg_aphi2 = scaletofullwedge((nz*avg_psisq)**0.5)
    #aphi1 = scaletofullwedge(_dx3*_dx2*(avg_gdetB[0]).cumsum(1))
    #aphi2 = scaletofullwedge(-_dx3*_dx2*(avg_gdetB[0])[:,::-1].cumsum(1)[:,::-1])
    aphi = avg_aphi if dosq==True else avg_aphi
    aphi1 = aphi
    aphi2 = aphi
    maxaphibh = np.max(aphi[ihor])
    mdotden    = scaletofullwedge(nz*(-gdet*avg_rhouu[1]*_dx2*_dx3).sum(axis=2))
    mdottot       = mdotden.sum(-1)
    #
    eout1den   = scaletofullwedge(nz*(-gdet*avg_Tud[1,0]*_dx2*_dx3).sum(axis=2))
    eout1denEM = scaletofullwedge(nz*(-gdet*avg_TudEM[1,0]*_dx2*_dx3).sum(axis=2))
    eout1denMA = scaletofullwedge(nz*(-gdet*avg_TudMA[1,0]*_dx2*_dx3).sum(axis=2))
    #subtract off rest-energy flux
    eout1denKE = scaletofullwedge(nz*(gdet*(-avg_TudMA[1,0]-avg_rhouu[1])*_dx2*_dx3).sum(axis=2))
    #eout1den=eout1denEM+eout1denMA
    #eout1   = eout1den.cumsum(axis=1)
    eoutEM1 = eout1denEM.cumsum(axis=1)
    eoutEMtot = eout1denEM.sum(axis=1)[ihor]
    eoutMA1 = eout1denMA.cumsum(axis=1)
    eoutKE1 = eout1denKE.cumsum(axis=1)
    eout1 = eoutEM1+eoutMA1
    eouttot = eout1den.sum(axis=-1)
    #sum from from theta = pi
    eout2den   = scaletofullwedge(nz*(-gdet*avg_Tud[1,0]*_dx2*_dx3)[:,::-1].sum(axis=2))
    eout2denEM = scaletofullwedge(nz*(-gdet*avg_TudEM[1,0]*_dx2*_dx3)[:,::-1].sum(axis=2))
    eout2denMA = scaletofullwedge(nz*(-gdet*avg_TudMA[1,0]*_dx2*_dx3)[:,::-1].sum(axis=2))
    eout2denKE = scaletofullwedge(nz*(gdet*(-avg_TudMA[1,0]-avg_rhouu[1])*_dx2*_dx3).sum(axis=2))
    #eout2den=eout2denEM+eout2denMA
    #eout2   = eout2den.cumsum(axis=1)[:,::-1]
    eoutEM2 = eout2denEM.cumsum(axis=1)[:,::-1]
    eoutMA2 = eout2denMA.cumsum(axis=1)[:,::-1]
    eoutKE2 = eout2denKE.cumsum(axis=1)[:,::-1]
    eout2 = eoutEM2+eoutMA2
    eout = np.zeros_like(eout1)
    eout[tj[:,:,0]>ny/2] = eout2[tj[:,:,0]>ny/2]
    eout[tj[:,:,0]<=ny/2] = eout1[tj[:,:,0]<=ny/2]
    eoutden = np.zeros_like(eout1den)
    eoutden[tj[:,:,0]>ny/2] = eout2den[tj[:,:,0]>ny/2]
    eoutden[tj[:,:,0]<=ny/2] = eout1den[tj[:,:,0]<=ny/2]
    eoutdenEM = np.zeros_like(eout1denEM)
    eoutdenEM[tj[:,:,0]>ny/2] = eout2denEM[tj[:,:,0]>ny/2]
    eoutdenEM[tj[:,:,0]<=ny/2] = eout1denEM[tj[:,:,0]<=ny/2]
    aphip1 = np.zeros((aphi.shape[0],aphi.shape[1]+1,aphi.shape[2]))    
    aphip1[:,0:ny] = aphi
    daphi = np.zeros_like(ti)
    daphi[:,0:ny]=aphip1[:,1:ny+1]-aphip1[:,0:ny]
    mdot = scaletofullwedge(nz*(gdet*avg_rhouu[1]*_dx2*_dx3)).sum(-1).sum(-1)
    #
    mymu = np.copy(avg_mu)
    mymu[(tj[:,:,0] > ny-10)+(tj[:,:,0] < 10)]=50
    mymu[mymu<1]=50
    #
    #tot
    if False:
        #keep same sign in jet
        hjet1aphia = findroot2d( (aphi1[:,:,0]-maxaphibh)*daphi[:,:,0], h, isleft=True, fallback = 1, fallbackval = np.pi/2 )
        hjet2aphia = findroot2d( (aphi2[:,:,0]-maxaphibh)*daphi[:,:,0], h, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    else:
        #allow different signs in jet
        hjet1aphia = findroot2d( (aphi1[:,:,0]-1*maxaphibh), h, isleft=True, fallback = 1, fallbackval = np.pi/2 )
        hjet2aphia = findroot2d( (aphi2[:,:,0]-1*maxaphibh), h, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    #hjet1aphia*=3
    #hjet2aphia=np.pi-(np.pi-hjet2aphia)*3
    hjet1aphi = np.copy(hjet1aphia)
    hjet2aphi = np.copy(hjet2aphia)
    if False:
        rx=1
        hjet1aphi[r[:,0,0]>rx] = findroot2d( -mymu[:,:,0]+muminjet, h, isleft=True, fallback = 1, fallbackval = np.pi/2  )[r[:,0,0]>rx]
        hjet2aphi[r[:,0,0]>rx] = findroot2d( -mymu[:,:,0]+muminjet, h, isleft=False, fallback = 1, fallbackval = np.pi/2  )[r[:,0,0]>rx]
        hjet1aphi = amin(hjet1aphi,hjet1aphia)
        hjet2aphi = amax(hjet2aphi,hjet2aphia)
        hwind1aphi = findroot2d( -mymu[:,:,0]+muminwind, h, isleft=True, fallback = 1, fallbackval = np.pi/2  )
        hwind2aphi = findroot2d( -mymu[:,:,0]+muminwind, h, isleft=False, fallback = 1, fallbackval = np.pi/2  )
    else:
        hwind1aphi = findroot2d( -avg_uu[1,:,0:ny/2,0], h[:,0:ny/2], isleft=False, fallback = 1, fallbackval = np.pi/2  )
        hwind2aphi = findroot2d( -avg_uu[1,:,ny/2:ny,0], h[:,ny/2:ny], isleft=True, fallback = 1, fallbackval = np.pi/2  )
    ################
    #WIND
    ################
    #
    powwind1 = findroot2d( h[:,:,0] - hwind1aphi[:,None], eout1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powwind2 = findroot2d( h[:,:,0] - hwind2aphi[:,None], eout2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powwind = powwind1+powwind2
    powwindEM1 = findroot2d( h[:,:,0] - hwind1aphi[:,None], eoutEM1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powwindEM2 = findroot2d( h[:,:,0] - hwind2aphi[:,None], eoutEM2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powwindEM = powwindEM1+powwindEM2
    powwindMA1 = findroot2d( h[:,:,0] - hwind1aphi[:,None], eoutMA1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powwindMA2 = findroot2d( h[:,:,0] - hwind2aphi[:,None], eoutMA2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powwindMA = powwindMA1+powwindMA2
    powwindEMKE1 = findroot2d( h[:,:,0] - hwind1aphi[:,None], eoutEM1+eoutKE1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powwindEMKE2 = findroot2d( h[:,:,0] - hwind2aphi[:,None], eoutEM2+eoutKE2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powwindEMKE = powwindEMKE1+powwindEMKE2
    powtot1 = eout1[:,ny/2-1]
    powtot2 = eout2[:,ny/2]
    powtot = powtot1 + powtot2
    powtotEM1 = eoutEM1[:,ny/2-1]
    powtotEM2 = eoutEM2[:,ny/2]
    powtotEM = powtotEM1 + powtotEM2
    powtotMA1 = eoutMA1[:,ny/2-1]
    powtotMA2 = eoutMA2[:,ny/2]
    powtotMA = powtotMA1 + powtotMA2
    #
    ################
    # JET
    ################
    #
    #Tot
    #
    powjet1 = findroot2d( h[:,:,0] - hjet1aphi[:,None], eout1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjet2 = findroot2d( h[:,:,0] - hjet2aphi[:,None], eout2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjet = powjet1+powjet2
    #
    #EM
    #
    powjetEM1 = findroot2d( h[:,:,0] - hjet1aphi[:,None], eoutEM1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjetEM2 = findroot2d( h[:,:,0] - hjet2aphi[:,None], eoutEM2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjetEM = powjetEM1+powjetEM2
    #
    #KE
    #
    powjetKE1 = findroot2d( h[:,:,0] - hjet1aphi[:,None], eoutKE1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjetKE2 = findroot2d( h[:,:,0] - hjet2aphi[:,None], eoutKE2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjetKE = powjetKE1+powjetKE2
    powjetEMKE1 = findroot2d( h[:,:,0] - hjet1aphi[:,None], eoutEM1+eoutKE1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjetEMKE2 = findroot2d( h[:,:,0] - hjet2aphi[:,None], eoutEM2+eoutKE2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjetEMKE = powjetEMKE1+powjetEMKE2
    #
    #MA
    #
    powjetMA1 = findroot2d( h[:,:,0] - hjet1aphi[:,None], eoutMA1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjetMA2 = findroot2d( h[:,:,0] - hjet2aphi[:,None], eoutMA2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjetMA = powjetMA1+powjetMA2
    #
    #################
    #
    # powjetEM1aphi = findroot2d( aphi1[:,:,0]-maxaphibh, eoutEM1, isleft=True )
    # powjetEM2aphi = findroot2d( aphi2[:,:,0]-maxaphibh, eoutEM2, isleft=False )
    # powjetEM1 = powjetEM1aphi
    # powjetEM2 = powjetEM2aphi
    # powjetEM = powjetEM1+powjetEM2
    #
    #powjetwind1a = findroot2d( (-avg_unb[:,:,0]-(1.0+unbcutoff))*(avg_uu[1,:,:,0]), eout1, isleft=True )
    #powjetwind2a = findroot2d( (-avg_unb[:,:,0]-(1.0+unbcutoff))*(avg_uu[1,:,:,0]), eout2, isleft=False )
    hjetwind1a = findroot2d( (-avg_unb[:,:,0]-(1.0+unbcutoff)), h, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    hjetwind2a = findroot2d( (-avg_unb[:,:,0]-(1.0+unbcutoff)), h, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    hjetwind1b = findroot2d( daphi[:,:,0], h, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    hjetwind2b = findroot2d( daphi[:,:,0], h, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    #limit jet+wind power to be no smaller than jet power
    if False:
        hjetwind1 = amin(hjetwind1b, hjetwind1a) #amax(powjet1,powjetwind1a)
        hjetwind2 = amax(hjetwind2b, hjetwind2a) #amax(powjet2,powjetwind2a)
    else:
        hjetwind1 = hjetwind1a
        hjetwind2 = hjetwind2a
    powjetwind1 = findroot2d( h-hjetwind1[:,None,None], eout1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjetwind2 = findroot2d( h-hjetwind2[:,None,None], eout2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjetwind = powjetwind1 + powjetwind2
    powjetwindEMKE1 = findroot2d( h-hjetwind1[:,None,None], eoutEM1+eoutKE1, isleft=True, fallback = 1, fallbackval = np.pi/2 )
    powjetwindEMKE2 = findroot2d( h-hjetwind2[:,None,None], eoutEM2+eoutKE2, isleft=False, fallback = 1, fallbackval = np.pi/2 )
    powjetwindEMKE = powjetwindEMKE1 + powjetwindEMKE2
    #
    #Write out power
    #
    rprintout = 100.
    powjetatr = powjetEMKE[iofr(rprintout)]
    powjetwindatr = powjetwindEMKE[iofr(rprintout)]
    powwindatr = powwindEMKE[iofr(rprintout)]
    print( "r = %g: Mdot = %g, etajet = %g, Pjet = %g, etawind = %g, Pwind = %g, Ftot = %g, Fsqtot = %g, pjemtot = %g, eoutEMtot = %g" % ( rprintout, md, powjetatr/md, powjetatr, powjetwindatr/md, powjetwindatr, ftot, fsqtot, pjemtot, eoutEMtot ) )
    foutpower = open( "pjet_2davg_%s.txt" %  os.path.basename(os.getcwd()), "w" )
    # radius of jet power measurement
    rjetin=10.
    if modelname=="blandford3d_new":
        rjetout=30.
    else:
        rjetout=50.
    #
    rjet=rjetout
    #
    printjetwindpower(filehandle = foutpower, r = rjet, stage = 0, powjet = powjet, powwind = powwind, muminjet = muminjet, muminwind = muminwind, md=md, powjetEMKE=powjetEMKE, powjetwindEMKE=powjetwindEMKE, 
                      ftot=ftot, fsqtot=fsqtot, f30=f30, fsq30=fsq30, pjemtot=pjemtot, eoutEMtot=eoutEMtot)
    printjetwindpower(filehandle = foutpower, r = 200., stage = 1, powjet = powjet, powwind = powwind, muminjet = muminjet, muminwind = muminwind, md=md, powjetEMKE=powjetEMKE, powjetwindEMKE=powjetwindEMKE)
    printjetwindpower(filehandle = foutpower, r = 400., stage = 2, powjet = powjet, powwind = powwind, muminjet = muminjet, muminwind = muminwind, md=md, powjetEMKE=powjetEMKE, powjetwindEMKE=powjetwindEMKE)
    foutpower.close()
    #HHH
    if whichplot==1:
        #Plot jet, wind, disk powers vs. r
        plt.figure(1)
        plt.clf()
        rhor=1+(1-a**2)**0.5
        r1d=r[:,0,0]
        plt.plot(r1d, powjet, 'b', lw=3,label=r"$P_{\rm j,tot}$")
        plt.plot(r1d, powjetEM, 'b', lw=1,label=r"$P_{\rm j,EM}$")
        plt.plot(r1d, powjetMA, 'b--',lw=1,label=r"$P_{\rm j,MA}$")
        cond=(r1d>5)
        plt.plot(r1d[cond], (powwind-powjet)[cond], 'g', lw=3, label=r"$P_{\rm w,tot}$")
        plt.plot(r1d[cond], (powwindEM-powjetEM)[cond], 'g', lw=1, label=r"$P_{\rm w,EM}$")
        plt.plot(r1d[cond], (powwindMA-powjetMA)[cond], 'g--',lw=1, label=r"$P_{\rm w,MA}$")
        plt.plot(r1d[cond], (powtot-powwind)[cond], 'c', lw=3, label=r"$P_{\rm d,tot}$")
        plt.plot(r1d[cond], (powtotEM-powwindEM)[cond], 'c', lw=1, label=r"$P_{\rm d,EM}$")
        plt.plot(r1d[cond], (powtotMA-powwindMA)[cond], 'c--',lw=1, label=r"$P_{\rm d,MA}$")
        plt.plot(r1d, (powtot-powjet), 'm', lw=3, label=r"$P_{\rm d+w,tot}$")
        plt.plot(r1d, (powtotEM-powjetEM), 'm', lw=1, label=r"$P_{\rm d+w,EM}$")
        plt.plot(r1d, (powtotMA-powjetMA), 'm--',lw=1, label=r"$P_{\rm d+w,MA}$")
        plt.plot(r1d, powtot, 'r', lw=3, label=r"$P_{\rm tot}$")
        plt.plot(r1d, powtotEM, 'r', lw=1, label=r"$P_{\rm tot,EM}$")
        plt.plot(r1d, powtotMA, 'r--',lw=1, label=r"$P_{\rm tot,MA}$")
        plt.plot(r1d, mdot, 'y',lw=3, label=r"$\dot M$")
        plt.legend(ncol=6)
        #plt.plot(r1d, powwind-powjet, label=r"$P_{\rm j,tot}$")
        plt.xlim(rhor,35)
        plt.ylim(-20,30)
        plt.xlabel(r"$r\ [r_g]$",fontsize=16)
        plt.ylabel("Fluxes",fontsize=16)
        plt.grid()
        #
        plt.figure(2)
        plt.clf()
        #plco(aphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),colors='k',nc=30)
        #plc(daphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='r')
        d=500
        plt.xlim(0,d/2.); plt.ylim(-d,d)
        plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hjet1aphi[:,None,None],levels=(0,),colors='m',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hjet2aphi[:,None,None],levels=(0,),colors='m',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hwind1aphi[:,None,None],levels=(0,),colors='c',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hwind2aphi[:,None,None],levels=(0,),colors='c',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(avg_uu[1,:,:,0],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        #plc(h-hjetwind1[:,None,None],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        #plc(h-hjetwind2[:,None,None],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
     #
    if whichplot==-1:
        #PLOT EVERYTHING
        ##################
        #
        # FIGURE 1
        #
        ##################
        plt.figure(1)
        plt.clf()
        #plco( np.log10(avg_rho), cb=True )
        #plco(choplo(chophi(avg_mu,40),2),cb=True,nc=39)
        plco(avg_mu,levels=np.concatenate(((1.01,),np.arange(2,120,1.))),cb=True)
        #plc(avg_aphi,nc=30,cmap=cm.bone)
        #plc(avg_gamma,levels=np.arange(1.,3.4,0.1),cb=True)
        #
        #plt.clf()
        r1 = 250
        r2 = 1000
        ############
        #
        # FIG 2
        #
        ############
        plt.figure(2)
        plt.clf()
        gs3 = GridSpec(3, 3)
        #gs3.update(left=0.05, right=0.95, top=0.30, bottom=0.03, wspace=0.01, hspace=0.04)
        #mdot
        ax31 = plt.subplot(gs3[-3,:])
        #ymax=ax31.get_ylim()[1]
        #ymax=2*(np.floor(np.floor(ymax+1.5)/2))
        #ax31.set_yticks((ymax/2.0,ymax))
        i=iofr(r1)
        plt.plot( aphi[i,:,0]/maxaphibh, eout[i,:],'g-' )
        i=iofr(r2)
        plt.plot( aphi[i,:,0]/maxaphibh, eout[i,:],'b-' )
        plt.xlim( 0, 2 )
        plt.ylim( 0, 20 )
        plt.ylabel(r"$P_{\rm j,enc}(\Psi)$")
        ax31.grid(True)
        ax32 = plt.subplot(gs3[-2,:])
        i=iofr(r1)
        print i
        plt.plot( aphi[i,:,0]/maxaphibh, avg_mu[i,:],'g-' )
        plt.plot( aphi[i,:,0]/maxaphibh, avg_gamma[i,:]*(avg_bsqorho[i,:]+1),'g--' )
        i=iofr(r2)
        plt.plot( aphi[i,:,0]/maxaphibh, avg_mu[i,:], 'b-' )
        #somehow don't show up on plot; maybe make use of avg_bsquuud, etc.
        plt.plot( aphi[i,:,0]/maxaphibh, avg_ud[0,i,:]*((gam*avg_ug/avg_rho+avg_bsqorho)[i,:]+1),'b--' )
        plt.plot( aphi[i,:,0]/maxaphibh, avg_ud[0,i,:]*(-avg_sigma[i,:]+1),'b-.' )
        plt.xlim( 0, 2 )
        plt.ylim( 0, 10 )
        plt.ylabel(r"$\mu(\Psi)$")
        ax32.grid(True)
        ax33 = plt.subplot(gs3[-1,:])
        myunb = np.copy(avg_unb)
        myunb[-myunb<=1.+unbcutoff]=myunb[-myunb<=1.0+unbcutoff]*0
        i=iofr(r1)
        #plt.plot( aphi[i,:,0]/maxaphibh, avg_B[0,i,:]/(avg_rhouu[1,i]),'g-' )
        plt.plot( aphi[i,:,0]/maxaphibh, -myunb[i,:],'g-' )
        plt.plot( aphi[i,:,0]/maxaphibh, (avg_uu[1]*dxdxp[1,1])[i,:],'g--' )
        i=iofr(r2)
        #plt.plot( aphi[i,:,0]/maxaphibh, avg_B[0,i,:]/(avg_rhouu[1,i]),'b-' )
        plt.plot( aphi[i,:,0]/maxaphibh, -myunb[i,:],'b-' )
        plt.plot( aphi[i,:,0]/maxaphibh, (avg_uu[1]*dxdxp[1,1])[i,:],'b--' )
        plt.xlim( 0, 2 )
        plt.ylim( -0.5,2)
        plt.ylabel(r"$(1+u/\rho) u_t$")
        ax33.grid(True)
        #print maxaphibh
        #FIG 3
        plt.figure(3)
        plt.clf()
        i=iofr(r1)
        plt.plot( aphi[i,:]/maxaphibh, 'g' )
        plt.plot( aphi[i,:]/maxaphibh, 'gx' )
        i=iofr(r2)
        plt.plot( aphi[i,:]/maxaphibh, 'b' )
        plt.plot( aphi[i,:]/maxaphibh, 'bx' )
        plt.grid()
        ##############
        #
        #  FIGURE 5
        #
        ##############
        plt.figure(5)
        plt.clf()
        plt.plot(r[:,0,0],powjet,'m:',label=r'$P_{jet,EM+MA}$')
        #plt.plot(r[:,0,0],mdottot,'r')
        #plt.plot(r[:,0,0],powjet,'bx')
        plt.ylim(0,20)
        plt.xlim(rhor,30)
        #plt.plot(findroot2d(aphix[:,:,0]-maxaphibh,eout)+findroot2d(aphix[:,:,0]-maxaphibh,eout,isleft=False),'y--')
        #plt.plot(powxjet,'b--')
        #plt.plot(r[:,0,0],powxjetEM,'b--')
        #plt.plot(r[:,0,0],powxjetwind,'g')
        plt.plot(r[:,0,0],eouttot,'r',label=r'$P_{tot}$')
        plt.plot(r[:,0,0],powjetEM,'m-.',label=r'$P_{jet,EM}$')
        plt.plot(r[:,0,0],powjetKE,'m--',label=r'$P_{jet,KE}$')
        plt.plot(r[:,0,0],powjetEMKE,'m',label=r'$P_{jet,EMKE}$')
        #xxx
        #plt.plot(r[iofr(16):,0,0],powjetwind[iofr(16):],'g',label=r'$P_{unbound}(-u_t(1+\Gamma u_g/\rho)>1)$')
        #plt.plot(r[iofr(rjet):,0,0],powwind[iofr(rjet):],'c',label=r'$P_{jetwind}(\mu>1.005)$')
        plt.plot(r[iofr(10):,0,0],powjetwindEMKE[iofr(10):],'c--',label=r'$P_{jetwindEMKE}$')
        plt.legend(loc='upper right',ncol=3)
        plt.ylabel(r'Energy fluxes in jet region, $\mu>2$')
        plt.xlabel(r'$r$')
        #plt.plot(r[:,0,0],powjetEM+powjetMA,'k')
        plt.grid()
        plt.figure(8)
        plt.clf()
        plt.plot(r[:,0,0],hjet1aphi,'k')
        plt.plot(r[:,0,0],h[:,ny/4,0],'g')
        plt.plot(r[:,0,0],np.pi-hjet2aphi,'k:')
        plt.xlim(0,1500)
        #xxx
        ##############
        #
        #  FIGURE 6
        #
        ##############
        #
        plt.figure(6)
        plco(aphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),colors='k',nc=30)
        #plc(daphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='r')
        d=500
        plt.xlim(0,d/2.); plt.ylim(-d,d)
        plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hjet1aphi[:,None,None],levels=(0,),colors='m',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hjet2aphi[:,None,None],levels=(0,),colors='m',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hwind1aphi[:,None,None],levels=(0,),colors='c',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hwind2aphi[:,None,None],levels=(0,),colors='c',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hjetwind1[:,None,None],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(h-hjetwind2[:,None,None],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        #plc(chophi(choplo(-avg_unb[:,:,0]-(1.0),0),0.001),xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        #plc(avg_gamma,nc=50,xcoord=r*np.sin(h),ycoord=r*np.cos(h),cb=True)
        #
        #plc(chophi((r/rhor)**0.75*(1-np.abs(np.cos(h))),1),xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        #plc(avg_omegaf2*2*np.pi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),cb=True)
        #plc(avg_uu[1]*dxdxp[1][1],xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,))
        #plc(avg_uu[1]*dxdxp[1][1],xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='g')
        #plc(-avg_unb[:,:,0]-(1.0),levels=(0,0.01,0.1),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        #plc(avg_mu[:,:,0]-(1.0),levels=(0,0.01,0.1),colors='r',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        if False:
            plc(chophi(choplo(-avg_unb[:,:,0]-(1.0),0),0.001),xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            rfd("fieldline0000.bin")
            #plc(np.log10(avg_rho),xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            plc(avg_uu[1],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            #plc(daphi,levels=(0,),colors='r',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            #plc(h-hjet1aphia[:,None,None],levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            plc(h-hjetwind1[:,None,None],levels=(0,),colors='c',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            plc(h-hjetwind2[:,None,None],levels=(0,),colors='y',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            plc(chophi(choplo(-avg_sigma,0.1),10),xcoord=r*np.sin(h),ycoord=r*np.cos(h))
            plc(chophi((r/rhor)**0.75*(1-np.abs(np.cos(h))),1),xcoord=r*np.sin(h),ycoord=r*np.cos(h))
    #xxx
    #plc(h,xcoord=r*np.sin(h),ycoord=r*np.cos(h))
    #plc(lrho,xcoord=r*np.sin(h),ycoord=r*np.cos(h))

def printjetwindpower(filehandle = None, r = None, stage = 0, powjet = 0, powwind = 0, muminjet = 0, muminwind = 0, md = 0, powjetEMKE=0, powjetwindEMKE=0, ftot=0, fsqtot=0, f30=0, fsq30=0, pjemtot=0, eoutEMtot = 0):
    if filehandle == None or r == None:
        raise( ValuseError("filehandle and r have to be specified") )
    #
    #foutpower.write( "#Name a Mdot   Pjet    Etajet  Psitot Psisqtot**0.5 Psijet Psisqjet**0.5 rstag Pjtotmax Pjtot1rstag Pjtot2rstag Pjtot4rstag Pjtot8rstag\n"  )
    #
    i = iofr(r)
    if stage == 0:
        #initial stage
        filehandle.write( "%s %f %f %f %f %f %f %f %f %f %f %f %f" % (os.path.basename(os.getcwd()), a, avg_ts[0], avg_te[0], muminjet, muminwind, md, ftot, fsqtot, f30, fsq30, pjemtot, eoutEMtot) )
    if stage == 0 or stage == 1:
        #intermediate stage
        filehandle.write( " %f %f %f %f %f" % (powjetEMKE[i], powjetwindEMKE[i], powjet[i], powwind[i], r) )
    if stage == 2:
        #final stage
        filehandle.write( " %f %f %f %f %f\n" % (powjetEMKE[i], powjetwindEMKE[i], powjet[i], powwind[i], r) )
    #flush to disk just in case to make sure all is written
    filehandle.flush()
    os.fsync(filehandle.fileno())

# MRI stability:
# v_a^2 > (-1/k^2)*d(Omega^2)/dlnR ~ (-H^2/\pi^2)*(d\Omega^2)/(dlnR)
#
# so if v_\phi = R\Omega \propto R^-a then \Omega = \Omega_0 (R/r0)^{-a-1}
# so Omega^2 = \Omega_0^2 (R/R0)^{-2a-2}
# so d\Omega^2/(dlnR) = -2*(1+a)\Omega^2
# then:
# v_a^2 > (2H^2/\pi^2)*(1+a)\Omega^2
#
# lambdamri-actual from BH98 113:
# \kappa^2 = (1/R^3) d(R^4\Omega^2)/dR = 2*(1-a)
# (k.ua)^2_{\rm max} = -(1/4 + \kappa^2/(16\Omega^2) d\Omega^2/(dlnR)
# -> lambdaz = 4\pi vaz/(\Omega0*\sqrt{(3-a)*(1+a)}) so is weakly dependent upon a=1/2 to a=1
# -> lambaaz \approx 2\pi vaz/\Omega0

def compute_resires(hoverrwhich=None):
    mydH = r*dxdxp[2][2]*_dx2
    mydP = r*np.sin(h)*dxdxp[3][3]*_dx3
    #
    
    ################ IF USE OMEGAFIX==1, should use Kep Omega here
    #
    #omega = np.fabs(dxdxp[3][3]*uu[3]/uu[0])+1.0e-15
    # much of thick disk remains sub-Keplerian, so for estimate of Q must force consistency with assumptions of the Qmri measure
    R = r*np.sin(h)
    omega = 1.0/(a + R**(3.0/2.0))
    #
    #####################################
    #
    # don't use 0==1 part anymore (since can't readily compute res2 consistently)
    if 0==1:
        vau2 = np.abs(bu[2])/np.sqrt(rho+bsq+gam*ug)
        lambdamriu2 = 2*np.pi * vau2 / omega
        res=np.fabs(lambdamriu2/_dx2)
        res2=0
    #
    if 1==1:
        va2sq = np.fabs(bu[2]*bd[2]/(rho+bsq+gam*ug))
        lambda2 = 2.0*np.pi * np.sqrt(va2sq) / omega
        # vertical grid cells per MRI wavelength
        res=np.fabs(lambda2/mydH)
        #
        va3sq = np.fabs(bu[3]*bd[3]/(rho+bsq+gam*ug))
        lambda3 = 2.0*np.pi * np.sqrt(va3sq) / omega
        # azimuthal grid cells per MRI wavelength
        res3=np.fabs(lambda3/mydP)
        #
        # MRI wavelengths over the whole disk
        if hoverrwhich is not None:
            #ires2=np.fabs(lambda2)
            ires2=np.fabs(lambda2*divideavoidinf(r*(2.0*hoverrwhich)))
            #sumhoverrwhich=np.sum(hoverrwhich)
            #print("sumhoverrwhich")
            #print(sumhoverrwhich)
            #sumires2=np.sum(ires2)
            #print("sumires2")
            #print(sumires2)
            #ires2=np.fabs(lambda2/(r*(2.0*0.2)))
            ires2[np.fabs(hoverrwhich)<10^(-10)]=0
            ires2[hoverrwhich!=hoverrwhich]=0
            ires2[np.isnan(hoverrwhich)==1]=0
            ires2[np.isinf(hoverrwhich)==1]=0
        else:
            # h/r=1 set, so can use <h/r>_t later so more stable result
            ires2=np.fabs(lambda2*divideavoidinf(r*(2.0*1.0)))
        #
    return(res,res3,ires2)

    
def Qmri_simple(which=1,hoverrwhich=None,weak=None):
    #
    #
    res,res3,ires=compute_resires(hoverrwhich)
    #
    #
    if weak==1:
        denfactor=(rho)**(1.0)
    else:
        denfactor=(rho*bsq)**(0.5)
    #
    # res
    # also weight with rho**2 so divisor on va2sq doesn't drop out.
    # so weight is where both rho and vau2 are large
    tiny=np.finfo(rho.dtype).tiny
    up=(gdet*denfactor*res*which).sum(axis=1)
    dn=(gdet*denfactor*which).sum(axis=1)
    dnmin=np.min(dn)
    if dnmin==0:
        print("Problem with dn for res") ; sys.stdout.flush()
    qmri2d= (up/(dn+tiny))**1.0
    norm3d=np.empty((nx,ny,nz),dtype=rho.dtype)
    qmri3d=np.empty((nx,ny,nz),dtype=rho.dtype)
    for j in np.arange(0,ny):
        qmri3d[:,j] = qmri2d
        norm3d[:,j] = dn
    #
    # res3
    # also weight with rho**2 so divisor on va2sq doesn't drop out.
    # so weight is where both rho and vau2 are large
    tiny=np.finfo(rho.dtype).tiny
    up=(gdet*denfactor*res3*which).sum(axis=1)
    dn=(gdet*denfactor*which).sum(axis=1)
    dnmin=np.min(dn)
    if dnmin==0:
        print("Problem with dn for res3") ; sys.stdout.flush()
    q3mri2d= (up/(dn+tiny))**1.0
    norm33d=np.empty((nx,ny,nz),dtype=rho.dtype)
    q3mri3d=np.empty((nx,ny,nz),dtype=rho.dtype)
    for j in np.arange(0,ny):
        q3mri3d[:,j] = q3mri2d
        norm33d[:,j] = dn
    #
    # ires2
    tiny=np.finfo(rho.dtype).tiny
    up=(gdet*denfactor*ires*which).sum(axis=1)
    dn=(gdet*denfactor*which).sum(axis=1)
    dnmin=np.min(dn)
    if dnmin==0:
        print("Problem with dn for ires") ; sys.stdout.flush()
    iq2mri2d= (up/(dn+tiny))**1.0
    iq2mri3d=np.empty((nx,ny,nz),dtype=rho.dtype)
    for j in np.arange(0,ny):
        iq2mri3d[:,j] = iq2mri2d
    #
    #
    return(qmri3d,norm3d,q3mri3d,norm33d,iq2mri3d)

    
def horcalc(hortype=1,which1=1,which2=1,denfactor=None):
    """
    Compute root mean square deviation of disk body from equatorial plane
    """
    if denfactor is None:
        denfactor=rho
    #
    # determine when have to revert to which2
    which=which1
    testit=which1.sum(axis=1)
    for i in np.arange(0,nx):
        for k in np.arange(0,nz):
            if testit[i,k]==0:
                which[i,:,k]=which2[i,:,k]
    #
    tiny=np.finfo(rho.dtype).tiny
    #
    thetamid3d=np.zeros((nx,ny,nz),dtype=h.dtype)
    if hortype==1:
        up=(gdet*denfactor*(h-np.pi/2)*which).sum(axis=1)
        dn=(gdet*denfactor*which).sum(axis=1)
        thetamid2d=up/(dn+tiny)+np.pi/2.0
        #print("thetamid2d")
        #god=thetamid2d[iofr(100),:]
        #print(god)
        for j in np.arange(0,ny):
            thetamid3d[:,j] = thetamid2d
    else:
        thetamid3d=0.5*np.pi+thetamid3d
    #
    up=(gdet*denfactor*(h-thetamid3d)**2*which).sum(axis=1)
    #up=(gdet*denfactor*(h-1.57)**2*which).sum(axis=1)
    dn=(gdet*denfactor*which).sum(axis=1)
    hoverr2d= (up/(dn+tiny))**0.5
    hoverr3d=np.empty((nx,ny,nz),dtype=h.dtype)
    for j in np.arange(0,ny):
        hoverr3d[:,j] = hoverr2d
    #
    #
    return((hoverr3d,thetamid3d))


def gridcalc(hoverrconst=None,hoverr=None):
    """
    Compute dr:r d\theta : r\sin\theta d\phi along equator vs. radius
    """
    #
    print("h.shape") ; sys.stdout.flush()
    print(h.shape) ; sys.stdout.flush()
    #
    print("hoverr.shape") ; sys.stdout.flush()
    print(hoverr.shape) ; sys.stdout.flush()
    #
    if hoverrconst!=None:
        which=(np.fabs(h-np.pi*0.5)<=hoverrconst)
        print("hoverrconst=%g" % (hoverrconst))
    #
    if hoverr!=None:
        which=(np.fabs(h-np.pi*0.5)<=hoverr)
    #
    print("which.shape") ; sys.stdout.flush()
    print(which.shape) ; sys.stdout.flush()
    #
    norm = (which.sum(axis=1))
    if len(norm.shape)==2:
        norm=norm.sum(axis=1)
    whichalt=(np.fabs(h-np.pi*0.5)<=np.pi*0.5)
    normalt = (whichalt.sum(axis=1))
    if len(normalt.shape)==2:
        normalt=normalt.sum(axis=1)
    #
    norm[norm==0] = normalt[norm==0]
    #
    drup=np.empty((nx,nz),dtype=h.dtype)
    drup = ((dxdxp[1][1]*_dx1*which).sum(axis=1))
    if len(drup.shape)==2:
        drup=drup.sum(axis=1)
    dr = drup/norm
    #
    dHup=np.empty((nx,nz),dtype=h.dtype)
    dHup = ((r*dxdxp[2][2]*_dx2*which).sum(axis=1))
    if len(dHup.shape)==2:
        dHup=dHup.sum(axis=1)
    dH = dHup/norm
    #
    dPup=np.empty((nx,nz),dtype=h.dtype)
    dPup = ((r*np.sin(h)*dxdxp[3][3]*_dx3*which).sum(axis=1))
    if len(dPup.shape)==2:
        dPup=dPup.sum(axis=1)
    dP = dPup/norm
    #
    #print(norm)
    #print(normalt)
    #
    # now have dr,dH,dP vs. r
    #
    # for each radius, write aspect ratio such that smallest thing is 1
    minvalue = np.minimum(np.minimum(dr,dH),dP)
    minvaluealt = dP*0+1
    minvalue[minvalue==0] = minvaluealt[minvalue==0]
    #
    #print(minvalue)
    #
    drnorm = dr/minvalue
    dHnorm = dH/minvalue
    dPnorm = dP/minvalue
    #
    #print( "drnorm50=%g dHnorm50=%g dPnorm50=%g" % (drnorm[50],dHnorm[50],dPnorm[50]) )
    #
    return((dr,dH,dP,drnorm,dHnorm,dPnorm))

#    mdin=intangle(gdet*rho*uu[1],inflowonly=1,maxbsqorho=maxbsqorhonear)


def ravel_index(pos, shape):
    res = 0
    acc = 1
    for pi, si in zip(reversed(pos), reversed(shape)):
        res += pi * acc
        acc *= si
    return res


def betascalc(which=1,rdown=0.0,rup=1.0E3):
    pg=((gam-1)*ug)
    pb=bsq*0.5
    # avoid below since this will set beta=0 if bsq=0 but we want actual minimum beta
    #beta=((gam-1)*ug)*divideavoidinf(bsq*0.5)
    ibeta=pb/pg
    beta=pg/pb
    #
    # don't take max over entire region since for thickdisk models with HyperExp, field is actually large at the equator at very large radii
    condition1=(which)
    condition1=condition1*(r<rup)
    condition1=condition1*(r>rdown)
    #
    rhocond=rho*condition1
    rhomax=np.max(rhocond)
    rhomaxindex=np.unravel_index(rhocond.argmax(), rhocond.shape)
    print("rhomaxindex")
    print(rhomaxindex)
    rrhomax=r[rhomaxindex[0],0,0]
    hrhomax=h[0,rhomaxindex[1],0]
    phrhomax=ph[0,0,rhomaxindex[2]]
    print("rhph rhomax: %g %g %g" % (rrhomax, hrhomax, phrhomax) )
    #
    pgcond=pg*condition1
    pgmax=np.max(pgcond)
    pgmaxindex=np.unravel_index(pgcond.argmax(), pgcond.shape)
    print("pgmaxindex")
    print(pgmaxindex)
    rpgmax=r[pgmaxindex[0],0,0]
    hpgmax=h[0,pgmaxindex[1],0]
    phpgmax=ph[0,0,pgmaxindex[2]]
    print("rhph pgmax: %g %g %g" % (rpgmax, hpgmax, phpgmax) )
    #
    pbcond=pb*condition1
    pbmax=np.max(pbcond)
    pbmaxindex=np.unravel_index(pbcond.argmax(), pbcond.shape)
    print("pbmaxindex")
    print(pbmaxindex)
    rpbmax=r[pbmaxindex[0],0,0]
    hpbmax=h[0,pbmaxindex[1],0]
    phpbmax=ph[0,0,pbmaxindex[2]]
    print("rhph pbmax: %g %g %g" % (rpbmax, hpbmax, phpbmax) )
    #
    #condition2=condition1*(rho>0.25*rhomax)
    #condition2=condition2*(pg>0.25*pgmax)
    condition2=condition1
    #
    ibetaavg=np.average(ibeta,weights=condition2*gdet)
    betaavg=1.0/ibetaavg
    pgavg=np.average(pg,weights=condition2*gdet)
    pbavg=np.average(pb,weights=condition2*gdet)
    #
    # find actual minimum beta
    ibetacond=condition1*ibeta
    ibetamax=np.max(ibetacond)
    ibetamax=np.max(ibetacond)
    ibetamaxindex=np.unravel_index(ibetacond.argmax(), ibetacond.shape)
    print("ibetamaxindex")
    print(ibetamaxindex)
    ribetamax=r[ibetamaxindex[0],0,0]
    hibetamax=h[0,ibetamaxindex[1],0]
    phibetamax=ph[0,0,ibetamaxindex[2]]
    print("rhph ibetamax: %g %g %g" % (ribetamax, hibetamax, phibetamax) )
    #
    betamin=1.0/ibetamax
    #betamin=np.min(beta)
    #betamin=np.min(beta)
    # find ratio of averages
    betaratofavg=pgavg/pbavg
    # ratio of maxes
    betaratofmax=pgmax/pbmax
    #
    #print("betascalc: %g %g %g" % (rhomax, pgmax, pbmax) )
    return betamin,betaavg,betaratofavg,betaratofmax




def luminosities(which=1,rdown=0.0,rup=1.0E3):
    pg=((gam-1)*ug)
    pb=bsq*0.5
    # avoid below since this will set beta=0 if bsq=0 but we want actual minimum beta
    #beta=((gam-1)*ug)*divideavoidinf(bsq*0.5)
    ibeta=pb/pg
    beta=pg/pb
    #
    omegak=1.0/(r**(1.5)+a)
    taucool=2.0*np.pi/omegak
    #
    # dU/dtau = ug/dtau = ug/1 = ug/dt*uu[0]
    # L = dU/dt_infty = (dU/dtau)*(-ud[0])
    # L = ug*(-ud[0])
    #
    #################################################################
    # don't take max over entire region since for thickdisk models with HyperExp, field is actually large at the equator at very large radii
    condition1=(which)
    condition1=condition1*(r<rup)
    condition1=condition1*(r>rdown)
    #
    #################################################################
    den=(ugclean)*condition1 # avoid floor
    lumdenug=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenug=scaletofullwedge(lumdenug)
    lumdenugmax=np.max(lumdenug)
    lumdenugmaxindex=np.unravel_index(lumdenug.argmax(), lumdenug.shape)
    print("lumdenugmaxindex")
    print(lumdenugmaxindex)
    rlumdenug=r[lumdenugmaxindex[0],0,0]
    hlumdenug=h[0,lumdenugmaxindex[1],0]
    phlumdenug=ph[0,0,lumdenugmaxindex[2]]
    print("rhph lumdenug: %g %g %g" % (rlumdenug, hlumdenug, phlumdenug) )
    # actually sum
    lumug=np.sum(lumdenug)
    #
    #################################################################
    den=(bsq*0.5)*condition1
    lumdenbsq=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumbsq=np.sum(lumdenbsq)
    #
    #################################################################
    den=(rho+ug+pg+bsq)*condition1
    lumdenfull=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenfull=scaletofullwedge(lumdenfull)
    lumdenfullmax=np.max(lumdenfull)
    lumdenfullmaxindex=np.unravel_index(lumdenfull.argmax(), lumdenfull.shape)
    print("lumdenfullmaxindex")
    print(lumdenfullmaxindex)
    rlumdenfull=r[lumdenfullmaxindex[0],0,0]
    hlumdenfull=h[0,lumdenfullmaxindex[1],0]
    phlumdenfull=ph[0,0,lumdenfullmaxindex[2]]
    print("rhph lumdenfull: %g %g %g" % (rlumdenfull, hlumdenfull, phlumdenfull) )
    # actually sum
    lumfull=np.sum(lumdenfull)
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    condition1=(which)
    condition1=condition1*(r<30.0)
    condition1=condition1*(r>rdown)
    #
    #################################################################
    den=(ugclean)*condition1 # avoid floor
    lumdenug=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenug=scaletofullwedge(lumdenug)
    lumdenugmax=np.max(lumdenug)
    lumdenugmaxindex=np.unravel_index(lumdenug.argmax(), lumdenug.shape)
    print("lumdenugmaxindex")
    print(lumdenugmaxindex)
    rlumdenug=r[lumdenugmaxindex[0],0,0]
    hlumdenug=h[0,lumdenugmaxindex[1],0]
    phlumdenug=ph[0,0,lumdenugmaxindex[2]]
    print("rhph lumdenug: %g %g %g" % (rlumdenug, hlumdenug, phlumdenug) )
    # actually sum
    lumug2=np.sum(lumdenug)
    #
    #################################################################
    den=(bsq*0.5)*condition1
    lumdenbsq=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumbsq2=np.sum(lumdenbsq)
    #
    #################################################################
    den=(rho+ug+pg+bsq)*condition1
    lumdenfull=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenfull=scaletofullwedge(lumdenfull)
    lumdenfullmax=np.max(lumdenfull)
    lumdenfullmaxindex=np.unravel_index(lumdenfull.argmax(), lumdenfull.shape)
    print("lumdenfullmaxindex")
    print(lumdenfullmaxindex)
    rlumdenfull=r[lumdenfullmaxindex[0],0,0]
    hlumdenfull=h[0,lumdenfullmaxindex[1],0]
    phlumdenfull=ph[0,0,lumdenfullmaxindex[2]]
    print("rhph lumdenfull: %g %g %g" % (rlumdenfull, hlumdenfull, phlumdenfull) )
    # actually sum
    lumfull2=np.sum(lumdenfull)
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    condition1=(which)
    condition1=condition1*(r<rup)
    condition1=condition1*(r>rdown)
    rpho=2.0*(1.0+np.cos(2.0/3.0*(np.arccos(-a))))
    condition1=condition1*(r>rpho)
    #
    rhocond=rho*condition1
    #################################################################
    den=(ugclean)*condition1 # avoid floor
    lumdenug=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenug=scaletofullwedge(lumdenug)
    lumdenugmax=np.max(lumdenug)
    lumdenugmaxindex=np.unravel_index(lumdenug.argmax(), lumdenug.shape)
    print("lumdenugmaxindex")
    print(lumdenugmaxindex)
    rlumdenug=r[lumdenugmaxindex[0],0,0]
    hlumdenug=h[0,lumdenugmaxindex[1],0]
    phlumdenug=ph[0,0,lumdenugmaxindex[2]]
    print("rhph lumdenug: %g %g %g" % (rlumdenug, hlumdenug, phlumdenug) )
    # actually sum
    lumug3=np.sum(lumdenug)
    #
    #################################################################
    den=(bsq*0.5)*condition1
    lumdenbsq=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumbsq3=np.sum(lumdenbsq)
    #
    #################################################################
    den=(rho+ug+pg+bsq)*condition1
    lumdenfull=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenfull=scaletofullwedge(lumdenfull)
    lumdenfullmax=np.max(lumdenfull)
    lumdenfullmaxindex=np.unravel_index(lumdenfull.argmax(), lumdenfull.shape)
    print("lumdenfullmaxindex")
    print(lumdenfullmaxindex)
    rlumdenfull=r[lumdenfullmaxindex[0],0,0]
    hlumdenfull=h[0,lumdenfullmaxindex[1],0]
    phlumdenfull=ph[0,0,lumdenfullmaxindex[2]]
    print("rhph lumdenfull: %g %g %g" % (rlumdenfull, hlumdenfull, phlumdenfull) )
    # actually sum
    lumfull3=np.sum(lumdenfull)
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    condition1=(which)
    condition1=condition1*(r<30.0)
    condition1=condition1*(r>rdown)
    rpho=2.0*(1.0+np.cos(2.0/3.0*(np.arccos(-a))))
    condition1=condition1*(r>rpho)
    #
    rhocond=rho*condition1
    #################################################################
    den=(ugclean)*condition1 # avoid floor
    lumdenug=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenug=scaletofullwedge(lumdenug)
    lumdenugmax=np.max(lumdenug)
    lumdenugmaxindex=np.unravel_index(lumdenug.argmax(), lumdenug.shape)
    print("lumdenugmaxindex")
    print(lumdenugmaxindex)
    rlumdenug=r[lumdenugmaxindex[0],0,0]
    hlumdenug=h[0,lumdenugmaxindex[1],0]
    phlumdenug=ph[0,0,lumdenugmaxindex[2]]
    print("rhph lumdenug: %g %g %g" % (rlumdenug, hlumdenug, phlumdenug) )
    # actually sum
    lumug4=np.sum(lumdenug)
    #
    #################################################################
    den=(bsq*0.5)*condition1
    lumdenbsq=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumbsq4=np.sum(lumdenbsq)
    #
    #################################################################
    den=(rho+ug+pg+bsq)*condition1
    lumdenfull=gdet*den*(-ud[0]/taucool)*_dx1*_dx2*_dx3
    lumdenfull=scaletofullwedge(lumdenfull)
    lumdenfullmax=np.max(lumdenfull)
    lumdenfullmaxindex=np.unravel_index(lumdenfull.argmax(), lumdenfull.shape)
    print("lumdenfullmaxindex")
    print(lumdenfullmaxindex)
    rlumdenfull=r[lumdenfullmaxindex[0],0,0]
    hlumdenfull=h[0,lumdenfullmaxindex[1],0]
    phlumdenfull=ph[0,0,lumdenfullmaxindex[2]]
    print("rhph lumdenfull: %g %g %g" % (rlumdenfull, hlumdenfull, phlumdenfull) )
    # actually sum
    lumfull4=np.sum(lumdenfull)
    #################################################################
    #
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    #################################################################
    condition1=(which)
    condition1=condition1*(r<100.0)
    condition1=condition1*(r>rdown)
    rpho=2.0*(1.0+np.cos(2.0/3.0*(np.arccos(-a))))
    condition1=condition1*(r>rpho)
    #
    #sigmat=1.0E-25
    sigmat=1.0
    #cc=3.0E10
    cc=1.0
    mee=1.0
    mbb=mee*2000.0
    # divide by normal rho to avoid mygam being large in jet
    # assumes Pe=Pi so Te=Ti since ne=nb and P=nkT.  So Pe=Pi=rhob c^2 means huge Ti=Te so very high mygam
    Pe=(gam-1.0)*ugclean
    mygam=(3.0*mbb*Pe + cc**2*mee*rhoclean)/(cc**2*mee*rho)
    ####### thermal e
    neden=rhoclean/mbb
    denrate=(neden*(4.0/3.0)*sigmat*cc*(mygam**2-1.0)*(bsq*0.5))*condition1
    lumdenbsq=gdet*denrate*(-ud[0])*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    print("lumdenbsqmax")
    print(lumdenbsqmax)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumsynch=np.sum(lumdenbsq)
    #
    ####### non-thermal e with ne\propto uth
    # thermal Pe shows no QPO
    Pe=(bsq/2.0)
    mygam=(3.0*mbb*Pe + cc**2*mee*rhoclean)/(cc**2*mee*rho)
    neden=ug/(mee*cc**2)
    denrate=(neden*(4.0/3.0)*sigmat*cc*(mygam**2-1.0)*(bsq*0.5))*condition1
    lumdenbsq=gdet*denrate*(-ud[0])*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    print("lumdenbsqmax")
    print(lumdenbsqmax)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumsynchnon1=np.sum(lumdenbsq)
    #
    ####### non-thermal e with ne\propto uem
    # thermal Pe shows no QPO
    Pe=(bsq/2.0)
    mygam=(3.0*mbb*Pe + cc**2*mee*rhoclean)/(cc**2*mee*rho)
    neden=(bsq*0.5)/(mee*cc**2)
    denrate=(neden*(4.0/3.0)*sigmat*cc*(mygam**2-1.0)*(bsq*0.5))*condition1
    lumdenbsq=gdet*denrate*(-ud[0])*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    print("lumdenbsqmax")
    print(lumdenbsqmax)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumsynchnon2=np.sum(lumdenbsq)
    #
    ####### non-thermal e with ne\propto uem
    # bsq Pe shows no QPO
    Pe=(bsq/2.0)
    # make mygam=bsq/rho in high bsq/rho limit so jet contributes most
    mygam=(Pe + rhoclean)/(rho)
    mygam[mygam<1.0]=1.0
    neden=(bsq*0.5)
    denrate=(neden*(4.0/3.0)*sigmat*cc*(mygam**2-1.0)*(bsq*0.5))*condition1
    lumdenbsq=gdet*denrate*(-ud[0])*_dx1*_dx2*_dx3
    lumdenbsq=scaletofullwedge(lumdenbsq)
    lumdenbsqmax=np.max(lumdenbsq)
    print("lumdenbsqmax")
    print(lumdenbsqmax)
    lumdenbsqmaxindex=np.unravel_index(lumdenbsq.argmax(), lumdenbsq.shape)
    print("lumdenbsqmaxindex")
    print(lumdenbsqmaxindex)
    rlumdenbsq=r[lumdenbsqmaxindex[0],0,0]
    hlumdenbsq=h[0,lumdenbsqmaxindex[1],0]
    phlumdenbsq=ph[0,0,lumdenbsqmaxindex[2]]
    print("rhph lumdenbsq: %g %g %g" % (rlumdenbsq, hlumdenbsq, phlumdenbsq) )
    # actually sum
    lumsynchnon3=np.sum(lumdenbsq)
    #
    #
    return lumug,lumbsq,lumfull,lumug2,lumbsq2,lumfull2,lumug3,lumbsq3,lumfull3,lumug4,lumbsq4,lumfull4,lumsynch,lumsynchnon1,lumsynchnon2,lumsynchnon3


# need integrate when nz=1 because just avg2d data.  Means averaged-out, so sum is recovered by multiplying by number of cells in \phi
def intangle_foravg2d(qty,hoverr=None,thetamid=np.pi/2,minbsqorho=None,maxbsqorho=None,inflowonly=None,mumax=None,mumin=None,maxbeta=None,which=1,doabs=0):
    #
    if doabs==1:
        qtynew=np.fabs(qty)
    else:
        qtynew=qty
    #
    # translate from avg to normal quantity
    global bsq,rho,ug,uu,ud,rhoclean,ugclean,rhounclean,ugunclean,enth,unb,isunbound,tiny,entropy
    bsq=avg_bsq
    rho=avg_rho
    ug=avg_ug
    uu=avg_uu
    ud=avg_ud
    # averages already removed jet densities
    rhoclean=rho
    rhounclean=rho
    ugclean=ug
    ugunclean=ug
    enth=1+ugclean*gam/rhoclean
    entropy=(gam-1.0)*ugclean/rho**(gam)
    unb=enth*ud[0]
    # unbound here means *thermally* rather than kinetically (-u_t>1) or fully thermo-magnetically (\mu>1) unbound.
    isunbound=(-unb>1.0)
    tiny=np.finfo(rho.dtype).tiny
    #
    result=intangle(qtynew,hoverr=hoverr,thetamid=thetamid,minbsqorho=minbsqorho,maxbsqorho=maxbsqorho,inflowonly=inflowonly,mumax=mumax,mumin=mumin,maxbeta=maxbeta,which=which)
    return(result)


def intangle(qty,hoverr=None,thetamid=np.pi/2,minbsqorho=None,maxbsqorho=None,inflowonly=None,mumax=None,mumin=None,maxbeta=None,which=1,doavgn3=1):
    integrand = qty
    #
    #somehow gives slightly different answer than when computed directly
    if hoverr is not None:
        insidehor = np.abs(h-thetamid)<hoverr
    else:
        hoverr = np.pi/2
        thetamid = np.pi/2
        insidehor = 1.0
    #
    # minbsqorho to look at flow in high mag regions to approximate floor injection
    if minbsqorho != None:
        insideminbsqorho = bsq/rho>=minbsqorho
    else:
        insideminbsqorho = 1
    #
    # maxbsqorho for mdin
    if maxbsqorho != None:
        insidemaxbsqorho = bsq/rho<=maxbsqorho
    else:
        insidemaxbsqorho = 1
    #
    # inflowonly for mdin
    if inflowonly != None:
        insideinflowonly = uu[1]<0.0
    else:
        insideinflowonly = 1
    #
    #
    #v4asq=bsq/(rho+ug+(gam-1)*ug)
    #mum1fake=uu[0]*(1.0+v4asq)-1.0
    # override (mum1fake or mu do poorly for marking boundary of jet)
    mum1fake=bsq/rho
    # mumax for wind
    if mumax is None:
        insidemumax = 1
    else:
        insidemumax = 1
        insidemumax = insidemumax * (mum1fake<mumax)
        insidemumax = insidemumax * (isunbound==1)
        insidemumax = insidemumax * (uu[1]>0.0)
    #
    # mumin for jet
    if mumin is None:
        insidemumin = 1
    else:
        insidemumin = 1
        insidemumin = insidemumin * (mum1fake>mumin)
        insidemumin = insidemumin * (isunbound==1)
        insidemumin = insidemumin * (uu[1]>0.0)
    #
    # beta for wind
    #beta=((gam-1)*ug)*divideavoidinf(bsq*0.5)
    beta=((gam-1)*ug)/(1E-30 + bsq*0.5)
    if maxbeta is None:
        insidebeta = 1
    else:
        insidebeta = (beta<maxbeta)
    #
    superintegrand=(integrand*insideinflowonly*insidehor*insideminbsqorho*insidemaxbsqorho*insidemumin*insidemumax*insidebeta*which)
    #
    if doavgn3==1:
        # this will be function of r
        integral=(superintegrand).sum(axis=2).sum(axis=1)*_dx2*_dx3
        # below factor accounts for whether inputted phi slice or averaged or full nz in size, so that integral is correctly summed to full amount
        integral=integral*(nz/len(superintegrand[0,0,:]))
        # below factor accounts for HARM vs. normal full 2\pi size of \phi-direction
        integral=scaletofullwedge(integral)
    else:
        # this will be function of r,\phi
        integral=(superintegrand).sum(axis=1)*_dx2
    #
    return(integral)






def intrpvsh(qty=None,rin=None,rout=None,phiin=None,phiout=None,minbsqorho=None,maxbsqorho=None,inflowonly=None,mumax=None,mumin=None,maxbeta=None,which=1):
    #
    # use direct avoidance of some cells (rather than just using which) in order to speed-up this otherwise slowish calculation
    iin=iofr(rin)
    iout=iofr(rout)
    #
    kin=kofph(phiin)
    kout=kofph(phiout)
    if kin<0:
        kin=0
    if kout>nz-1:
        kout=nz-1
    #
    #
    integrand = qty
    #
    # minbsqorho to look at flow in high mag regions to approximate floor injection
    if minbsqorho != None:
        insideminbsqorho = bsq/rho>=minbsqorho
    else:
        insideminbsqorho = 1
    #
    # maxbsqorho for mdin
    if maxbsqorho != None:
        insidemaxbsqorho = bsq/rho<=maxbsqorho
    else:
        insidemaxbsqorho = 1
    #
    # inflowonly for mdin
    if inflowonly != None:
        insideinflowonly = uu[1]<0.0
    else:
        insideinflowonly = 1
    #
    #
    #v4asq=bsq/(rho+ug+(gam-1)*ug)
    #mum1fake=uu[0]*(1.0+v4asq)-1.0
    # override (mum1fake or mu do poorly for marking boundary of jet)
    mum1fake=bsq/rho
    # mumax for wind
    if mumax is None:
        insidemumax = 1
    else:
        insidemumax = 1
        insidemumax = insidemumax * (mum1fake<mumax)
        insidemumax = insidemumax * (isunbound==1)
        insidemumax = insidemumax * (uu[1]>0.0)
    #
    # mumin for jet
    if mumin is None:
        insidemumin = 1
    else:
        insidemumin = 1
        insidemumin = insidemumin * (mum1fake>mumin)
        insidemumin = insidemumin * (isunbound==1)
        insidemumin = insidemumin * (uu[1]>0.0)
    #
    # beta for wind
    #beta=((gam-1)*ug)*divideavoidinf(bsq*0.5)
    beta=((gam-1)*ug)/(1E-30 + bsq*0.5)
    if maxbeta is None:
        insidebeta = 1
    else:
        insidebeta = (beta<maxbeta)
    #
    ####################
    # DO SUM
    tosum=(integrand*insideinflowonly*insideminbsqorho*insidemaxbsqorho*insidemumin*insidemumax*insidebeta*which*_dx1*_dx3)
    #
    integral=restrictrphi_sum_vstheta(tosum,iin=iin,iout=iout,kin=kin,kout=kout)
    #
    ####################
    # now interpolate from size ny to size nx
    xold=tj[0,0,0]+(tj[0,:,0]-tj[0,0,0])/(tj[0,-1,0]-tj[0,0,0])
    xnew=ti[0,0,0]+(ti[:,0,0]-ti[0,0,0])/(ti[-1,0,0]-ti[0,0,0])
    fixedintegral=np.interp(xnew,xold,integral)
    #
    return(fixedintegral)




# restricted radial range for sum so faster sum
def restrictrphi_sum_vstheta(qty=None,iin=None,iout=None,kin=None,kout=None):

    result=np.zeros(ny,dtype=np.float32)
    for ii in np.arange(iin,iout+1):
        for kk in np.arange(kin,kout+1):
            result=result+qty[ii,:,kk]
    #
    result=scaletofullwedge(result)

    return(result)





# can't just truncate for spatial dependence because would then trigger on zeros.
def powervsm(doabs=0,rin=None,rout=None,qty=None,minbsqorho=None,maxbsqorho=None,which=1):
    #
    # Assumptions:
    # 1) which should *not* have any phi dependence.
    # 2) qty includes gdet factor for integrals
    #
    # use direct avoidance of some cells (rather than just using which) in order to speed-up this otherwise slowish calculation
    iin=iofr(rin)
    iout=iofr(rout)
    if iout<iin:
        iout=iin
    #
    ################
    # first form average bsq/rho so can get power in a mode without triggering on artificial phi-dependent cut
    bsqorho_phiavg0_up=np.sum(gdet*bsq/rho,axis=2)
    bsqorho_phiavg0_dn=np.sum(gdet*1.0+rho*0.0,axis=2) # gdet is 2D by default
    bsqorho_phiavg0=bsqorho_phiavg0_up/bsqorho_phiavg0_dn
    #
    #print("bsqorho_phiavg @ iin:")
    #print(bsqorho_phiavg0[iin,:])
    #print("bsqorho_phiavg @ iout:")
    #print(bsqorho_phiavg0[iout,:])
    #
    # create 3D version
    bsqorho_phiavg = np.zeros_like(bsq)
    for kk in np.arange(0,nz):
        bsqorho_phiavg[:,:,kk]=bsqorho_phiavg0[:,:]
    #
    #
    ################
    # setup properly-phi-cut integrand
    integrand=qty
    #
    if minbsqorho is not None:
        integrand = integrand*(bsqorho_phiavg>minbsqorho)
    #
    if maxbsqorho is not None:
        integrand = integrand*(bsqorho_phiavg<maxbsqorho)
    #
    # required for things that are (e.g.) anti-symmetric across equator
    if doabs==1:
        integrand=np.fabs(integrand)
    #
    ################
    # get P_m
    # have zeros for non-measured m
    qtyvsphi=np.zeros(nz,dtype=np.float32)
    powervsmresult=np.zeros(nx,dtype=np.float32)
    # now find powers for given cut, with nx m modes (generally, nx>=nz for most simulations, so should be fine)
    #
    ################
    # FAST WAY
    qtyvsphi=qty_vsphi(qty=integrand*which*_dx1*_dx2*_dx3,iin=iin,iout=iout)
    # get FFT
    Yfft=np.fft.rfft(qtyvsphi)
    nfft=len(Yfft)
    if nfft!=nz/2+1:
        print("nfft=%d is not nz/2+1=%d",nfft,nz/2+1) ; sys.stdout.flush()
    #
    print("qtyvsphi: nfft(ninput/2+1)=%d" % (nfft)) ; sys.stdout.flush()
    # power saved as |a_j|^2
    powerfft = np.absolute(Yfft[0:nfft])**2
    #
    #translate to nx size
    numm=min(nx,nfft)
    for mm in np.arange(0,numm):
        powervsmresult[mm]=powerfft[mm]
    #
    ##################
    # very slow way
    # numm=min(nx,nz)
    # for mm in np.arange(0,numm):
    #     # restricted sum to avoid most i indicies so faster since otherwise very slow.
    #     # Also could avoid based upon bsqorho and choose theta range for that.
    #     cospart=restrictr_sum_3d(qty=integrand*np.cos(mm*ph)*which*_dx1*_dx2*_dx3,iin=iin,iout=iout)
    #     sinpart=restrictr_sum_3d(qty=integrand*np.sin(mm*ph)*which*_dx1*_dx2*_dx3,iin=iin,iout=iout)
    #     powervsmresult[mm] = np.sqrt( cospart**2 + sinpart**2 )
    #
    #
    return(powervsmresult)


# form \phi-only-dependent array
def qty_vsphi(qty=None,iin=None,iout=None):

    result=np.zeros(nz,dtype=np.float32)
    # sum over part of radial range
    for ii in np.arange(iin,iout+1):
        qtyslice=qty[ii,:,:]
        #
        # sum over theta (axis=0 really for \theta)
        # result is only phi-dependent
        result=result + qtyslice.sum(axis=0)
    #
    result=scaletofullwedge(result)

    return(result)

# restricted radial range for sum so faster sum
def restrictr_sum_3d(qty=None,iin=None,iout=None):

    result=0
    for ii in np.arange(iin,iout+1):
        qtyslice=qty[ii,:,:]
        # axis=0,1 really for \theta,\phi
        result=result + qtyslice.sum(axis=1).sum(axis=0)
    #
    result=scaletofullwedge(result)

    return(result)








# def inttheta(qty,dtheta=np.pi/2):
#     integrand = qty
#     insidedtheta = np.abs(h-np.pi/2)<=dtheta
#     integral=np.sum(np.sum(integrand*insidetheta,axis=2),axis=1)
#     return(integral)

    
def Qmri():
    """
    APPROXIMATELY Computes number of theta cells resolving one MRI wavelength
    """
    global bu,rho,uu,_dx2
    cvel()
    #corrected this expression to include both 2pi and dxdxp[3][3]
    #also corrected defition of va^2 to contain bsq+gam*ug term
    #need to figure out how to properly measure this in fluid frame
    vau2 = np.abs(bu[2])/np.sqrt(rho+bsq+gam*ug)
    omega = dxdxp[3][3]*uu[3]/uu[0]+1e-15
    lambdamriu2 = 2*np.pi * vau2 / omega
    res=np.fabs(lambdamriu2/_dx2)
    return(res)


def plco(myvar,xcoord=None,ycoord=None,ax=None,**kwargs):
    plt.clf()
    plc(myvar,xcoord,ycoord,ax,**kwargs)

def plc(myvar,xcoord=None,ycoord=None,ax=None,**kwargs): #plc
    #
    #
    #
    #xcoord = kwargs.pop('x1', None)
    #ycoord = kwargs.pop('x2', None)
    if(np.min(myvar)==np.max(myvar)):
        print("The quantity you are trying to plot is a constant = %g." % np.min(myvar)) ; sys.stdout.flush()
        return
    cb = kwargs.pop('cb', False)
    nc = kwargs.pop('nc', 15)
    k = kwargs.pop('k',0)
    if None != xcoord and None != ycoord:
        xcoord = xcoord[:,:,None] if xcoord.ndim == 2 else xcoord[:,:,k:k+1]
        ycoord = ycoord[:,:,None] if ycoord.ndim == 2 else ycoord[:,:,k:k+1]
    myvar = myvar[:,:,None] if myvar.ndim == 2 else myvar[:,:,k:k+1]
    if ax is None:
        ax = plt.gca()
    if( xcoord == None or ycoord == None ):
        res = ax.contour(myvar[:,:,0].transpose(),nc,**kwargs)
    else:
        res = ax.contour(xcoord[:,:,0],ycoord[:,:,0],myvar[:,:,0],nc,**kwargs)
    if( cb == True): #use color bar
        plt.colorbar(res,ax=ax)

def reinterp(vartointerp,extent,ncell,domask=1,isasymmetric=False):
    global xi,yi,zi
    #grid3d("gdump")
    #rfd("fieldline0250.bin")
    xraw=r*np.sin(h)
    yraw=r*np.cos(h)
    x=xraw[:,:,0].view().reshape(-1)
    y=yraw[:,:,0].view().reshape(-1)
    var=vartointerp[:,:,0].view().reshape(-1)
    #mirror
    x=np.concatenate((-x,x))
    y=np.concatenate((y,y))
    kval=min(vartointerp.shape[2]-1,nz/2)
    varmirror = vartointerp[:,:,kval].view().reshape(-1)
    if isasymmetric:
        varmirror *= -1.
    var=np.concatenate((varmirror,var))
    # define grid.
    xi = np.linspace(extent[0], extent[1], ncell)
    yi = np.linspace(extent[2], extent[3], ncell)
    # grid the data.
    zi = griddata((x, y), var, (xi[None,:], yi[:,None]), method='cubic')
    #zi[interior] = np.ma.masked
    if domask!=0:
        interior = np.sqrt((xi[None,:]**2) + (yi[:,None]**2)) < (1+np.sqrt(1-a**2))*domask
        varinterpolated = ma.masked_where(interior, zi)
    else:
        varinterpolated = zi
    return(varinterpolated)

def reinterpxy(vartointerp,extent,ncell,domask=1):
    global xi,yi,zi
    #grid3d("gdump")
    #rfd("fieldline0250.bin")
    xraw=r*np.sin(h)*np.cos(ph)
    yraw=r*np.sin(h)*np.sin(ph)
    #2 cells below the midplane
    x=xraw[:,ny/2+1,:].view().reshape(-1)
    y=yraw[:,ny/2+1,:].view().reshape(-1)
    var=vartointerp[:,ny/2+1,:].view().reshape(-1)
    #mirror
    if nz*_dx3*dxdxp[3,3,0,0,0] < 0.99 * 2 * np.pi:
        x=np.concatenate((-x,x))
        y=np.concatenate((-y,y))
        var=np.concatenate((var,var))
    # define grid.
    xi = np.linspace(extent[0], extent[1], ncell)
    yi = np.linspace(extent[2], extent[3], ncell)
    # grid the data.
    zi = griddata((x, y), var, (xi[None,:], yi[:,None]), method='cubic')
    #zi[interior] = np.ma.masked
    if domask!=0:
        interior = np.sqrt((xi[None,:]**2) + (yi[:,None]**2)) < (1+np.sqrt(1-a**2))*domask
        varinterpolated = ma.masked_where(interior, zi)
    else:
        varinterpolated = zi
    return(varinterpolated)
    
def ftr(x,xb,xf):
    return( amax(0.0*x,amin(1.0+0.0*x,1.0*(x-xb)/(xf-xb))) )


# What Sasha uses for streamlines:
#    The new code is at http://www.atm.damtp.cam.ac.uk/people/tjf37/streamplot.py and 
#there are new sample plots at 
#http://www.atm.damtp.cam.ac.uk/people/tjf37/streamlines1.png and 
#http://www.atm.damtp.cam.ac.uk/people/tjf37/streamlines2.png .

# other stream line methods:
# http://github.enthought.com/mayavi/mayavi/mlab.html
# http://permalink.gmane.org/gmane.comp.python.matplotlib.general/26362
# http://comments.gmane.org/gmane.comp.python.matplotlib.general/26354
# http://mindseye.no/tag/python/
# http://scikits.appspot.com/vectorplot  (includes LIC)
# http://wiki.chem.vu.nl/dirac/index.php/How_to_plot_vector_fields_calculated_with_DIRAC11_as_streamline_plots_using_PyNGL


# LIC code:
# http://reference.wolfram.com/mathematica/ref/ListLineIntegralConvolutionPlot.html
# http://reference.wolfram.com/legacy/v7/ref/LineIntegralConvolutionPlot.html
# http://www.zhanpingliu.org/research/flowvis/LIC/LIC.htm
# http://www.cs.utah.edu/~wmartin/cs523project/
# http://www.scipy.org/Cookbook/LineIntegralConvolution


# dobhfield=True : GODMARK: Set to False since already showing BH penetrating field because comes from large radii down to hole
def mkframe(fname,ax=None,cb=True,tight=False,useblank=True,vmin=None,vmax=None,len=20,lenx=None,leny=None,ncell=800,pt=True,shrink=1,dovel=False,doaphi=False,dostreamlines=True,doaphiavg=False,downsample=4,density=2,dodiskfield=False,minlendiskfield=0.2,minlenbhfield=0.2,dorho=True,doentropy=False,dobsq=False,dobeta=False,doQ1=False,doQ2=False,dovarylw=True,dobhfield=False,dsval=0.01,color='k',dorandomcolor=False,doarrows=True,lw=None,skipblankint=False,detectLoops=True,minindent=1,minlengthdefault=0.2,startatmidplane=True,domidfield=True,showjet=False,arrowsize=1,forceeqsym=0,dojonwindplot=False,doaphicont=None,inputlevs=None,numcontours=30,signaphi=1,aphipow=1.0,showuu1eq0=True):
    #
    levs=inputlevs
    #
    if lenx is not None and leny is not None:
        extent=(-lenx,lenx,-leny,leny)
    elif lenx is not None:
        extent=(-lenx,lenx,-len,len)
    elif leny is not None:
        extent=(-len,len,-leny,leny)
    else:
        extent=(-len,len,-len,len)
    #
    if lenx is None:
        lenx=len
    if leny is None:
        leny=len
    #
    palette=cm.jet
    palette.set_bad('k', 1.0)
    #palette.set_over('r', 1.0)
    #palette.set_under('g', 1.0)
    rhor=1+(1-a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    #
    #
    ####################
    if dojonwindplot==1:
        #
        # below needed in case operating on averages instead of from rfd()
        uu=uutrue
        (rhoclean,ugclean,uu,maxbsqorhonear,maxbsqorhofar,condmaxbsqorho,condmaxbsqorhorhs,rinterp)=getrhouclean(rho,ug,uu)
        localmaxbsqorho=maxbsqorhonear
        #ud = mdot(gv3,uu)                  #g_mn u^n
        # no, assume any cleaning occurs upon rfd() and averages get that result
        #localmaxbsqorho=maxbsqorho
        #
        ibeta = reinterp(beta,extent,ncell,domask=1.0)
        iud0  = reinterp(ud[0],extent,ncell,domask=1.0)
        #
        enth=1+ugclean*gam/rhoclean
        # limit value for same reason as below
        enth[rhoclean<1E-10]=1
        enth[enth>100]=100
        enth[enth<1]=1
        unb=(enth*ud[0])
        iunb  = reinterp(unb,extent,ncell,domask=1.0)
        bsqorho=bsq/rho
        # if using avg_rho, already cleaned so can be very small and contours will oscillate stupidly, so limit value
        bsqorho[bsqorho>localmaxbsqorho]=localmaxbsqorho
        ibsqorho = reinterp(bsqorho,extent,ncell,domask=1.0)
        # limit value for same reason as above
        #mu[mu>localmaxbsqorho]=localmaxbsqorho
        #imu = reinterp(mu,extent,ncell,domask=1.0)
        #
        iuu1  = reinterp(uu[1],extent,ncell,domask=1.0)
    #
    ####################
    #
    # get iqty
    print("dorho=%d doentropy=%d dobsq=%d dobeta=%d doQ1=%d doQ2=%d : vmin=%g vmax=%g" % (dorho,doentropy,dobsq,dobeta,doQ1,doQ2,vmin,vmax)) ; sys.stdout.flush()
    doqty=0
    dologz=0
    if dorho:
        lrho=np.log10(rho+1E-30)
        dologz=1
        qty=lrho
        doqty=1
    elif doentropy:
        lentropy=np.log10(entropy+1E-30)
        dologz=1
        qty=lentropy
        doqty=1
    elif dobsq:
        lbsq=np.log10(bsq*0.5+1E-30)
        dologz=1
        qty=lbsq
        doqty=1
    elif dobeta:
        lbeta=np.log10(betatoplot+1E-30)
        dologz=1
        qty=lbeta
        doqty=1
    elif doQ1:
        qty=np.fabs(Q1)
        dologz=0
        doqty=1
    elif doQ2:
        qty=np.fabs(Q2toplot)
        dologz=0
        doqty=1
    #
    if doqty==1:
        # limit values so really consistent with vmin&vmax and interpolation doesn't go nuts
        qty[qty<vmin]=vmin
        qty[qty>vmax]=vmax
        qty[np.isinf(qty)]=vmax
        qty[np.isnan(qty)]=vmax
        #
        iqty = reinterp(qty,extent,ncell,domask=1.0)
    #
    #
    ###########################################
    # setup field stuff
    radmax=np.sqrt(lenx**2 + leny**2)
    iouter=iofr(radmax)
    #
    if doaphi==1:
        if numcontours is not None:
            print("numcontoursA check: %s %d" % (fname,numcontours))
        else:
            print("numcontoursA checkB: %s None" % (fname))
        #
        aphi = fieldcalc() # keep sign information
        # flip sign in some model cases to highlight field in desired way
        if modelname=="thickdisk7":
            aphi=-aphi
            if doaphicont!=None:
                doaphicont=-doaphicont
                doaphicont=0.7*doaphicont
        #
        aphimod = np.sign(aphi)*(np.fabs(aphi))**(aphipow)
        #
        if signaphi==-1: # indicates want to change things so sign doesn't matter for contour plot
            aphimod = np.sqrt(aphimod**2)
        # force equatorial symmetry by averaging
        if forceeqsym==1:
            aphimodtemp=np.copy(aphimod)
            for j in np.arange(0,ny):
                aphimod[:,j,:]=0.5*(aphimodtemp[:,j,:]+aphimodtemp[:,ny-1-j,:])
        #
        iaphi = reinterp(aphimod,extent,ncell,domask=0)
        if 1==0:
            miniaphi=np.min((iaphi))
            maxiaphi=np.max((iaphi))
        else:
            # restrict contour level choices to those relevant for radial region showing
            miniaphi=np.min((aphimod[0:iouter+1,:,:]))
            maxiaphi=np.max((aphimod[0:iouter+1,:,:]))
        #
        #maxabsiaphi = 100 #50
        ncont = numcontours #30
        if inputlevs is None:
            levs=np.linspace(miniaphi,maxiaphi,ncont)
            print("levsA=%g",levs)
        else:
            levs=inputlevs
            print("levsB=%g",levs)
        #
    #
    if doaphiavg==1:
        if numcontours is not None:
            print("numcontoursB check: %s %d" % (fname,numcontours))
        else:
            print("numcontoursB checkB: %s None" % (fname))
        #
        #aphi=np.sqrt(avg_psisq[0:iofr(30.0),:,0])
        aphi=np.sqrt(avg_psisq) # so loses sign-information
        #
        aphimod = np.sign(aphi)*(np.fabs(aphi))**(aphipow)
        #
        # force equatorial symmetry by averaging
        if forceeqsym==1:
            aphimodtemp=np.copy(aphimod)
            for j in np.arange(0,ny):
                aphimod[:,j,:]=0.5*(aphimodtemp[:,j,:]+aphimodtemp[:,ny-1-j,:])
        #
        iaphi = reinterp(aphimod,extent,ncell,domask=0)
        #
        if 1==0:
            maxabsiaphi=np.max(np.abs(iaphi))
        else:
            # restrict contour level choices to those relevant for radial region showing
            miniaphi=np.min((aphimod[0:iouter+1,:,:]))
            maxiaphi=np.max((aphimod[0:iouter+1,:,:]))
            maxabsiaphi=np.max(np.fabs(miniaphi),np.fabs(maxiaphi))
        #
        #maxabsiaphi = 100 #50
        ncont = numcontours #30
        if inputlevs is None:
            #levs=np.linspace(-maxabsiaphi,maxabsiaphi,ncont) # um, iaphi is never negative
            levs=np.linspace(0,maxabsiaphi,ncont)
            print("levs2A=%g",levs)
        else:
            levs=inputlevs
            print("levs2B=%g",levs)
        #
    #
    print("dovel=%d checkstream: %g" % (dovel,B[1][30,ny/2,0]))
    #
    if dostreamlines==1:
        if numcontours is not None:
            print("numcontoursC check: %s %d" % (fname,numcontours))
        else:
            print("numcontoursC checkB: %s None" % (fname))
        #
        #
        #
        aphi = fieldcalc()
        # flip sign in some model cases to highlight field in desired way
        if modelname=="thickdisk7":
            aphi=-aphi
        iaphi = reinterp(aphi,extent,ncell,domask=0)
        #
        # note, below is not necessarily B, can be uu
        # convert from x^(i) to B^{r,h,ph}
        Br = dxdxp[1,1]*B[1]+dxdxp[1,2]*B[2]
        Bh = dxdxp[2,1]*B[1]+dxdxp[2,2]*B[2]
        Bp = B[3]*dxdxp[3,3]
        #
        # note that this conversion to orthonormal basis ignores GR!
        Brnorm=Br
        Bhnorm=Bh*np.abs(r)
        Bpnorm=Bp*np.abs(r*np.sin(h))
        #
        # polar fix-up
        #Brnorm[:,0,:]=Brnorm[:,2,:]
        #Brnorm[:,1,:]=Brnorm[:,2,:]
        #Brnorm[:,ny-1,:]=Brnorm[:,ny-3,:]
        #Brnorm[:,ny-2,:]=Brnorm[:,ny-3,:]
        #
        # polar fix-up (doesn't seem to help)
        #Bhnorm[:,0,:]=Bhnorm[:,2,:]
        #Bhnorm[:,1,:]=Bhnorm[:,2,:]
        #Bhnorm[:,ny-1,:]=Bhnorm[:,ny-3,:]
        #Bhnorm[:,ny-2,:]=Bhnorm[:,ny-3,:]
        #
        # polar fix-up
        #Bhnorm[:,0,:]=0
        #Bhnorm[:,1,:]=0
        #Bhnorm[:,2,:]=0
        #Bhnorm[:,ny-1,:]=0
        #Bhnorm[:,ny-2,:]=0
        #Bhnorm[:,ny-3,:]=0
        #
        #
        # equatorial symmetry check
        #for j in np.arange(0,ny):
        #for j in np.arange(ny-1,-1,-1):
        #    Brnorm[:,j,:]=Brnorm[:,ny-1-j,:]
        #    Bhnorm[:,j,:]=-Bhnorm[:,ny-1-j,:]
        #    Bpnorm[:,j,:]=Bpnorm[:,ny-1-j,:]
        #
        # force equatorial symmetry by averaging
        if forceeqsym==1:
            Brnormtemp=np.copy(Brnorm)
            Bhnormtemp=np.copy(Bhnorm)
            Bpnormtemp=np.copy(Bpnorm)
            for j in np.arange(0,ny):
                if dovel==0:
                    Brnorm[:,j,:]=0.5*(Brnormtemp[:,j,:]-Brnormtemp[:,ny-1-j,:]) # assumes split-monopole or higher, not monopole
                    Bhnorm[:,j,:]=0.5*(Bhnormtemp[:,j,:] + Bhnormtemp[:,ny-1-j,:]) # assumes field vertically passes from lower to upper side
                    Bpnorm[:,j,:]=0.5*(Bpnormtemp[:,j,:]-Bpnormtemp[:,ny-1-j,:]) # assumes split-monopole or higher, not monopole
                else:
                    Brnorm[:,j,:]=0.5*(Brnormtemp[:,j,:]+Brnormtemp[:,ny-1-j,:])
                    Bhnorm[:,j,:]=0.5*(Bhnormtemp[:,j,:]-Bhnormtemp[:,ny-1-j,:])
                    Bpnorm[:,j,:]=0.5*(Bpnormtemp[:,j,:]+Bpnormtemp[:,ny-1-j,:])
                #
            #
        Bznorm=Brnorm*np.cos(h)-Bhnorm*np.sin(h)
        BRnorm=Brnorm*np.sin(h)+Bhnorm*np.cos(h)
        #
        iBz = reinterp(Bznorm,extent,ncell,domask=0.8)
        #isasymmetric = True tells to flip the sign across polar axis
        iBR = reinterp(BRnorm,extent,ncell,isasymmetric=True,domask=0.8)
        #
        if dorandomcolor:
            # note, below is not necessarily B, can be uu
            Ba=np.copy(B)
            cond = (B[1]<0)
            Ba[2,cond]*=-1
            Ba[3,cond]*=-1
            Ba[1,cond]*=-1
            Bar = dxdxp[1,1]*Ba[1]+dxdxp[1,2]*Ba[2]
            Bah = dxdxp[2,1]*Ba[1]+dxdxp[2,2]*Ba[2]
            Bap = Ba[3]*dxdxp[3,3]
            #
            Barnorm=Bar
            Bahnorm=Bah*np.abs(r)
            Bapnorm=Bap*np.abs(r*np.sin(h))
            #
            # force equatorial symmetry by averaging
            if forceeqsym==1:
                Barnormtemp=np.copy(Barnorm)
                Bahnormtemp=np.copy(Bahnorm)
                Bapnormtemp=np.copy(Bapnorm)
                for j in np.arange(0,ny):
                    if dovel==0:
                        Barnorm[:,j,:]=0.5*(Barnormtemp[:,j,:]-Barnormtemp[:,ny-1-j,:]) # assumes split-monopole or higher, not monopole
                        Bahnorm[:,j,:]=0.5*(Bahnormtemp[:,j,:] + Bahnormtemp[:,ny-1-j,:]) # assumes field vertically passes from lower to upper side
                        Bapnorm[:,j,:]=0.5*(Bapnormtemp[:,j,:]-Bapnormtemp[:,ny-1-j,:]) # assumes split-monopole or higher, not monopole
                    else:
                        Barnorm[:,j,:]=0.5*(Barnormtemp[:,j,:]+Barnormtemp[:,ny-1-j,:])
                        Bahnorm[:,j,:]=0.5*(Bahnormtemp[:,j,:]-Bahnormtemp[:,ny-1-j,:])
                        Bapnorm[:,j,:]=0.5*(Bapnormtemp[:,j,:]+Bapnormtemp[:,ny-1-j,:])
                    #
            #
            Baznorm=Barnorm*np.cos(h)-Bahnorm*np.sin(h)
            BaRnorm=Barnorm*np.sin(h)+Bahnorm*np.cos(h)
            #
            iBaz = reinterp(Baznorm,extent,ncell,domask=0.8)
            iBaR = reinterp(BaRnorm,extent,ncell,isasymmetric=True,domask=0.8) #isasymmetric = True tells to flip the sign across polar axis
        else:
            iBaz = None
            iBaR = None
        #if showjet:
        #    imu = reinterp(mu,extent,ncell,domask=0.8)
        #
        if dovarylw:
            iibeta = reinterp(0.5*bsq/(gam-1)/ug,extent,ncell,domask=0)
            ibsqorho = reinterp(bsq/rho,extent,ncell,domask=0)
            ibsqo2rho = 0.5 * ibsqorho
        xi = np.linspace(extent[0], extent[1], ncell)
        yi = np.linspace(extent[2], extent[3], ncell)
        #myspeed=np.sqrt(iBR**2+iBz**2)
    #
    #myslines=streamplot(ti[:,0,0],tj[0,:,0],avg_gdetB[0,:,:,0].transpose(),avg_gdetB[1,:,:,0].transpose(),density=2,downsample=4,linewidth=1)
    #for c in cset2.collections:
    #    c.set_linestyle('solid')
    #CS = plt.contourf(xi,yi,zi,15,cmap=palette)
    if ax == None:
        ax = plt.gca()
        # CS = plt.imshow(ilrho, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=vmin,vmax=vmax)
        # if not dostreamlines:
        #     cset2 = plt.contour(iaphi,linewidths=0.5,colors='k', extent=extent,hold='on',origin='lower',levels=levs)
        # else:
        #     lw = 0.5+1*ftr(np.log10(amax(ibsqo2rho,1e-6+0*ibsqorho)),np.log10(1),np.log10(2))
        #     lw += 1*ftr(np.log10(amax(iibeta,1e-6+0*ibsqorho)),np.log10(1),np.log10(2))
        #     lw *= ftr(np.log10(amax(iibeta,1e-6+0*iibeta)),-3.5,-3.4)
        #     # if t < 1500:
        #     #     lw *= ftr(ilrho,-2.,-1.9)
        #     fstreamplot(yi,xi,iBR,iBz,density=2,downsample=4,linewidth=lw,ax=ax,detectLoops=True,dodiskfield=False,dobhfield=True,startatmidplane=True,a=a)
        #     #streamplot(yi,xi,iBR,iBz,density=3,linewidth=1,ax=ax)
        # plt.xlim(extent[0],extent[1])
        # plt.ylim(extent[2],extent[3])
    #
    #
    ###########################################
    # plot image
    if doqty==1:
        CS = ax.imshow(iqty, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=vmin,vmax=vmax)
        if True == cb:
            if dologz==0:
                cbar = plt.colorbar(CS,ax=ax,shrink=shrink) # draw colorbar
            else:
                cbar = plt.colorbar(CS,ax=ax,shrink=shrink,format=r'$10^{%0.1f}$')
        #
        if tight==True:
            plt.axis('tight')
        #CS = plt.contour(X, Y, Z)
    #
    ###########################################
    # other stuff
    if showjet:
        #ax.contour(imu,linewidths=0.5,colors='g', extent=extent,hold='on',origin='lower',levels=(2,))
        ax.contour(iaphi,linewidths=0.5,colors='b', extent=extent,hold='on',origin='lower',levels=(aphi[ihor,ny/2,0],))
    #
    #
    ###########################################
    # plot field stuff
    if doaphi==1 or doaphiavg==1:
        #cset2 = ax.contour(iaphi,linewidths=0.5,colors='k', extent=extent,hold='on',origin='lower',levels=levs)
        cset2 = ax.contour(iaphi,linewidths=2.0,colors='r', extent=extent,hold='on',origin='lower',levels=levs)
        if doaphicont is not None:
            cset3 = ax.contour(iaphi,linewidths=3.0,colors='black', extent=extent,hold='on',origin='lower',levels=(doaphicont,))
    #
    if dostreamlines==1:
        if dovarylw:
            lw = 0.5+1*ftr(np.log10(amax(ibsqo2rho,1e-6+0*ibsqorho)),np.log10(1),np.log10(2))
            lw += 1*ftr(np.log10(amax(iibeta,1e-6+0*ibsqorho)),np.log10(1),np.log10(2))
            lw *= ftr(np.log10(amax(iibeta,1e-6+0*iibeta)),-3.5,-3.4)
            # if t < 1500:
            #lw *= ftr(iaphi,0.001,0.002)
        fstreamplot(yi,xi,iBR,iBz,ua=iBaR,va=iBaz,useblank=useblank,density=density,downsample=downsample,linewidth=lw,ax=ax,detectLoops=detectLoops,dodiskfield=dodiskfield,dobhfield=dobhfield,startatmidplane=startatmidplane,domidfield=domidfield,a=a,minlendiskfield=minlendiskfield,minlenbhfield=minlenbhfield,dsval=dsval,color=color,doarrows=doarrows,dorandomcolor=dorandomcolor,skipblankint=skipblankint,minindent=minindent,minlengthdefault=minlengthdefault,arrowsize=arrowsize)
        #streamplot(yi,xi,iBR,iBz,density=3,linewidth=1,ax=ax)
    #
    # goes on top:
    if dojonwindplot:
        mwindmaxbeta=2
        #ax.contour(imu,linewidths=4,colors='g', extent=extent,hold='on',origin='lower',levels=(1,2,))
        ax.contour(ibeta,linewidths=4,colors='cyan', extent=extent,hold='on',origin='lower',levels=(mwindmaxbeta,))
        #ax.contour(ibeta,linewidths=4,colors='magenta', extent=extent,hold='on',origin='lower',levels=(1,))
        ax.contour(ibsqorho,linewidths=4,colors='blue', extent=extent,hold='on',origin='lower',levels=(1,))  # 29.5
        ax.contour(-iud0,linewidths=4,colors='black', extent=extent,hold='on',origin='lower',levels=(1,))
        #ax.contour(-iunb,linewidths=4,colors='red', extent=extent,hold='on',origin='lower',levels=(1,))
        if showuu1eq0==True:
            ax.contour(iuu1,linewidths=4,colors='green', extent=extent,hold='on',origin='lower',levels=(0,))
    #
    #
    ax.set_xlim(extent[0],extent[1])
    ax.set_ylim(extent[2],extent[3])
    #CS.cmap=cm.jet
    #CS.set_axis_bgcolor("#bdb76b")
    #plt.title(r'$\log_{10}\rho$ at $t = %4.0f$' % t)
    if True == pt:
        plt.title('log rho at t = %4.0f' % t)
    #if None != fname:
    #    plt.savefig( fname + '.png' )
    return(levs)



def mkframexy(fname,ax=None,cb=True,vmin=None,vmax=None,len=20,ncell=800,pt=True,shrink=1,dostreamlines=True,arrowsize=1,dorho=True,doentropy=False,dobsq=False,dobeta=False,doQ1=False,doQ2=False):
    extent=(-len,len,-len,len)
    palette=cm.jet
    palette.set_bad('k', 1.0)
    #palette.set_over('r', 1.0)
    #palette.set_under('g', 1.0)
    #
    ####################
    # get iqty
    print("dorho=%d doentropy=%d dobsq=%d dobeta=%d doQ1=%d doQ2=%d : vmin=%g vmax=%g" % (dorho,doentropy,dobsq,dobeta,doQ1,doQ2,vmin,vmax)) ; sys.stdout.flush()
    doqty=0
    dologz=0
    if dorho:
        lrho=np.log10(rho+1E-30)
        dologz=1
        qty=lrho
        doqty=1
    elif doentropy:
        lentropy=np.log10(entropy+1E-30)
        dologz=1
        qty=lentropy
        doqty=1
    elif dobsq:
        lbsq=np.log10(bsq*0.5+1E-30)
        dologz=1
        qty=lbsq
        doqty=1
    elif dobeta:
        qty=betatoplot
        dologz=0
        doqty=1
    elif doQ1:
        qty=np.fabs(Q1)
        dologz=0
        doqty=1
    elif doQ2:
        qty=np.fabs(Q2toplot)
        dologz=0
        doqty=1
    #
    if doqty==1:
        # limit values so really consistent with vmin&vmax and interpolation doesn't go nuts
        qty[qty<vmin]=vmin
        qty[qty>vmax]=vmax
        qty[np.isinf(qty)]=vmax
        qty[np.isnan(qty)]=vmax
        #
        iqty = reinterpxy(qty,extent,ncell,domask=1.0)
    #
    ##########################
    # get field
    aphi = fieldcalc()+rho*0
    iaphi = reinterpxy(aphi,extent,ncell)
    #maxabsiaphi=np.max(np.abs(iaphi))
    #maxabsiaphi = 100 #50
    #ncont = 100 #30
    #levs=np.linspace(-maxabsiaphi,maxabsiaphi,ncont)
    #cset2 = plt.contour(iaphi,linewidths=0.5,colors='k', extent=extent,hold='on',origin='lower',levels=levs)
    #for c in cset2.collections:
    #    c.set_linestyle('solid')
    #CS = plt.contourf(xi,yi,zi,15,cmap=palette)
    if dostreamlines:
        Br = dxdxp[1,1]*B[1]+dxdxp[1,2]*B[2]
        Bh = dxdxp[2,1]*B[1]+dxdxp[2,2]*B[2]
        Bp = B[3]*dxdxp[3,3]
        #
        Brnorm=Br
        Bhnorm=Bh*np.abs(r)
        Bpnorm=Bp*np.abs(r*np.sin(h))
        #
        Bznorm=Brnorm*np.cos(h)-Bhnorm*np.sin(h)
        BRnorm=Brnorm*np.sin(h)+Bhnorm*np.cos(h)
        Bxnorm=BRnorm*np.cos(ph)-Bpnorm*np.sin(ph)
        Bynorm=BRnorm*np.sin(ph)+Bpnorm*np.cos(ph)
        #
        iBx = reinterpxy(Bxnorm,extent,ncell,domask=1)
        iBy = reinterpxy(Bynorm,extent,ncell,domask=1)
        iibeta = reinterpxy(0.5*bsq/(gam-1)/ug,extent,ncell,domask=0)
        ibsqorho = reinterpxy(bsq/rho,extent,ncell,domask=0)
        ibsqo2rho = 0.5 * ibsqorho
        xi = np.linspace(extent[0], extent[1], ncell)
        yi = np.linspace(extent[2], extent[3], ncell)
    ##########################
    # do plot
    if doqty==1:
        if ax == None:
            CS = plt.imshow(iqty, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=vmin,vmax=vmax)
            plt.xlim(extent[0],extent[1])
            plt.ylim(extent[2],extent[3])
        else:
            CS = ax.imshow(iqty, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=vmin,vmax=vmax)
            if dostreamlines:
                lw = 0.5+1*ftr(np.log10(amax(ibsqo2rho,1e-6+0*ibsqorho)),np.log10(1),np.log10(2))
                lw += 1*ftr(np.log10(amax(iibeta,1e-6+0*ibsqorho)),np.log10(1),np.log10(2))
                lw *= ftr(np.log10(amax(iibeta,1e-6+0*iibeta)),-3.5,-3.4)
                # if t < 1500:
                #     lw *= ftr(iqty,-2.,-1.9)
                #lw *= ftr(iaphi,0.001,0.002)
                fstreamplot(yi,xi,iBx,iBy,density=1,downsample=1,linewidth=lw,detectLoops=True,dodiskfield=False,dobhfield=False,startatmidplane=False,a=a,arrowsize=arrowsize)
            ax.set_xlim(extent[0],extent[1])
            ax.set_ylim(extent[2],extent[3])
        #CS.cmap=cm.jet
        #CS.set_axis_bgcolor("#bdb76b")
        if True == cb:
            if dologz==0:
                cbar = plt.colorbar(CS,ax=ax,shrink=shrink) # draw colorbar
            else:
                cbar = plt.colorbar(CS,ax=ax,shrink=shrink,format=r'$10^{%0.1f}$')
    #plt.title(r'$\log_{10}\rho$ at $t = %4.0f$' % t)
    if True == pt:
        plt.title('log rho at t = %4.0f' % t)
    #
    #if None != fname:
    #    plt.savefig( fname + '.png' )


def setupframe(gs=3,loadq=0,which=1):
    #
    if loadq==1:
        grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]), use2d=True )
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
        firstfieldlinefile=flist[0]
        rfdheaderonly(firstfieldlinefile)
        #
        qtymem=None #clear to free mem
        rhor=1+(1+a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        qtymem=getqtyvstime(ihor,0.2)
    #
    params = {'backend': 'ps',
              'axes.labelsize': 14,
              'text.fontsize': 14,
              'legend.fontsize': 10,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              #'axes.formatter.limits': (-2,2),
              'text.usetex': True}
#              'figure.figsize': fig_size}
    plt.rcParams.update(params)
    #plt.rcParams['axes.formatter.limits']=[0,0]
    #plt.rcParams['axes.formatter.limits'] = (-1,1)
    # Couldn't figure out how to get scientific notation -- seems bug since takes normal numbers and makes it like log plot for y-axis
    #
    #
    if gs==1:
        gs1 = GridSpec(1, 1)
        gs1.update(left=0.15, right=0.95, top=0.99, bottom=0.10, wspace=0.01, hspace=0.05)
        ax1 = plt.subplot(gs1[:, -1])
    #
    if gs==2:
        gs1 = GridSpec(1, 1)
        gs1.update(left=0.25, right=0.85, top=0.99, bottom=0.15, wspace=0.10, hspace=0.05)
        ax1 = plt.subplot(gs1[:, -1])
    #
    if gs==3:
        gs1 = GridSpec(1, 1)
        gs1.update(left=0.25, right=0.9, top=0.95, bottom=0.08, wspace=0.10, hspace=0.05)
        ax1 = plt.subplot(gs1[:, -1])
    #
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    #ax1.yaxis.set_major_formatter(FormatStrFormatter('%e'))
    #


def maketsuniform(toplot=None):
    # toplot[time,space] has assumed to have space dimension processed, but time needs to be processed to account for non-uniform fieldline sampling.
    # plt.imshow doesn't interpolate.  Could interpolate to correct time, but same as just removing extra time data up to point where fieldline sampling is fixed.  So just remove those extra time data.
    #
    # detect late-time sampling rate
    dtsample1 = ts[-3] - ts[-4]
    dtsample2 = ts[-4] - ts[-5]
    dtsample = 0.5*(dtsample1+dtsample2)
    print("dtsample=%g" % (dtsample)) ; sys.stdout.flush()
    #
    ###################
    # get number of subsamples
    numsubtics=0
    for tic in ts:
        tici=np.where(ts==tic)[0]
        #
        if tici==0:
            dog=1 # skip
        elif tici==len(ts)-1:
            dog=1 # skip
        else:
            dtsamplenow=ts[tici]-ts[tici-1]
            if np.fabs(dtsamplenow-dtsample)>dtsample*0.5 and dtsamplenow>dtsample:
                print("SUBSAMPLE: tici=%d ts[tici]=%g dtsample=%g dtsamplenow=%g" % (tici,ts[tici],dtsample,dtsamplenow)) ; sys.stdout.flush()
                # thickdisk7 has sub samples:
                #SUBSAMPLE: tici=1000 ts[tici]=2404 dtsample=3.99902 dtsamplenow=7.99902
                #SUBSAMPLE: tici=2599 ts[tici]=8804 dtsample=3.99902 dtsamplenow=8.00098
                #SUBSAMPLE: tici=2873 ts[tici]=9904 dtsample=3.99902 dtsamplenow=8.00098
                numsubtics=numsubtics+1
            #
        #
    #
    print("lents=%d numsubtics=%d" % (len(ts),numsubtics))  ; sys.stdout.flush()
    #
    ############ fill-in missing places where subtics are
    if numsubtics>0:
        # setup new array space
        newlentssub=len(ts)+numsubtics
        toplotnewsub=np.zeros((newlentssub,nx),dtype=toplot.dtype)
        tsnewsub=np.zeros(newlentssub,dtype=ts.dtype)
        #
        #
        newtici=0
        for tici in np.arange(0,len(ts)): # over old ts tici's
            #
            if tici==0:
                toplotnewsub[newtici,:]=toplot[tici,:]
                tsnewsub[newtici]=ts[tici]
                newtici=newtici+1
            elif tici==len(ts)-1:
                toplotnewsub[newtici,:]=toplot[tici,:]
                tsnewsub[newtici]=ts[tici]
                newtici=newtici+1
            else: # fill-in subsamples
                dtsamplenow=ts[tici]-ts[tici-1]
                if np.fabs(dtsamplenow-dtsample)>dtsample*0.5 and dtsamplenow>dtsample:
                    print("FILLSUBSAMPLE: tici=%d ts[tici]=%g dtsample=%g dtsamplenow=%g" % (tici,ts[tici],dtsample,dtsamplenow)) ; sys.stdout.flush()
                    toplotnewsub[newtici,:]=toplot[tici,:]
                    tsnewsub[newtici]=ts[tici]-dtsample # iterate ts as required (already jumped to bad time, so just back a bit
                    newtici=newtici+1
                    toplotnewsub[newtici,:]=toplot[tici,:] # duplicate data
                    tsnewsub[newtici]=ts[tici] # iterate ts as required
                    newtici=newtici+1
                else:
                    toplotnewsub[newtici,:]=toplot[tici,:]
                    tsnewsub[newtici]=ts[tici]
                    newtici=newtici+1
                #
                #
            #
    else:
        # just copy if no subtics
        toplotnewsub=toplot
        tsnewsub=ts
        newlentssub=len(ts)
    #
    print("newlentssub=%d newtici=%d" % (newlentssub,newtici))  ; sys.stdout.flush()
    #
    #########################################
    # get time up to which super-sampled (and just confirm no subtics)
    numsubtics=0
    supertici=-1
    for tici in np.arange(0,newlentssub):
        #
        if tici==0:
            dog=1 # skip
        elif tici==newlentssub-1:
            dog=1 # skip
        else:
            dtsamplenow=tsnewsub[tici]-tsnewsub[tici-1]
            if np.fabs(dtsamplenow-dtsample)>dtsample*0.5 and dtsamplenow<dtsample: # if current dt and late-time dt are different by more than 1 time unit
                # keep updating supertic until last tici
                supertici=tici
                print("SUPERSAMPLE: tici=%d tsnewsub[tici]=%g dtsample=%g dtsamplenow=%g" % (tici,tsnewsub[tici],dtsample,dtsamplenow)) ; sys.stdout.flush()
            #
            elif np.fabs(dtsamplenow-dtsample)>dtsample*0.5 and dtsamplenow>dtsample:
                print("BADSUBSAMPLE: tici=%d tsnewsub[tici]=%g dtsample=%g dtsamplenow=%g" % (tici,tsnewsub[tici],dtsample,dtsamplenow)) ; sys.stdout.flush()
                numsubtics=numsubtics+1
            #
        #
    #
    print("supertici=%d lents=%d BADnumsubtics=%d" % (supertici,len(ts),numsubtics))  ; sys.stdout.flush()
    #
    ##############################
    # setup new array space (as if sub was original input)
    newlents=newlentssub-supertici/2+1
    toplotnew=np.zeros((newlents,nx),dtype=toplotnewsub.dtype)
    tsnew=np.zeros(newlents,dtype=tsnewsub.dtype)
    #
    # add to new space
    if supertici!=-1:
        newtici=0
        for tici in np.arange(0,newlentssub):
            if tici==0:
                tsnew[newtici]=tsnewsub[tici]
                newtici=newtici+1 # iterate new tici
            elif tici<=supertici:
                if tici%2==1: # only include data if odd tici
                    toplotnew[newtici,:]=toplotnewsub[tici,:]
                    tsnew[newtici]=tsnewsub[tici]
                    newtici=newtici+1
            else:
                # normal data at correct sampling period
                toplotnew[newtici,:]=toplotnewsub[tici,:]
                tsnew[newtici]=tsnewsub[tici]
                newtici=newtici+1
            #
        #
        # can end-up with 1 extra left over to do
        print("newtici=%d newlents=%d" % (newtici,newlents)) ; sys.stdout.flush()
        if newtici+1==newlents:
            toplotnew[newtici,:]=toplotnew[newtici-1,:]
            tsnew[newtici]=tsnewsub[newtici-1]+dtsample

    #
    return(tsnew,toplotnew)



def finishframe(cb=1,label=1,tight=1,useextent=1,uselim=1,testdpiinches=0,toplot=None,extent=None,vmin=None,vmax=None,which=1,mintoplot=-6,maxtoplot=1,filenum=None,fileletter=None,pllabel="",maxbsqorho=None,maxbsqou=None,radius=None):
    #
    # make time uniformly stepping
    tsnew,toplotnew=maketsuniform(toplot=toplot)
    #
    #
    #
    palette=cm.jet
    palette.set_bad('k', 1.0)
    #palette.set_over('r', 1.0)
    #palette.set_under('g', 1.0)
    #
    if useextent==1:
        CS = plt.imshow(toplotnew, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=mintoplot,vmax=maxtoplot)
    else:
        CS = plt.imshow(toplotnew, vmin=mintoplot,vmax=maxtoplot)
    #
    if tight==1:
        plt.axis('tight')
    #
    if which==1:
        plt.xscale('log')
    #
    if uselim==1:
        plt.xlim([extent[0],extent[1]])
        plt.ylim([extent[2],extent[3]])
    #
    #
    #
    #
    #ax1.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
    #ax2.ticklabel_format(style='sci', scilimits=(0,0), axis='y')      
    #
    if label==1:
        if which==1:
            #plt.xlabel(r"$\log_{10}(r/r_g)$",ha='center',labelpad=0,fontsize=14)
            plt.xlabel(r"$r [r_g]$",ha='center',labelpad=0,fontsize=14)
            plt.ylabel(r"$t [r_g/c]$",ha='left',labelpad=20,fontsize=14)
        if which==2:
            if maxbsqorho is not None and maxbsqou is not None:
                plt.xlabel(r"$\theta$ [$r=%dr_g$ mbr=%g mbu=%g]" % (radius,maxbsqorho,maxbsqou) ,ha='center',labelpad=2,fontsize=14)
            elif maxbsqorho is not None:
                plt.xlabel(r"$\theta$ [$r=%dr_g$ mbr=%g]" % (radius,maxbsqorho) ,ha='center',labelpad=2,fontsize=14)
            elif maxbsqou is not None:
                plt.xlabel(r"$\theta$ [$r=%dr_g$ mbu=%g]" % (radius,maxbsqou) ,ha='center',labelpad=2,fontsize=14)
            else:
                plt.xlabel(r"$\theta$ [$r=%dr_g$]" % (radius) ,ha='center',labelpad=2,fontsize=14)
            #
            plt.ylabel(r"$t [r_g/c]$",ha='left',labelpad=20,fontsize=14)
    #
    #
    #gs2 = GridSpec(1, 1)
    #gs2.update(left=0.5, right=1, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
    #ax2 = plt.subplot(gs2[:, -1])
    #
    if cb==1:
        plt.colorbar(CS) # draw colorbar
    #
    print("pllabel=%s" % (pllabel)) ; sys.stdout.flush()
    if fileletter=="q":
        plt.title(r"$b_\phi$",fontsize=8)
    elif fileletter=="r":
        plt.title(r"$b^2$",fontsize=8)
    else:
        #plt.subptitle(pllabel,fontsize=8)
        plt.title(pllabel,fontsize=8)
    #
    F = pylab.gcf()
    #
    if testdpiinches==1:
        # Now check everything with the defaults:
        DPI = F.get_dpi()
        print "DPI:", DPI ; sys.stdout.flush()
        DefaultSize = F.get_size_inches()
        print "Default size in Inches", DefaultSize ; sys.stdout.flush()
        print "Which should result in a %i x %i Image"%(DPI*DefaultSize[0], DPI*DefaultSize[1]) ; sys.stdout.flush()
        F.set_size_inches( (DefaultSize[0]*2, DefaultSize[1]*2) )
        Size = F.get_size_inches()
        print "Size in Inches", Size ; sys.stdout.flush()
    #
    #
    # need resolution to show all time resolution -- space is resolved normally
    #
    # total size in inches
    xinches=3.0
    yinches=6.0
    # non-plotting part that takes up space
    xnonplot=1.5
    ynonplot=0.75
    DPIy=len(ts)/(yinches-ynonplot)
    DPIx=len(r[:,0,0])/(xinches-xnonplot)
    maxresx=10000
    maxresy=10000
    maxDPIx=maxresx/xinches
    maxDPIy=maxresy/yinches
    DPIx=min(DPIx,maxDPIx)
    DPIy=min(DPIy,maxDPIy)
    DPI=max(DPIx,DPIy)
    resx=DPI*xinches
    resy=DPI*yinches
    minres=600
    if resx<minres:
        DPI=minres/xinches
        resx=DPI*xinches
        resy=DPI*yinches
    if resy<minres:
        DPI=minres/yinches
        resx=DPI*xinches
        resy=DPI*yinches
    F.set_size_inches( (xinches, yinches) )
    print("Resolution should be %i x %i pixels from DPI=%d (DPIxy=%d %d)" % (resx,resy,DPI,DPIx,DPIy)) ; sys.stdout.flush()
    #
    #
    if which==1:
        plt.savefig( "plot%d%svstr_%s.png" % (filenum,fileletter,pllabel),dpi=DPI)
        plt.savefig( "plot%d%svstr_%s.eps" % (filenum,fileletter,pllabel),dpi=DPI)
    if which==2:
        if maxbsqorho is not None and maxbsqou is not None:
            plt.savefig( "plot%d%s%d%dvsth_%s.png" % (filenum,fileletter,maxbsqorho,maxbsqou,pllabel),dpi=DPI)
            plt.savefig( "plot%d%s%d%dvsth_%s.eps" % (filenum,fileletter,maxbsqorho,maxbsqou,pllabel),dpi=DPI)
        elif maxbsqorho is not None:
            plt.savefig( "plot%d%sr%dvsth_%s.png" % (filenum,fileletter,maxbsqorho,pllabel),dpi=DPI)
            plt.savefig( "plot%d%sr%dvsth_%s.eps" % (filenum,fileletter,maxbsqorho,pllabel),dpi=DPI)
        elif maxbsqou is not None:
            plt.savefig( "plot%d%su%dvsth_%s.png" % (filenum,fileletter,maxbsqou,pllabel),dpi=DPI)
            plt.savefig( "plot%d%su%dvsth_%s.eps" % (filenum,fileletter,maxbsqou,pllabel),dpi=DPI)
        else:
            plt.savefig( "plot%d%svsth_%s.png" % (filenum,fileletter,pllabel),dpi=DPI)
            plt.savefig( "plot%d%svsth_%s.eps" % (filenum,fileletter,pllabel),dpi=DPI)
    #
    print( "Done frame!" ) ; sys.stdout.flush()



def setminmax4mk(fun0=None,which=1,myRout=None,logvalue=None,bsqorho=None,bsqou=None,maxbsqorho=None,maxbsqou=None):
    #
    
    #
    # ignore until t=100M over first time period
    itstart=max(1,tofts(100.0))
    #
    if which==1:
        # Also ignore inside horizon for setting min/max of colors for data to show
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        istart=ihor
        iend=min(nx-1,iofr(myRout))
    #
    if which==2:
        istart=0
        iend=nx-1
    #
    copyfun0=np.copy(fun0)
    # modify fun0 based upon bsqorho or bsqou
    if maxbsqorho is not None:
        copyfun0[bsqorho>maxbsqorho]=np.nan
    if maxbsqou is not None:
        copyfun0[bsqou>maxbsqou]=np.nan
    #
    maxtoplot=np.nanmax(copyfun0[itstart:-1,istart:iend+1])
    mintoplot=np.nanmin(copyfun0[itstart:-1,istart:iend+1])
    #
    #
    print("pre min=%g max=%g" % (mintoplot,maxtoplot)) ; sys.stdout.flush()
    #
    if logvalue==1:
        #toplot = np.log10(qty+1E-30)
        #somehow interpolation goes nuts and goes far beyond original values
        #maxtoplot=np.max(toplot)
        mintoplottoolow=maxtoplot-4
        mintoplot=max(mintoplot,mintoplottoolow)
    #
    print("final min=%g max=%g itstart=%d" % (mintoplot,maxtoplot,itstart)) ; sys.stdout.flush()
    #
    return(mintoplot,maxtoplot)




def mktr(loadq=1,qty=None,filenum=1,fileletter="a",logvalue=1,pllabel="",bsqorho=None,bsqou=None,maxbsqorho=None,maxbsqou=None):
    #
    # now interpolate to uniform-in-log radial grid
    #myRout=200
    # focuson inner disk region -- don't need outer region
    # go up to 30 because we use that radius for one of the t vs. \theta plots.
    myRout=30
    #myRin=Rin
    # no need to show inside horizon
    rhor=1+(1-a**2)**0.5
    myRin=rhor
    #
    #
    if logvalue==1:
        fun0 = np.log10(np.fabs(qty)+1E-30)
    else:
        fun0 = np.copy(qty)
    #
    if maxbsqorho is not None or maxbsqou is not None:
        (mintoplot,maxtoplot)=setminmax4mk(logvalue=logvalue,fun0=fun0,myRout=myRout,which=1,bsqorho=bsqorho,bsqou=bsqou,maxbsqorho=maxbsqorho,maxbsqou=maxbsqou)
        #
        # modify fun0 based upon bsqorho or bsqou
        if maxbsqorho is not None:
            fun0[bsqorho>maxbsqorho]=mintoplot
        if maxbsqou is not None:
            fun0[bsqou>maxbsqou]=mintoplot
        #
    #
    (mintoplot,maxtoplot)=setminmax4mk(logvalue=logvalue,fun0=fun0,myRout=myRout,which=1)
    # ignore nans in any case
    fun0[np.isnan(fun0)==1]=mintoplot
    #
    #
    #
    #
    #
    r1dold=r[:,0,0]
    sx11=np.log(myRin)
    dx11=np.log(myRout/myRin)/len(ti[:,0,0])
    x1d=sx11+ti[:,0,0]*dx11
    r1d=np.exp(x1d)
    t1d=ts
    #
    #fun = sp.interpolate.interp2d(r1dold, t1d, fun0)
    #,kind='cubic')
    # 2d interp above doesn't seem to work right, so do line-by-line 1d interp since only radius changes positions (same number of elements, though)
    #funnew=fun(r1d,t1d)
    sizet=len(ts)
    funnew=np.zeros((sizet,nx),dtype=r.dtype)
    fold=np.zeros(nx,dtype=r.dtype)
    #
    for tic in ts:
        tici=np.where(ts==tic)[0]
        xold=r[:,0,0]
        xnew=r1d
        fold=fun0[tici,:]
        if len(fold)==1:
            fold=fold[0]
        #print("AS")
        #print(xnew)
        #print(xold)
        #print(fold)
        funnew[tici,:]=np.interp(xnew,xold,fold)
    toplot=funnew
    #extent=(np.log10(myRin),np.log10(myRout),ts[0],ts[-1])
    # assume plot shows in log
    extent=(myRin,myRout,ts[0],ts[-1])
    #
    #
    #
    print("mktr: num=%d let=%s" % (filenum,fileletter)) ; sys.stdout.flush()
    setupframe(which=1,gs=3)
    finishframe(which=1,toplot=toplot,extent=extent,cb=1,tight=1,useextent=1,uselim=1,label=1,mintoplot=mintoplot,maxtoplot=maxtoplot,filenum=filenum,fileletter=fileletter,pllabel=pllabel,maxbsqorho=maxbsqorho,maxbsqou=maxbsqou)
    #


def mkthrad(loadq=1,qty=None,filenum=1,fileletter="a",logvalue=1,radius=4,pllabel="",bsqorho=None,bsqou=None,maxbsqorho=None,maxbsqou=None):
    #
    hin=0
    hout=np.pi
    #
    #
    if logvalue==1:
        fun0 = np.log10(np.fabs(qty)+1E-30)
    else:
        fun0 = qty
    #
    if maxbsqorho is not None or maxbsqou is not None:
        (mintoplot,maxtoplot)=setminmax4mk(logvalue=logvalue,fun0=fun0,which=2,bsqorho=bsqorho,bsqou=bsqou,maxbsqorho=maxbsqorho,maxbsqou=maxbsqou)
        #
        # modify fun0 based upon bsqorho or bsqou
        if maxbsqorho is not None:
            fun0[bsqorho>maxbsqorho]=mintoplot
            print("mkthrad: maxbsqorho=%g" % (maxbsqorho)) ; sys.stdout.flush()
        if maxbsqou is not None:
            fun0[bsqou>maxbsqou]=mintoplot
            print("mkthrad: maxbsqou=%g" % (maxbsqou)) ; sys.stdout.flush()
        #
    #
    (mintoplot,maxtoplot)=setminmax4mk(logvalue=logvalue,fun0=fun0,which=2)
    #
    # ignore nans in any case
    fun0[np.isnan(fun0)==1]=mintoplot
    #
    #
    irad=iofr(radius)
    # get nx-sized original h
    xold=(tj[0,:,0]-tj[0,0,0])/(tj[0,-1,0]-tj[0,0,0])
    xnew=(ti[:,0,0]-ti[0,0,0])/(ti[-1,0,0]-ti[0,0,0])
    hnx=np.interp(xnew,xold,h[irad,:,0])
    #
    # now interpolate to uniform-in-log radial grid
    #j1d=(tj[irad,:,0]-tj[irad,0,0])/(tj[irad,-1,0]-tj[irad,0,0])
    j1dnx=xnew
    h1d=hin+(hout-hin)*j1dnx
    #print("h1d")
    #print(h1d)
    #print("hnx")
    #print(hnx)
    #
    t1d=ts
    #
    ###############
    # interpolation from xold (using y-dimension) to xnew (using x-dimension) so that same plotting function can be used
    #
    # cubic is too aggressive at smoothing in radius if unresolved in time
    #fun = sp.interpolate.interp2d(hnx, t1d, fun0) #,kind='cubic')
    #funnew=fun(h1d,t1d)
    #toplot=funnew
    # 2d interp doesn't work, so do line-by-line
    sizet=len(ts)
    funnew=np.zeros((sizet,nx),dtype=r.dtype)
    fold=np.zeros(nx,dtype=r.dtype)
    #
    for tic in ts:
        tici=np.where(ts==tic)[0]
        xold=hnx
        xnew=h1d
        fold=fun0[tici,:]
        if len(fold)==1:
            fold=fold[0]
        #print("AS")
        #print(xnew)
        #print(xold)
        #print(fold)
        funnew[tici,:]=np.interp(xnew,xold,fold)
    toplot=funnew
    extent=(hin,hout,ts[0],ts[-1])
    #
    #
    print("mkthrad (radius=%g): num=%d let=%s" % (radius,filenum,fileletter)) ; sys.stdout.flush()
    #
    #
    setupframe(which=2,gs=3)
    finishframe(which=2,toplot=toplot,extent=extent,cb=1,tight=1,useextent=1,uselim=1,label=1,mintoplot=mintoplot,maxtoplot=maxtoplot,filenum=filenum,fileletter=fileletter,pllabel=pllabel,maxbsqorho=maxbsqorho,maxbsqou=maxbsqou,radius=radius)
    #


def mainfunc(imgname):
    global xi,yi,zi,CS
    #grid3d("gdump")
    #rfd("fieldline0250.bin")
    xraw=r*np.sin(h)
    yraw=r*np.cos(h)
    lrhoraw=np.log10(rho)
    x=xraw[:,:,0].view().reshape(-1)
    y=yraw[:,:,0].view().reshape(-1)
    lrho=lrhoraw[:,:,0].view().reshape(-1)
    #mirror
    x=np.concatenate((-x,x))
    y=np.concatenate((y,y))
    lrho=np.concatenate((lrho,lrho))
    extent=(-41,41,-41,41)
    # define grid.
    xi = np.linspace(-41.0, 41.0, 800)
    yi = np.linspace(-41.0, 41.0, 800)
    # grid the data.
    zi = griddata((x, y), lrho, (xi[None,:], yi[:,None]), method='cubic')
    interior = np.sqrt((xi[None,:]**2) + (yi[:,None]**2)) < 1+np.sqrt(1-a**2)
    #zi[interior] = np.ma.masked
    zim = ma.masked_where(interior, zi)
    palette=cm.jet
    palette.set_bad('k', 1.0)
    palette.set_over('r', 1.0)
    palette.set_under('g', 1.0)
    # contour the gridded data, plotting dots at the randomly spaced data points.
    cset2 = plt.contour(zi,15,linewidths=0.5,colors='k', extent=extent,hold='on',origin='lower')
    #for c in cset2.collections:
    #    c.set_linestyle('solid')
    #CS = plt.contourf(xi,yi,zi,15,cmap=palette)
    #CS = plt.imshow(zim, extent=[0.01,80,-40,40], cmap = palette, norm = colors.Normalize(vmin=-1,vmax=-0.2,clip = False))
    CS = plt.imshow(zim, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower')
    #CS.cmap=cm.jet
    #CS.set_axis_bgcolor("#bdb76b")
    plt.colorbar(CS) # draw colorbar
    plt.xlim(-40,40)
    plt.ylim(-40,40)
    plt.title('t = %f' % t)
    #plt.show()
    # rbf = Rbf(x[0:288:8,:,0].view().reshape(-1),y[0:288:8,:,0].view().reshape(-1),rho[0:288:8,:,0].view().reshape(-1),epsilon=2)
    # ZI = rbf( XI, YI )
    # # plot the result
    # n = plt.normalize(0.0, 40.0)
    # plt.subplot(1, 1, 1)
    # plt.imshow(XI, YI, ZI, cmap=cm.jet)
    # #plt.scatter(x, y, 100, z, cmap=cm.jet)
    # plt.title('RBF interpolation - multiquadrics')
    # plt.xlim(0, 40.0)
    # plt.ylim(0, 40.0)
    # plt.colorbar()
    # plt.figure()
    # plt.plot(r[:,0,0],np.log10(absflux),'b')
    # plt.legend(['Grid'])
    # plt.axis([r[0,0,0],100,-5,5])
    # plt.title('Grid plot')
    # plt.show()


def ravg(dumpname):
    global t,nx,ny,nz,_dx1,_dx2,_dx3,gam,a,Rin,Rout,avgU,avgTud10
    #read image
    ilist=np.array([128,144,160,176,192,208,224])
    for (j,i) in enumerate(ilist):
        fin = open( "dumps/%s-col%04d" % ( dumpname, i ) , "rb" )
        print("Reading %s-col%04d..." % (dumpname,i) ) ; sys.stdout.flush()
        header = fin.readline().split()
        t = myfloat(np.float64(header[0]))
        nx = int(header[1])
        ny = int(header[2])
        nz = int(header[3])
        if j == 0:
            avgU=np.zeros((ilist.shape[0],nx,ny,nz),dtype=np.float32)
        _dx1=myfloat(float(header[7]))
        _dx2=myfloat(float(header[8]))
        _dx3=myfloat(float(header[9]))
        gam=myfloat(float(header[11]))
        a=myfloat(float(header[12]))
        Rin=myfloat(float(header[14]))
        Rout=myfloat(float(header[15]))
        if dumpname.endswith(".bin"):
            body = np.fromfile(fin,dtype=np.float64,count=-1)  #nx*ny*nz*11)
            gd = body.view().reshape((-1,nx,ny,nz),order='F')
            fin.close()
        else:
            fin.close()
            gd = np.loadtxt( "dumps/"+dumpname, 
                          dtype=np.float64, 
                          skiprows=1, 
                          unpack = True ).view().reshape((-1,nx,ny,nz), order='F')
        #print np.max(gd)
        avgU[j:j+1] = gd[:,:,:,:].view() 
    avgTud10=avgU.sum(axis=0)
    return

def computeavg(qty):
    avgqty=intangle(gdet*qty)
    return(avgqty)

def doall():
    grid3d("gdump.bin",use2d=True)
    
    if np.abs(a - 0.99)<1e-4 and scaletofullwedge(1.0) < 1.5:
        #lo-res 0.99 settings
        print( "Using hires a = 0.99 settings")
        ilist=np.arange(221,286)
        dtlist=100.+0*ilist
        dtlist[ilist==221]=22200-22167.6695855045
        dtlist[ilist==222]=22300-22231.9647756934
        dtlist[ilist==228]=22900-22890.8671337456
        dtlist[ilist==232]=23300-23292.5857662206
        dtlist[ilist==239]=24000-23951.5226133435
        dtlist[ilist==245]=24600-24594.4658011928
        dtlist[ilist==251]=25200-25124.6341346588
        dtlist[ilist==257]=25800-25799.8775611997
        dtlist[ilist==263]=26400-26330.0889135128
        dtlist[ilist==267]=26800-26763.9946654502
        dtlist[ilist==274]=27500-27406.4732593203
        dtlist[ilist==280]=28100-28097.4708711805
    elif np.abs(a - 0.99)<1e-4 and scaletofullwedge(1.0) > 1.5:
        #lo-res 0.99 settings
        print( "Using lores a = 0.99 settings")
        ilist=np.arange(120,137)
        dtlist=100.+0*ilist

    print dtlist 

    for (j,i) in enumerate(ilist):
        dt=dtlist[j]
        ravg("avg%04d.bin" % i)
        if j == 0:
            FE=computeavg(avgTud10)*dt
        else:
            FE+=computeavg(avgTud10)*dt
    #get time average by dividing by the total averaging time
    FE /= dtlist.sum()
    np.save("fe.npy",FE)
    plt.clf()
    plt.plot(r[:,0,0],FE); 
    plt.xlim(rhor,20)
    plt.ylim(-15,15)

def rfloor(dumpname):
    global t,nx,ny,nz,_dx1,_dx2,_dx3,gam,a,Rin,Rout,dUfloor
    #read image
    fin = open( "dumps/" + dumpname, "rb" )
    print("Reading %s..." % dumpname)
    header = fin.readline().split()
    t = np.float64(header[0])
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    _dx1=float(header[7])
    _dx2=float(header[8])
    _dx3=float(header[9])
    gam=float(header[11])
    a=float(header[12])
    Rin=float(header[14])
    Rout=float(header[15])
    if dumpname.endswith(".bin"):
        body = np.fromfile(fin,dtype=np.float64,count=-1)  #nx*ny*nz*11)
        gd = body.view().reshape((-1,nx,ny,nz),order='F')
        fin.close()
    else:
        fin.close()
        gd = np.loadtxt( "dumps/"+dumpname, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True ).view().reshape((-1,nx,ny,nz), order='F')
    dUfloor = gd[:,:,:,:].view() 
    return

#
#Thanks, I like your approach for its simplicity (avoiding A_i).  I checked your code and it seems to make sense.  I'm not sure why you were reading in primitives, computing the ZAMO stuff, and then not using them.  Maybe you can comment on that?
#
#Actually, one doesn't even have to run things over each dimension.  As you probably knew, that lowest order averaging only acts on each field independently in the divb=0 expression.  So one can change all 3 fields at the same time.  Every new position along some direction (e.g. B1 along 1-dir) is averaged, while every other direction (e.g. B1 along 2-dir) is simply copied in the even-odd way you already do.  So the only new step is to duplicate the last few lines in your code to act on the other 2 fields -- and of course one should change the new resolution as appropriate.
#
#I think the only restriction is that one must increase the grid by factors of 2^n in each dimension.
#
#I think you assumed (with is sufficient) that the non-field conserved quantities aren't used for the non-higher-order STAG method, right?  As we talked before as related to floor U diagnostics, the conserved quantities are constantly being reconstructed.  Even upon restarting, the advance step still avoids using the read-in ucum->ui and just uses the currently-computed Uitemp->ui for non-field quantities.  But field quantities do use ucum->ui.
#
#The only issue is that the Uitemp comes from primitives that include the centered fields.  So if you only copy over the centered fields, they won't be entirely consistent with what the interpolated stag->cent fields would have given.  But this is only a truncation level error and only occurs over 1 full step (4 substeps).  I think that's not worth fixing.
#
# just do (e.g.):
# 1) put file in dumps/rdump-0.bin
# 2) and file in dumps/fieldline*.bin (just 1 file needed -- any file number)
# 3) ipython ~/py/mread/__init__.py
# 4) reresrdump('rdump-0.bin',writenew=1,newf1=2,newf2=2,newf3=2)
#
# only works for 1 or 2 for newf? for now
def reresrdump(dumpname,writenew=False,newf1=None,newf2=None,newf3=None):
    global nx,ny,nz,t,a,rho,ug,vu,vd,B,gd,gd1,numcols,gdetB
    #print( "Reading " + "dumps/" + dumpname + " ..." )
    gin = open( "dumps/" + dumpname, "rb" )
    header = gin.readline().split()
    nx = int(header[0])
    ny = int(header[1])
    nz = int(header[2])
    t  = float(header[3])
    a  = float(header[6])
    #nx+=8
    #ny+=8
    #nz+=8
    if dumpname.endswith(".bin"):
        body = np.fromfile(gin,dtype=np.float64,count=-1)  #nx*ny*nz*11)
        gdraw = body
        gin.close()
    else:
        gin.close()
        gdraw = np.loadtxt( "dumps/"+dump, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True )
    gd=gdraw.view().reshape((-1,nx,ny,nz), order='F')
    rho,ug = gd[0:2,:,:,:].view() 
    B = np.zeros_like(gd[4:8])
    vu = np.zeros_like(B)
    vu[1:4] = gd[2:5].view() #relative 4-velocity only has non-zero spatial components
    B[1:4] = gd[5:8].view()
    numcols = gd.shape[0]  #total number of columns is made up of (n prim vars) + (n cons vars) = numcols
    gdetB = np.zeros_like(B)
    gdetB[1:4] = gd[numcols/2+5:numcols/2+5+3]  #gdetB starts with 5th conserved variable
    if 'gv3' in globals() and 'gn3' in globals(): 
        vd = mdot(gv3,vu)
        gamma = (1+mdot(mdot(gv3,vu),vu))**0.5
        etad = np.zeros_like(vu)
        etad[0] = -1/(-gn3[0,0])**0.5      #ZAMO frame velocity (definition)
        etau = mdot(gn3,etad)
        uu = gamma * etau + vu
        ud = mdot(gv3,uu)
    else:
        print( 'Metric (gv3, gn3) not defined, I am skipping the computation of uu and ud' )
    if writenew:
        print( "Writing out new rdump...", ) ; sys.stdout.flush()
        #write out a dump with twice as many cells in phi-direction:
        gout = open( "dumps/" + dumpname + "%d.%d.%d" % (newf1,newf2,newf3), "wb")
        #double the number of phi-cells
        newnx=newf1*nx
        newny=newf2*ny
        newnz=newf3*nz
        header[0] = "%d" % (newnx)
        header[1] = "%d" % (newny)
        header[2] = "%d" % (newnz)
        for headerel in header:
            s = "%s " % headerel
            gout.write( s )
        #
        # assume DOGRIDSECTIONING==0 and don't care about DOLUMVSR==1 or DODISSVSR==1.  Need (newnx-nx)*(1+18) zeros.
        NUMDISSVERSIONS=18
        for tic in np.arange(0,(newnx-nx)*(1+NUMDISSVERSIONS)):
            s = " 0 "
            gout.write( s )
        #
        gout.write( "\n" )
        gout.flush()
        os.fsync(gout.fileno())
        #reshape the rdump content
        gd1 = gdraw.view().reshape((nz,ny,nx,-1),order='C')
        #allocate memory for refined grid, nz' = 2*nz
        gd2 = np.zeros((newnz,newny,newnx,numcols),order='C',dtype=np.float64)
        #
        gdetB1index = numcols/2+5+0
        gdetB2index = numcols/2+5+1
        gdetB3index = numcols/2+5+2
        #################
        # First, copy every old index -> new same 2*index and new 2*index+1
        #
        #copy kji both even and odds
        for kst in np.arange(0,newf3):
            for jst in np.arange(0,newf2):
                for ist in np.arange(0,newf1):
                    gd2[kst::newf3,jst::newf2,ist::newf1,:] = gd1[:,:,:,:]
                #
            #
        #
        ####################
        # Second, in the new cells, adjust gdetB[1,2,3] along 1,2,3 direction to be averages of immediately adjacent cells (this ensures divb=0)
        #
        #
        if 1==0:
         for kst in np.arange(0,newf3):
            for jst in np.arange(0,newf2):
                gd2[kst::newf3,jst::newf2,1:-1:newf1,gdetB1index] = 0.5*(gd1[:,:,:-1,gdetB1index]+gd1[:,:,1:,gdetB1index])
                # fake setting of last radial B1 value somehow since don't have enough data to average locally (would need ti+1 staggered value)
                gd2[kst::newf3,jst::newf2,-1,gdetB1index] = 0.5*(gd1[:,:,-1,gdetB1index]+gd1[:,:,-1,gdetB1index])
         #
         for kst in np.arange(0,newf3):
            for ist in np.arange(0,newf1):
                gd2[kst::newf3,1:-1:newf2,ist::newf1,gdetB2index] = 0.5*(gd1[:,:-1,:,gdetB2index]+gd1[:,1:,:,gdetB2index])
                # use assumed reflective condition to set last value (i.e. B2[tj]=0)
                gd2[kst::newf3,-1,ist::newf1,gdetB2index] = 0.0
         #
         for jst in np.arange(0,newf2):
            for ist in np.arange(0,newf1):
                gd2[1:-1:newf3,jst::newf2,ist::newf1,gdetB3index] = 0.5*(gd1[:-1,:,:,gdetB3index]+gd1[1:,:,:,gdetB3index])
                # use assumed periodicity in \phi to set last value (i.e. B3[tk]=B3[0]).  gdet and metric are same since metric also periodic.
                gd2[-1,jst::newf2,ist::newf1,gdetB3index] = 0.5*(gd1[0,:,:,gdetB3index]+gd1[-1,:,:,gdetB3index])
        elif 1==1:
            # better way -- use gd2 directly
            gd2[:,:,1:newnx-2:newf1,gdetB1index] = 0.5*(gd2[:,:,0:newnx-3:newf1,gdetB1index]+gd2[:,:,2:newnx-1:newf1,gdetB1index])
            # fake setting of last radial B1 value somehow since don't have enough data to average locally (would need ti+1 staggered value)
            gd2[:,:,-1,gdetB1index] = gd2[:,:,-2,gdetB1index]
            #
            gd2[:,1:newny-2:newf2,:,gdetB2index] = 0.5*(gd2[:,0:newny-3:newf2,:,gdetB2index]+gd2[:,2:newny-1:newf2,:,gdetB2index])
            # use assumed reflective condition to set last value (i.e. B2[tj]=0)
            #gd2[:,0,:,gdetB2index] = 0.0
            gd2[:,-1,:,gdetB2index] = 0.5*(gd2[:,-2,:,gdetB2index]+0.0)
            #
            gd2[1:newnz-2:newf3,:,:,gdetB3index] = 0.5*(gd2[0:newnz-3:newf3,:,:,gdetB3index]+gd2[2:newnz-1:newf3,:,:,gdetB3index])
            # use assumed periodicity in \phi to set last value (i.e. B3[tk]=B3[0]).  gdet and metric are same since metric also periodic.
            gd2[-1,:,:,gdetB3index] = 0.5*(gd2[0,:,:,gdetB3index]+gd2[-2,:,:,gdetB3index])
        #
        # check divbB=0 for old and new data, but need dx[1,2,3] for that, so get header from a fieldline file.
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
        if len(flist)>0:
            firstfieldlinefile=flist[0]
            rfdheaderonly(firstfieldlinefile)
            # gdet needed to normalize divb
            #grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]), use2d=True )
            #
            # OLD:
            divbcentold1=(gd1[0:nz-1,0:ny-1,1:nx  ,gdetB1index]-gd1[0:nz-1,0:ny-1,0:nx-1,gdetB1index])/_dx1
            divbcentold2=(gd1[0:nz-1,1:ny  ,0:nx-1,gdetB2index]-gd1[0:nz-1,0:ny-1,0:nx-1,gdetB2index])/_dx2
            divbcentold3=(gd1[1:nz  ,0:ny-1,0:nx-1,gdetB3index]-gd1[0:nz-1,0:ny-1,0:nx-1,gdetB3index])/_dx3
            #
            adivbcentold1=(np.fabs(gd1[0:nz-1,0:ny-1,1:nx  ,gdetB1index])+np.fabs(gd1[0:nz-1,0:ny-1,0:nx-1,gdetB1index]))/_dx1
            adivbcentold2=(np.fabs(gd1[0:nz-1,1:ny  ,0:nx-1,gdetB2index])+np.fabs(gd1[0:nz-1,0:ny-1,0:nx-1,gdetB2index]))/_dx2
            adivbcentold3=(np.fabs(gd1[1:nz  ,0:ny-1,0:nx-1,gdetB3index])+np.fabs(gd1[0:nz-1,0:ny-1,0:nx-1,gdetB3index]))/_dx3
            #
            divbcentold=divbcentold1+divbcentold2+divbcentold3
            olddimens=(nx>1)+(ny>1)+(nz>1)
            adivbcentold=(adivbcentold1+adivbcentold2+adivbcentold3)/olddimens
            divbcentoldavg=np.average(np.fabs(divbcentold/adivbcentold))
            divbcentoldmax=np.max(np.fabs(divbcentold/adivbcentold))
            print("divbcentoldavg=%g divbcentoldmax=%g" % (divbcentoldavg,divbcentoldmax)) ; sys.stdout.flush()
            #badi=np.where(np.fabs(fabs[ivalue,:])==np.max(np.fabs(fabs[ivalue,:])))[0]
            badijk=np.where(divbcentoldmax==np.fabs(divbcentold/adivbcentold))
            print("badijk") ; sys.stdout.flush()
            print(badijk) ; sys.stdout.flush()

            #
            # NEW (old->new, gd1->gd2, n? -> newn?, _dx? -> (0.5*_dx?) )
            divbcentnew1=(gd2[0:newnz-1,0:newny-1,1:newnx  ,gdetB1index]-gd2[0:newnz-1,0:newny-1,0:newnx-1,gdetB1index])/(0.5*_dx1)
            divbcentnew2=(gd2[0:newnz-1,1:newny  ,0:newnx-1,gdetB2index]-gd2[0:newnz-1,0:newny-1,0:newnx-1,gdetB2index])/(0.5*_dx2)
            divbcentnew3=(gd2[1:newnz  ,0:newny-1,0:newnx-1,gdetB3index]-gd2[0:newnz-1,0:newny-1,0:newnx-1,gdetB3index])/(0.5*_dx3)
            #
            adivbcentnew1=(np.fabs(gd2[0:newnz-1,0:newny-1,1:newnx  ,gdetB1index])+np.fabs(gd2[0:newnz-1,0:newny-1,0:newnx-1,gdetB1index]))/(0.5*_dx1)
            adivbcentnew2=(np.fabs(gd2[0:newnz-1,1:newny  ,0:newnx-1,gdetB2index])+np.fabs(gd2[0:newnz-1,0:newny-1,0:newnx-1,gdetB2index]))/(0.5*_dx2)
            adivbcentnew3=(np.fabs(gd2[1:newnz  ,0:newny-1,0:newnx-1,gdetB3index])+np.fabs(gd2[0:newnz-1,0:newny-1,0:newnx-1,gdetB3index]))/(0.5*_dx3)
            #
            newdimens=(newnx>1)+(newny>1)+(newnz>1)
            divbcentnew=divbcentnew1+divbcentnew2+divbcentnew3
            adivbcentnew=(adivbcentnew1+adivbcentnew2+adivbcentnew3)/newdimens
            divbcentnew[:,:,newnx-2]=0
            divbcentnewavg=np.average(np.fabs(divbcentnew/adivbcentnew))
            divbcentnewmax=np.max(np.fabs(divbcentnew/adivbcentnew))
            print("divbcentnewavg=%g divbcentnewmax=%g" % (divbcentnewavg,divbcentnewmax))
            #
        else:
            print("No fieldline file to check divb=0") ; sys.stdout.flush()
            #
        #
        gd2.tofile(gout)
        gout.close()
        print( " done!" ) ; sys.stdout.flush()





      

def fieldcalctoth():
    """
    Computes the field vector potential
    """
    daphi = -(gdetB[1]).sum(-1)*_dx2/nz
    aphi=daphi[:,::-1].cumsum(axis=1)[:,::-1]
    aphi-=0.5*daphi #correction for half-cell shift between face and center in theta
    return(aphi)

# pure 2D version   
def fieldcalcU2D(gdetB1=None):
    """
    Computes cell-centered vector potential
    """
    aphi=fieldcalcface(gdetB1)
    #center it properly in theta
    aphi[:,0:ny-1]=0.5*(aphi[:,0:ny-1]+aphi[:,1:ny]) 
    #special treatment for last cell since no cell at j = ny, and we know aphi[:,ny] should vanish
    aphi[:,ny-1] *= 0.5
    #and in r
    aphi[0:nx-1] = 0.5*(aphi[0:nx-1]  +aphi[1:nx])
    aphi/=(nz*_dx3)
    return(aphi)

def fieldcalcface(gdetB1=None):
    """
    Computes the field vector potential
    """
    global aphi
    if gdetB1 == None:
        gdetB1 = gdetB[1]
    #average in phi and add up
    daphi = (gdetB1).sum(-1)[:,:,None]/nz*_dx2
    aphi = np.zeros_like(daphi)
    aphi[:,1:ny/2+1]=(daphi.cumsum(axis=1))[:,0:ny/2]
    #sum up from the other pole
    aphi[:,ny/2+1:ny]=(-daphi[:,::-1].cumsum(axis=1))[:,::-1][:,ny/2+1:ny]
    return(aphi)


def fieldcalcU(gdetB1=None):
    # 3D wacky in time-dep flow
    #aphi=fieldcalcU3D(gdetB1=gdetB1)
    # below stable but doesn't match flow
    aphi=fieldcalcU2D(gdetB1=gdetB1)
    # below compomises
    #aphi=fieldcalcU3Davg(gdetB1=gdetB1)
    return(aphi)


def rolling_window(a, window):
    """
    Make an ndarray with a rolling window of the last dimension

    Parameters
    ----------
    a : array_like
        Array to add rolling window to
    window : int
        Size of rolling window

    Returns
    -------
    Array that is a view of the original array with a added dimension
    of size w.

    Examples
    --------
    >>> x=np.arange(10).reshape((2,5))
    >>> rolling_window(x, 3)
    array([[[0, 1, 2], [1, 2, 3], [2, 3, 4]],
           [[5, 6, 7], [6, 7, 8], [7, 8, 9]]])

    Calculate rolling mean of last dimension:
    >>> np.mean(rolling_window(x, 3), -1)
    array([[ 1.,  2.,  3.],
           [ 6.,  7.,  8.]])

    """
    if window < 1:
        raise ValueError, "`window` must be at least 1."
    if window > a.shape[-1]:
        raise ValueError, "`window` is too long."
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)



#def fieldcalcU3Davg(gdetB1=None):
#    aphi=fieldcalcU3D(gdetB1=gdetB1)
#    # now average such that plot in z-x plane shows averaged behavior but not entirely full \phi-averaged.  Average over \pi/2
#    aphi=
#    return(aphi)

# 3D version
def fieldcalcU3D(gdetB1=None):
    global aphi
    if gdetB1 == None:
        gdetB1 = gdetB[1]
    #
    # get result for each k
    aphi = np.zeros_like(gdetB1)
    daphi = gdetB1*_dx2
    aphi[:,1:ny/2+1,:]=(daphi.cumsum(axis=1))[:,0:ny/2,:]
    #sum up from the other pole
    aphi[:,ny/2+1:ny,:]=(-daphi[:,::-1,:].cumsum(axis=1))[:,::-1,:][:,ny/2+1:ny,:]
    #
    #center it properly in theta
    aphi[:,0:ny-1,:]=0.5*(aphi[:,0:ny-1,:]+aphi[:,1:ny,:]) 
    #special treatment for last cell since no cell at j = ny, and we know aphi[:,ny] should vanish
    aphi[:,ny-1,:] *= 0.5
    #and in r
    aphi[0:nx-1,:] = 0.5*(aphi[0:nx-1,:]  +aphi[1:nx,:])
    #
    return(aphi)



def fieldcalcface2():
    """
    Computes the field vector potential
    """
    daphi = np.sum(gdetB[2], axis=2)[:,:,None]*_dx1*_dx3
    aphi=daphi.cumsum(axis=0)
    aphi-=daphi #correction for half-cell shift between face and center in theta
    #aphi[0:nx-1] = 0.5*(aphi[0:nx-1]+aphi[1:nx]) #and in r
    aphi/=(nz*_dx3)
    return(aphi)

def rdo(dump,oldfmt=False):
    """ Read in old dump format """
    rd(dump,oldfmt=True)

def rd(dump,oldfmt=False):
    global t,nx,ny,nz,_dx1,_dx2,_dx3,gam,a,Rin,Rout,ti,tj,tk,x1,x2,x3,r,h,ph,rho,ug,vu,B,pg,cs2,Sden,U,gdetB,divb,uu,ud,bu,bd
    global v1m,v1p,v2m,v2p,v3m,v3p,bsq,olddumpfmt
    #read image
    olddumpfmt = oldfmt
    fin = open( "dumps/" + dump, "rb" )
    header = fin.readline().split()
    t = myfloat(np.float64(header[0]))
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    _dx1=myfloat(float(header[7]))
    _dx2=myfloat(float(header[8]))
    _dx3=myfloat(float(header[9]))
    gam=myfloat(float(header[11]))
    a=myfloat(float(header[12]))
    Rin=myfloat(float(header[14]))
    Rout=myfloat(float(header[15]))
    if dump.endswith(".bin"):
        body = np.fromfile(fin,dtype=np.float64,count=-1)  #nx*ny*nz*11)
        gd = body.view().reshape((-1,nx,ny,nz),order='F')
        fin.close()
    else:
        fin.close()
        gd = np.loadtxt( "dumps/"+dump, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True ).view().reshape((-1,nx,ny,nz), order='F')
    gd=myfloat(gd)
    gc.collect()
    ti,tj,tk,x1,x2,x3,r,h,ph,rho,ug = gd[0:11,:,:,:].view() 
    vu=np.zeros_like(gd[0:4])
    B=np.zeros_like(gd[0:4])
    vu[1:4] = gd[11:14]
    B[1:4] = gd[14:17]
    if not oldfmt:
        pg,cs2,Sden = gd[17:20]
        U = gd[20:29]
        gdetB = np.zeros_like(B)
        gdetB[1:4] = U[5:8]
        divb = gd[29]
        uu = gd[30:34]
        ud = gd[34:38]
        bu = gd[38:42]
        bd = gd[42:46]
        bsq = mdot(bu,bd)
        v1m,v1p,v2m,v2p,v3m,v3p=gd[46:52]
        gdet=gd[53]
    else:
        U = gd[17:25]
        divb = gd[25]
        uu = gd[26:30]
        ud = gd[30:34]
        bu = gd[34:38]
        bd = gd[38:42]
        bsq = mdot(bu,bd)
        v1m,v1p,v2m,v2p,v3m,v3p=gd[42:48]
        gdet=gd[48]
        #gdetB = np.zeros_like(B)
        #gdetB[1:4] = U[5:8]
        gdetB = gdet*B

def rgfd(fieldlinefilename,**kwargs):
    if not os.path.isfile(os.path.join("dumps/", fieldlinefilename)):
        print( "File " + fieldlinefilename + " does not exist. Aborting." )
        return
    if 'gv3' not in globals():
        gdumpname = glob.glob( os.path.join("dumps/", "gdump*") )
        #read the 1st found file
        grid3d(os.path.basename(gdumpname[0]))
    rfd(fieldlinefilename,**kwargs)
    cvel()


#  http://norvig.com/python-lisp.html   

def rfdheader():
    global t,nx,ny,nz,_dx1,_dx2,_dx3,gam,a,Rin,Rout
    header = fin.readline().split()
    #time of the dump
    t = myfloat(np.float64(header[0]))
    print("rfdheader: t=%g" % (t)) ; sys.stdout.flush()
    #dimensions of the grid
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    #cell size in internal coordintes
    _dx1=myfloat(float(header[7]))
    _dx2=myfloat(float(header[8]))
    _dx3=myfloat(float(header[9]))
    #other information: 
    #polytropic index
    gam=myfloat(float(header[11]))
    #black hole spin
    a=myfloat(float(header[12]))
    rhor = 1+(1-a**2)**0.5
    #Spherical polar radius of the innermost radial cell
    Rin=myfloat(float(header[14]))
    #Spherical polar radius of the outermost radial cell
    Rout=myfloat(float(header[15]))

def rfdheaderonly(fullfieldlinefilename="dumps/fieldline0000.bin"):
    global fin
    fin = open(fullfieldlinefilename, "rb" )
    rfdheader()
    fin.close()

def rfdheaderfirstfile():
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    firstfieldlinefile=flist[0]
    #rfd("fieldline0000.bin")  #to definea
    rfdheaderonly(firstfieldlinefile)


def rfdfirstfile():
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    firstfieldlinefile=flist[0]
    basenamefirst=os.path.basename(firstfieldlinefile)
    rfd(basenamefirst)

def rfdlastfile():
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    lastfieldlinefile=flist[-1]
    basenamelast=os.path.basename(lastfieldlinefile)
    rfd(basenamelast)


def rfd(fieldlinefilename,**kwargs):
    #read information from "fieldline" file: 
    #Densities: rho, u, 
    #Velocity components: u1, u2, u3, 
    #Cell-centered magnetic field components: B1, B2, B3, 
    #Face-centered magnetic field components multiplied by metric determinant: gdetB1, gdetB2, gdetB3
    global rho,lrho,ug,uu,uut,uu,B,uux,gdetB,rhor,r,h,ph,rhoclean,rhounclean,ugclean,ugunclean,uuclean,entropy
    global maxbsqorhonear,maxbsqorhofar,condmaxbsqorho,condmaxbsqorhorhs,rinterp
    #
    #read image
    global fin
    #
    #
    fin = open( "dumps/" + fieldlinefilename, "rb" )
    rfdheader()
    #
    #read grid dump per-cell data
    #
    if(0):
        # new way
        # http://www.mail-archive.com/numpy-discussion@scipy.org/msg07631.html
        # http://docs.scipy.org/doc/numpy/reference/generated/numpy.memmap.html
        # still doesn't quite work once beyond this function!
        numcolumns=int(header[29])
        from numpy import memmap
        d = np.memmap(fin, dtype='float32', mode='c', shape=(numcolumns,nx,ny,nz),order='F')
    #
    else:
        # old way:
        body = np.fromfile(fin,dtype=np.float32,count=-1)
        #body = np.load(fin,dtype=np.float32,count=-1)
        d=body.view().reshape((-1,nx,ny,nz),order='F')
        del(body)
    #
    #rho, u, -hu_t, -T^t_t/U0, u^t, v1,v2,v3,B1,B2,B3
    #matter density in the fluid frame
    rho=np.zeros((1,nx,ny,nz),dtype='float32',order='F')
    rho=d[0,:,:,:]
    lrho=np.zeros((1,nx,ny,nz),dtype='float32',order='F')
    lrho = np.log10(rho)
    #matter internal energy in the fluid frame
    ug=np.zeros((1,nx,ny,nz),dtype='float32',order='F')
    ug=d[1,:,:,:]
    #d[4] is the time component of 4-velocity, u^t
    #d[5:8] are 3-velocities, v^i
    uu=np.zeros((4,nx,ny,nz),dtype='float32',order='F')
    uu=d[4:8,:,:,:]  #again, note uu[i] are 3-velocities (as read from the fieldline file)
    #multiply by u^t to get 4-velocities: u^i = u^t v^i
    uu[1:4]=uu[1:4] * uu[0]
    #B = np.zeros_like(uu)
    #cell-centered magnetic field components
    #B[1:4,:,:,:]=d[8:11,:,:,:]
    # start at 7 so B[1] is correct.  7=<ignore> 8=B[1] 9=B[2] 10=B[3]
    # below assumes B[0] is never needed
    B=np.zeros((4,nx,ny,nz),dtype='float32',order='F')
    B=d[7:11,:,:,:]
    #if the input file contains additional data
    #
    if(d.shape[0]>=14): 
        #new image format additionally contains gdet*B^i
        #face-centered magnetic field components multiplied by gdet
        # below assumes gdetB[0] is never needed
        gdetB=np.zeros((4,nx,ny,nz),dtype='float32',order='F')
        gdetB = d[10:14,:,:,:]
    else:
        print("No data on gdetB, approximating it.") ; sys.stdout.flush()
        gdetB = np.zeros((4,nx,ny,nz),dtype='float32',order='F')
        print("shapes:") ; sys.stdout.flush()
        print(gdet.shape) ; sys.stdout.flush()
        print(B.shape) ; sys.stdout.flush()
        print(gdetB.shape) ; sys.stdout.flush()
        gdetB[1:4] = gdet * B[1:4]
        #
        #
    #
    # get floor-cleaned versions (override uu[3] completely)
    #
    getbsq_pre()
    (rhoclean,ugclean,uuclean,maxbsqorhonear,maxbsqorhofar,condmaxbsqorho,condmaxbsqorhorhs,rinterp)=getrhouclean(rho,ug,uu)
    maxbsqorho=np.copy(maxbsqorhonear)
    uu=np.copy(uuclean)
    rhounclean=np.copy(rho)
    ugunclean=np.copy(ug)
    if 1==0:
        # go here if want rho and ug to be clean versions always.  Including for movie frames.
        # assume if need bsqorho or something like that, ok if goes to infinity (except some plots need fixing)
        rho=np.copy(rhoclean)
        ug=np.copy(ugclean)
    #
    #     if 'gdet' in globals():
    #         #first set everything approximately (B's are at shifted locations by half-cell)
    #         B = gdetB/gdet  
    #         #then, average the inner cells to proper locations
    #         B[1,0:nx-1,:,:] = 0.5*(gdetB[1,0:nx-1,:,:]+gdetB[1,1:nx,:,:])/gdet[0:nx-1,:,:]
    #         B[2,:,0:ny-1,:] = 0.5*(gdetB[2,:,0:ny-1,:]+gdetB[2,:,1:ny,:])/gdet[:,0:ny-1,:]
    #         B[3,:,:,0:nz-1] = 0.5*(gdetB[3,:,:,0:nz-1]+gdetB[3,:,:,1:nz])/gdet[:,:,0:nz-1]
    #         #note: last cells on the grids (near upper boundaries of each dir are at
    #         #      approximate locations
    #     else:
    #         print( "rfd: warning: since gdet is not defined, I am skipping the computation of cell-centered fields, B" )
    # else:
    if 'r' in globals() and r.shape[2] != nz:
        #dynamically change the 3rd dimension size
        rnew = np.zeros((nx,ny,nz),dtype=r.dtype)
        hnew = np.zeros((nx,ny,nz),dtype=h.dtype)
        phnew = np.zeros((nx,ny,nz),dtype=ph.dtype)
        rnew += r[:,:,0:1]
        hnew += h[:,:,0:1]
        #compute size of phi wedge assuming dxdxp[3][3] is up to date
        phiwedge = dxdxp[3][3][0,0,0]*_dx3*nz
        a_phi = phiwedge/(2.*nz)+np.linspace(0,phiwedge,num=nz,endpoint=False)
        phnew += a_phi[None,None,:]
        del r
        del h
        del ph
        r = rnew
        h = hnew
        ph = phnew
        gc.collect()
    #
    # other stuff
    entropy=(gam-1.0)*ugclean/rho**(gam)
    #
    fin.close()
    #

# need bsq even if modify later ud or uu, but assume bsq not sensitive to those modifications so this is ok
def getbsq_pre():
    global ud, bu, bd, bsq
    ud = mdot(gv3,uu)                  #g_mn u^n
    #
    bu=np.empty_like(uu)              #allocate memory for bu
    #set component per component
    bu[0]=mdot(B[1:4], ud[1:4])             #B^i u_i
    bu[1:4]=(B[1:4] + bu[0]*uu[1:4])/uu[0]  #b^i = (B^i + b^t u^i)/u^t
    bd=mdot(gv3,bu)
    bsq=mdot(bu,bd)


def cvel():
    global ud,etad, etau, gamma, vu, vd, bu, bd, bsq,beta,betatoplot,Q1,Q2,Q2toplot
    #
    #
    ud = mdot(gv3,uu)                  #g_mn u^n
    etad = np.zeros_like(uu)
    etad[0] = -1/(-gn3[0,0])**0.5      #ZAMO frame velocity (definition)
    etau = mdot(gn3,etad)
    gamma=-mdot(uu,etad)                #Lorentz factor as measured by ZAMO
    vu = uu - gamma*etau               #u^m = v^m + gamma eta^m
    vd = mdot(gv3,vu)
    #
    bu=np.empty_like(uu)              #allocate memory for bu
    #set component per component
    bu[0]=mdot(B[1:4], ud[1:4])             #B^i u_i
    bu[1:4]=(B[1:4] + bu[0]*uu[1:4])/uu[0]  #b^i = (B^i + b^t u^i)/u^t
    bd=mdot(gv3,bu)
    bsq=mdot(bu,bd)
    #
    beta=((gam-1)*ug)/(1E-30 + bsq*0.5)
    #betatoplot=np.ma.masked_array(beta,mask=(np.isnan(beta)==True)*(np.isinf(beta)==True)*(beta>1E10))
    betatoplot=np.copy(beta)
    #betatoplot[(betatoplot<30)]=30.0
    #betatoplot[(betatoplot>1E3)]=1E3
    #betatoplot[np.isinf(betatoplot)]=1E3
    #betatoplot[np.isnan(betatoplot)]=1E3
    ##############################
    # compute some things one might plot
    #
    # disk mass density scale height
    #diskcondition=(beta>2.0)
    # was (bsq/rho<1.0)
    #diskcondition=diskcondition*(mum1fake<1.0)
    # just avoid floor mass
    #cond1=(bsq/rho<30)
    #cond2=(bsq/rho<10)
    #condmaxbsqorho=cond1*(r<9.0)+cond2*(r>=9.0)
    # need smooth change since notice small glitches in things with the above
    #rinterp=(r-9.0)*(1.0-0.0)/(0.0-9.0) # gives 0 for use near 9   gives 1 for use near 0
    #rinterp[rinterp>1.0]=1.0
    #rinterp[rinterp<0.0]=0.0
    #condmaxbsqorho=(bsq/rho < rinterp*30.0 + (1.0-rinterp)*10.0)
    diskcondition1=condmaxbsqorho
    diskcondition2=condmaxbsqorho
    # was denfactor=rho, but want uniform with corona and jet
    hoverr3dtoplot,thetamid3dtoplot=horcalc(hortype=1,which1=diskcondition1,which2=diskcondition2,denfactor=rho)
    hoverr2dtoplot=hoverr3dtoplot.sum(2)/(nz)
    thetamid2dtoplot=thetamid3dtoplot.sum(2)/(nz)
    #
    #
    #
    Q1,Q3,OQ2=compute_resires(hoverrwhich=hoverr3dtoplot)
    Q2=hoverr3dtoplot/OQ2
    #Q2toplot=np.ma.masked_array(Q2,mask=(np.isnan(Q2)==True)*(np.isinf(Q2)==True)*(Q2>1E10))
    Q2toplot=np.copy(Q2)
    #Q2toplot[(Q2toplot<0)]=0.0
    #Q2toplot[(Q2toplot>1E3)]=1E3
    #Q2toplot[np.isinf(Q2toplot)]=1E3
    #Q2toplot[np.isnan(Q2toplot)]=1E3
    #
    aphi = fieldcalc()


def decolumnify(dumpname):
    print( "Reading data from " + "dumps/" + dumpname + " ..." )
    gin = open( "dumps/" + dumpname + "-col0000", "rb" )
    header = gin.readline()
    gin.close()
    headersplt = header.split()
    nx = int(headersplt[1])
    ny = int(headersplt[2])
    nz = int(headersplt[3])
    gout = open( "dumps/" + dumpname, "wb" )
    gout.write(header)
    gout.flush()
    os.fsync(gout.fileno())
    flist = np.sort(glob.glob( os.path.join("dumps/", "gdump.bin-col*") ) )
    numfiles = flist.shape[0]
    gd = np.zeros((nz,ny,nx,numfiles),order='C',dtype=np.float64)
    for i,f in enumerate(flist):
        print( "Reading from " + f + " ..." )
        gin = open( f, "rb" )
        header = gin.readline()
        body = np.fromfile(gin,dtype=np.float64,count=-1)  #nx*ny*nz*1
        gd[:,:,:,i:i+1] = body.view().reshape((nz,ny,nx,-1),order='C')
        gin.close()
    print( "Writing to file..." )
    gd.tofile(gout)
    gout.close()
    print( "Done decolumnify!" )

             
def myfloat(f,acc=1):
    """ acc=1 means np.float32, acc=2 means np.float64 """
    if acc==1:
        return( np.float32(f) )
    else:
        return( np.float64(f) )

def grid3d(dumpname,use2d=False,doface=False): #read grid dump file: header and body
    #The internal cell indices along the three axes: (ti, tj, tk)
    #The internal uniform coordinates, (x1, x2, x3), are mapped into the physical
    #non-uniform coordinates, (r, h, ph), which correspond to radius (r), polar angle (theta), and toroidal angle (phi).
    #There are more variables, e.g., dxdxp, which is the Jacobian of (x1,x2,x3)->(r,h,ph) transformation, that I can
    #go over, if needed.
    global nx,ny,nz,_startx1,_startx2,_startx3,_dx1,_dx2,_dx3,gam,a,Rin,Rout,ti,tj,tk,x1,x2,x3,r,h,ph,conn,gn3,gv3,ck,dxdxp,gdet
    global tif,tjf,tkf,rf,hf,phf,rhor
    print( "Reading grid from " + "dumps/" + dumpname + " ..." ) ; sys.stdout.flush()
    gin = open( "dumps/" + dumpname, "rb" )
    #First line of grid dump file is a text line that contains general grid information:
    header = gin.readline().split()
    #dimensions of the grid
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    #grid internal coordinates starting point
    _startx1=myfloat(float(header[4]))
    _startx2=myfloat(float(header[5]))
    _startx3=myfloat(float(header[6]))
    #cell size in internal coordintes
    _dx1=myfloat(float(header[7]))
    _dx2=myfloat(float(header[8]))
    _dx3=myfloat(float(header[9]))
    #other information: 
    #polytropic index
    gam=myfloat(float(header[11]))
    #black hole spin
    a=myfloat(float(header[12]))
    rhor = 1+(1-a**2)**0.5
    #Spherical polar radius of the innermost radial cell
    Rin=myfloat(float(header[14]))
    #Spherical polar radius of the outermost radial cell
    Rout=myfloat(float(header[15]))
    #read grid dump per-cell data
    #
    if use2d:
        lnz = 1
    else:
        lnz = nz
    ncols = 126
    if dumpname.endswith(".bin"):
        body = np.fromfile(gin,dtype=np.float64,count=ncols*nx*ny*lnz) 
        gd = body.view().reshape((-1,nx,ny,lnz),order='F')
        gin.close()
    else:
        gin.close()
        gd = np.loadtxt( "dumps/" + dumpname, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True ).view().reshape((126,nx,ny,lnz), order='F')
    gd=myfloat(gd)
    gc.collect()
    # SUPERNOTEMARK: for use2d, note that tk depends upon \phi unlike all other things for a Kerr metric in standard coordinates
    ti,tj,tk,x1,x2,x3,r,h,ph = gd[0:9,:,:,:].view()
    #get the right order of indices by reversing the order of indices i,j(,k)
    #conn=gd[9:73].view().reshape((4,4,4,nx,ny,lnz), order='F').transpose(2,1,0,3,4,5)
    #contravariant metric components, g^{\mu\nu}
    gn3 = gd[73:89].view().reshape((4,4,nx,ny,lnz), order='F').transpose(1,0,2,3,4)
    #covariant metric components, g_{\mu\nu}
    gv3 = gd[89:105].view().reshape((4,4,nx,ny,lnz), order='F').transpose(1,0,2,3,4)
    #metric determinant
    gdet = gd[105]
    ck = gd[106:110].view().reshape((4,nx,ny,lnz), order='F')
    #grid mapping Jacobian
    dxdxp = gd[110:126].view().reshape((4,4,nx,ny,lnz), order='F').transpose(1,0,2,3,4)
    #CELL VERTICES:
    #RADIAL:
    #add an extra dimension to rf container since one more faces than centers
    rf = np.zeros((r.shape[0]+1,r.shape[1]+1,r.shape[2]+1))
    #operate on log(r): average becomes geometric mean, etc
    rf[1:nx,0:ny,0:lnz] = (r[1:nx]*r[0:nx-1])**0.5 #- 0.125*(dxdxp[1,1,1:nx]/r[1:nx]-dxdxp[1,1,0:nx-1]/r[0:nx-1])*_dx1
    #extend in theta
    rf[1:nx,ny,0:lnz] = rf[1:nx,ny-1,0:lnz]
    #extend in phi
    rf[1:nx,:,lnz]   = rf[1:nx,:,lnz-1]
    #extend in r
    rf[0] = 0*rf[0] + Rin
    rf[nx] = 0*rf[nx] + Rout
    #ANGULAR:
    hf = np.zeros((h.shape[0]+1,h.shape[1]+1,h.shape[2]+1))
    hf[0:nx,1:ny,0:lnz] = 0.5*(h[:,1:ny]+h[:,0:ny-1]) #- 0.125*(dxdxp[2,2,:,1:ny]-dxdxp[2,2,:,0:ny-1])*_dx2
    hf[1:nx-1,1:ny,0:lnz] = 0.5*(hf[0:nx-2,1:ny,0:lnz]+hf[1:nx-1,1:ny,0:lnz])
    #populate ghost cells in r
    hf[nx,1:ny,0:lnz] = hf[nx-1,1:ny,0:lnz]
    #populate ghost cells in phi
    hf[:,1:ny,lnz] = hf[:,1:ny,lnz-1]
    #populate ghost cells in theta (note: no need for this since already initialized everything to zero)
    hf[:,0] = 0*hf[:,0] + 0
    hf[:,ny] = 0*hf[:,ny] + np.pi
    #TOROIDAL:
    phf = np.zeros((ph.shape[0]+1,ph.shape[1]+1,ph.shape[2]+1))
    phf[0:nx,0:ny,0:lnz] = ph[0:nx,0:ny,0:lnz] - dxdxp[3,3,0,0,0]*0.5*_dx3
    #extend in phi
    phf[0:nx,0:ny,lnz]   = ph[0:nx,0:ny,lnz-1] + dxdxp[3,3,0,0,0]*0.5*_dx3
    #extend in r
    phf[nx,0:ny,:]   =   phf[nx-1,0:ny,:]
    #extend in theta
    phf[:,ny,:]   =   phf[:,ny-1,:]
    #indices
    #tif=np.zeros(ti.shape[0]+1,ti.shape[1]+1,ti.shape[2]+1)
    #tjf=np.zeros(tj.shape[0]+1,tj.shape[1]+1,tj.shape[2]+1)
    #tkf=np.zeros(tk.shape[0]+1,tk.shape[1]+1,tk.shape[2]+1)
    tif=np.arange(0,(nx+1)*(ny+1)*(lnz+1)).reshape((nx+1,ny+1,lnz+1),order='F')
    tjf=np.arange(0,(nx+1)*(ny+1)*(lnz+1)).reshape((nx+1,ny+1,lnz+1),order='F')
    tkf=np.arange(0,(nx+1)*(ny+1)*(lnz+1)).reshape((nx+1,ny+1,lnz+1),order='F')
    tif %= (nx+1)
    tjf /= (nx+1)
    tjf %= (ny+1)
    tkf /= (ny+1)*(lnz+1)
    gc.collect() #try to release unneeded memory
    print( "Done grid3d!" ) ; sys.stdout.flush()


# DO NOT USE grid3dlight()
def grid3dlight(dumpname): #read gdump: header and body
    global nx,ny,nz,_dx1,_dx2,_dx3,ti,tj,tk,x1,x2,x3,r,h,ph,conn,gn3,gv3,ck,dxdxp,gdet
    print( "Reading grid from " + "dumps/" + dumpname + " ..." )
    gin = open( "dumps/" + dumpname, "rb" )
    header = gin.readline().split()
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    _dx1=float(header[7])
    _dx2=float(header[8])
    _dx3=float(header[9])
    gin.close()
    #read gdump
    #
    gd = np.loadtxt( "dumps/" + dumpname, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True,
                      usecols=(0,1,2,3,4,5,6,7,8,105)).view().reshape((-1,nx,ny,nz), order='F')
    #gd = np.genfromtxt( "dumps/gdump", 
    #                 dtype=np.float64, 
    #                 skip_header=1, 
    #                 skip_footer=nx*ny*(nz-1),
    #                 unpack = True ).view().reshape((137,nx,ny,nz), order='F')
    ti,tj,tk,x1,x2,x3,r,h,ph,gdet = gd[:,:,:,:].view() 
    #get the right order of indices by reversing the order of indices i,j(,k)
    #conn=gd[9:73].view().reshape((4,4,4,nx,ny,nz), order='F').transpose(2,1,0,3,4,5)
    #gn3 = gd[73:89].view().reshape((4,4,nx,ny,nz), order='F').transpose(1,0,2,3,4)
    #gv3 = gd[89:105].view().reshape((4,4,nx,ny,nz), order='F').transpose(1,0,2,3,4)
    #gdet = gd[105]
    #ck = gd[106:110].view().reshape((4,nx,ny,nz), order='F')
    #dxdxp = gd[110:136].view().reshape((4,4,nx,ny,nz), order='F').transpose(1,0,2,3,4)

def rdebug(debugfname):
    global t,nx,ny,nz,_dx1,_dx2,_dx3,gam,a
    global fail0,floor0,limitgamma0,inflow0,failrho0,failu0,failrhou0,precgam0,precu0,toentropy0,tocold0,eosfail0
    global fail1,floor1,limitgamma1,inflow1,failrho1,failu1,failrhou1,precgam1,precu1,toentropy1,tocold1,eosfail1
    global fail2,floor2,limitgamma2,inflow2,failrho2,failu2,failrhou2,precgam2,precu2,toentropy2,tocold2,eosfail2
    global fail3,floor3,limitgamma3,inflow3,failrho3,failu3,failrhou3,precgam3,precu3,toentropy3,tocold3,eosfail3
    global dtot0, dtot1, dtot2, dtot3
    global lgdtot0, lgdtot1, lgdtot2, lgdtot3
    global failtot0, failtot1, failtot2, failtot3 
    global lgftot0, lgftot1, lgftot2, lgftot3 
    #read image
    fin = open( "dumps/" + debugfname, "rb" )
    header = fin.readline().split()
    t = np.float64(header[0])
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    _dx1=myfloat(float(header[7]))
    _dx2=myfloat(float(header[8]))
    _dx3=myfloat(float(header[9]))
    gam=myfloat(float(header[11]))
    a=myfloat(float(header[12]))
    if debugfname.endswith(".bin"):
        body = np.fromfile(fin,dtype=np.float64,count=-1)  #nx*ny*nz*11)
        gd = body.view().reshape((-1,nx,ny,nz),order='F')
        fin.close()
    else:
        fin.close()
        gd = np.loadtxt( "dumps/"+debugfname, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True ).view().reshape((-1,nx,ny,nz), order='F')
    gd=myfloat(gd)
    (
       fail0,floor0,limitgamma0,inflow0,failrho0,failu0,failrhou0,precgam0,precu0,toentropy0,tocold0,eosfail0,
       fail1,floor1,limitgamma1,inflow1,failrho1,failu1,failrhou1,precgam1,precu1,toentropy1,tocold1,eosfail1,
       fail2,floor2,limitgamma2,inflow2,failrho2,failu2,failrhou2,precgam2,precu2,toentropy2,tocold2,eosfail2,
       fail3,floor3,limitgamma3,inflow3,failrho3,failu3,failrhou3,precgam3,precu3,toentropy3,tocold3,eosfail3
    ) = gd[0:48,:,:,:].view() 
 
    # shows where *ever* failed or not
    lg1fail=np.log10(fail0+1)
    lg1tot=np.log10(fail0+failrho0+failu0+failrhou0+1)
    #
    lg1precgam=np.log10(precgam0+1)
    lg1precu=np.log10(precu0+1)
    #
    failtot0=fail0+failrho0+failu0+failrhou0
    failtot1=fail1+failrho1+failu1+failrhou1
    failtot2=fail2+failrho2+failu2+failrhou2
    failtot3=fail3+failrho3+failu3+failrhou3
    #
    lgftot0=np.log10(failtot0+1)
    lgftot1=np.log10(failtot1+1)
    lgftot2=np.log10(failtot2+1)
    lgftot3=np.log10(failtot3+1)
    #
    failtot0sum=np.sum(failtot0)
    failtot1sum=np.sum(failtot1)
    failtot2sum=np.sum(failtot2)
    failtot3sum=np.sum(failtot3)
    #
    print( "failtotsum(0,1,2,3): %10d, %10d, %10d, %10d" % (failtot0sum, failtot1sum, failtot2sum, failtot3sum) )
    #
    # absolute totals
    dtot0=fail0+floor0+limitgamma0+failrho0+failu0+failrhou0+precgam0+precu0
    dtot1=fail1+floor1+limitgamma1+failrho1+failu1+failrhou1+precgam1+precu1
    dtot2=fail2+floor2+limitgamma2+failrho2+failu2+failrhou2+precgam2+precu2
    dtot3=fail3+floor3+limitgamma3+failrho3+failu3+failrhou3+precgam3+precu3
    #
    lgdtot0=np.log10(dtot0+1)
    lgdtot1=np.log10(dtot1+1)
    lgdtot2=np.log10(dtot2+1)
    lgdtot3=np.log10(dtot3+1)
    #
    dtot0sum=np.sum(dtot0)
    dtot1sum=np.sum(dtot1)
    dtot2sum=np.sum(dtot2)
    dtot3sum=np.sum(dtot3)
    #
    print( "   dtotsum(0,1,2,3): %10d, %10d, %10d, %10d" % (dtot0sum, dtot1sum, dtot2sum, dtot3sum) )
    #


def rfdgrid(dumpname): #read gdump: header and body
    global nx,ny,nz,_dx1,_dx2,_dx3,ti,tj,tk,x1,x2,x3,r,h,ph,conn,gn3,gv3,ck,dxdxp,gdet
    print( "Reading grid from " + "dumps/" + dumpname + " ..." )
    gin = open( "dumps/" + dumpname, "rb" )
    header = gin.readline().split()
    nx = int(header[1])
    ny = int(header[2])
    nz = int(header[3])
    _dx1=float(header[7])
    _dx2=float(header[8])
    _dx3=float(header[9])
    gin.close()
    #read gdump
    #
    gd = np.loadtxt( "dumps/" + dumpname, 
                      dtype=np.float64, 
                      skiprows=1, 
                      unpack = True,
                      usecols=(0,1,2,3,4,5,6,7,8)).view().reshape((-1,nx,ny,nz), order='F')
    #gd = np.genfromtxt( "dumps/gdump", 
    #                 dtype=float64, 
    #                 skip_header=1, 
    #                 skip_footer=nx*ny*(nz-1),
    #                 unpack = True ).view().reshape((137,nx,ny,nz), order='F')
    ti,tj,tk,x1,x2,x3,r,h,ph,gdet = gd[:,:,:,:].view() 

def compute_delta():
    """
    Returns a unit matrix
    """
    global delta
    if 'delta' in globals():
        return delta
    #
    delta = np.zeros_like((4,4,nx,ny,nz))
    for i in arange(0,4):
        delta[i,i] = 1
    return(delta)

def odot(a,b):
    """ Outer product of two vectors a^mu b_nu"""
    #the shape of the product is (4,4,nx,ny,max(a.nz,b.nz))
    outer_product = np.zeros(np.concatenate((np.array((4,4)),amax(a[0].shape,b[0].shape))),dtype=np.float32,order='F')
    for mu in np.arange(4):
        for nu in np.arange(4):
            outer_product[mu,nu] = a[mu]*b[nu]
    return(outer_product)

def mdot(a,b):
    """
    Computes a contraction of two tensors/vectors.  Assumes
    the following structure: tensor[m,n,i,j,k] OR vector[m,i,j,k], 
    where i,j,k are spatial indices and m,n are variable indices. 
    """
    if a.ndim == 4 and b.ndim == 4:
          c = (a*b).sum(0)
    elif a.ndim == 5 and b.ndim == 4:
          c = np.empty(amax(a[:,0,:,:,:].shape,b.shape),dtype=b.dtype)      
          for i in range(a.shape[0]):
                c[i,:,:,:] = (a[i,:,:,:,:]*b).sum(0)
    elif a.ndim == 4 and b.ndim == 5:
          c = np.empty(amax(b[0,:,:,:,:].shape,a.shape),dtype=a.dtype)      
          for i in range(b.shape[1]):
                c[i,:,:,:] = (a*b[:,i,:,:,:]).sum(0)
    elif a.ndim == 5 and b.ndim == 5:
          c = np.empty((a.shape[0],b.shape[1],a.shape[2],a.shape[3],max(a.shape[4],b.shape[4])),dtype=a.dtype)
          for i in range(c.shape[0]):
                for j in range(c.shape[1]):
                      c[i,j,:,:,:] = (a[i,:,:,:,:]*b[:,j,:,:,:]).sum(0)
    else:
           raise Exception('mdot', 'wrong dimensions')
    return c

def fieldcalc(gdetB1=None):
    """
    Computes the field vector potential
    """
    #return((1-h[:,:,0]/np.pi)[:,:,None]*fieldcalcp()+(h[:,:,0]/np.pi)[:,:,None]*fieldcalcm())
    return(fieldcalcU(gdetB1))

def mysum2(vec):
    #return( vec[:,:,0][:,:,None]*nz )
    return( np.sum(vec, axis=2)[:,:,None] )

def fcalc():
    """
    Computes the field vector potential
    """
    daphi = np.sum(gdet*B[1],axis=2)*_dx2*_dx3
    aphi=daphi.cumsum(axis=1)
    aphi/=(nz*_dx3)
    return(aphi)

def fieldcalcp():
    """
    Computes the field vector potential
    """
    daphi = mysum2(gdet*B[1])*_dx2*_dx3
    aphi=daphi.cumsum(axis=1)
    aphi/=(nz*_dx3)
    return(aphi)

def fieldcalcm():
    """
    Computes the field vector potential
    """
    daphi = mysum2(gdet*B[1])*_dx2*_dx3
    aphi=(-daphi[:,::-1].cumsum(axis=1))[:,::-1]
    aphi/=(nz*_dx3)
    return(aphi)

def fieldcalc2():
    """
    Computes the field vector potential
    """
    #daphi = (gdet*B[1]).sum(2)*_dx2*_dx3
    #aphi=daphi.cumsum(axis=1)
    daphi = (-gdet*B[2]).sum(2)*_dx2*_dx3
    #np.zeros_like(B[1,:,:,0:1])
    daphi1 = (gdet[0]*B[1,0]).sum(1).cumsum(axis=0)*_dx2*_dx3
    daphi[0,:] += daphi1
    aphi=daphi.cumsum(axis=0)
    aphi/=(nz*_dx3)
    return(aphi[:,:,None])

def fieldcalc2U():
    """
    Computes the field vector potential
    """
    #daphi = (gdet*B[1]).sum(2)*_dx2*_dx3
    #aphi=daphi.cumsum(axis=1)
    daphi = (-gdetB[2]).sum(2)*_dx2*_dx3
    #np.zeros_like(B[1,:,:,0:1])
    daphi1 = (gdetB[1,0]).sum(1).cumsum(axis=0)*_dx2*_dx3
    daphi[0,:] += daphi1
    aphi=daphi.cumsum(axis=0)
    aphi=scaletofullwedge(aphi)
    return(aphi[:,:,None])




def horfluxcalc(ivalue=None,jvalue=None,takeabs=1,takecumsum=0,takeextreme=0,minbsqorho=10,inflowonly=None,whichcondition=True,uphalf=None):
    """
    Computes the absolute flux through the sphere i = ivalue
    """
    global gdetB, _dx2, _dx3
    #1D function of theta only:
    if takeabs==1:
        tosum=np.abs(gdetB[1]*(bsq/rho>=minbsqorho))
    else:
        tosum=gdetB[1]*(bsq/rho>=minbsqorho)
    #
    if inflowonly==None:
        tosum=tosum
    else:
        tosum=tosum*(uu[1]<0)
    #
    if uphalf==None:
        tosum=tosum
    else:
        tosum=tosum*(h<=np.pi*0.5)
    #
    #
    tosum=tosum*(whichcondition==True)
    #
    dfabs = (tosum).sum(2)*_dx2*_dx3
    #
    #account for the wedge
    dfabs=scaletofullwedge(dfabs)
    #
    if takecumsum==0:
        fabs = dfabs.sum(axis=1)
        if ivalue == None:
            return(fabs)
        else:
            return(fabs[ivalue])
        #
    else:
        fabs = dfabs.cumsum(axis=1)
        if ivalue == None and jvalue == None:
            if takeextreme==1:
                bigj=np.zeros(nx,dtype=int)
                finalresult=np.zeros(nx,dtype=float)
                for ii in np.arange(0,nx):
                    condition=(np.fabs(fabs[ii,:])==np.max(np.fabs(fabs[ii,:])))
                    condition=condition*(np.fabs(fabs[ii,:])>1E-15)
                    tempresultO=np.where(condition==1)[0]
                    tempresult=tempresultO.astype(np.integer)
                    #
                    # assume all values are zero if here, so just choose one of the zero values
                    if len(tempresult)==0:
                        tempresult=ny/2
                    #
                    if type(tempresult) is not int:
                        tempresult=tempresult[0]
                    #
                    #print("tempresult")
                    #print(tempresult)
                    #print("ii=%d tempresult=%d fabs=%g" % (ii,tempresult,fabs[ii,tempresult]) )
                    bigj[ii]=tempresult
                    finalresult[ii]=fabs[ii,bigj[ii]]
                #
                #print("shape of bigj")
                #print(bigj.shape)
                #
                #print("sizefinalresult")
                #print(finalresult.shape)
                #
                return(finalresult)
            else:
                return(fabs)
        elif ivalue is not None:
            if takeextreme==1:
                bigj=np.where(np.fabs(fabs[ivalue,:])==np.max(np.fabs(fabs[ivalue,:])))[0]
                #print("bigj=%d" % (bigj) )
                return(fabs[ivalue,bigj])
            else:
                return(fabs[ivalue,:])
            #
        elif jvalue is not None:
            return(fabs[:,jvalue])
        else:
            return(fabs[ivalue,jvalue])
        #
    #


def eqfluxcalc(ivalue=None,jvalue=None,takeabs=1,takecumsum=0,minbsqorho=10):
    """
    Computes the absolute flux through the plane j=ny/2
    """
    global gdetB, _dx1, _dx3
    #1D function of r only:
    if takeabs==1:
        toavg=np.abs(gdetB[2]*(bsq/rho>minbsqorho))
    else:
        toavg=gdetB[2]*(bsq/rho>minbsqorho)
    #
    dfabs = (toavg).sum(2)*_dx1*_dx3
    #account for the wedge
    dfabs=scaletofullwedge(dfabs)
    #
    #
    if takecumsum==0:
        fabs = dfabs.sum(axis=0)
        if jvalue == None:
            return(fabs)
        else:
            return(fabs[jvalue])
        #
    else:
        fabs = dfabs.cumsum(axis=0)
        #
        if ivalue == None and jvalue == None:
            return(fabs)
        elif ivalue is not None:
            return(fabs[ivalue,:])
        elif jvalue is not None:
            return(fabs[:,jvalue])
        else:
            return(fabs[ivalue,jvalue])
        #
    #


def scaletofullwedge(val):
    return(val * 2*np.pi/(dxdxp[3,3,0,0,0]*nz*_dx3))

# def mdotcalc(whichi=None,minbsqorho=None):
#     mdotden = -gdet*rho*uu[1]
#     if minbsqorho != None:
#         mdotden[bsq/rho<minbsqorho<minbsqorho] = 0*mdotden[bsq/rho<minbsqorho<minbsqorho] 
#     mdottot = scaletofullwedge(np.sum(np.sum(mdotden,axis=2),axis=1)*_dx2*_dx3)
#     if whichi == None:
#         return(mdottot)
#     else:
#         return(mdottot[whichi])

def mdotcalc(ihor=None,**kwargs):
    """
    Computes the absolute flux through the sphere i = ihor
    """
    #1D function of theta only:
    md = intangle( -gdet*rho*uu[1], **kwargs)
    if ihor==None:
        return(md)
    else:
        return(md[ihor])

def diskfluxcalc(jmid,rmin=None,rmax=None):
    """
    Computes the absolute flux through the disk midplane at j = jmid
    """
    global gdetB,_dx1,_dx3,r
    #1D function of theta only:
    dfabs = (np.abs(gdetB[2,:,jmid,:])).sum(1)*_dx1*_dx3
    if rmax != None:
        dfabs = dfabs*(r[:,0,0]<=rmax)
    if rmin != None:
        dfabs = dfabs*(r[:,0,0]>=rmin)
    fabs = dfabs.sum(axis=0)
    fabs=scaletofullwedge(fabs)
    return(fabs)

def mfjhorvstime(ihor):
    """
    Returns a tuple (ts,fs,mdot,pjetem,pjettot): lists of times, horizon fluxes, and Mdot
    """
    #flist = np.sort(glob.glob( os.path.join("dumps/", "fieldline*.bin") ) )
    #flist.sort()
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    #
    ts=np.empty(len(flist),dtype=np.float32)
    fs=np.empty(len(flist),dtype=np.float32)
    md=np.empty(len(flist),dtype=np.float32)
    jem=np.empty(len(flist),dtype=np.float32)
    jtot=np.empty(len(flist),dtype=np.float32)
    for findex, fname in enumerate(flist):
        print( "Reading " + fname + " ..." )
        rfd("../"+fname)
        cvel()
        Tcalcud()
        fs[findex]=horfluxcalc(ivalue=ihor)
        md[findex]=mdotcalc(ihor)
        #EM
        jem[findex]=jetpowcalc(0,minbsqorho=10)[ihor]
        #tot
        jtot[findex]=jetpowcalc(2,minbsqorho=10)[ihor]
        ts[findex]=t
        #if os.path.isfile("lrho%04d.png" % findex):
        #    print( "Skipping " + fname + " as lrho%04d.png exists" % findex );
        #else:
        #    print( "Reinterpolating " + fname + " ..." )
        #    plt.figure(0)
        #    plt.clf()
        #    mkframe("lrho%04d" % findex, vmin=-8,vmax=0.2)
    print( "Done mfjhorvstime!" )
    return((ts,fs,md,jem,jtot))

def mergeqtyvstime(n):
    for i in np.arange(n):
        #load each file
        fname = "qty2_%d_%d.npy" % (i, n)
        print( "Loading " + fname + " ..." ) ; sys.stdout.flush()
        qtymemtemp = np.load( fname )
        #per-element sum relevant parts of each file
        if i == 0:
            qtymem = np.zeros_like(qtymemtemp)
        #1st index: whichqty
        #2nd index: whichdumpnumber
        qtymem[:,i::n] += qtymemtemp[:,i::n]
    fname = "qty2.npy"
    print( "Saving into " + fname + " ..." ) ; sys.stdout.flush()
    np.save( fname , qtymem )
    print( "Done mergeqtyvstime!" ) ; sys.stdout.flush()


def getnonbobnqty():
    value=1+6+10+3 + 21+21+21+21+21+24 + 21*3 + 12*4+12*4 + 11+15+12+2+36+36
    return(value)


def getqtymem(qtymem):
    ###########################
    # for global creation, used regexp in emacs:  \(.*\)=qtymem\[i\];i\+=1 ->     global \1^J\1=qtymem[i];i+=1
    ###########################
    #qty defs
    i=0
    # 1
    global ts
    ts=qtymem[i,:,0];i+=1
    #HoverR: 6
    global     hoverr
    hoverr=qtymem[i];i+=1
    global     thetamid
    thetamid=qtymem[i];i+=1
    global     hoverrcorona
    hoverrcorona=qtymem[i];i+=1
    global     thetamidcorona
    thetamidcorona=qtymem[i];i+=1
    global     hoverr_jet
    hoverr_jet=qtymem[i];i+=1
    global     thetamidjet
    thetamidjet=qtymem[i];i+=1
    # 10
    global     qmridisk
    qmridisk=qtymem[i];i+=1
    global     iq2mridisk
    iq2mridisk=qtymem[i];i+=1
    global     normmridisk
    normmridisk=qtymem[i];i+=1
    global     qmridiskweak
    qmridiskweak=qtymem[i];i+=1
    global     iq2mridiskweak
    iq2mridiskweak=qtymem[i];i+=1
    global     normmridiskweak
    normmridiskweak=qtymem[i];i+=1
    global     betamin
    betamin=qtymem[i];i+=1
    global     betaavg
    betaavg=qtymem[i];i+=1
    global     betaratofavg
    betaratofavg=qtymem[i];i+=1
    global     betaratofmax
    betaratofmax=qtymem[i];i+=1
    #alphamag: 3
    global     alphamag1
    alphamag1=qtymem[i];i+=1
    global     alphamag2
    alphamag2=qtymem[i];i+=1
    global     alphamag3
    alphamag3=qtymem[i];i+=1
    #
    #rhosq: 14+7=21
    global     rhosqs
    rhosqs=qtymem[i];i+=1
    global     rhosrhosq
    rhosrhosq=qtymem[i];i+=1
    global     ugsrhosq
    ugsrhosq=qtymem[i];i+=1
    global     uu0rhosq
    uu0rhosq=qtymem[i];i+=1
    global     vus1rhosq
    vus1rhosq=qtymem[i];i+=1
    global     vuas1rhosq
    vuas1rhosq=qtymem[i];i+=1
    global     vus3rhosq
    vus3rhosq=qtymem[i];i+=1
    global     vuas3rhosq
    vuas3rhosq=qtymem[i];i+=1
    global     Bs1rhosq
    Bs1rhosq=qtymem[i];i+=1
    global     Bas1rhosq
    Bas1rhosq=qtymem[i];i+=1
    global     Bs2rhosq
    Bs2rhosq=qtymem[i];i+=1
    global     Bas2rhosq
    Bas2rhosq=qtymem[i];i+=1
    global     Bs3rhosq
    Bs3rhosq=qtymem[i];i+=1
    global     Bas3rhosq
    Bas3rhosq=qtymem[i];i+=1
    global     bs1rhosq
    bs1rhosq=qtymem[i];i+=1
    global     bas1rhosq
    bas1rhosq=qtymem[i];i+=1
    global     bs2rhosq
    bs2rhosq=qtymem[i];i+=1
    global     bas2rhosq
    bas2rhosq=qtymem[i];i+=1
    global     bs3rhosq
    bs3rhosq=qtymem[i];i+=1
    global     bas3rhosq
    bas3rhosq=qtymem[i];i+=1
    global     bsqrhosq
    bsqrhosq=qtymem[i];i+=1
    #rhosqdc: 14+7=21
    global     rhosqdcs
    rhosqdcs=qtymem[i];i+=1
    global     rhosrhosqdc
    rhosrhosqdc=qtymem[i];i+=1
    global     ugsrhosqdc
    ugsrhosqdc=qtymem[i];i+=1
    global     uu0rhosqdc
    uu0rhosqdc=qtymem[i];i+=1
    global     vus1rhosqdc
    vus1rhosqdc=qtymem[i];i+=1
    global     vuas1rhosqdc
    vuas1rhosqdc=qtymem[i];i+=1
    global     vus3rhosqdc
    vus3rhosqdc=qtymem[i];i+=1
    global     vuas3rhosqdc
    vuas3rhosqdc=qtymem[i];i+=1
    global     Bs1rhosqdc
    Bs1rhosqdc=qtymem[i];i+=1
    global     Bas1rhosqdc
    Bas1rhosqdc=qtymem[i];i+=1
    global     Bs2rhosqdc
    Bs2rhosqdc=qtymem[i];i+=1
    global     Bas2rhosqdc
    Bas2rhosqdc=qtymem[i];i+=1
    global     Bs3rhosqdc
    Bs3rhosqdc=qtymem[i];i+=1
    global     Bas3rhosqdc
    Bas3rhosqdc=qtymem[i];i+=1
    global     bs1rhosqdc
    bs1rhosqdc=qtymem[i];i+=1
    global     bas1rhosqdc
    bas1rhosqdc=qtymem[i];i+=1
    global     bs2rhosqdc
    bs2rhosqdc=qtymem[i];i+=1
    global     bas2rhosqdc
    bas2rhosqdc=qtymem[i];i+=1
    global     bs3rhosqdc
    bs3rhosqdc=qtymem[i];i+=1
    global     bas3rhosqdc
    bas3rhosqdc=qtymem[i];i+=1
    global     bsqrhosqdc
    bsqrhosqdc=qtymem[i];i+=1
    #rhosqdcden: 14+7=21
    global     rhosqdcdens
    rhosqdcdens=qtymem[i];i+=1
    global     rhosrhosqdcden
    rhosrhosqdcden=qtymem[i];i+=1
    global     ugsrhosqdcden
    ugsrhosqdcden=qtymem[i];i+=1
    global     uu0rhosqdcden
    uu0rhosqdcden=qtymem[i];i+=1
    global     vus1rhosqdcden
    vus1rhosqdcden=qtymem[i];i+=1
    global     vuas1rhosqdcden
    vuas1rhosqdcden=qtymem[i];i+=1
    global     vus3rhosqdcden
    vus3rhosqdcden=qtymem[i];i+=1
    global     vuas3rhosqdcden
    vuas3rhosqdcden=qtymem[i];i+=1
    global     Bs1rhosqdcden
    Bs1rhosqdcden=qtymem[i];i+=1
    global     Bas1rhosqdcden
    Bas1rhosqdcden=qtymem[i];i+=1
    global     Bs2rhosqdcden
    Bs2rhosqdcden=qtymem[i];i+=1
    global     Bas2rhosqdcden
    Bas2rhosqdcden=qtymem[i];i+=1
    global     Bs3rhosqdcden
    Bs3rhosqdcden=qtymem[i];i+=1
    global     Bas3rhosqdcden
    Bas3rhosqdcden=qtymem[i];i+=1
    global     bs1rhosqdcden
    bs1rhosqdcden=qtymem[i];i+=1
    global     bas1rhosqdcden
    bas1rhosqdcden=qtymem[i];i+=1
    global     bs2rhosqdcden
    bs2rhosqdcden=qtymem[i];i+=1
    global     bas2rhosqdcden
    bas2rhosqdcden=qtymem[i];i+=1
    global     bs3rhosqdcden
    bs3rhosqdcden=qtymem[i];i+=1
    global     bas3rhosqdcden
    bas3rhosqdcden=qtymem[i];i+=1
    global     bsqrhosqdcden
    bsqrhosqdcden=qtymem[i];i+=1
    #rhosqeq: 14+7=21
    global     rhosqeqs
    rhosqeqs=qtymem[i];i+=1
    global     rhosrhosqeq
    rhosrhosqeq=qtymem[i];i+=1
    global     ugsrhosqeq
    ugsrhosqeq=qtymem[i];i+=1
    global     uu0rhosqeq
    uu0rhosqeq=qtymem[i];i+=1
    global     vus1rhosqeq
    vus1rhosqeq=qtymem[i];i+=1
    global     vuas1rhosqeq
    vuas1rhosqeq=qtymem[i];i+=1
    global     vus3rhosqeq
    vus3rhosqeq=qtymem[i];i+=1
    global     vuas3rhosqeq
    vuas3rhosqeq=qtymem[i];i+=1
    global     Bs1rhosqeq
    Bs1rhosqeq=qtymem[i];i+=1
    global     Bas1rhosqeq
    Bas1rhosqeq=qtymem[i];i+=1
    global     Bs2rhosqeq
    Bs2rhosqeq=qtymem[i];i+=1
    global     Bas2rhosqeq
    Bas2rhosqeq=qtymem[i];i+=1
    global     Bs3rhosqeq
    Bs3rhosqeq=qtymem[i];i+=1
    global     Bas3rhosqeq
    Bas3rhosqeq=qtymem[i];i+=1
    global     bs1rhosqeq
    bs1rhosqeq=qtymem[i];i+=1
    global     bas1rhosqeq
    bas1rhosqeq=qtymem[i];i+=1
    global     bs2rhosqeq
    bs2rhosqeq=qtymem[i];i+=1
    global     bas2rhosqeq
    bas2rhosqeq=qtymem[i];i+=1
    global     bs3rhosqeq
    bs3rhosqeq=qtymem[i];i+=1
    global     bas3rhosqeq
    bas3rhosqeq=qtymem[i];i+=1
    global     bsqrhosqeq
    bsqrhosqeq=qtymem[i];i+=1
    #rhosqhorpick: 14+7=21
    global     rhosqhorpicks
    rhosqhorpicks=qtymem[i];i+=1
    global     rhosrhosqhorpick
    rhosrhosqhorpick=qtymem[i];i+=1
    global     ugsrhosqhorpick
    ugsrhosqhorpick=qtymem[i];i+=1
    global     uu0rhosqhorpick
    uu0rhosqhorpick=qtymem[i];i+=1
    global     vus1rhosqhorpick
    vus1rhosqhorpick=qtymem[i];i+=1
    global     vuas1rhosqhorpick
    vuas1rhosqhorpick=qtymem[i];i+=1
    global     vus3rhosqhorpick
    vus3rhosqhorpick=qtymem[i];i+=1
    global     vuas3rhosqhorpick
    vuas3rhosqhorpick=qtymem[i];i+=1
    global     Bs1rhosqhorpick
    Bs1rhosqhorpick=qtymem[i];i+=1
    global     Bas1rhosqhorpick
    Bas1rhosqhorpick=qtymem[i];i+=1
    global     Bs2rhosqhorpick
    Bs2rhosqhorpick=qtymem[i];i+=1
    global     Bas2rhosqhorpick
    Bas2rhosqhorpick=qtymem[i];i+=1
    global     Bs3rhosqhorpick
    Bs3rhosqhorpick=qtymem[i];i+=1
    global     Bas3rhosqhorpick
    Bas3rhosqhorpick=qtymem[i];i+=1
    global     bs1rhosqhorpick
    bs1rhosqhorpick=qtymem[i];i+=1
    global     bas1rhosqhorpick
    bas1rhosqhorpick=qtymem[i];i+=1
    global     bs2rhosqhorpick
    bs2rhosqhorpick=qtymem[i];i+=1
    global     bas2rhosqhorpick
    bas2rhosqhorpick=qtymem[i];i+=1
    global     bs3rhosqhorpick
    bs3rhosqhorpick=qtymem[i];i+=1
    global     bas3rhosqhorpick
    bas3rhosqhorpick=qtymem[i];i+=1
    global     bsqrhosqhorpick
    bsqrhosqhorpick=qtymem[i];i+=1
    #2.0hor: 24
    global     gdetinthor
    gdetinthor=qtymem[i];i+=1
    global     rhoshor
    rhoshor=qtymem[i];i+=1
    global     ugshor
    ugshor=qtymem[i];i+=1
    global     bsqshor
    bsqshor=qtymem[i];i+=1
    global     bsqorhoshor
    bsqorhoshor=qtymem[i];i+=1
    global     bsqougshor
    bsqougshor=qtymem[i];i+=1
    global     uu0hor
    uu0hor=qtymem[i];i+=1
    global     vus1hor
    vus1hor=qtymem[i];i+=1
    global     vuas1hor
    vuas1hor=qtymem[i];i+=1
    global     vus3hor
    vus3hor=qtymem[i];i+=1
    global     vuas3hor
    vuas3hor=qtymem[i];i+=1
    global     Bs1hor
    Bs1hor=qtymem[i];i+=1
    global     Bas1hor
    Bas1hor=qtymem[i];i+=1
    global     Bs2hor
    Bs2hor=qtymem[i];i+=1
    global     Bas2hor
    Bas2hor=qtymem[i];i+=1
    global     Bs3hor
    Bs3hor=qtymem[i];i+=1
    global     Bas3hor
    Bas3hor=qtymem[i];i+=1
    global     bs1hor
    bs1hor=qtymem[i];i+=1
    global     bas1hor
    bas1hor=qtymem[i];i+=1
    global     bs2hor
    bs2hor=qtymem[i];i+=1
    global     bas2hor
    bas2hor=qtymem[i];i+=1
    global     bs3hor
    bs3hor=qtymem[i];i+=1
    global     bas3hor
    bas3hor=qtymem[i];i+=1
    global     bsqhor
    bsqhor=qtymem[i];i+=1
    #rhosqrad4: 14+7=21
    global     rhosqrad4
    rhosqrad4=qtymem[i];i+=1
    global     rhosrhosqrad4
    rhosrhosqrad4=qtymem[i];i+=1
    global     ugsrhosqrad4
    ugsrhosqrad4=qtymem[i];i+=1
    global     uu0rhosqrad4
    uu0rhosqrad4=qtymem[i];i+=1
    global     vus1rhosqrad4
    vus1rhosqrad4=qtymem[i];i+=1
    global     vuas1rhosqrad4
    vuas1rhosqrad4=qtymem[i];i+=1
    global     vus3rhosqrad4
    vus3rhosqrad4=qtymem[i];i+=1
    global     vuas3rhosqrad4
    vuas3rhosqrad4=qtymem[i];i+=1
    global     Bs1rhosqrad4
    Bs1rhosqrad4=qtymem[i];i+=1
    global     Bas1rhosqrad4
    Bas1rhosqrad4=qtymem[i];i+=1
    global     Bs2rhosqrad4
    Bs2rhosqrad4=qtymem[i];i+=1
    global     Bas2rhosqrad4
    Bas2rhosqrad4=qtymem[i];i+=1
    global     Bs3rhosqrad4
    Bs3rhosqrad4=qtymem[i];i+=1
    global     Bas3rhosqrad4
    Bas3rhosqrad4=qtymem[i];i+=1
    global     bs1rhosqrad4
    bs1rhosqrad4=qtymem[i];i+=1
    global     bas1rhosqrad4
    bas1rhosqrad4=qtymem[i];i+=1
    global     bs2rhosqrad4
    bs2rhosqrad4=qtymem[i];i+=1
    global     bas2rhosqrad4
    bas2rhosqrad4=qtymem[i];i+=1
    global     bs3rhosqrad4
    bs3rhosqrad4=qtymem[i];i+=1
    global     bas3rhosqrad4
    bas3rhosqrad4=qtymem[i];i+=1
    global     bsqrhosqrad4
    bsqrhosqrad4=qtymem[i];i+=1
    #rhosqrad8: 14+7=21
    global     rhosqrad8
    rhosqrad8=qtymem[i];i+=1
    global     rhosrhosqrad8
    rhosrhosqrad8=qtymem[i];i+=1
    global     ugsrhosqrad8
    ugsrhosqrad8=qtymem[i];i+=1
    global     uu0rhosqrad8
    uu0rhosqrad8=qtymem[i];i+=1
    global     vus1rhosqrad8
    vus1rhosqrad8=qtymem[i];i+=1
    global     vuas1rhosqrad8
    vuas1rhosqrad8=qtymem[i];i+=1
    global     vus3rhosqrad8
    vus3rhosqrad8=qtymem[i];i+=1
    global     vuas3rhosqrad8
    vuas3rhosqrad8=qtymem[i];i+=1
    global     Bs1rhosqrad8
    Bs1rhosqrad8=qtymem[i];i+=1
    global     Bas1rhosqrad8
    Bas1rhosqrad8=qtymem[i];i+=1
    global     Bs2rhosqrad8
    Bs2rhosqrad8=qtymem[i];i+=1
    global     Bas2rhosqrad8
    Bas2rhosqrad8=qtymem[i];i+=1
    global     Bs3rhosqrad8
    Bs3rhosqrad8=qtymem[i];i+=1
    global     Bas3rhosqrad8
    Bas3rhosqrad8=qtymem[i];i+=1
    global     bs1rhosqrad8
    bs1rhosqrad8=qtymem[i];i+=1
    global     bas1rhosqrad8
    bas1rhosqrad8=qtymem[i];i+=1
    global     bs2rhosqrad8
    bs2rhosqrad8=qtymem[i];i+=1
    global     bas2rhosqrad8
    bas2rhosqrad8=qtymem[i];i+=1
    global     bs3rhosqrad8
    bs3rhosqrad8=qtymem[i];i+=1
    global     bas3rhosqrad8
    bas3rhosqrad8=qtymem[i];i+=1
    global     bsqrhosqrad8
    bsqrhosqrad8=qtymem[i];i+=1
    #rhosqrad30: 14+7=21
    global     rhosqrad30
    rhosqrad30=qtymem[i];i+=1
    global     rhosrhosqrad30
    rhosrhosqrad30=qtymem[i];i+=1
    global     ugsrhosqrad30
    ugsrhosqrad30=qtymem[i];i+=1
    global     uu0rhosqrad30
    uu0rhosqrad30=qtymem[i];i+=1
    global     vus1rhosqrad30
    vus1rhosqrad30=qtymem[i];i+=1
    global     vuas1rhosqrad30
    vuas1rhosqrad30=qtymem[i];i+=1
    global     vus3rhosqrad30
    vus3rhosqrad30=qtymem[i];i+=1
    global     vuas3rhosqrad30
    vuas3rhosqrad30=qtymem[i];i+=1
    global     Bs1rhosqrad30
    Bs1rhosqrad30=qtymem[i];i+=1
    global     Bas1rhosqrad30
    Bas1rhosqrad30=qtymem[i];i+=1
    global     Bs2rhosqrad30
    Bs2rhosqrad30=qtymem[i];i+=1
    global     Bas2rhosqrad30
    Bas2rhosqrad30=qtymem[i];i+=1
    global     Bs3rhosqrad30
    Bs3rhosqrad30=qtymem[i];i+=1
    global     Bas3rhosqrad30
    Bas3rhosqrad30=qtymem[i];i+=1
    global     bs1rhosqrad30
    bs1rhosqrad30=qtymem[i];i+=1
    global     bas1rhosqrad30
    bas1rhosqrad30=qtymem[i];i+=1
    global     bs2rhosqrad30
    bs2rhosqrad30=qtymem[i];i+=1
    global     bas2rhosqrad30
    bas2rhosqrad30=qtymem[i];i+=1
    global     bs3rhosqrad30
    bs3rhosqrad30=qtymem[i];i+=1
    global     bas3rhosqrad30
    bas3rhosqrad30=qtymem[i];i+=1
    global     bsqrhosqrad30
    bsqrhosqrad30=qtymem[i];i+=1


    #rhosq_diskcorona_phipow_radhor: 12
    global     rhosq_diskcorona_phipow_radhor
    rhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     rhosrhosq_diskcorona_phipow_radhor
    rhosrhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     ugsrhosq_diskcorona_phipow_radhor
    ugsrhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     uu0rhosq_diskcorona_phipow_radhor
    uu0rhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     vuas3rhosq_diskcorona_phipow_radhor
    vuas3rhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     bas1rhosq_diskcorona_phipow_radhor
    bas1rhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     bas2rhosq_diskcorona_phipow_radhor
    bas2rhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     bas3rhosq_diskcorona_phipow_radhor
    bas3rhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     bsqrhosq_diskcorona_phipow_radhor
    bsqrhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     FMrhosq_diskcorona_phipow_radhor
    FMrhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     FEMArhosq_diskcorona_phipow_radhor
    FEMArhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    global     FEEMrhosq_diskcorona_phipow_radhor
    FEEMrhosq_diskcorona_phipow_radhor=qtymem[i];i+=1
    #rhosq_diskcorona_phipow_rad4: 12
    global     rhosq_diskcorona_phipow_rad4
    rhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     rhosrhosq_diskcorona_phipow_rad4
    rhosrhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     ugsrhosq_diskcorona_phipow_rad4
    ugsrhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     uu0rhosq_diskcorona_phipow_rad4
    uu0rhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     vuas3rhosq_diskcorona_phipow_rad4
    vuas3rhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     bas1rhosq_diskcorona_phipow_rad4
    bas1rhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     bas2rhosq_diskcorona_phipow_rad4
    bas2rhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     bas3rhosq_diskcorona_phipow_rad4
    bas3rhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     bsqrhosq_diskcorona_phipow_rad4
    bsqrhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     FMrhosq_diskcorona_phipow_rad4
    FMrhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     FEMArhosq_diskcorona_phipow_rad4
    FEMArhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    global     FEEMrhosq_diskcorona_phipow_rad4
    FEEMrhosq_diskcorona_phipow_rad4=qtymem[i];i+=1
    #rhosq_diskcorona_phipow_rad8: 12
    global     rhosq_diskcorona_phipow_rad8
    rhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     rhosrhosq_diskcorona_phipow_rad8
    rhosrhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     ugsrhosq_diskcorona_phipow_rad8
    ugsrhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     uu0rhosq_diskcorona_phipow_rad8
    uu0rhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     vuas3rhosq_diskcorona_phipow_rad8
    vuas3rhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     bas1rhosq_diskcorona_phipow_rad8
    bas1rhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     bas2rhosq_diskcorona_phipow_rad8
    bas2rhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     bas3rhosq_diskcorona_phipow_rad8
    bas3rhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     bsqrhosq_diskcorona_phipow_rad8
    bsqrhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     FMrhosq_diskcorona_phipow_rad8
    FMrhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     FEMArhosq_diskcorona_phipow_rad8
    FEMArhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    global     FEEMrhosq_diskcorona_phipow_rad8
    FEEMrhosq_diskcorona_phipow_rad8=qtymem[i];i+=1
    #rhosq_diskcorona_phipow_rad30: 12
    global     rhosq_diskcorona_phipow_rad30
    rhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     rhosrhosq_diskcorona_phipow_rad30
    rhosrhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     ugsrhosq_diskcorona_phipow_rad30
    ugsrhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     uu0rhosq_diskcorona_phipow_rad30
    uu0rhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     vuas3rhosq_diskcorona_phipow_rad30
    vuas3rhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     bas1rhosq_diskcorona_phipow_rad30
    bas1rhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     bas2rhosq_diskcorona_phipow_rad30
    bas2rhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     bas3rhosq_diskcorona_phipow_rad30
    bas3rhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     bsqrhosq_diskcorona_phipow_rad30
    bsqrhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     FMrhosq_diskcorona_phipow_rad30
    FMrhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     FEMArhosq_diskcorona_phipow_rad30
    FEMArhosq_diskcorona_phipow_rad30=qtymem[i];i+=1
    global     FEEMrhosq_diskcorona_phipow_rad30
    FEEMrhosq_diskcorona_phipow_rad30=qtymem[i];i+=1


    #rhosq_jet_phipow_radhor: 12
    global     rhosq_jet_phipow_radhor
    rhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     rhosrhosq_jet_phipow_radhor
    rhosrhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     ugsrhosq_jet_phipow_radhor
    ugsrhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     uu0rhosq_jet_phipow_radhor
    uu0rhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     vuas3rhosq_jet_phipow_radhor
    vuas3rhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     bas1rhosq_jet_phipow_radhor
    bas1rhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     bas2rhosq_jet_phipow_radhor
    bas2rhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     bas3rhosq_jet_phipow_radhor
    bas3rhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     bsqrhosq_jet_phipow_radhor
    bsqrhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     FMrhosq_jet_phipow_radhor
    FMrhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     FEMArhosq_jet_phipow_radhor
    FEMArhosq_jet_phipow_radhor=qtymem[i];i+=1
    global     FEEMrhosq_jet_phipow_radhor
    FEEMrhosq_jet_phipow_radhor=qtymem[i];i+=1
    #rhosq_jet_phipow_rad4: 12
    global     rhosq_jet_phipow_rad4
    rhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     rhosrhosq_jet_phipow_rad4
    rhosrhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     ugsrhosq_jet_phipow_rad4
    ugsrhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     uu0rhosq_jet_phipow_rad4
    uu0rhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     vuas3rhosq_jet_phipow_rad4
    vuas3rhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     bas1rhosq_jet_phipow_rad4
    bas1rhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     bas2rhosq_jet_phipow_rad4
    bas2rhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     bas3rhosq_jet_phipow_rad4
    bas3rhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     bsqrhosq_jet_phipow_rad4
    bsqrhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     FMrhosq_jet_phipow_rad4
    FMrhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     FEMArhosq_jet_phipow_rad4
    FEMArhosq_jet_phipow_rad4=qtymem[i];i+=1
    global     FEEMrhosq_jet_phipow_rad4
    FEEMrhosq_jet_phipow_rad4=qtymem[i];i+=1
    #rhosq_jet_phipow_rad8: 12
    global     rhosq_jet_phipow_rad8
    rhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     rhosrhosq_jet_phipow_rad8
    rhosrhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     ugsrhosq_jet_phipow_rad8
    ugsrhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     uu0rhosq_jet_phipow_rad8
    uu0rhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     vuas3rhosq_jet_phipow_rad8
    vuas3rhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     bas1rhosq_jet_phipow_rad8
    bas1rhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     bas2rhosq_jet_phipow_rad8
    bas2rhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     bas3rhosq_jet_phipow_rad8
    bas3rhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     bsqrhosq_jet_phipow_rad8
    bsqrhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     FMrhosq_jet_phipow_rad8
    FMrhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     FEMArhosq_jet_phipow_rad8
    FEMArhosq_jet_phipow_rad8=qtymem[i];i+=1
    global     FEEMrhosq_jet_phipow_rad8
    FEEMrhosq_jet_phipow_rad8=qtymem[i];i+=1
    #rhosq_jet_phipow_rad30: 12
    global     rhosq_jet_phipow_rad30
    rhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     rhosrhosq_jet_phipow_rad30
    rhosrhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     ugsrhosq_jet_phipow_rad30
    ugsrhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     uu0rhosq_jet_phipow_rad30
    uu0rhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     vuas3rhosq_jet_phipow_rad30
    vuas3rhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     bas1rhosq_jet_phipow_rad30
    bas1rhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     bas2rhosq_jet_phipow_rad30
    bas2rhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     bas3rhosq_jet_phipow_rad30
    bas3rhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     bsqrhosq_jet_phipow_rad30
    bsqrhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     FMrhosq_jet_phipow_rad30
    FMrhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     FEMArhosq_jet_phipow_rad30
    FEMArhosq_jet_phipow_rad30=qtymem[i];i+=1
    global     FEEMrhosq_jet_phipow_rad30
    FEEMrhosq_jet_phipow_rad30=qtymem[i];i+=1



    #Flux: 11
    global     fstot
    fstot=qtymem[i];i+=1
    global     fsin
    fsin=qtymem[i];i+=1
    global     feqtot
    feqtot=qtymem[i];i+=1
    global     fsmaxtot
    fsmaxtot=qtymem[i];i+=1
    global     fsuphalf
    fsuphalf=qtymem[i];i+=1
    global     fs2hor
    fs2hor=qtymem[i];i+=1
    global     fsj5
    fsj5=qtymem[i];i+=1
    global     fsj10
    fsj10=qtymem[i];i+=1
    global     fsj20
    fsj20=qtymem[i];i+=1
    global     fsj30
    fsj30=qtymem[i];i+=1
    global     fsj40
    fsj40=qtymem[i];i+=1

    #Mdot: 15
    global     mdtot
    mdtot=qtymem[i];i+=1
    global     md2h
    md2h=qtymem[i];i+=1
    global     md4h
    md4h=qtymem[i];i+=1
    global     md2hor
    md2hor=qtymem[i];i+=1
    global     md5
    md5=qtymem[i];i+=1
    global     md10
    md10=qtymem[i];i+=1
    global     md20
    md20=qtymem[i];i+=1
    global     md30
    md30=qtymem[i];i+=1
    global     mdwind
    mdwind=qtymem[i];i+=1
    global     mdmwind
    mdmwind=qtymem[i];i+=1
    global     mdjet
    mdjet=qtymem[i];i+=1
    global     md40
    md40=qtymem[i];i+=1
    global     mdrhosq
    mdrhosq=qtymem[i];i+=1
    global     mdtotbound
    mdtotbound=qtymem[i];i+=1
    global     mdin
    mdin=qtymem[i];i+=1

    #Edot: 12
    global     edtot
    edtot=qtymem[i];i+=1
    global     ed2h
    ed2h=qtymem[i];i+=1
    global     ed4h
    ed4h=qtymem[i];i+=1
    global     ed2hor
    ed2hor=qtymem[i];i+=1
    global     edrhosq
    edrhosq=qtymem[i];i+=1
    #
    global     edem
    edem=qtymem[i];i+=1
    global     edma
    edma=qtymem[i];i+=1
    global     edm
    edm=qtymem[i];i+=1
    #
    global     edma30
    edma30=qtymem[i];i+=1
    global     edm30
    edm30=qtymem[i];i+=1
    #
    global     edtotbound
    edtotbound=qtymem[i];i+=1
    global     edmabound
    edmabound=qtymem[i];i+=1
    #
    #Pjet : 2
    global     pjem5
    pjem5=qtymem[i];i+=1
    global     pjma5
    pjma5=qtymem[i];i+=1
    #

    # Pj and Phiabsj: 36
    global     pjem_n_mu1
    pjem_n_mu1=qtymem[i];i+=1
    global     pjem_n_mumax1
    pjem_n_mumax1=qtymem[i];i+=1
    global     pjem_n_mumax1m
    pjem_n_mumax1m=qtymem[i];i+=1
    #
    global     pjrm_n_mu1
    pjrm_n_mu1=qtymem[i];i+=1
    global     pjrm_n_mumax1
    pjrm_n_mumax1=qtymem[i];i+=1
    global     pjrm_n_mumax1m
    pjrm_n_mumax1m=qtymem[i];i+=1
    #
    global     pjrm_n_mu1_flr
    pjrm_n_mu1_flr=qtymem[i];i+=1
    global     pjrm_n_mumax1_flr
    pjrm_n_mumax1_flr=qtymem[i];i+=1
    global     pjrm_n_mumax1m_flr
    pjrm_n_mumax1m_flr=qtymem[i];i+=1
    #
    global     pjma_n_mu1
    pjma_n_mu1=qtymem[i];i+=1
    global     pjma_n_mumax1
    pjma_n_mumax1=qtymem[i];i+=1
    global     pjma_n_mumax1m
    pjma_n_mumax1m=qtymem[i];i+=1
    #
    global     pjma_n_mu1_flr
    pjma_n_mu1_flr=qtymem[i];i+=1
    global     pjma_n_mumax1_flr
    pjma_n_mumax1_flr=qtymem[i];i+=1
    global     pjma_n_mumax1m_flr
    pjma_n_mumax1m_flr=qtymem[i];i+=1
    #
    global     phiabsj_n_mu1
    phiabsj_n_mu1=qtymem[i];i+=1
    global     phiabsj_n_mumax1
    phiabsj_n_mumax1=qtymem[i];i+=1
    global     phiabsj_n_mumax1m
    phiabsj_n_mumax1m=qtymem[i];i+=1
    #
    global     pjem_s_mu1
    pjem_s_mu1=qtymem[i];i+=1
    global     pjem_s_mumax1
    pjem_s_mumax1=qtymem[i];i+=1
    global     pjem_s_mumax1m
    pjem_s_mumax1m=qtymem[i];i+=1
    #
    global     pjrm_s_mu1
    pjrm_s_mu1=qtymem[i];i+=1
    global     pjrm_s_mumax1
    pjrm_s_mumax1=qtymem[i];i+=1
    global     pjrm_s_mumax1m
    pjrm_s_mumax1m=qtymem[i];i+=1
    #
    global     pjrm_s_mu1_flr
    pjrm_s_mu1_flr=qtymem[i];i+=1
    global     pjrm_s_mumax1_flr
    pjrm_s_mumax1_flr=qtymem[i];i+=1
    global     pjrm_s_mumax1m_flr
    pjrm_s_mumax1m_flr=qtymem[i];i+=1
    #
    global     pjma_s_mu1
    pjma_s_mu1=qtymem[i];i+=1
    global     pjma_s_mumax1
    pjma_s_mumax1=qtymem[i];i+=1
    global     pjma_s_mumax1m
    pjma_s_mumax1m=qtymem[i];i+=1
    #
    global     pjma_s_mu1_flr
    pjma_s_mu1_flr=qtymem[i];i+=1
    global     pjma_s_mumax1_flr
    pjma_s_mumax1_flr=qtymem[i];i+=1
    global     pjma_s_mumax1m_flr
    pjma_s_mumax1m_flr=qtymem[i];i+=1
    #
    global     phiabsj_s_mu1
    phiabsj_s_mu1=qtymem[i];i+=1
    global     phiabsj_s_mumax1
    phiabsj_s_mumax1=qtymem[i];i+=1
    global     phiabsj_s_mumax1m
    phiabsj_s_mumax1m=qtymem[i];i+=1
    #

    # ldot stuff: 6+3*10=36
    global     ldtot
    ldtot=qtymem[i];i+=1
    global     ldem
    ldem=qtymem[i];i+=1
    global     ldma
    ldma=qtymem[i];i+=1
    global     ldm
    ldm=qtymem[i];i+=1
    #
    global     ldma30
    ldma30=qtymem[i];i+=1
    global     ldm30
    ldm30=qtymem[i];i+=1
    # 
    global     ljem_n_mu1
    ljem_n_mu1=qtymem[i];i+=1
    global     ljem_n_mumax1
    ljem_n_mumax1=qtymem[i];i+=1
    global     ljem_n_mumax1m
    ljem_n_mumax1m=qtymem[i];i+=1
    #
    global     ljrm_n_mu1
    ljrm_n_mu1=qtymem[i];i+=1
    global     ljrm_n_mumax1
    ljrm_n_mumax1=qtymem[i];i+=1
    global     ljrm_n_mumax1m
    ljrm_n_mumax1m=qtymem[i];i+=1
    #
    global     ljrm_n_mu1_flr
    ljrm_n_mu1_flr=qtymem[i];i+=1
    global     ljrm_n_mumax1_flr
    ljrm_n_mumax1_flr=qtymem[i];i+=1
    global     ljrm_n_mumax1m_flr
    ljrm_n_mumax1m_flr=qtymem[i];i+=1
    #
    global     ljma_n_mu1
    ljma_n_mu1=qtymem[i];i+=1
    global     ljma_n_mumax1
    ljma_n_mumax1=qtymem[i];i+=1
    global     ljma_n_mumax1m
    ljma_n_mumax1m=qtymem[i];i+=1
    #
    global     ljma_n_mu1_flr
    ljma_n_mu1_flr=qtymem[i];i+=1
    global     ljma_n_mumax1_flr
    ljma_n_mumax1_flr=qtymem[i];i+=1
    global     ljma_n_mumax1m_flr
    ljma_n_mumax1m_flr=qtymem[i];i+=1
    #
    global     ljem_s_mu1
    ljem_s_mu1=qtymem[i];i+=1
    global     ljem_s_mumax1
    ljem_s_mumax1=qtymem[i];i+=1
    global     ljem_s_mumax1m
    ljem_s_mumax1m=qtymem[i];i+=1
    #
    global     ljrm_s_mu1
    ljrm_s_mu1=qtymem[i];i+=1
    global     ljrm_s_mumax1
    ljrm_s_mumax1=qtymem[i];i+=1
    global     ljrm_s_mumax1m
    ljrm_s_mumax1m=qtymem[i];i+=1
    #
    global     ljrm_s_mu1_flr
    ljrm_s_mu1_flr=qtymem[i];i+=1
    global     ljrm_s_mumax1_flr
    ljrm_s_mumax1_flr=qtymem[i];i+=1
    global     ljrm_s_mumax1m_flr
    ljrm_s_mumax1m_flr=qtymem[i];i+=1
    #
    global     ljma_s_mu1
    ljma_s_mu1=qtymem[i];i+=1
    global     ljma_s_mumax1
    ljma_s_mumax1=qtymem[i];i+=1
    global     ljma_s_mumax1m
    ljma_s_mumax1m=qtymem[i];i+=1
    #
    global     ljma_s_mu1_flr
    ljma_s_mu1_flr=qtymem[i];i+=1
    global     ljma_s_mumax1_flr
    ljma_s_mumax1_flr=qtymem[i];i+=1
    global     ljma_s_mumax1m_flr
    ljma_s_mumax1m_flr=qtymem[i];i+=1
    #
    ###################################
    return(i)


def getbobnqty():
    return(134)

def getnqty(dobob=0):
    nqtynonbob=getnonbobnqty()
    nqty=getbobnqty()*(dobob==1) + nqtynonbob
    return(nqty)



        
def getqtyvstime(ihor,horval=1.0,fmtver=2,dobob=0,whichi=None,whichn=None,altread=False):
    """
    Returns a tuple (ts,fs,mdot,pjetem,pjettot): lists of times, horizon fluxes, and Mdot
    """
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        horval=0.2
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        horval=0.2
    else:
        horval=0.6
    #
    if whichn != None and (whichi < 0 or whichi > whichn):
        print( "whichi = %d shoudl be >= 0 and < whichn = %d" % (whichi, whichn) ) ; sys.stdout.flush()
        return( -1 )
    if 'rho' in globals():
        tiny=np.finfo(rho.dtype).tiny
    else:
        tiny = np.finfo(np.float64).tiny
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    #flist.sort()
    sort_nicely(flist)
    #
    nqty=getnqty(dobob=dobob)
    #
    ####################################
    #store 1D data
    numtimeslices=len(flist)
    global qtymem
    qtymem=np.zeros((nqty,numtimeslices,nx),dtype=np.float32)
    #np.seterr(invalid='raise',divide='raise')
    #
    print "Number of time slices: %d" % numtimeslices ; sys.stdout.flush()
    if whichi >=0 and whichi < whichn:
        fname = "qty2_%d_%d.npy" % (whichi, whichn)
    else:
        fname = "qty2.npy" 
    #
    print("File trying to load or see if exist: %s" % fname) ; sys.stdout.flush()
    #
    if fmtver == 2 and os.path.isfile( fname ):
        qtymem2=np.load( fname )
        numtimeslices2 = qtymem2.shape[1]
        #require same number of variables, don't allow format changes on the fly for safety
        print "Number of previously saved time slices: %d" % numtimeslices2  ; sys.stdout.flush()
        if( numtimeslices2 >= numtimeslices ):
            print "Number of previously saved time slices is >= than of timeslices to be loaded, re-using previously saved time slices" ; sys.stdout.flush()
            #np.save("qty2.npy",qtymem2[:,:-1])  #kill last time slice
            return(qtymem2)
        else:
            assert qtymem2.shape[0] == qtymem.shape[0]
            print "Number of previously saved time slices is < than of timeslices to be loaded, re-using previously saved time slices" ; sys.stdout.flush()
            qtymem[:,0:numtimeslices2] = qtymem2[:,0:numtimeslices2]
            qtymem2=None
    elif fmtver == 1 and os.path.isfile("qty.npy"):
        qtymem2=np.load( "qty.npy" )
        numtimeslices2 = qtymem2.shape[1]
        print "Number of previously saved time slices: %d" % numtimeslices2  ; sys.stdout.flush()
        print "Instructed to use old format, reusing prev. saved slices" ; sys.stdout.flush()
        return(qtymem2)
    else:
        numtimeslices2 = 0
    #
    ###########################
    #
    # take qtymem and fill in variable names
    #
    totalnum=getqtymem(qtymem)
    if totalnum!=nqty:
        print("totalnum=%d does not equal nqty=%d" % (totalnum,nqty)) ; sys.stdout.flush()
    #
    # get starting time so can compute time differences
    start_time=datetime.now()
    ##################################
    #
    if dobob == 1:
        print "Total number of quantities: %d+%d = %d" % (totalnum, getbobnqty(), totalnum+getbobnqty()) ; sys.stdout.flush()
    else:
        print "Total number of quantities: %d" % (totalnum) ; sys.stdout.flush()
    if( whichi >=0 and whichn > 0 ):
        print "Doing every %d-th slice of %d" % (whichi, whichn) ; sys.stdout.flush()
    sys.stdout.flush()
    #end qty defs
    ##############################################
    for findex, fname in enumerate(flist):
        if( whichi >=0 and whichn > 0 ):
            if( findex % whichn != whichi ):
                continue
        #skip pre-loaded time slices
        if findex < numtimeslices2: 
            continue
        #call garbage collector -- trying to get req'd memory under control
        gc.collect()
        print( "Reading " + fname + " ..." ) ; sys.stdout.flush()
        sys.stdout.flush()
        rfd("../"+fname)
        print("Computing getqtyvstime:" + fname + " ..." + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        print("computing cvel()" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        cvel()
        print("computing Tcalcud()" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        Tcalcud()
        #
        print("Setting ts" + " time elapsed: %d" % (datetime.now()-start_time).seconds ); sys.stdout.flush()
        ts[findex]=t
        #################################
        #
        # Begin quantities
        #
        ##################################
        #
        print("HoverR" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #v4asq=bsq/(rho+ug+(gam-1)*ug)
        #mum1fake=uu[0]*(1.0+v4asq)-1.0
        # mum1fake not good marker of where jet is for near the BH.
        # mu>2 is also poor, since mu\propto sin\theta so mu turns small again near pole.
        # bsq/rho>1 much better.
        #
        beta=((gam-1)*ug)/(1E-30 + bsq*0.5)
        #
        # disk mass density scale height
        #diskcondition=(beta>2.0)
        # was (bsq/rho<1.0)
        #diskcondition=diskcondition*(mum1fake<1.0)
        # just avoid floor mass
        #cond1=(bsq/rho<30)
        #cond2=(bsq/rho<10)
        #condmaxbsqorho=cond1*(r<9.0)+cond2*(r>=9.0)
        #rinterp=(r-9.0)*(1.0-0.0)/(0.0-9.0) # gives 0 for use near 9   gives 1 for use near 0
        #rinterp[rinterp>1.0]=1.0
        #rinterp[rinterp<0.0]=0.0
        #condmaxbsqorho=(bsq/rho < rinterp*30.0 + (1.0-rinterp)*10.0)
        diskcondition1=condmaxbsqorho
        diskcondition2=condmaxbsqorho
        # was denfactor=rho, but want uniform with corona and jet
        hoverr3d,thetamid3d=horcalc(hortype=1,which1=diskcondition1,which2=diskcondition2,denfactor=rho)
        hoverr[findex]=hoverr3d.sum(2).sum(1)/(ny*nz)
        thetamid[findex]=thetamid3d.sum(2).sum(1)/(ny*nz)
        #
        #
        # disk-corona boundary
        coronacondition1=(beta<1.0)
        coronacondition1=coronacondition1*(beta>0.5)
        coronacondition1=coronacondition1*condmaxbsqorho
        coronacondition2=(beta<1.0)
        coronacondition2=coronacondition2*(beta>0.1)
        coronacondition2=coronacondition2*condmaxbsqorho
        # was (bsq/rho<1.0)
        hoverr3dcorona,thetamid3dcorona=horcalc(hortype=2,which1=coronacondition1,which2=coronacondition2,denfactor=bsq+rho+gam*ug)
        hoverrcorona[findex]=hoverr3dcorona.sum(2).sum(1)/(ny*nz)
        thetamidcorona[findex]=thetamid3dcorona.sum(2).sum(1)/(ny*nz)
        #
        # corona-jet boundary
        # was jetcondition=(bsq/rho>2.0)
        #jetcondition=(mum1fake>1.0)
        #jetcondition=(mum1fake<1.5)
        #jetcondition=jetcondition*(mum1fake>1.0)
        # can't use just bsq/rho<2.0 below, since too sparse and some radii have no such smallish range of bsq/rho
        jetcondition1=(bsq/rho<2.0)
        jetcondition1=jetcondition1*(bsq/rho>1.0)
        jetcondition2=condmaxbsqorho
        jetcondition2=jetcondition2*(bsq/rho>1.0)
        hoverr3djet,thetamid3djet=horcalc(hortype=2,which1=jetcondition1,which2=jetcondition2,denfactor=bsq+rho+gam*ug)
        hoverr_jet[findex]=hoverr3djet.sum(2).sum(1)/(ny*nz)
        thetamidjet[findex]=thetamid3djet.sum(2).sum(1)/(ny*nz)
        #
        diskcondition=condmaxbsqorho
        diskcondition=diskcondition*(beta>1.0)
        # was (bsq/rho<1.0)
        #diskcondition=diskcondition*(mum1fake<1.0)
        #
        diskeqcondition=diskcondition
        # (qmri3d,norm3d,q3mri3d,norm33d,iq2mri3d)
        qmri3ddisk,normmri3ddisk,q3mri3ddisk,norm3mri3ddisk,iq2mri3ddisk=Qmri_simple(which=diskeqcondition)
        qmridisk[findex]=qmri3ddisk.sum(2).sum(1)/(ny*nz)
        # number of wavelengths per disk scale height
        iq2mridisk[findex]=iq2mri3ddisk.sum(2).sum(1)/(ny*nz)
        normmridisk[findex]=normmri3ddisk.sum(2).sum(1)/(ny*nz)
        #
        qmri3ddiskweak,normmri3ddiskweak,q3mri3ddiskweak,norm3mri3ddiskweak,iq2mri3ddiskweak=Qmri_simple(weak=1,which=diskeqcondition)
        qmridiskweak[findex]=qmri3ddiskweak.sum(2).sum(1)/(ny*nz)
        # number of wavelengths per disk scale height
        iq2mridiskweak[findex]=iq2mri3ddiskweak.sum(2).sum(1)/(ny*nz)
        normmridiskweak[findex]=normmri3ddiskweak.sum(2).sum(1)/(ny*nz)
        #
        diskaltcondition=(bsq/rho<1.0)
        #diskaltcondition=diskaltcondition*(beta>1.0)
        betamin[findex,0],betaavg[findex,0],betaratofavg[findex,0],betaratofmax[findex,0]=betascalc(which=diskaltcondition)
        # no condition, use clean versions if required
        betamin[findex,1:17]=luminosities()
        #
        #
        #################################
        print("alphamag" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #################################
        #
        #
        diskcondition=condmaxbsqorho
        denfactor=1.0 + rho*0.0
        keywordsrhosq={'which': diskcondition}
        rhosqint=intangle(gdet*denfactor,**keywordsrhosq)+tiny
        #
        diskcondition=condmaxbsqorho
        keywordsrhosq={'which': diskcondition}
        alphamag1[findex]=intangle(gdet*np.abs(bu[1]*np.sqrt(gv3[1,1])*bd[3]*np.sqrt(gn3[3,3]))/(bsq*0.5+(gam-1.0)*ug)*denfactor,**keywordsrhosq)/rhosqint
        #
        diskcondition=(bsq/rho<1)
        keywordsrhosq={'which': diskcondition}
        alphamag2[findex]=intangle(gdet*np.abs(bu[1]*np.sqrt(gv3[1,1])*bd[3]*np.sqrt(gn3[3,3]))/(bsq*0.5+(gam-1.0)*ug)*denfactor,**keywordsrhosq)/rhosqint
        #
        denfactor=rho**2
        diskcondition=condmaxbsqorho
        keywordsrhosq={'which': diskcondition}
        rhosqint=intangle(gdet*denfactor,**keywordsrhosq)+tiny
        alphamag3[findex]=intangle(gdet*np.abs(bu[1]*np.sqrt(gv3[1,1])*bd[3]*np.sqrt(gn3[3,3]))/(bsq*0.5+(gam-1.0)*ug)*denfactor,**keywordsrhosq)/rhosqint
        #
        #
        #
        #
        #
        #
        #################################
        print("all primitives in various forms" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #################################
        #
        # whether velocity outputted will be 4-vel or fake orthonormal 3-vel
        output4vel=1
        #
        if output4vel==0:
            # avoid nan inside r=2M.  But set get fabs, so can recover values
            mygv300=-gv3[0,0]
            mygv300=np.fabs(mygv300)
            iuu0hat=1.0/(uu[0]*np.sqrt(mygv300))
            myuu0=uu[0]*np.sqrt(mygv300)
            myuu1=uu[1]*np.sqrt(gv3[1,1])*iuu0hat
            myuu2=uu[2]*np.sqrt(gv3[2,2])*iuu0hat
            myuu3=uu[3]*np.sqrt(gv3[3,3])*iuu0hat
            myB1=B[1]*np.sqrt(gv3[1,1])
            myB2=B[2]*np.sqrt(gv3[2,2])
            myB3=B[3]*np.sqrt(gv3[3,3])
            mybu1=bu[1]*np.sqrt(gv3[1,1])
            mybu2=bu[2]*np.sqrt(gv3[2,2])
            mybu3=bu[3]*np.sqrt(gv3[3,3])
        elif output4vel==1:
            # fully obtain approximate invariant 3-vel and 4-field so averaging makes sense
            sigmaks=r**2+(a*np.cos(h))**2
            deltaks=r**2-2*r+a**2
            Aks=(r**2+a**2)**2-a**2*deltaks*(np.sin(h))**2
            #
            gvks00=-(1.0-2.0*r/sigmaks)
            gvks11=(1.0+2.0*r/sigmaks)
            gvks22=sigmaks
            gvks33=(np.sin(h))**2*(sigmaks + a**2*(1.0 + 2.0*r/sigmaks)*(np.sin(h))**2)
            #
            myuu0=uu[0]*dxdxp[0,0]
            myuu1=(uu[1]*dxdxp[1,1] + uu[2]*dxdxp[1,2])*np.sqrt(gvks11)/myuu0
            myuu2=(uu[1]*dxdxp[2,1] + uu[2]*dxdxp[2,2])*np.sqrt(gvks22)/myuu0
            myuu3=(uu[3]*dxdxp[3,3])*np.sqrt(gvks33)/myuu0
            myB1=(B[1]*dxdxp[1,1] + B[2]*dxdxp[1,2])*np.sqrt(gvks11)
            myB2=(B[1]*dxdxp[2,1] + B[2]*dxdxp[2,2])*np.sqrt(gvks22)
            myB3=(B[3]*dxdxp[3,3])*np.sqrt(gvks33)
            mybu1=(bu[1]*dxdxp[1,1] + bu[2]*dxdxp[1,2])*np.sqrt(gvks11)
            mybu2=(bu[1]*dxdxp[2,1] + bu[2]*dxdxp[2,2])*np.sqrt(gvks22)
            mybu3=(bu[3]*dxdxp[3,3])*np.sqrt(gvks33)
        elif output4vel==2:
            print("Not yet")
        #
        # 0 = 1 + u^t u_t + u^r u_r + u^h u_h + u^p u_p
        # 0 = 1 + u^r u_r / (1+u^t u_t) + u^h u_h / (1+u^t u_t) + u^p u_p / (1+u^t u_t)
        # 1/(-u^t u_t) + 1 =  + u^r u_r / (-u^t u_t) + u^h u_h / (-u^t u_t) + u^p u_p / (-u^t u_t)
        #
        #
        #
        #
        #############
        print("over full flow" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        #rhosq:
        # for most dense part of flow:
        #denfactor=rho**2
        # for entire flow:
        denfactor=1.0 + rho*0.0
        #
        diskcondition=condmaxbsqorho
        keywordsrhosq={'which': diskcondition}
        rhosqint=intangle(gdet*denfactor,**keywordsrhosq)+tiny # gdet is 2d by default
        rhosqs[findex]=rhosqint
        maxrhosq2d=(denfactor*diskcondition).max(1)+tiny
        maxrhosq3d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosq3d[:,j,:] = maxrhosq2d
        rhosrhosq[findex]=intangle(gdet*denfactor*rho,**keywordsrhosq)/rhosqint
        ugsrhosq[findex]=intangle(gdet*denfactor*ug,**keywordsrhosq)/rhosqint
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        # yes, over whole disk so include jet for vel/field
        diskcondition=1 + condmaxbsqorho*0.0
        keywordsrhosq={'which': diskcondition}
        rhosqint=intangle(gdet*denfactor,**keywordsrhosq)+tiny
        uu0rhosq[findex]=intangle(gdet*denfactor*myuu0,**keywordsrhosq)/rhosqint
        vus1rhosq[findex]=intangle(gdet*denfactor*myuu1,**keywordsrhosq)/rhosqint
        vuas1rhosq[findex]=intangle(gdet*denfactor*np.abs(myuu1),**keywordsrhosq)/rhosqint
        vus3rhosq[findex]=intangle(gdet*denfactor*myuu3,**keywordsrhosq)/rhosqint
        vuas3rhosq[findex]=intangle(gdet*denfactor*np.abs(myuu3),**keywordsrhosq)/rhosqint
        Bs1rhosq[findex]=intangle(gdet*myB1*denfactor,**keywordsrhosq)/rhosqint
        Bas1rhosq[findex]=intangle(gdet*np.fabs(myB1)*denfactor,**keywordsrhosq)/rhosqint
        Bs2rhosq[findex]=intangle(gdet*myB2*denfactor,**keywordsrhosq)/rhosqint
        Bas2rhosq[findex]=intangle(gdet*np.fabs(myB2)*denfactor,**keywordsrhosq)/rhosqint
        Bs3rhosq[findex]=intangle(gdet*myB3*denfactor,**keywordsrhosq)/rhosqint
        Bas3rhosq[findex]=intangle(gdet*np.fabs(myB3)*denfactor,**keywordsrhosq)/rhosqint
        bs1rhosq[findex]=intangle(gdet*mybu1*denfactor,**keywordsrhosq)/rhosqint
        bas1rhosq[findex]=intangle(gdet*np.fabs(mybu1)*denfactor,**keywordsrhosq)/rhosqint
        bs2rhosq[findex]=intangle(gdet*mybu2*denfactor,**keywordsrhosq)/rhosqint
        bas2rhosq[findex]=intangle(gdet*np.fabs(mybu2)*denfactor,**keywordsrhosq)/rhosqint
        bs3rhosq[findex]=intangle(gdet*mybu3*denfactor,**keywordsrhosq)/rhosqint
        bas3rhosq[findex]=intangle(gdet*np.fabs(mybu3)*denfactor,**keywordsrhosq)/rhosqint
        bsqrhosq[findex]=intangle(gdet*bsq*denfactor,**keywordsrhosq)/rhosqint
        #rhosq:
        #
        #############
        print("over disk+corona" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        #rhosqdc:
        # for most dense part of flow:
        #denfactor=rho**2
        # for entire flow:
        denfactor=1.0 + rho*0.0
        #
        diskcondition=condmaxbsqorho*(bsq/rho<1.0) # non-jet
        keywordsrhosqdc={'which': diskcondition}
        rhosqdcint=intangle(gdet*denfactor,**keywordsrhosqdc)+tiny # gdet is 2d by default
        rhosqdcs[findex]=rhosqdcint
        maxrhosqdc2d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqdc3d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqdc3d[:,j,:] = maxrhosqdc2d
        rhosrhosqdc[findex]=intangle(gdet*denfactor*rho,**keywordsrhosqdc)/rhosqdcint
        ugsrhosqdc[findex]=intangle(gdet*denfactor*ug,**keywordsrhosqdc)/rhosqdcint
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        diskcondition=condmaxbsqorho*(bsq/rho<1.0) # non-jet
        keywordsrhosqdc={'which': diskcondition}
        rhosqdcint=intangle(gdet*denfactor,**keywordsrhosqdc)+tiny
        uu0rhosqdc[findex]=intangle(gdet*myuu0*denfactor,**keywordsrhosqdc)/rhosqdcint
        vus1rhosqdc[findex]=intangle(gdet*myuu1*denfactor,**keywordsrhosqdc)/rhosqdcint
        vuas1rhosqdc[findex]=intangle(gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqdc)/rhosqdcint
        vus3rhosqdc[findex]=intangle(gdet*myuu3*denfactor,**keywordsrhosqdc)/rhosqdcint
        vuas3rhosqdc[findex]=intangle(gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqdc)/rhosqdcint
        Bs1rhosqdc[findex]=intangle(gdet*myB1*denfactor,**keywordsrhosqdc)/rhosqdcint
        Bas1rhosqdc[findex]=intangle(gdet*np.fabs(myB1)*denfactor,**keywordsrhosqdc)/rhosqdcint
        Bs2rhosqdc[findex]=intangle(gdet*myB2*denfactor,**keywordsrhosqdc)/rhosqdcint
        Bas2rhosqdc[findex]=intangle(gdet*np.fabs(myB2)*denfactor,**keywordsrhosqdc)/rhosqdcint
        Bs3rhosqdc[findex]=intangle(gdet*myB3*denfactor,**keywordsrhosqdc)/rhosqdcint
        Bas3rhosqdc[findex]=intangle(gdet*np.fabs(myB3)*denfactor,**keywordsrhosqdc)/rhosqdcint
        bs1rhosqdc[findex]=intangle(gdet*mybu1*denfactor,**keywordsrhosqdc)/rhosqdcint
        bas1rhosqdc[findex]=intangle(gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqdc)/rhosqdcint
        bs2rhosqdc[findex]=intangle(gdet*mybu2*denfactor,**keywordsrhosqdc)/rhosqdcint
        bas2rhosqdc[findex]=intangle(gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqdc)/rhosqdcint
        bs3rhosqdc[findex]=intangle(gdet*mybu3*denfactor,**keywordsrhosqdc)/rhosqdcint
        bas3rhosqdc[findex]=intangle(gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqdc)/rhosqdcint
        bsqrhosqdc[findex]=intangle(gdet*bsq*denfactor,**keywordsrhosqdc)/rhosqdcint
        #rhosqdc:
        #
        #############
        print("over dense part of disk+corona" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        #rhosqdcden:
        # for most dense part of flow:
        #denfactor=rho**2
        # for entire flow:
        denfactor=rho
        #
        diskcondition=condmaxbsqorho # full non-jet
        keywordsrhosqdcden={'which': diskcondition}
        rhosqdcdenint=intangle(gdet*denfactor,**keywordsrhosqdcden)+tiny # gdet is 2d by default
        rhosqdcdens[findex]=rhosqdcdenint
        maxrhosqdcden2d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqdcden3d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqdcden3d[:,j,:] = maxrhosqdcden2d
        rhosrhosqdcden[findex]=intangle(gdet*denfactor*rho,**keywordsrhosqdcden)/rhosqdcdenint
        ugsrhosqdcden[findex]=intangle(gdet*denfactor*ug,**keywordsrhosqdcden)/rhosqdcdenint
        denfactor=rho
        diskcondition=condmaxbsqorho # full non-jet
        keywordsrhosqdcden={'which': diskcondition}
        rhosqdcdenint=intangle(gdet*denfactor,**keywordsrhosqdcden)+tiny
        uu0rhosqdcden[findex]=intangle(gdet*myuu0*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        vus1rhosqdcden[findex]=intangle(gdet*myuu1*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        vuas1rhosqdcden[findex]=intangle(gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        vus3rhosqdcden[findex]=intangle(gdet*myuu3*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        vuas3rhosqdcden[findex]=intangle(gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        Bs1rhosqdcden[findex]=intangle(gdet*myB1*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        Bas1rhosqdcden[findex]=intangle(gdet*np.fabs(myB1)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        Bs2rhosqdcden[findex]=intangle(gdet*myB2*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        Bas2rhosqdcden[findex]=intangle(gdet*np.fabs(myB2)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        Bs3rhosqdcden[findex]=intangle(gdet*myB3*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        Bas3rhosqdcden[findex]=intangle(gdet*np.fabs(myB3)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bs1rhosqdcden[findex]=intangle(gdet*mybu1*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bas1rhosqdcden[findex]=intangle(gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bs2rhosqdcden[findex]=intangle(gdet*mybu2*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bas2rhosqdcden[findex]=intangle(gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bs3rhosqdcden[findex]=intangle(gdet*mybu3*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bas3rhosqdcden[findex]=intangle(gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        bsqrhosqdcden[findex]=intangle(gdet*bsq*denfactor,**keywordsrhosqdcden)/rhosqdcdenint
        #rhosqdcden:
        #
        #############
        print("at equator and portion of \phi" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        # for entire flow:
        denfactor=1.0 + rho*0.0
        # pick out equator (within 3 cells to smear out grid-scale noise) and a restricted portion of \phi in order to avoid averaging over warping disk
        diskcondition0=(np.abs(tj-ny/2)<3)
        if nz>1:
            diskcondition0=diskcondition0*(ph>0.0)
            diskcondition0=diskcondition0*(ph<np.pi/4.0)
        #
        diskcondition=diskcondition0*condmaxbsqorho
        keywordsrhosqeq={'which': diskcondition}
        rhosqeqint=intangle(gdet*denfactor,**keywordsrhosqeq)+tiny
        rhosqeqs[findex]=rhosqeqint
        maxrhosqeq2d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqeq3d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqeq3d[:,j,:] = maxrhosqeq2d
        rhosrhosqeq[findex]=intangle(gdet*denfactor*rho,**keywordsrhosqeq)/rhosqeqint
        ugsrhosqeq[findex]=intangle(gdet*denfactor*ug,**keywordsrhosqeq)/rhosqeqint
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        # yes avoid restriction, at equator no matter if disk or jet
        diskcondition=diskcondition0*(1 + condmaxbsqorho*0.0)
        keywordsrhosqeq={'which': diskcondition}
        rhosqeqint=intangle(gdet*denfactor,**keywordsrhosqeq)+tiny
        uu0rhosqeq[findex]=intangle(gdet*myuu0*denfactor,**keywordsrhosqeq)/rhosqeqint
        vus1rhosqeq[findex]=intangle(gdet*myuu1*denfactor,**keywordsrhosqeq)/rhosqeqint
        vuas1rhosqeq[findex]=intangle(gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqeq)/rhosqeqint
        vus3rhosqeq[findex]=intangle(gdet*myuu3*denfactor,**keywordsrhosqeq)/rhosqeqint
        vuas3rhosqeq[findex]=intangle(gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqeq)/rhosqeqint
        Bs1rhosqeq[findex]=intangle(gdet*myB1*denfactor,**keywordsrhosqeq)/rhosqeqint
        Bas1rhosqeq[findex]=intangle(gdet*np.fabs(myB1)*denfactor,**keywordsrhosqeq)/rhosqeqint
        Bs2rhosqeq[findex]=intangle(gdet*myB2*denfactor,**keywordsrhosqeq)/rhosqeqint
        Bas2rhosqeq[findex]=intangle(gdet*np.fabs(myB2)*denfactor,**keywordsrhosqeq)/rhosqeqint
        Bs3rhosqeq[findex]=intangle(gdet*myB3*denfactor,**keywordsrhosqeq)/rhosqeqint
        Bas3rhosqeq[findex]=intangle(gdet*np.fabs(myB3)*denfactor,**keywordsrhosqeq)/rhosqeqint
        bs1rhosqeq[findex]=intangle(gdet*mybu1*denfactor,**keywordsrhosqeq)/rhosqeqint
        bas1rhosqeq[findex]=intangle(gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqeq)/rhosqeqint
        bs2rhosqeq[findex]=intangle(gdet*mybu2*denfactor,**keywordsrhosqeq)/rhosqeqint
        bas2rhosqeq[findex]=intangle(gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqeq)/rhosqeqint
        bs3rhosqeq[findex]=intangle(gdet*mybu3*denfactor,**keywordsrhosqeq)/rhosqeqint
        bas3rhosqeq[findex]=intangle(gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqeq)/rhosqeqint
        bsqrhosqeq[findex]=intangle(gdet*bsq*denfactor,**keywordsrhosqeq)/rhosqeqint
        #
        #############
        print("at 2.5H/R and portion of \phi" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        # for entire flow:
        denfactor=1.0 + rho*0.0
        # pick out *at* horpickit*H/R
        horpickit=2.5
        diskcondition0=(np.abs(h-np.pi*0.5)<horpickit*hoverr3d)
        diskcondition0=diskcondition0*(np.abs(h-np.pi*0.5)>0.5*horpickit*hoverr3d)
        if nz>1:
            diskcondition0=diskcondition0*(ph>0.0)
            diskcondition0=diskcondition0*(ph<np.pi/4.0)
        diskcondition=diskcondition0*condmaxbsqorho
        # and avoid averaging over warp by restricing phi range
        keywordsrhosqhorpick={'which': diskcondition}
        rhosqhorpickint=intangle(gdet*denfactor,**keywordsrhosqhorpick)+tiny
        rhosqhorpicks[findex]=rhosqhorpickint
        maxrhosqhorpick2d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqhorpick3d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqhorpick3d[:,j,:] = maxrhosqhorpick2d
        rhosrhosqhorpick[findex]=intangle(gdet*denfactor*rho,**keywordsrhosqhorpick)/rhosqhorpickint
        ugsrhosqhorpick[findex]=intangle(gdet*denfactor*ug,**keywordsrhosqhorpick)/rhosqhorpickint
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        # don't restrict since fixed point in space related to disk but not entirely.  The bsq/rho condition would also remove the disk at inner radii even for H/R within hoverr3d that is mass-density weighted.
        diskcondition=diskcondition0*(1 + condmaxbsqorho*0.0)
        keywordsrhosqhorpick={'which': diskcondition}
        rhosqhorpickint=intangle(gdet*denfactor,**keywordsrhosqhorpick)+tiny
        uu0rhosqhorpick[findex]=intangle(gdet*myuu0*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        vus1rhosqhorpick[findex]=intangle(gdet*myuu1*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        vuas1rhosqhorpick[findex]=intangle(gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        vus3rhosqhorpick[findex]=intangle(gdet*myuu3*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        vuas3rhosqhorpick[findex]=intangle(gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        Bs1rhosqhorpick[findex]=intangle(gdet*myB1*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        Bas1rhosqhorpick[findex]=intangle(gdet*np.fabs(myB1)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        Bs2rhosqhorpick[findex]=intangle(gdet*myB2*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        Bas2rhosqhorpick[findex]=intangle(gdet*np.fabs(myB2)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        Bs3rhosqhorpick[findex]=intangle(gdet*myB3*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        Bas3rhosqhorpick[findex]=intangle(gdet*np.fabs(myB3)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bs1rhosqhorpick[findex]=intangle(gdet*mybu1*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bas1rhosqhorpick[findex]=intangle(gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bs2rhosqhorpick[findex]=intangle(gdet*mybu2*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bas2rhosqhorpick[findex]=intangle(gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bs3rhosqhorpick[findex]=intangle(gdet*mybu3*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bas3rhosqhorpick[findex]=intangle(gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        bsqrhosqhorpick[findex]=intangle(gdet*bsq*denfactor,**keywordsrhosqhorpick)/rhosqhorpickint
        #
        ##2h
        keywords2h={'hoverr': 2*horval, 'which': diskcondition}
        #denfactor=1.0 + rho*0.0
        #gdetint=intangle(gdet*denfactor,**keywords2h)+tiny
        #gdetint2h[findex]=gdetint
        #rhos2h[findex]=intangle(gdet*rho,**keywords2h)/gdetint
        #ugs2h[findex]=intangle(gdet*ug,**keywords2h)/gdetint
        #uu02h[findex]=intangle(gdet*myuu0,**keywords2h)/gdetint
        #vus12h[findex]=intangle(gdet*myuu1,**keywords2h)/gdetint
        #vuas12h[findex]=intangle(gdet*np.fabs(myuu1),**keywords2h)/gdetint
        #vus32h[findex]=intangle(gdet*myuu3,**keywords2h)/gdetint
        #vuas32h[findex]=intangle(gdet*np.fabs(myuu3),**keywords2h)/gdetint
        #Bs12h[findex]=intangle(gdet*myB1,**keywords2h)/gdetint
        #Bas12h[findex]=intangle(np.abs(gdet*myB1),**keywords2h)/gdetint
        #Bs22h[findex]=intangle(gdet*myB2,**keywords2h)/gdetint
        #Bas22h[findex]=intangle(np.abs(gdet*myB2),**keywords2h)/gdetint
        #Bs32h[findex]=intangle(gdet*myB3,**keywords2h)/gdetint
        #Bas32h[findex]=intangle(np.abs(gdet*myB3),**keywords2h)/gdetint
        ##4h
        keywords4h={'hoverr': 4*horval, 'which': diskcondition}
        #denfactor=1.0 + rho*0.0
        #gdetint=intangle(gdet*denfactor,**keywords4h)+tiny
        #gdetint4h[findex]=gdetint
        #rhos4h[findex]=intangle(gdet*rho,**keywords4h)/gdetint
        #ugs4h[findex]=intangle(gdet*ug,**keywords4h)/gdetint
        #uu04h[findex]=intangle(gdet*myuu0,**keywords4h)/gdetint
        #vus14h[findex]=intangle(gdet*myuu1,**keywords4h)/gdetint
        #vuas14h[findex]=intangle(gdet*np.fabs(myuu1),**keywords4h)/gdetint
        #vus34h[findex]=intangle(gdet*myuu3,**keywords4h)/gdetint
        #vuas34h[findex]=intangle(gdet*np.fabs(myuu3),**keywords4h)/gdetint
        #Bs14h[findex]=intangle(gdet*myB1,**keywords4h)/gdetint
        #Bas14h[findex]=intangle(np.abs(gdet*myB1),**keywords4h)/gdetint
        #Bs24h[findex]=intangle(gdet*myB2,**keywords4h)/gdetint
        #Bas24h[findex]=intangle(np.abs(gdet*myB2),**keywords4h)/gdetint
        #Bs34h[findex]=intangle(gdet*myB3,**keywords4h)/gdetint
        #Bas34h[findex]=intangle(np.abs(gdet*myB3),**keywords4h)/gdetint
        ##
        #############
        print("within 2.0H/R" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        #2.0hor
        diskcondition=condmaxbsqorho
        keywordshor={'hoverr': 2.0*hoverr3d, 'thetamid': thetamid3d, 'which': diskcondition}
        denfactor=1.0 + rho*0.0
        gdetint=intangle(gdet*denfactor,**keywordshor) # gdet is 2D by default
        gdetinthor[findex]=gdetint+tiny
        rhoshor[findex]=intangle(gdet*rho,**keywordshor)/gdetint
        ugshor[findex]=intangle(gdet*ug,**keywordshor)/gdetint
        # no restriction for velocity or field quantities!
        #diskcondition=1 + condmaxbsqorho*0.0
        # no, should still restrict since this is choosing within 2H/R -- so focus is the disk!
        diskcondition=condmaxbsqorho
        keywordshor={'hoverr': 2.0*hoverr3d, 'thetamid': thetamid3d, 'which': diskcondition}
        gdetint=intangle(gdet*denfactor,**keywordshor)
        gdetinthor[findex]=gdetint+tiny
        bsqshor[findex]=intangle(gdet*bsq,**keywordshor)/gdetint
        bsqorhoshor[findex]=intangle(gdet*(bsq/rho),**keywordshor)/gdetint
        bsqougshor[findex]=intangle(gdet*(bsq/ug),**keywordshor)/gdetint
        uu0hor[findex]=intangle(gdet*myuu0,**keywordshor)/gdetint
        vus1hor[findex]=intangle(gdet*myuu1,**keywordshor)/gdetint
        vuas1hor[findex]=intangle(gdet*np.fabs(myuu1),**keywordshor)/gdetint
        vus3hor[findex]=intangle(gdet*myuu3,**keywordshor)/gdetint
        vuas3hor[findex]=intangle(gdet*np.fabs(myuu3),**keywordshor)/gdetint
        Bs1hor[findex]=intangle(gdet*myB1,**keywordshor)/gdetint
        Bas1hor[findex]=intangle(np.abs(gdet*myB1),**keywordshor)/gdetint
        Bs2hor[findex]=intangle(gdet*myB2,**keywordshor)/gdetint
        Bas2hor[findex]=intangle(np.abs(gdet*myB2),**keywordshor)/gdetint
        Bs3hor[findex]=intangle(gdet*myB3,**keywordshor)/gdetint
        Bas3hor[findex]=intangle(np.abs(gdet*myB3),**keywordshor)/gdetint
        bs1hor[findex]=intangle(gdet*mybu1,**keywordshor)/gdetint
        bas1hor[findex]=intangle(np.abs(gdet*mybu1),**keywordshor)/gdetint
        bs2hor[findex]=intangle(gdet*mybu2,**keywordshor)/gdetint
        bas2hor[findex]=intangle(np.abs(gdet*mybu2),**keywordshor)/gdetint
        bs3hor[findex]=intangle(gdet*mybu3,**keywordshor)/gdetint
        bas3hor[findex]=intangle(np.abs(gdet*mybu3),**keywordshor)/gdetint
        bsqhor[findex]=intangle(gdet*bsq,**keywordshor)/gdetint
        #
        #
        #
        #
        #
        #
        #############
        print("Along theta, not r.  Only portion in \phi to avoid washing out warping" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        #
        #
        print("pick out *at* r\sim 4M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        # for entire flow:
        denfactor=1.0 + rho*0.0
        pickr=4.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        if nz>1:
            phiin=0.0
            phiout=np.pi/4.0  # pi/4 so can capture m=1,2,3,4,5,6,7,8 modes in time series while averaging over noise to promote signal
        else:
            phiin=0.0
            phiout=2.0*np.pi
        #
        diskcondition=condmaxbsqorho
        # and avoid averaging over warp by restricing phi range
        keywordsrhosqrad4={'which': diskcondition}
        rhosqrad4int=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor,**keywordsrhosqrad4)+tiny
        rhosqrad4[findex]=rhosqrad4int
        maxrhosqrad42d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqrad43d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqrad43d[:,j,:] = maxrhosqrad42d
        rhosrhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*rho,**keywordsrhosqrad4)/rhosqrad4int
        ugsrhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*ug,**keywordsrhosqrad4)/rhosqrad4int
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        diskcondition=(1 + condmaxbsqorho*0.0)
        keywordsrhosqrad4={'which': diskcondition}
        rhosqrad4int=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor,**keywordsrhosqrad4)+tiny
        uu0rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu0*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        #uu0rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*uu[0],**keywordsrhosqrad4)/rhosqrad4int
        vus1rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu1*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        vuas1rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        vus3rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu3*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        vuas3rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        Bs1rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB1*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        Bas1rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB1)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        Bs2rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB2*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        Bas2rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB2)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        Bs3rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB3*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        Bas3rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB3)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bs1rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu1*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bas1rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bs2rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu2*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bas2rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bs3rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu3*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bas3rhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        bsqrhosqrad4[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*bsq*denfactor,**keywordsrhosqrad4)/rhosqrad4int
        #
        #
        print("pick out *at* r\sim 8M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        # for entire flow:
        denfactor=1.0 + rho*0.0
        pickr=8.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        if nz>1:
            phiin=0.0
            phiout=np.pi/4.0
        else:
            phiin=0.0
            phiout=2.0*np.pi
        #
        diskcondition=condmaxbsqorho
        # and avoid averaging over warp by restricing phi range
        keywordsrhosqrad8={'which': diskcondition}
        rhosqrad8int=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor,**keywordsrhosqrad8)+tiny
        rhosqrad8[findex]=rhosqrad8int
        maxrhosqrad82d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqrad83d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqrad83d[:,j,:] = maxrhosqrad82d
        rhosrhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*rho,**keywordsrhosqrad8)/rhosqrad8int
        ugsrhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*ug,**keywordsrhosqrad8)/rhosqrad8int
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        diskcondition=(1 + condmaxbsqorho*0.0)
        keywordsrhosqrad8={'which': diskcondition}
        rhosqrad8int=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor,**keywordsrhosqrad8)+tiny
        uu0rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu0*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        #uu0rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*uu[0],**keywordsrhosqrad8)/rhosqrad8int
        vus1rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu1*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        vuas1rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        vus3rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu3*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        vuas3rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        Bs1rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB1*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        Bas1rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB1)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        Bs2rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB2*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        Bas2rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB2)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        Bs3rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB3*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        Bas3rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB3)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bs1rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu1*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bas1rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bs2rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu2*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bas2rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bs3rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu3*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bas3rhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        bsqrhosqrad8[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*bsq*denfactor,**keywordsrhosqrad8)/rhosqrad8int
        #
        #
        print("pick out *at* r\sim 30M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        # for entire flow:
        denfactor=1.0 + rho*0.0
        pickr=30.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        if nz>1:
            phiin=0.0
            phiout=np.pi/4.0
        else:
            phiin=0.0
            phiout=2.0*np.pi
        #
        diskcondition=condmaxbsqorho
        # and avoid averaging over warp by restricing phi range
        keywordsrhosqrad30={'which': diskcondition}
        rhosqrad30int=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor,**keywordsrhosqrad30)+tiny
        rhosqrad30[findex]=rhosqrad30int
        maxrhosqrad302d=(denfactor*diskcondition).max(1)+tiny
        maxrhosqrad303d=np.empty_like(rho)
        for j in np.arange(0,ny):
            maxrhosqrad303d[:,j,:] = maxrhosqrad302d
        rhosrhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*rho,**keywordsrhosqrad30)/rhosqrad30int
        ugsrhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*ug,**keywordsrhosqrad30)/rhosqrad30int
        # no restriction for velocity or field quantities! (as long as denfactor=1 this is good)
        denfactor=1.0 + rho*0.0
        diskcondition=(1 + condmaxbsqorho*0.0)
        keywordsrhosqrad30={'which': diskcondition}
        rhosqrad30int=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor,**keywordsrhosqrad30)+tiny
        uu0rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu0*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        #uu0rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*denfactor*uu[0],**keywordsrhosqrad30)/rhosqrad30int
        vus1rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu1*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        vuas1rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myuu1)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        vus3rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myuu3*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        vuas3rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myuu3)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        Bs1rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB1*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        Bas1rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB1)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        Bs2rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB2*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        Bas2rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB2)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        Bs3rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*myB3*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        Bas3rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(myB3)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bs1rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu1*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bas1rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu1)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bs2rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu2*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bas2rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu2)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bs3rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*mybu3*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bas3rhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*np.fabs(mybu3)*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        bsqrhosqrad30[findex]=intrpvsh(rin=rin,rout=rout,phiin=phiin,phiout=phiout,qty=gdet*bsq*denfactor,**keywordsrhosqrad30)/rhosqrad30int
        #
        #
        #
        #
        #
        #
        #
        #############
        print("Along m (i.e. power for \exp(im\phi) modes)." + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #############
        #
        #
        print("DISK+CORONA ONLY (never jet)" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        print("pick out *at* r\sim r+" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=rhor
        spreadr=0.1*pickr
        rin=max(pickr-spreadr,1.01*Rin)
        rout=pickr+spreadr
        print("rin=%g rout=%g Rin=%g rhor=%g r0=%g" % (rin,rout,Rin,rhor,r[0,0,0]))
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_diskcorona_phipow_radhor={'which': diskcondition}
        maxbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=rhor
        rhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        rhosrhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_diskcorona_phipow_radhor)
        ugsrhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_diskcorona_phipow_radhor)
        uu0rhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        vuas3rhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        bas1rhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        bas2rhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        bas3rhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        bsqrhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        FMrhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        FEMArhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        FEEMrhosq_diskcorona_phipow_radhor[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_radhor)
        #
        #
        print("pick out *at* r\sim 4M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=4.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_diskcorona_phipow_rad4={'which': diskcondition}
        maxbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=4
        rhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        rhosrhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_diskcorona_phipow_rad4)
        ugsrhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_diskcorona_phipow_rad4)
        uu0rhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        vuas3rhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        bas1rhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        bas2rhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        bas3rhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        bsqrhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        FMrhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        FEMArhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        FEEMrhosq_diskcorona_phipow_rad4[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_rad4)
        #
        #
        print("pick out *at* r\sim 8M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=8.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_diskcorona_phipow_rad8={'which': diskcondition}
        maxbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=8
        rhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        rhosrhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_diskcorona_phipow_rad8)
        ugsrhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_diskcorona_phipow_rad8)
        uu0rhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        vuas3rhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        bas1rhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        bas2rhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        bas3rhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        bsqrhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        FMrhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        FEMArhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        FEEMrhosq_diskcorona_phipow_rad8[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_rad8)
        #
        print("pick out *at* r\sim 30M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=30.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_diskcorona_phipow_rad30={'which': diskcondition}
        maxbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=30
        rhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        rhosrhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_diskcorona_phipow_rad30)
        ugsrhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_diskcorona_phipow_rad30)
        uu0rhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        vuas3rhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        bas1rhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        bas2rhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        bas3rhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        bsqrhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        FMrhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        FEMArhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        FEEMrhosq_diskcorona_phipow_rad30[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_diskcorona_phipow_rad30)
        #
        #
        #
        #
        #
        #
        #
        #
        #
        print("Jet ONLY (never DISK+CORONA)" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        print("pick out *at* r\sim 4M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=rhor
        spreadr=0.1*pickr
        rin=max(pickr-spreadr,1.01*Rin)
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_jet_phipow_radhor={'which': diskcondition}
        minbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=rhor
        rhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor,**keywordsrhosq_jet_phipow_radhor)
        rhosrhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_jet_phipow_radhor)
        ugsrhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_jet_phipow_radhor)
        uu0rhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_jet_phipow_radhor)
        vuas3rhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_jet_phipow_radhor)
        bas1rhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_jet_phipow_radhor)
        bas2rhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_jet_phipow_radhor)
        bas3rhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_jet_phipow_radhor)
        bsqrhosq_jet_phipow_radhor[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_jet_phipow_radhor)
        FMrhosq_jet_phipow_radhor[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_jet_phipow_radhor)
        FEMArhosq_jet_phipow_radhor[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_jet_phipow_radhor)
        FEEMrhosq_jet_phipow_radhor[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_jet_phipow_radhor)
        #
        #
        print("pick out *at* r\sim 4M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=4.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_jet_phipow_rad4={'which': diskcondition}
        minbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=4
        rhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor,**keywordsrhosq_jet_phipow_rad4)
        rhosrhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_jet_phipow_rad4)
        ugsrhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_jet_phipow_rad4)
        uu0rhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_jet_phipow_rad4)
        vuas3rhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_jet_phipow_rad4)
        bas1rhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_jet_phipow_rad4)
        bas2rhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_jet_phipow_rad4)
        bas3rhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_jet_phipow_rad4)
        bsqrhosq_jet_phipow_rad4[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_jet_phipow_rad4)
        FMrhosq_jet_phipow_rad4[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_jet_phipow_rad4)
        FEMArhosq_jet_phipow_rad4[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_jet_phipow_rad4)
        FEEMrhosq_jet_phipow_rad4[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_jet_phipow_rad4)
        #
        #
        print("pick out *at* r\sim 8M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=8.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_jet_phipow_rad8={'which': diskcondition}
        minbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=8
        rhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor,**keywordsrhosq_jet_phipow_rad8)
        rhosrhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_jet_phipow_rad8)
        ugsrhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_jet_phipow_rad8)
        uu0rhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_jet_phipow_rad8)
        vuas3rhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_jet_phipow_rad8)
        bas1rhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_jet_phipow_rad8)
        bas2rhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_jet_phipow_rad8)
        bas3rhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_jet_phipow_rad8)
        bsqrhosq_jet_phipow_rad8[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_jet_phipow_rad8)
        FMrhosq_jet_phipow_rad8[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_jet_phipow_rad8)
        FEMArhosq_jet_phipow_rad8[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_jet_phipow_rad8)
        FEEMrhosq_jet_phipow_rad8[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_jet_phipow_rad8)
        #
        print("pick out *at* r\sim 30M" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        denfactor=1.0 + rho*0.0
        pickr=30.0
        spreadr=0.1*pickr
        rin=pickr-spreadr
        rout=pickr+spreadr
        diskcondition=1.0 + rho*0.0 #(np.abs(r-pickr)<spreadr)
        keywordsrhosq_jet_phipow_rad30={'which': diskcondition}
        minbsqorho=condmaxbsqorhorhs[iofr(pickr),0,0] # good for r=30
        rhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor,**keywordsrhosq_jet_phipow_rad30)
        rhosrhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*rho,**keywordsrhosq_jet_phipow_rad30)
        ugsrhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*denfactor*ug,**keywordsrhosq_jet_phipow_rad30)
        uu0rhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu0*denfactor,**keywordsrhosq_jet_phipow_rad30)
        vuas3rhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*myuu3*denfactor,**keywordsrhosq_jet_phipow_rad30)
        bas1rhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu1*denfactor,**keywordsrhosq_jet_phipow_rad30)
        bas2rhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu2*denfactor,**keywordsrhosq_jet_phipow_rad30)
        bas3rhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*mybu3*denfactor,**keywordsrhosq_jet_phipow_rad30)
        bsqrhosq_jet_phipow_rad30[findex]=powervsm(doabs=1,rin=rin,rout=rout,minbsqorho=minbsqorho,qty=gdet*bsq*denfactor,**keywordsrhosq_jet_phipow_rad30)
        FMrhosq_jet_phipow_rad30[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(-rho*uu[1])*denfactor,**keywordsrhosq_jet_phipow_rad30)
        FEMArhosq_jet_phipow_rad30[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudMA[1,0])*denfactor,**keywordsrhosq_jet_phipow_rad30)
        FEEMrhosq_jet_phipow_rad30[findex]=powervsm(doabs=0,rin=rin,rout=rout,maxbsqorho=maxbsqorho,qty=gdet*(TudEM[1,0])*denfactor,**keywordsrhosq_jet_phipow_rad30)
        #
        #
        #
        #
        #
        #
        #
        diskcondition=condmaxbsqorho
        keywords2hor={'hoverr': 2.0*hoverr3d, 'thetamid': thetamid3d, 'which': diskcondition}
        #
        print("Flux" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        # radial absolute flux as function of radius
        fstot[findex]=horfluxcalc(minbsqorho=0)
        # ingoing flow's absolute magnetic flux (so use same bsq/rho and inflow condition)
        fscondition=condmaxbsqorho
        fsin[findex]=horfluxcalc(minbsqorho=0,inflowonly=1,whichcondition=fscondition)
        #
        # horizon radial cumulative flux as function of theta (not function of radius!)
        #fhortot[findex]=horfluxcalc(ivalue=ihor,takeabs=0,takecumsum=1)
        # equatorial vertical cumulative flux as function of radius
        feqtot[findex]=eqfluxcalc(jvalue=ny/2,takeabs=0,takecumsum=1,minbsqorho=0)
        #
        fsmaxtot[findex]=horfluxcalc(minbsqorho=0,takeextreme=1,takecumsum=1,takeabs=0)
        #
        # upper-hemisphere radial flux to be added or compared to equatorial vertical flux
        fsuphalf[findex]=horfluxcalc(minbsqorho=0,takeabs=0,uphalf=1)
        #
        #
        fs2hor[findex]==intangle(np.abs(gdetB[1]),**keywords2hor)
        fsj5[findex]=horfluxcalc(ivalue=ihor,minbsqorho=5)
        fsj10[findex]=horfluxcalc(ivalue=ihor,minbsqorho=10)
        fsj20[findex]=horfluxcalc(ivalue=ihor,minbsqorho=20)
        fsj30[findex]=horfluxcalc(ivalue=ihor,minbsqorho=30)
        fsj40[findex]=horfluxcalc(ivalue=ihor,minbsqorho=40)
        #
        print("Mdot" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        avoidfloorcondition=condmaxbsqorho
        keywordsavoidfloor={'which': avoidfloorcondition}
        #
        enth=1+ug*gam/rho
        mdtot[findex]=mdotcalc(which=avoidfloorcondition)
        mdtotbound[findex]=mdotcalc(which=avoidfloorcondition*(-enth*ud[0]<=1))
        md2h[findex]=mdotcalc(**keywords2h)
        md4h[findex]=mdotcalc(**keywords4h)
        md2hor[findex]=mdotcalc(**keywords2hor)
        md5[findex]=intangle(-gdet*rho*uu[1],minbsqorho=5)
        md10[findex]=intangle(-gdet*rho*uu[1],minbsqorho=10)
        md20[findex]=intangle(-gdet*rho*uu[1],minbsqorho=20)
        # md30 really is Mdot for floor
        md30[findex]=intangle(-gdet*rho*uu[1],which=(avoidfloorcondition==0))
        # use 10 for jet and wind since at larger radii jet has lower bsqorho
        # don't include maxbeta=3 since outflows from disk can have larger beta
        windmaxbeta=1E30
        mdwind[findex]=intangle(gdet*rho*uu[1],mumax=1,maxbeta=windmaxbeta,which=condmaxbsqorho)
        mwindmaxbeta=2
        mdmwind[findex]=intangle(gdet*rho*uu[1],mumax=1,maxbeta=mwindmaxbeta,which=condmaxbsqorho)
        #
        mdjet[findex]=intangle(gdet*rho*uu[1],mumin=1,which=condmaxbsqorho)
        #
        md40[findex]=intangle(-gdet*rho*uu[1],minbsqorho=40)
        mdrhosq[findex]=scaletofullwedge(((-gdet*rho**2*rho*uu[1]*diskcondition).sum(1)/maxrhosq2d).sum(1)*_dx2*_dx3)
        #mdrhosq[findex]=(-gdet*rho**2*rho*uu[1]).sum(1).sum(1)/(-gdet*rho**2).sum(1).sum(1)*(-gdet).sum(1).sum(1)*_dx2*_dx3
        #
        # use same below maxbsqorho condition for fsin for proper division comparison
        mdin[findex]=intangle(-gdet*rho*uu[1],inflowonly=1,which=condmaxbsqorho)
        #
        print("Edot" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        edtot[findex]=intangle(-gdet*Tud[1][0])
        ed2h[findex]=intangle(-gdet*Tud[1][0],hoverr=2*horval)
        ed4h[findex]=intangle(-gdet*Tud[1][0],hoverr=4*horval)
        ed2hor[findex]=intangle(-gdet*Tud[1][0],hoverr=2*hoverr3d,thetamid=thetamid3d)
        edrhosq[findex]=scaletofullwedge(((-gdet*rho**2*Tud[1][0]).sum(1)/maxrhosq2d).sum(1)*_dx2*_dx3)
        #
        #
        edem[findex]=intangle(-gdet*TudEM[1][0])
        edma[findex]=intangle(-gdet*TudMA[1][0])
        edm[findex]=intangle(gdet*rho*uu[1])
        #
        edma30[findex]=intangle(-gdet*TudMA[1][0],which=(condmaxbsqorho==0))
        edm30[findex]=intangle(gdet*rho*uu[1],which=(condmaxbsqorho==0))
        #
        edtotbound[findex]=intangle(-gdet*Tud[1][0],which=(-enth*ud[0]<=1))
        edmabound[findex]=intangle(-gdet*TudMA[1][0],which=(-enth*ud[0]<=1))
        #
        print("Pjet" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        pjem5[findex]=jetpowcalc(0,minbsqorho=5)
        pjma5[findex]=jetpowcalc(1,minbsqorho=5)
        #
        #
        # use md10-like restriction since in jet or wind at large radii bsq/rho doesn't reach ~30 but floors still fed in mass
        # OLD style floor calculation kept, but not using _flr stuff anymore
        jetwind_minbsqorho=10.0
        #
        print("north hemisphere" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        pjem_n_mu1[findex]=jetpowcalc(0,mumin=1,donorthsouth=1)
        pjem_n_mumax1[findex]=jetpowcalc(0,mumax=1,maxbeta=windmaxbeta,donorthsouth=1)
        pjem_n_mumax1m[findex]=jetpowcalc(0,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1)
        #
        pjrm_n_mu1[findex]=jetpowcalc(3,mumin=1,donorthsouth=1,conditional=condmaxbsqorho)
        pjrm_n_mumax1[findex]=jetpowcalc(3,mumax=1,maxbeta=windmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        pjrm_n_mumax1m[findex]=jetpowcalc(3,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        #
        pjrm_n_mu1_flr[findex]=jetpowcalc(3,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        pjrm_n_mumax1_flr[findex]=jetpowcalc(3,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        pjrm_n_mumax1m_flr[findex]=jetpowcalc(3,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        #
        pjma_n_mu1[findex]=jetpowcalc(1,mumin=1,donorthsouth=1,conditional=condmaxbsqorho)
        pjma_n_mumax1[findex]=jetpowcalc(1,mumax=1,maxbeta=windmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        pjma_n_mumax1m[findex]=jetpowcalc(1,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        #
        pjma_n_mu1_flr[findex]=jetpowcalc(1,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        pjma_n_mumax1_flr[findex]=jetpowcalc(1,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        pjma_n_mumax1m_flr[findex]=jetpowcalc(1,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        #
        phiabsj_n_mu1[findex]=jetpowcalc(4,mumin=1,donorthsouth=1)
        phiabsj_n_mumax1[findex]=jetpowcalc(4,mumax=1,maxbeta=windmaxbeta,donorthsouth=1)
        phiabsj_n_mumax1m[findex]=jetpowcalc(4,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1)
        #
        print("south hemisphere" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        pjem_s_mu1[findex]=jetpowcalc(0,mumin=1,donorthsouth=-1)
        pjem_s_mumax1[findex]=jetpowcalc(0,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1)
        pjem_s_mumax1m[findex]=jetpowcalc(0,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1)
        #
        pjrm_s_mu1[findex]=jetpowcalc(3,mumin=1,donorthsouth=-1,conditional=condmaxbsqorho)
        pjrm_s_mumax1[findex]=jetpowcalc(3,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        pjrm_s_mumax1m[findex]=jetpowcalc(3,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        #
        pjrm_s_mu1_flr[findex]=jetpowcalc(3,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        pjrm_s_mumax1_flr[findex]=jetpowcalc(3,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        pjrm_s_mumax1m_flr[findex]=jetpowcalc(3,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        #
        pjma_s_mu1[findex]=jetpowcalc(1,mumin=1,donorthsouth=-1,conditional=condmaxbsqorho)
        pjma_s_mumax1[findex]=jetpowcalc(1,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        pjma_s_mumax1m[findex]=jetpowcalc(1,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        #
        pjma_s_mu1_flr[findex]=jetpowcalc(1,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        pjma_s_mumax1_flr[findex]=jetpowcalc(1,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        pjma_s_mumax1m_flr[findex]=jetpowcalc(1,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        #
        phiabsj_s_mu1[findex]=jetpowcalc(4,mumin=1,donorthsouth=-1)
        phiabsj_s_mumax1[findex]=jetpowcalc(4,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1)
        phiabsj_s_mumax1m[findex]=jetpowcalc(4,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1)
        #
        #
        #
        print("Ldot" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        ldtot[findex]=intangle(gdet*Tud[1][3]/dxdxp[3,3])
        ldem[findex]=intangle(gdet*TudEM[1][3]/dxdxp[3,3])
        ldma[findex]=intangle(gdet*TudMA[1][3]/dxdxp[3,3])
        ldm[findex]=intangle(0.0*gdet*rho*uu[3]*dxdxp[3,3])
        #
        ldma30[findex]=intangle(gdet*TudMA[1][3]/dxdxp[3,3],which=(condmaxbsqorho==0))
        ldm30[findex]=intangle(0.0*gdet*rho*uu[3]*dxdxp[3,3],which=(condmaxbsqorho==0))
        #
        print("north hemisphere" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        ljem_n_mu1[findex]=jetpowcalc(10,mumin=1,donorthsouth=1)
        ljem_n_mumax1[findex]=jetpowcalc(10,mumax=1,maxbeta=windmaxbeta,donorthsouth=1)
        ljem_n_mumax1m[findex]=jetpowcalc(10,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1)
        #
        ljrm_n_mu1[findex]=jetpowcalc(13,mumin=1,donorthsouth=1,conditional=condmaxbsqorho)
        ljrm_n_mumax1[findex]=jetpowcalc(13,mumax=1,maxbeta=windmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        ljrm_n_mumax1m[findex]=jetpowcalc(13,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        #
        ljrm_n_mu1_flr[findex]=jetpowcalc(13,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        ljrm_n_mumax1_flr[findex]=jetpowcalc(13,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        ljrm_n_mumax1m_flr[findex]=jetpowcalc(13,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        #
        ljma_n_mu1[findex]=jetpowcalc(11,mumin=1,donorthsouth=1,conditional=condmaxbsqorho)
        ljma_n_mumax1[findex]=jetpowcalc(11,mumax=1,maxbeta=windmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        ljma_n_mumax1m[findex]=jetpowcalc(11,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=1,conditional=condmaxbsqorho)
        #
        ljma_n_mu1_flr[findex]=jetpowcalc(11,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        ljma_n_mumax1_flr[findex]=jetpowcalc(11,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        ljma_n_mumax1m_flr[findex]=jetpowcalc(11,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=1)
        #
        print("south hemisphere" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        ljem_s_mu1[findex]=jetpowcalc(10,mumin=1,donorthsouth=-1)
        ljem_s_mumax1[findex]=jetpowcalc(10,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1)
        ljem_s_mumax1m[findex]=jetpowcalc(10,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1)
        #
        ljrm_s_mu1[findex]=jetpowcalc(13,mumin=1,donorthsouth=-1,conditional=condmaxbsqorho)
        ljrm_s_mumax1[findex]=jetpowcalc(13,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        ljrm_s_mumax1m[findex]=jetpowcalc(13,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        #
        ljrm_s_mu1_flr[findex]=jetpowcalc(13,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        ljrm_s_mumax1_flr[findex]=jetpowcalc(13,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        ljrm_s_mumax1m_flr[findex]=jetpowcalc(13,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        #
        ljma_s_mu1[findex]=jetpowcalc(11,mumin=1,donorthsouth=-1,conditional=condmaxbsqorho)
        ljma_s_mumax1[findex]=jetpowcalc(11,mumax=1,maxbeta=windmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        ljma_s_mumax1m[findex]=jetpowcalc(11,mumax=1,maxbeta=mwindmaxbeta,donorthsouth=-1,conditional=condmaxbsqorho)
        #
        ljma_s_mu1_flr[findex]=jetpowcalc(11,mumin=1,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        ljma_s_mumax1_flr[findex]=jetpowcalc(11,mumax=1,maxbeta=windmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        ljma_s_mumax1m_flr[findex]=jetpowcalc(11,mumax=1,maxbeta=mwindmaxbeta,minbsqorho=jetwind_minbsqorho,donorthsouth=-1)
        #
        #
        if dobob==1:
            #
            print("Bob's 1D quantities" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
            #
            dVF=_dx1*_dx2*_dx3
            dVA=_dx2*_dx3
            Dt=1
            TT=0
            RR=1
            TH=2
            PH=3
            qtymem[i+0,findex]=intangle(Dt*dVF*gdet*rho,**keywords2hor)
            qtymem[i+1,findex]=intangle(Dt*dVF*gdet*rho*rho,**keywords2hor)
            qtymem[i+2,findex]=intangle(Dt*dVF*gdet*rho*ug,**keywords2hor)
            qtymem[i+3,findex]=intangle(Dt*dVF*gdet*rho*bsq,**keywords2hor)
        
            qtymem[i+4,findex]=intangle(Dt*dVF*gdet*rho*uu[1],**keywords2hor) #pr[2]
            qtymem[i+5,findex]=intangle(Dt*dVF*gdet*rho*uu[2],**keywords2hor) #pr[3]
            qtymem[i+6,findex]=intangle(Dt*dVF*gdet*rho*uu[3],**keywords2hor) #pr[4]
        
            qtymem[i+7,findex]=intangle(Dt*dVF*gdet*rho*B[1],**keywords2hor) #pr[5]
            qtymem[i+8,findex]=intangle(Dt*dVF*gdet*rho*B[2],**keywords2hor) #pr[6]
            qtymem[i+9,findex]=intangle(Dt*dVF*gdet*rho*B[3],**keywords2hor) #pr[7]
        
            #rho * u * u
        
            qtymem[i+10,findex]=intangle(Dt*dVA*gdet*rho*(ud[TT])*(ud[TT]),**keywords2hor)
            qtymem[i+11,findex]=intangle(Dt*dVA*gdet*rho*(ud[TT])*(ud[RR]),**keywords2hor)
            qtymem[i+12,findex]=intangle(Dt*dVA*gdet*rho*(ud[TT])*(ud[TH]),**keywords2hor)
            qtymem[i+13,findex]=intangle(Dt*dVA*gdet*rho*(ud[TT])*(ud[PH]),**keywords2hor)
            qtymem[i+14,findex]=intangle(Dt*dVA*gdet*rho*(ud[RR])*(ud[RR]),**keywords2hor)
            qtymem[i+15,findex]=intangle(Dt*dVA*gdet*rho*(ud[RR])*(ud[TH]),**keywords2hor)
            qtymem[i+16,findex]=intangle(Dt*dVA*gdet*rho*(ud[RR])*(ud[PH]),**keywords2hor)
            qtymem[i+17,findex]=intangle(Dt*dVA*gdet*rho*(ud[TH])*(ud[TH]),**keywords2hor)
            qtymem[i+18,findex]=intangle(Dt*dVA*gdet*rho*(ud[TH])*(ud[PH]),**keywords2hor)
            qtymem[i+19,findex]=intangle(Dt*dVA*gdet*rho*(ud[PH])*(ud[PH]),**keywords2hor)
        
            qtymem[i+20,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(ud[TT]),**keywords2hor)
            qtymem[i+21,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(ud[RR]),**keywords2hor)
            qtymem[i+22,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(ud[TH]),**keywords2hor)
            qtymem[i+23,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(ud[PH]),**keywords2hor)
            qtymem[i+24,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR])*(ud[RR]),**keywords2hor)
            qtymem[i+25,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR])*(ud[TH]),**keywords2hor)
            qtymem[i+26,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR])*(ud[PH]),**keywords2hor)
            qtymem[i+27,findex]=intangle(Dt*dVA*gdet*rho*(uu[TH])*(ud[TH]),**keywords2hor)
            qtymem[i+28,findex]=intangle(Dt*dVA*gdet*rho*(uu[TH])*(ud[PH]),**keywords2hor)
            qtymem[i+29,findex]=intangle(Dt*dVA*gdet*rho*(uu[PH])*(ud[PH]),**keywords2hor)
        
            qtymem[i+30,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(uu[TT]),**keywords2hor)
            qtymem[i+31,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(uu[RR]),**keywords2hor)
            qtymem[i+32,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(uu[TH]),**keywords2hor)
            qtymem[i+33,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT])*(uu[PH]),**keywords2hor)
            qtymem[i+34,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR])*(uu[RR]),**keywords2hor)
            qtymem[i+35,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR])*(uu[TH]),**keywords2hor)
            qtymem[i+36,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR])*(uu[PH]),**keywords2hor)
            qtymem[i+37,findex]=intangle(Dt*dVA*gdet*rho*(uu[TH])*(uu[TH]),**keywords2hor)
            qtymem[i+38,findex]=intangle(Dt*dVA*gdet*rho*(uu[TH])*(uu[PH]),**keywords2hor)
            qtymem[i+39,findex]=intangle(Dt*dVA*gdet*rho*(uu[PH])*(uu[PH]),**keywords2hor)
        
        
            #UU * u * u
        
            qtymem[i+40,findex]=intangle(Dt*dVA*gdet*ug*(ud[TT])*(ud[TT]),**keywords2hor)
            qtymem[i+41,findex]=intangle(Dt*dVA*gdet*ug*(ud[TT])*(ud[RR]),**keywords2hor)
            qtymem[i+42,findex]=intangle(Dt*dVA*gdet*ug*(ud[TT])*(ud[TH]),**keywords2hor)
            qtymem[i+43,findex]=intangle(Dt*dVA*gdet*ug*(ud[TT])*(ud[PH]),**keywords2hor)
            qtymem[i+44,findex]=intangle(Dt*dVA*gdet*ug*(ud[RR])*(ud[RR]),**keywords2hor)
            qtymem[i+45,findex]=intangle(Dt*dVA*gdet*ug*(ud[RR])*(ud[TH]),**keywords2hor)
            qtymem[i+46,findex]=intangle(Dt*dVA*gdet*ug*(ud[RR])*(ud[PH]),**keywords2hor)
            qtymem[i+47,findex]=intangle(Dt*dVA*gdet*ug*(ud[TH])*(ud[TH]),**keywords2hor)
            qtymem[i+48,findex]=intangle(Dt*dVA*gdet*ug*(ud[TH])*(ud[PH]),**keywords2hor)
            qtymem[i+49,findex]=intangle(Dt*dVA*gdet*ug*(ud[PH])*(ud[PH]),**keywords2hor)
        
            qtymem[i+50,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(ud[TT]),**keywords2hor)
            qtymem[i+51,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(ud[RR]),**keywords2hor)
            qtymem[i+52,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(ud[TH]),**keywords2hor)
            qtymem[i+53,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(ud[PH]),**keywords2hor)
            qtymem[i+54,findex]=intangle(Dt*dVA*gdet*ug*(uu[RR])*(ud[RR]),**keywords2hor)
            qtymem[i+55,findex]=intangle(Dt*dVA*gdet*ug*(uu[RR])*(ud[TH]),**keywords2hor)
            qtymem[i+56,findex]=intangle(Dt*dVA*gdet*ug*(uu[RR])*(ud[PH]),**keywords2hor)
            qtymem[i+57,findex]=intangle(Dt*dVA*gdet*ug*(uu[TH])*(ud[TH]),**keywords2hor)
            qtymem[i+58,findex]=intangle(Dt*dVA*gdet*ug*(uu[TH])*(ud[PH]),**keywords2hor)
            qtymem[i+59,findex]=intangle(Dt*dVA*gdet*ug*(uu[PH])*(ud[PH]),**keywords2hor)
        
            qtymem[i+60,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(uu[TT]),**keywords2hor)
            qtymem[i+61,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(uu[RR]),**keywords2hor)
            qtymem[i+62,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(uu[TH]),**keywords2hor)
            qtymem[i+63,findex]=intangle(Dt*dVA*gdet*ug*(uu[TT])*(uu[PH]),**keywords2hor)
            qtymem[i+64,findex]=intangle(Dt*dVA*gdet*ug*(uu[RR])*(uu[RR]),**keywords2hor)
            qtymem[i+65,findex]=intangle(Dt*dVA*gdet*ug*(uu[RR])*(uu[TH]),**keywords2hor)
            qtymem[i+66,findex]=intangle(Dt*dVA*gdet*ug*(uu[RR])*(uu[PH]),**keywords2hor)
            qtymem[i+67,findex]=intangle(Dt*dVA*gdet*ug*(uu[TH])*(uu[TH]),**keywords2hor)
            qtymem[i+68,findex]=intangle(Dt*dVA*gdet*ug*(uu[TH])*(uu[PH]),**keywords2hor)
            qtymem[i+69,findex]=intangle(Dt*dVA*gdet*ug*(uu[PH])*(uu[PH]),**keywords2hor)
        
            #bsq * u * u
        
            qtymem[i+70,findex]=intangle(Dt*dVA*gdet*bsq*(ud[TT])*(ud[TT]),**keywords2hor)
            qtymem[i+71,findex]=intangle(Dt*dVA*gdet*bsq*(ud[TT])*(ud[RR]),**keywords2hor)
            qtymem[i+72,findex]=intangle(Dt*dVA*gdet*bsq*(ud[TT])*(ud[TH]),**keywords2hor)
            qtymem[i+73,findex]=intangle(Dt*dVA*gdet*bsq*(ud[TT])*(ud[PH]),**keywords2hor)
            qtymem[i+74,findex]=intangle(Dt*dVA*gdet*bsq*(ud[RR])*(ud[RR]),**keywords2hor)
            qtymem[i+75,findex]=intangle(Dt*dVA*gdet*bsq*(ud[RR])*(ud[TH]),**keywords2hor)
            qtymem[i+76,findex]=intangle(Dt*dVA*gdet*bsq*(ud[RR])*(ud[PH]),**keywords2hor)
            qtymem[i+77,findex]=intangle(Dt*dVA*gdet*bsq*(ud[TH])*(ud[TH]),**keywords2hor)
            qtymem[i+78,findex]=intangle(Dt*dVA*gdet*bsq*(ud[TH])*(ud[PH]),**keywords2hor)
            qtymem[i+79,findex]=intangle(Dt*dVA*gdet*bsq*(ud[PH])*(ud[PH]),**keywords2hor)
        
            qtymem[i+80,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(ud[TT]),**keywords2hor)
            qtymem[i+81,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(ud[RR]),**keywords2hor)
            qtymem[i+82,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(ud[TH]),**keywords2hor)
            qtymem[i+83,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(ud[PH]),**keywords2hor)
            qtymem[i+84,findex]=intangle(Dt*dVA*gdet*bsq*(uu[RR])*(ud[RR]),**keywords2hor)
            qtymem[i+85,findex]=intangle(Dt*dVA*gdet*bsq*(uu[RR])*(ud[TH]),**keywords2hor)
            qtymem[i+86,findex]=intangle(Dt*dVA*gdet*bsq*(uu[RR])*(ud[PH]),**keywords2hor)
            qtymem[i+87,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TH])*(ud[TH]),**keywords2hor)
            qtymem[i+88,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TH])*(ud[PH]),**keywords2hor)
            qtymem[i+89,findex]=intangle(Dt*dVA*gdet*bsq*(uu[PH])*(ud[PH]),**keywords2hor)
        
            qtymem[i+90,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(uu[TT]),**keywords2hor)
            qtymem[i+91,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(uu[RR]),**keywords2hor)
            qtymem[i+92,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(uu[TH]),**keywords2hor)
            qtymem[i+93,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TT])*(uu[PH]),**keywords2hor)
            qtymem[i+94,findex]=intangle(Dt*dVA*gdet*bsq*(uu[RR])*(uu[RR]),**keywords2hor)
            qtymem[i+95,findex]=intangle(Dt*dVA*gdet*bsq*(uu[RR])*(uu[TH]),**keywords2hor)
            qtymem[i+96,findex]=intangle(Dt*dVA*gdet*bsq*(uu[RR])*(uu[PH]),**keywords2hor)
            qtymem[i+97,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TH])*(uu[TH]),**keywords2hor)
            qtymem[i+98,findex]=intangle(Dt*dVA*gdet*bsq*(uu[TH])*(uu[PH]),**keywords2hor)
            qtymem[i+99,findex]=intangle(Dt*dVA*gdet*bsq*(uu[PH])*(uu[PH]),**keywords2hor)
        
            # b * b
        
            qtymem[i+100,findex]=intangle(Dt*dVA*gdet*(bd[TT])*(bd[TT]),**keywords2hor)
            qtymem[i+101,findex]=intangle(Dt*dVA*gdet*(bd[TT])*(bd[RR]),**keywords2hor)
            qtymem[i+102,findex]=intangle(Dt*dVA*gdet*(bd[TT])*(bd[TH]),**keywords2hor)
            qtymem[i+103,findex]=intangle(Dt*dVA*gdet*(bd[TT])*(bd[PH]),**keywords2hor)
            qtymem[i+104,findex]=intangle(Dt*dVA*gdet*(bd[RR])*(bd[RR]),**keywords2hor)
            qtymem[i+105,findex]=intangle(Dt*dVA*gdet*(bd[RR])*(bd[TH]),**keywords2hor)
            qtymem[i+106,findex]=intangle(Dt*dVA*gdet*(bd[RR])*(bd[PH]),**keywords2hor)
            qtymem[i+107,findex]=intangle(Dt*dVA*gdet*(bd[TH])*(bd[TH]),**keywords2hor)
            qtymem[i+108,findex]=intangle(Dt*dVA*gdet*(bd[TH])*(bd[PH]),**keywords2hor)
            qtymem[i+109,findex]=intangle(Dt*dVA*gdet*(bd[PH])*(bd[PH]),**keywords2hor)
        
            qtymem[i+110,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bd[TT]),**keywords2hor)
            qtymem[i+111,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bd[RR]),**keywords2hor)
            qtymem[i+112,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bd[TH]),**keywords2hor)
            qtymem[i+113,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bd[PH]),**keywords2hor)
            qtymem[i+114,findex]=intangle(Dt*dVA*gdet*(bu[RR])*(bd[RR]),**keywords2hor)
            qtymem[i+115,findex]=intangle(Dt*dVA*gdet*(bu[RR])*(bd[TH]),**keywords2hor)
            qtymem[i+116,findex]=intangle(Dt*dVA*gdet*(bu[RR])*(bd[PH]),**keywords2hor)
            qtymem[i+117,findex]=intangle(Dt*dVA*gdet*(bu[TH])*(bd[TH]),**keywords2hor)
            qtymem[i+118,findex]=intangle(Dt*dVA*gdet*(bu[TH])*(bd[PH]),**keywords2hor)
            qtymem[i+119,findex]=intangle(Dt*dVA*gdet*(bu[PH])*(bd[PH]),**keywords2hor)
        
            qtymem[i+120,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bu[TT]),**keywords2hor)
            qtymem[i+121,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bu[RR]),**keywords2hor)
            qtymem[i+122,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bu[TH]),**keywords2hor)
            qtymem[i+123,findex]=intangle(Dt*dVA*gdet*(bu[TT])*(bu[PH]),**keywords2hor)
            qtymem[i+124,findex]=intangle(Dt*dVA*gdet*(bu[RR])*(bu[RR]),**keywords2hor)
            qtymem[i+125,findex]=intangle(Dt*dVA*gdet*(bu[RR])*(bu[TH]),**keywords2hor)
            qtymem[i+126,findex]=intangle(Dt*dVA*gdet*(bu[RR])*(bu[PH]),**keywords2hor)
            qtymem[i+127,findex]=intangle(Dt*dVA*gdet*(bu[TH])*(bu[TH]),**keywords2hor)
            qtymem[i+128,findex]=intangle(Dt*dVA*gdet*(bu[TH])*(bu[PH]),**keywords2hor)
            qtymem[i+129,findex]=intangle(Dt*dVA*gdet*(bu[PH])*(bu[PH]),**keywords2hor)
        
        
            #mass flux
            qtymem[i+130,findex]=intangle(Dt*dVA*gdet*rho*(uu[TT]),**keywords2hor)
            qtymem[i+131,findex]=intangle(Dt*dVA*gdet*rho*(uu[RR]),**keywords2hor)
            qtymem[i+132,findex]=intangle(Dt*dVA*gdet*rho*(uu[TH]),**keywords2hor)
            qtymem[i+133,findex]=intangle(Dt*dVA*gdet*rho*(uu[PH]),**keywords2hor)
        #END BOB's QUANTITIES
    #
    #if os.path.isfile("lrho%04d.png" % findex):
    #    print( "Skipping " + fname + " as lrho%04d.png exists" % findex );
    #else:
    #    print( "Reinterpolating " + fname + " ..." )
    #    plt.figure(0)
    #    plt.clf()
    #    mkframe("lrho%04d" % findex, vmin=-8,vmax=0.2)
    print("Saving to file..."  + " time elapsed: %d" % (datetime.now()-start_time).seconds  ) ; sys.stdout.flush()
    if( whichi >=0 and whichn > 0 ):
        np.save( "qty2_%d_%d.npy" % (whichi, whichn), qtymem )
    else:
        np.save( "qty2.npy", qtymem )
    print( "Done getqtyvstime!" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    return(qtymem)



def fhorvstime(ihor):
    """
    Returns a tuple (ts,fs,mdot): lists of times, horizon fluxes, and Mdot
    """
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    sort_nicely(flist)
    #
    ts=np.empty(len(flist),dtype=np.float32)
    fs=np.empty(len(flist),dtype=np.float32)
    md=np.empty(len(flist),dtype=np.float32)
    for findex, fname in enumerate(flist):
        print( "Reading " + fname + " ..." )
        rfd("../"+fname)
        fs[findex]=horfluxcalc(ivalue=ihor)
        md[findex]=mdotcalc(ihor)
        ts[findex]=t
    print( "Done fhorvstime!" )
    return((ts,fs,md))

def amax(arg1,arg2):
    arr1 = np.array(arg1)
    arr2 = np.array(arg2)
    ret=np.zeros_like(arr1)
    ret[arr1>=arr2]=arr1[arr1>=arr2]
    ret[arr2>arr1]=arr2[arr2>arr1]
    return(ret)
def amin(arg1,arg2):
    arr1 = np.array(arg1)
    arr2 = np.array(arg2)
    ret=np.zeros_like(arr1)
    ret[arr1<=arr2]=arr1[arr1<=arr2]
    ret[arr2<arr1]=arr2[arr2<arr1]
    return(ret)

# allow to remove rho and ug component to remove floor effects
def Tcalcud(maxbsqorho=None, which=None):
    global Tud, TudEM, TudMA, TudPA, TudIE
    global mu, sigma
    global enth
    global unb, isunbound
    #
    bsqo2rho = bsq/(2.0*rho) # uses original rho, which is as desired
    bsqorho = bsq/(rho) # uses original rho, which is as desired
    #
    # below needed in case operating on averages rather than from rfd()
    #(rhoclean,ugclean,uu,maxbsqorhonear,maxbsqorhofar,condmaxbsqorho)=getrhouclean(rho,ug,uu)
    #ud = mdot(gv3,uu)                  #g_mn u^n
    # no, assume averages formed out of rfd reads that already include whatever cleaning wanted
    #
    #
    pg = (gam-1)*ugclean
    w=rhoclean+ugclean+pg
    wnorhoclean=ugclean+pg
    eta=w+bsq
    Tud = np.zeros((4,4,nx,ny,nz),dtype=np.float32,order='F')
    TudMA = np.zeros((4,4,nx,ny,nz),dtype=np.float32,order='F')
    TudEM = np.zeros((4,4,nx,ny,nz),dtype=np.float32,order='F')
    TudPA = np.zeros((4,4,nx,ny,nz),dtype=np.float32,order='F')
    TudIE = np.zeros((4,4,nx,ny,nz),dtype=np.float32,order='F')
    for kapa in np.arange(4):
        for nu in np.arange(4):
            if(kapa==nu): delta = 1
            else: delta = 0
            TudEM[kapa,nu] = bsq*uu[kapa]*ud[nu] + 0.5*bsq*delta - bu[kapa]*bd[nu]
            TudMA[kapa,nu] = w*uu[kapa]*ud[nu]+pg*delta
            TudPA[kapa,nu] = rhoclean*uu[kapa]*ud[nu]
            TudIE[kapa,nu] = wnorhoclean*uu[kapa]*ud[nu]+pg*delta
            #Tud[kapa,nu] = eta*uu[kapa]*ud[nu]+(pg+0.5*bsq)*delta-bu[kapa]*bd[nu]
            Tud[kapa,nu] = TudEM[kapa,nu] + TudMA[kapa,nu]
    #mu = -Tud[1,0]/(rhoclean*uu[1])
    mu = -Tud[1,0]*divideavoidinf(rhoclean*uu[1])
    sigma = TudEM[1,0]*divideavoidinf(TudMA[1,0])
    enth=1+ugclean*gam/rhoclean
    unb=enth*ud[0]
    # unbound here means *thermally* rather than kinetically (-u_t>1) or fully thermo-magnetically (\mu>1) unbound.
    isunbound=(-unb>1.0)

def faraday():
    global fdd, fuu, omegaf1, omegaf1b, omegaf2, omegaf2b
    # these are native values according to HARM
    fdd = np.zeros((4,4,nx,ny,nz),dtype=rho.dtype)
    #fdd[0,0]=0*gdet
    #fdd[1,1]=0*gdet
    #fdd[2,2]=0*gdet
    #fdd[3,3]=0*gdet
    fdd[0,1]=gdet*(uu[2]*bu[3]-uu[3]*bu[2]) # f_tr
    fdd[1,0]=-fdd[0,1]
    fdd[0,2]=gdet*(uu[3]*bu[1]-uu[1]*bu[3]) # f_th
    fdd[2,0]=-fdd[0,2]
    fdd[0,3]=gdet*(uu[1]*bu[2]-uu[2]*bu[1]) # f_tp
    fdd[3,0]=-fdd[0,3]
    fdd[1,3]=gdet*(uu[2]*bu[0]-uu[0]*bu[2]) # f_rp = gdet*B2
    fdd[3,1]=-fdd[1,3]
    fdd[2,3]=gdet*(uu[0]*bu[1]-uu[1]*bu[0]) # f_hp = gdet*B1
    fdd[3,2]=-fdd[2,3]
    fdd[1,2]=gdet*(uu[0]*bu[3]-uu[3]*bu[0]) # f_rh = gdet*B3
    fdd[2,1]=-fdd[1,2]
    #
    fuu = np.zeros((4,4,nx,ny,nz),dtype=rho.dtype)
    #fuu[0,0]=0*gdet
    #fuu[1,1]=0*gdet
    #fuu[2,2]=0*gdet
    #fuu[3,3]=0*gdet
    fuu[0,1]=-1/gdet*(ud[2]*bd[3]-ud[3]*bd[2]) # f^tr
    fuu[1,0]=-fuu[0,1]
    fuu[0,2]=-1/gdet*(ud[3]*bd[1]-ud[1]*bd[3]) # f^th
    fuu[2,0]=-fuu[0,2]
    fuu[0,3]=-1/gdet*(ud[1]*bd[2]-ud[2]*bd[1]) # f^tp
    fuu[3,0]=-fuu[0,3]
    fuu[1,3]=-1/gdet*(ud[2]*bd[0]-ud[0]*bd[2]) # f^rp
    fuu[3,1]=-fuu[1,3]
    fuu[2,3]=-1/gdet*(ud[0]*bd[1]-ud[1]*bd[0]) # f^hp
    fuu[3,2]=-fuu[2,3]
    fuu[1,2]=-1/gdet*(ud[0]*bd[3]-ud[3]*bd[0]) # f^rh
    fuu[2,1]=-fuu[1,2]
    #
    # these 2 are equal in degen electrodynamics when d/dt=d/dphi->0
    omegaf1=fdd[0,1]/fdd[1,3] # = ftr/frp
    omegaf2=fdd[0,2]/fdd[2,3] # = fth/fhp
    #
    B1hat=B[1]*np.sqrt(gv3[1,1])
    B2hat=B[2]*np.sqrt(gv3[2,2])
    B3nonhat=B[3]
    v1hat=uu[1]*np.sqrt(gv3[1,1])/uu[0]
    v2hat=uu[2]*np.sqrt(gv3[2,2])/uu[0]
    v3nonhat=uu[3]/uu[0]
    #
    aB1hat=np.fabs(B1hat)
    aB2hat=np.fabs(B2hat)
    av1hat=np.fabs(v1hat)
    av2hat=np.fabs(v2hat)
    #
    vpol=np.sqrt(av1hat**2 + av2hat**2)
    Bpol=np.sqrt(aB1hat**2 + aB2hat**2)
    #
    #omegaf1b=(omegaf1*aB1hat+omegaf2*aB2hat)/(aB1hat+aB2hat)
    #E1hat=fdd[0,1]*np.sqrt(gn3[1,1])
    #E2hat=fdd[0,2]*np.sqrt(gn3[2,2])
    #Epabs=np.sqrt(E1hat**2+E2hat**2)
    #Bpabs=np.sqrt(aB1hat**2+aB2hat**2)+1E-15
    #omegaf2b=Epabs/Bpabs
    #
    # assume field swept back so omegaf is always larger than vphi (only true for outflow, so put in sign switch for inflow as relevant for disk near BH or even jet near BH)
    omegaf2b=np.fabs(v3nonhat) + np.sign(uu[1])*(vpol/Bpol)*np.fabs(B3nonhat)
    #
    omegaf1b=v3nonhat - B3nonhat*(v1hat*B1hat+v2hat*B2hat)/(B1hat**2+B2hat**2)
    #

def jetpowcalc(which=2,minbsqorho=None,mumin=None,mumax=None,maxbeta=None,maxbsqorho=None,donorthsouth=0,conditional=1):
    if which==3:
        #rest-mass flux
        jetpowden = gdet*rho*uu[1]
    if which==0:
        jetpowden = -gdet*TudEM[1,0]
    if which==1:
        jetpowden = -gdet*TudMA[1,0]
    if which==2:
        jetpowden = -gdet*Tud[1,0]
    if which==10:
        jetpowden = gdet*TudEM[1,3]/dxdxp[3,3]
    if which==11:
        jetpowden = gdet*TudMA[1,3]/dxdxp[3,3]
    if which==12:
        jetpowden = gdet*Tud[1,3]/dxdxp[3,3]
    if which==13:
        #rest-mass flux
        jetpowden = 0.0*gdet*rho*uu[3]*dxdxp[3,3]
    if which==4:
        #phi (mag. flux)
        jetpowden = np.abs(gdetB[1])
    #jetpowden[tj>=ny-2] = 0*jetpowden[tj>=ny-2]
    #jetpowden[tj<1] = 0*jetpowden[tj<1]
    if 1==1:
        #zero out outside jet (cut out low magnetization region)
        #cond=(mu<mumin)
        #
        #zero out outside jet (cut out low magnetization region)
        # for u^r\to 0, \mu \to b^2 \gamma/\rho, but \mu numerically becomes sick, so look at 4-Alfven velocity instead
        # v4a=1 is same as bsq=rho when ug=pg=0
        # follow mu unless <0.1 since the mu is unreliable
        #v4asq=bsq/(rho+ug+(gam-1)*ug)
        #mum1fake=uu[0]*(1.0+v4asq)-1.0
        # override (mum1fake or mu do poorly for marking boundary of jet)
        mum1fake=bsq/rho
        if mumax is None:
            cond=(mum1fake<mumin)
        else:
            cond=(mum1fake>mumax)
        #
        # avoid disk component that might be unbound and moving out as transient or as part of outer part of disk
        #beta=((gam-1)*ug)*divideavoidinf(bsq*0.5)
        beta=((gam-1)*ug)/(1E-30 + bsq*0.5)
        if maxbeta is None:
            donothing0000temp=1
        else:
            cond+=(beta>maxbeta)
        #
        if maxbsqorho is None:
            donothing0001temp=1
        else:
            cond+=(bsq/rho>maxbsqorho)
        #
        if minbsqorho is None:
            donothing0002temp=1
        else:
            cond+=(bsq/rho<minbsqorho)
        #
        #zero out bound region
        cond+=(1-isunbound)
        #zero out infalling region
        cond+=(uu[1]<=0.0)
        # 1 = north
        #-1 = south
        if donorthsouth==1:
            #NORTH
            #[zero out south hemisphere]
            cond += (tj>=ny/2)
        elif donorthsouth==-1:
            #SOUTH
            #[zero out north hemisphere]
            cond += (tj<ny/2)
        #
        jetpowden[cond] = 0*jetpowden[cond]
    #
    jetpowtot = scaletofullwedge(np.sum(np.sum(conditional*jetpowden,axis=2),axis=1)*_dx2*_dx3)
    #print "which = %d, minbsqorho = %g" % (which, minbsqorho)
    return(jetpowtot)
    
def plotit(ts,fs,md):
    #rc('font', family='serif')
    #plt.figure( figsize=(12,9) )
    fig,plotlist=plt.subplots(nrows=2,ncols=1,sharex=True,figsize=(12,9))
    #plt.subplots_adjust(hspace=0.4) #increase vertical spacing to avoid crowding
    plotlist[0].plot(ts,fs,label=r'$\Phi_{\rm h}/\Phi_{\rm i}$: Normalized Horizon Magnetic Flux')
    plotlist[0].plot(ts,fs,'r+') #, label=r'$\Phi_{\rm h}/0.5\Phi_{\rm i}$: Data Points')
    plotlist[0].legend(loc='lower right')
    #plt.xlabel(r'$t\;(r_g/c)$')
    plotlist[0].set_ylabel(r'$\Phi_{\rm h}$',fontsize=16)
    plt.setp( plotlist[0].get_xticklabels(), visible=False)
    plotlist[0].grid(True)
    #
    #plotlist[1].subplot(212,sharex=True)
    plotlist[1].plot(ts,md,label=r'$\dot M_{\rm h}$: Horizon Accretion Rate')
    plotlist[1].plot(ts,md,'r+') #, label=r'$\dot M_{\rm h}$: Data Points')
    plotlist[1].legend(loc='upper right')
    plotlist[1].set_xlabel(r'$t\;(r_g/c)$')
    plotlist[1].set_ylabel(r'$\dot M_{\rm h}$',fontsize=16)
    
    #title("\TeX\ is Number $\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!", 
    #      fontsize=16, color='r')
    plotlist[1].grid(True)
    fig.savefig('test.pdf')

def iofr(rval):
    return(iofrpole(rval))

def iofrpole(rval):
    if rval<=Rin or rval<=r[0,0,0]:
        return(0)
    elif rval>=Rout or rval>=r[-1,0,0]:
        return(ti[-1,0,0])
    else:
        res = interp1d(r[:,0,0], ti[:,0,0], kind='linear')
        return(np.floor(res(rval)+0.5))

def iofreq(rval):
    if rval<=Rin or rval<=r[0,0,0]:
        return(0)
    elif rval>=Rout or rval>=r[-1,0,0]:
        return(ti[-1,0,0])
    else:
        res = interp1d(r[:,ny/2,0], ti[:,ny/2,0], kind='linear')
        return(np.floor(res(rval)+0.5))

def tofts(tval):
    res = interp1d(ts[:], np.arange(0,len(ts)), kind='linear')
    return(np.floor(res(tval)+0.5))


def jofhfloat(hval,i):
    res = interp1d(h[i,:,0], tj[i,:,0], kind='linear')
    # return float result
    return(res(hval))

def jofh(hval,i):
    return(np.floor(jofhfloat(hval,i)+0.5))



def kofph(phval):
    if nz==1:
        return(0)
    #
    faketk=np.zeros(nz,dtype=np.int)
    for kk in np.arange(0,nz):
        faketk[kk]=kk
    #
    res = interp1d(ph[0,0,:], faketk[:], kind='linear',bounds_error=False,fill_value=-1)
    kval=np.floor(res(phval)+0.5)
    if kval==-1:
        if phval<np.pi:
            kval=0
        else:
            kval=nz-1
        #
    #
    return(kval)






# everything done inside this function only needs a final call to plot, not generating npy files or merging them.
def plotqtyvstime(qtymem,fullresultsoutput=0,whichplot=None,ax=None,findex=None,fti=None,ftf=None,showextra=False,prefactor=100,epsFm=None,epsFke=None):
    global mdotfinavgvsr, mdotfinavgvsr5, mdotfinavgvsr10,mdotfinavgvsr20, mdotfinavgvsr30,mdotfinavgvsr40
    #
    # need to compute this again
    rhor=1+(1-a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    #
    rjetin=10.
    if modelname=="blandford3d_new":
        rjetout=30.
    else:
        rjetout=50.
    # jon's Choice below
    showextra=True
    #
    #
    nqtynonbob = getnonbobnqty()
    nqty=nqtynonbob
    #
    ##################################
    #
    # in some cases want to read other data for other times and merge with current data
    # Do this for thickdiskhr3 and use thickdisk3 data for earlier times before started thickdiskhr3 -- including t=0 values
    if modelname=="thickdiskhr3":
        print("Reading from thickdisk3 for some times and merging with thickdiskhr3 data")
        #
        ##############################################
        # get low-res qty data (should make local link to this file)
        qtymemalt=np.load( "qty2_thickdisk3.npy" )
        # get size of low-res qty data
        numtimeslicesalt = qtymemalt.shape[1]
        numxalt = qtymemalt.shape[2]
        tslr=qtymemalt[0,:,0]
        tendlr=tslr[-1]
        print("orig: numtimeslicesalt=%d numxalt=%d" % (numtimeslicesalt,numxalt)) ; sys.stdout.flush()
        #
        ##############################################
        # get size of high-res qty data
        numtimeslices = qtymem.shape[1]
        numx = qtymem.shape[2]
        tshr=qtymem[0,:,0]
        print("hr: numtimeslices=%d numx=%d" % (numtimeslices,numx)) ; sys.stdout.flush()
        #
        ##############################################
        # include no data from t<tbreak from thickdiskhr3
        tbreak=100.0
        #
        gottstarthr=0
        for tic in tshr:
            tici=np.where(tshr==tic)[0]
            if tic>=tbreak:
                tstarthr=tic
                gottstarthr=1
                break
            #
        #
        if gottstarthr==0:
            print("Didn't get data beyond tbreak=%g" % (tbreak)) ; sys.stdout.flush()
            exit
        #
        #
        ##############################################
        # remove all data below tstarthr from high res data
        tconditionhr=(tshr>=tstarthr)
        qtymemhrnew=qtymem[:,tconditionhr,:]
        numtimeslices = qtymemhrnew.shape[1]
        numx = qtymemhrnew.shape[2]
        print("hrnew: numtimeslices=%d numx=%d" % (numtimeslices,numx)) ; sys.stdout.flush()
        #
        ##############################################
        # remove part of low-res qty data that overlaps with high res data
        tcondition=(tslr<tstarthr)
        print("tslr[-1]=%g tstarthr=%g" % (tslr[-1],tstarthr)) ; sys.stdout.flush()
        # qtymemalt is low-res data.  
        qtymemaltnew=qtymemalt[:,tcondition,:]
        # reget information
        numtimeslicesalt = qtymemaltnew.shape[1]
        numxalt = qtymemaltnew.shape[2]
        tslr=qtymemaltnew[0,:,0]
        tendlr=tslr[-1]
        print("numtimeslicesalt=%d numxalt=%d" % (numtimeslicesalt,numxalt)) ; sys.stdout.flush()
        # can't just use qtymem since number of time slices is different
        #qtymemalthr=np.copy(qtymem)
        qtymemalthr=np.zeros((nqty,numtimeslicesalt,nx),dtype=np.float32)
        #
        #
        # interpolate low-res data to high-res
        xi = np.linspace(0.0,1.0,numtimeslicesalt)
        yi = np.linspace(0.0,1.0,numxalt) # steps from 0 to 1 in steps based upon low-res data for radius part
        # hr nx size (just sets overall scale for interpolation)
        xxi = np.linspace(xi.min(),xi.max(),numtimeslicesalt) # same number of time slices
        yyi = np.linspace(yi.min(),yi.max(),numx) # new size in x from hr data
        # interpolate to thickdiskhr3 size
        print("thickdisk3->thickdiskhr3 shapes") ; sys.stdout.flush()
        print(xi.shape) ; sys.stdout.flush()
        print(yi.shape) ; sys.stdout.flush()
        print("nqty=%d" % nqty)
        print(qtymemaltnew.shape) ; sys.stdout.flush()
        #
        for qtyiter in np.arange(0,nqty):
            if 1==1:
                # below creates oscillations and changes how some of code handles t=0 data
                qtymemhrfun = sp.interpolate.RectBivariateSpline(xi,yi,qtymemaltnew[qtyiter,:,:], kx=2,ky=2)
                # below returns array of size [?;2] ?
                #qtymemhrfun = sp.interpolate.RectBivariateSpline(xi,yi,qtymemaltnew[qtyiter,:,:], kx=1,ky=1)
            else:
                # below is more conservative and sufficient
                # something is wrong with below -- stalls
                qtymemhrfun = sp.interpolate.interp2d(xi,yi,qtymemaltnew[qtyiter,:,:],kind='linear')
            #
            print("qtyiter=%d" % qtyiter)
            qtymemalthr[qtyiter] = qtymemhrfun(xxi,yyi)
        #
        #
        # now merge qtymem (hr version, generally with latter times) with qtymemalthr (generally with earlier times)
        # cat for times now that radii same
        qtymemcat=np.concatenate((qtymemalthr,qtymemhrnew),axis=1)
        #
        # remove times that overlap (keeping high res -- latter -- times)
        
        #
        # overwrite qtymem (overwrites any prior global assignment and creation of global memory)
        qtymem=np.copy(qtymemcat)
        numtimeslicesfinal = qtymem.shape[1]
        numxfinal = qtymem.shape[2]
        print("final: numtimeslicesfinal=%d numxfinal=%d" % (numtimeslicesfinal,numxfinal)) ; sys.stdout.flush()
        #
    #
    ###########################
    #
    # take qtymem and fill in variable names
    #
    totalnum=getqtymem(qtymem)
    if totalnum!=nqty:
        print("totalnum=%d does not equal nqty=%d" % (totalnum,nqty)) ; sys.stdout.flush()
    #
    #
    print("mdtot.shape")
    print(mdtot.shape)
    #
    #
    #
    #
    ##################################
    # get starting time so can compute time differences
    start_time=datetime.now()
    ##################################
    #
    ###################################
    #
    #derived
    #
    ########################
    # jet
    phiabsj_mu1 = phiabsj_n_mu1 + phiabsj_s_mu1
    #
    # Removing floors here from make (done *inside* ma calculation now)
    #pjmake_n_mu1=(pjma_n_mu1-pjma_n_mu1_flr) - (pjrm_n_mu1-pjrm_n_mu1_flr)
    #pjmake_s_mu1=(pjma_s_mu1-pjma_s_mu1_flr) - (pjrm_s_mu1-pjrm_s_mu1_flr)
    pjmake_n_mu1=(pjma_n_mu1) - (pjrm_n_mu1)
    pjmake_s_mu1=(pjma_s_mu1) - (pjrm_s_mu1)
    pjmake_mu1 = pjmake_n_mu1 + pjmake_s_mu1
    pjke_n_mu1 = pjem_n_mu1 + pjmake_n_mu1
    pjke_s_mu1 = pjem_s_mu1 + pjmake_s_mu1
    pjke_mu1 = pjke_n_mu1 + pjke_s_mu1
    pjem_mu1 = pjem_n_mu1 + pjem_s_mu1
    #
    # Removing floors here from make
    #ljmake_n_mu1=(ljma_n_mu1-ljma_n_mu1_flr) - (ljrm_n_mu1-ljrm_n_mu1_flr)
    #ljmake_s_mu1=(ljma_s_mu1-ljma_s_mu1_flr) - (ljrm_s_mu1-ljrm_s_mu1_flr)
    ljmake_n_mu1=(ljma_n_mu1) - (ljrm_n_mu1)
    ljmake_s_mu1=(ljma_s_mu1) - (ljrm_s_mu1)
    ljmake_mu1 = ljmake_n_mu1 + ljmake_s_mu1
    ljke_n_mu1 = ljem_n_mu1 + ljmake_n_mu1
    ljke_s_mu1 = ljem_s_mu1 + ljmake_s_mu1
    ljke_mu1 = ljke_n_mu1 + ljke_s_mu1
    ljem_mu1 = ljem_n_mu1 + ljem_s_mu1
    #
    ##############################
    # mwind
    phiabsj_mumax1m = phiabsj_n_mumax1m + phiabsj_s_mumax1m
    #
    # Removing floors here from make
    #pjmake_n_mumax1m=(pjma_n_mumax1m-pjma_n_mumax1m_flr) - (pjrm_n_mumax1m-pjrm_n_mumax1m_flr)
    #pjmake_s_mumax1m=(pjma_s_mumax1m-pjma_s_mumax1m_flr) - (pjrm_s_mumax1m-pjrm_s_mumax1m_flr)
    pjmake_n_mumax1m=(pjma_n_mumax1m) - (pjrm_n_mumax1m)
    pjmake_s_mumax1m=(pjma_s_mumax1m) - (pjrm_s_mumax1m)
    pjmake_mumax1m = pjmake_n_mumax1m + pjmake_s_mumax1m
    pjke_n_mumax1m = pjem_n_mumax1m + pjmake_n_mumax1m
    pjke_s_mumax1m = pjem_s_mumax1m + pjmake_s_mumax1m
    pjke_mumax1m = pjke_n_mumax1m + pjke_s_mumax1m
    pjem_mumax1m = pjem_n_mumax1m + pjem_s_mumax1m
    #
    # Removing floors here from make
    #ljmake_n_mumax1m=(ljma_n_mumax1m-ljma_n_mumax1m_flr) - (ljrm_n_mumax1m-ljrm_n_mumax1m_flr)
    #ljmake_s_mumax1m=(ljma_s_mumax1m-ljma_s_mumax1m_flr) - (ljrm_s_mumax1m-ljrm_s_mumax1m_flr)
    ljmake_n_mumax1m=(ljma_n_mumax1m) - (ljrm_n_mumax1m)
    ljmake_s_mumax1m=(ljma_s_mumax1m) - (ljrm_s_mumax1m)
    ljmake_mumax1m = ljmake_n_mumax1m + ljmake_s_mumax1m
    ljke_n_mumax1m = ljem_n_mumax1m + ljmake_n_mumax1m
    ljke_s_mumax1m = ljem_s_mumax1m + ljmake_s_mumax1m
    ljke_mumax1m = ljke_n_mumax1m + ljke_s_mumax1m
    ljem_mumax1m = ljem_n_mumax1m + ljem_s_mumax1m
    #
    ##############################
    # wind
    phiabsj_mumax1 = phiabsj_n_mumax1 + phiabsj_s_mumax1
    #
    # Removing floors here from make
    #pjmake_n_mumax1=(pjma_n_mumax1-pjma_n_mumax1_flr) - (pjrm_n_mumax1-pjrm_n_mumax1_flr)
    #pjmake_s_mumax1=(pjma_s_mumax1-pjma_s_mumax1_flr) - (pjrm_s_mumax1-pjrm_s_mumax1_flr)
    pjmake_n_mumax1=(pjma_n_mumax1) - (pjrm_n_mumax1)
    pjmake_s_mumax1=(pjma_s_mumax1) - (pjrm_s_mumax1)
    pjmake_mumax1 = pjmake_n_mumax1 + pjmake_s_mumax1
    pjke_n_mumax1 = pjem_n_mumax1 + pjmake_n_mumax1
    pjke_s_mumax1 = pjem_s_mumax1 + pjmake_s_mumax1
    pjke_mumax1 = pjke_n_mumax1 + pjke_s_mumax1
    pjem_mumax1 = pjem_n_mumax1 + pjem_s_mumax1
    #
    # Removing floors here from make
    #ljmake_n_mumax1=(ljma_n_mumax1-ljma_n_mumax1_flr) - (ljrm_n_mumax1-ljrm_n_mumax1_flr)
    #ljmake_s_mumax1=(ljma_s_mumax1-ljma_s_mumax1_flr) - (ljrm_s_mumax1-ljrm_s_mumax1_flr)
    ljmake_n_mumax1=(ljma_n_mumax1) - (ljrm_n_mumax1)
    ljmake_s_mumax1=(ljma_s_mumax1) - (ljrm_s_mumax1)
    ljmake_mumax1 = ljmake_n_mumax1 + ljmake_s_mumax1
    ljke_n_mumax1 = ljem_n_mumax1 + ljmake_n_mumax1
    ljke_s_mumax1 = ljem_s_mumax1 + ljmake_s_mumax1
    ljke_mumax1 = ljke_n_mumax1 + ljke_s_mumax1
    ljem_mumax1 = ljem_n_mumax1 + ljem_s_mumax1
    #
    #
    #end qty defs
    ##############################
    #end copy
    ##############################
    #
    #rc('font', family='serif')
    #plt.figure( figsize=(12,9) )
    if ftf is not None:
        iti = 1000 #dummy
        itf = 2000 #dummy
        if ftf > ts[-1]:
            ftf = ts[-1]
        print fti, ftf ; sys.stdout.flush()
        dotavg=1
    elif os.path.isfile(os.path.join("titf.txt")):
        dotavg=1
        gd1 = np.loadtxt( "titf.txt",
                          dtype=np.float64, 
                          skiprows=1, 
                          unpack = True )
        iti = gd1[0]
        itf = gd1[1]
        fti = gd1[2]
        ftf = gd1[3]
    else:
        dotavg=1
        #
        defaultfti,defaultftf=getdefaulttimes()
        #
        iti = min(3000,ts[-1])
        itf = max(4000,ts[0])
        fti = defaultfti
        ftf = defaultftf
        print( "Warning: titf.txt not found: using default numbers for averaging: %g %g %g %g" % (iti, itf, fti, ftf) ) ; sys.stdout.flush()
    #
    #######################
    # find true range that used for averaging
    #######################
    # exclude ts[0] that is probably t=0, so truetmin corresponds to true averaging period
    if ts[0]==0.0:
        truetmax=np.max(ts[1:len(ts)])
        truetmin=np.min(ts[1:len(ts)])
    else:
        truetmax=np.max(ts)
        truetmin=np.min(ts)
    #
    if truetmin<fti:
        truetmin=fti
    #
    if truetmax>ftf:
        truetmax=ftf
    #
    print("Part1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #################################
    # BEGIN PART1 some things vsr (nothing that depends upon rdiskin or rdiskout)
    #################################
    #mdotiniavg = timeavg(mdtot[:,ihor]-md10[:,ihor],ts,fti,ftf)
    #mdotfinavg = (mdtot[:,ihor]-md10[:,ihor])[(ts<ftf)*(ts>=fti)].sum()/(mdtot[:,ihor]-md10[:,ihor])[(ts<ftf)*(ts>=fti)].shape[0]
    mdotiniavgvsr = timeavg(mdtot,ts,iti,itf)
    mdotfinavgvsr = timeavg(mdtot,ts,fti,ftf)
    # full (disk + jet) accretion rate
    mdtotvsr = mdotfinavgvsr
    edtotvsr = timeavg(edtot,ts,fti,ftf)
    edemvsr = timeavg(edem,ts,fti,ftf)
    edmavsr = timeavg(edma-edma30,ts,fti,ftf)
    edmvsr = timeavg(edm-edm30,ts,fti,ftf)

    ldtotvsr = timeavg(ldtot,ts,fti,ftf)
    ldemvsr = timeavg(ldem,ts,fti,ftf)
    ldmavsr = timeavg(ldma-ldma30,ts,fti,ftf)
    ldmvsr = timeavg(ldm-ldm30,ts,fti,ftf)
    #
    phiabsj_mu1vsr = timeavg(phiabsj_mu1[:,:],ts,fti,ftf)
    #
    ######### full mdtot+md30=[total Mdot including floor] and then subtracting md5,md10,md20
    mdotfinavgvsr5 = timeavg(mdtot[:,:]+md30[:,:]-md5[:,:],ts,fti,ftf)
    mdotfinavgvsr10 = timeavg(mdtot[:,:]+md30[:,:]-md10[:,:],ts,fti,ftf)
    mdotfinavgvsr20 = timeavg(mdtot[:,:]+md30[:,:]-md20[:,:],ts,fti,ftf)
    #
    #mdotfinavgvsr30 = timeavg(mdtot[:,:],ts,fti,ftf)
    #
    # Using md30 instead of md10 for horizon value since bsq/rho>>30 since disk-jet boundary clean and can get more accurate mdot.
    # Using md10 doesn't change much, however.
    # Instead, pick Mdot at horizon
    mdotfinavgvsr30itself = timeavg(md30[:,:],ts,fti,ftf)
    mdotiniavgvsr30itself = timeavg(md30[:,:],ts,iti,itf)
    #
    # now mdtot includes floor correction already
    # quasi-name for *normal* mdot (no longer about md30 exactly)
    mdotfinavgvsr30 = timeavg(mdtot[:,:],ts,fti,ftf)
    mdotiniavgvsr30 = timeavg(mdtot[:,:],ts,iti,itf)
    #
    mdotfinavgvsr10 = timeavg(mdtot[:,:]-md10[:,:],ts,fti,ftf)
    mdotfinavgvsr10itself = timeavg(md10[:,:],ts,fti,ftf)
    mdotiniavgvsr10 = timeavg(mdtot[:,:]-md10[:,:],ts,iti,itf)
    mdotiniavgvsr10itself = timeavg(md10[:,:],ts,iti,itf)
    #
    mdotfinavgvsr40 = timeavg(mdtot[:,:]-md40[:,:],ts,fti,ftf)    
    #
    # Below 2 used as divisor to get efficiencies and normalized magnetic flux
    #mdotiniavg = np.float64(mdotiniavgvsr30)[r[:,0,0]<10].mean()
    #mdotfinavg = np.float64(mdotfinavgvsr30)[r[:,0,0]<10].mean()
    mdotiniavg = np.float64(mdotiniavgvsr30)[ihor]
    mdotfinavg = np.float64(mdotfinavgvsr30)[ihor]
    #
    mdot30iniavg = np.float64(mdotiniavgvsr30itself)[ihor]
    mdot30finavg = np.float64(mdotfinavgvsr30itself)[ihor]
    #
    mdot10iniavg = np.float64(mdotiniavgvsr10itself)[ihor]
    mdot10finavg = np.float64(mdotfinavgvsr10itself)[ihor]
    #
    # below as pjem30, but removed that
    pjetiniavg = timeavg(pjem5[:,ihor],ts,iti,itf)
    pjetfinavg = timeavg(pjem5[:,ihor],ts,fti,ftf)
    #
    # EM energy
    pjemtot = edem
    pjemfinavgtot = timeavg(pjemtot[:,ihor],ts,fti,ftf)
    pjemfinavgvsr = timeavg(pjemtot,ts,fti,ftf)
    pjemfinavgvsr5 = timeavg(pjem5[:,:],ts,fti,ftf)
    #
    # MA free energy (but remove matter-energy flux created by floors (i.e. bsq/rho>30) near horizon)
    pjmaketot = (edma-edma30) - (edm-edm30)
    pjmakefinavgtot = timeavg(pjmaketot[:,ihor],ts,fti,ftf)
    pjmakefinavgvsr = timeavg(pjmaketot,ts,fti,ftf)
    #
    # free energy (use em+make=ke so bsq/rho>30 correction can be made less number of times)
    pjketot = pjemtot + pjmaketot
    pjkefinavgtot = pjemfinavgtot + pjmakefinavgtot
    pjkefinavgvsr = pjemfinavgvsr + pjmakefinavgvsr
    #
    #
    pjmafinavgvsr = timeavg(edma[:,:],ts,fti,ftf)
    pjmafinavgvsr5 = timeavg(pjma5[:,:],ts,fti,ftf)
    #
    pjtotfinavgvsr = pjemfinavgvsr + pjmafinavgvsr
    pjtotfinavgvsr5 = pjemfinavgvsr5 + pjmafinavgvsr5
    #
    # T^\mu_\nu + \rho_0 u^\mu \eta_\nu
    # w u^r u_\phi vs. w u^r u_t
    # u_\phi ~ R u^\phi ~ R v^\phi ~ R R^{-1/2} ~ R^{1/2}
    # rho u^r u_\phi + rho u^r -> rho u^r (u_\phi+1) (stupid) vs. rho u^r u_t + rho u^r -> rho u^r (u_t+1) (correct)
    # EM energy
    ljemtot = ldtot - ldma
    ljemfinavgtot = timeavg(ljemtot[:,ihor],ts,fti,ftf)
    ljemfinavgvsr = timeavg(ljemtot,ts,fti,ftf)
    #
    # MA free energy
    ljmaketot = (ldma-ldma30) - (ldm-ldm30)
    ljmakefinavgtot = timeavg(ljmaketot[:,ihor],ts,fti,ftf)
    ljmakefinavgvsr = timeavg(ljmaketot,ts,fti,ftf)
    #
    # free energy (use em+make=ke so bsq/rho>30 correction can be made less number of times)
    ljketot = ljemtot + ljmaketot
    ljkefinavgtot = timeavg(ljketot[:,ihor],ts,fti,ftf)
    ljkefinavgvsr = timeavg(ljketot,ts,fti,ftf)
    #
    if 0==1:
        # TEMP FIX FUCKMARK
        global fstot,fsin,fsmaxtot,fsj5,fsj10,fsj20,fsj30,fsj40
        fstot=fstot*2.0
        fsin=fsin*2.0
        #fsmaxtot=fsmaxtot*2.0
        fsj5=fsj5*2.0
        fsj10=fsj10*2.0
        fsj20=fsj20*2.0
        fsj30=fsj30*2.0
        fsj40=fsj40*2.0
    #
    #
    fstotfinavg = timeavg(fstot[:,ihor],ts,fti,ftf)
    fstotsqfinavg = timeavg(fstot[:,ihor]**2,ts,fti,ftf)**0.5
    #
    fsinfinavg = timeavg(fsin[:,ihor],ts,fti,ftf)
    fsinsqfinavg = timeavg(fsin[:,ihor]**2,ts,fti,ftf)**0.5
    #
    fsmaxtotfinavg = timeavg(fsmaxtot[:,ihor],ts,fti,ftf)
    fsmaxtotsqfinavg = timeavg(fsmaxtot[:,ihor]**2,ts,fti,ftf)**0.5
    #
    fsuphalffinavg = timeavg(fsuphalf[:,ihor],ts,fti,ftf)
    fsuphalfsqfinavg = timeavg(fsuphalf[:,ihor]**2,ts,fti,ftf)**0.5
    #
    fsj30finavg = timeavg(fsj30[:,ihor],ts,fti,ftf)
    fsj30sqfinavg = timeavg(fsj30[:,ihor]**2,ts,fti,ftf)**0.5
    #
    #
    mdin_vsr=timeavg(mdin[:,:],ts,fti,ftf)
    mdjet_vsr=timeavg(mdjet[:,:],ts,fti,ftf)
    mdmwind_vsr=timeavg(mdmwind[:,:],ts,fti,ftf)
    mdwind_vsr=timeavg(mdwind[:,:],ts,fti,ftf)
    #
    alphamag1_vsr=timeavg(alphamag1[:,:],ts,fti,ftf)
    alphamag2_vsr=timeavg(alphamag2[:,:],ts,fti,ftf)
    alphamag3_vsr=timeavg(alphamag3[:,:],ts,fti,ftf)
    #
    fstot_vsr=timeavg(fstot[:,:],ts,fti,ftf)
    fsin_vsr=timeavg(fsin[:,:],ts,fti,ftf)
    feqtot_vsr=timeavg(feqtot[:,:],ts,fti,ftf)
    fsmaxtot_vsr=timeavg(fsmaxtot[:,:],ts,fti,ftf)
    fsuphalf_vsr=timeavg(fsuphalf[:,:],ts,fti,ftf)
    upsilon_vsr=timeavg(fstot[:,:],ts,fti,ftf)/(2.0)*((0.2*np.sqrt(4.0*np.pi))/mdotfinavg**0.5)
    #
    etajEM_vsr = timeavg(prefactor*pjem_mu1[:,:]/mdotfinavg,ts,fti,ftf)
    etajMAKE_vsr = timeavg(prefactor*pjmake_mu1[:,:]/mdotfinavg,ts,fti,ftf)
    etamwEM_vsr = timeavg(prefactor*pjem_mumax1m[:,:]/mdotfinavg,ts,fti,ftf)
    etamwMAKE_vsr = timeavg(prefactor*pjmake_mumax1m[:,:]/mdotfinavg,ts,fti,ftf)
    etamw_vsr = etamwEM_vsr +  etamwMAKE_vsr
    etawEM_vsr = timeavg(prefactor*pjem_mumax1[:,:]/mdotfinavg,ts,fti,ftf)
    etawMAKE_vsr = timeavg(prefactor*pjmake_mumax1[:,:]/mdotfinavg,ts,fti,ftf)
    etaw_vsr = etawEM_vsr +  etawMAKE_vsr
    #
    letajEM_vsr = timeavg(prefactor*ljem_mu1[:,:]/mdotfinavg,ts,fti,ftf)/prefactor
    letajMAKE_vsr = timeavg(prefactor*ljmake_mu1[:,:]/mdotfinavg,ts,fti,ftf)/prefactor
    letamwEM_vsr = timeavg(prefactor*ljem_mumax1m[:,:]/mdotfinavg,ts,fti,ftf)/prefactor
    letamwMAKE_vsr = timeavg(prefactor*ljmake_mumax1m[:,:]/mdotfinavg,ts,fti,ftf)/prefactor
    letamw_vsr = letamwEM_vsr +  letamwMAKE_vsr
    letawEM_vsr = timeavg(prefactor*ljem_mumax1[:,:]/mdotfinavg,ts,fti,ftf)/prefactor
    letawMAKE_vsr = timeavg(prefactor*ljmake_mumax1[:,:]/mdotfinavg,ts,fti,ftf)/prefactor
    letaw_vsr = letawEM_vsr +  letawMAKE_vsr
    #
    #
    #
    #################################
    # END PART1 some things vsr
    #################################
    #
    ######################################
    # BEGIN equatorial stagnation calculation
    ######################################
    print("EqStag" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    # Get position of flow stagnation (excluding highly magnetized jet region)
    # mdtot should be >0 (i.e. inflow) for all radii up to stagnation dominated by equatorial region
    # something like (but not right): indices[:]=ti[:,0,0][mdtot[:,:]<0]
    # for table, only need average stagnation surface:
    # using full mdot (excluding jet) because corona might carry in some flux if going in.
    # default is that istageq=nx-1 and rstageq=Rout
    #
    #####################################################
    # get time-averaged v^{x^1} weighted by density
    vus1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
    for ii in np.arange(0,nx):
        vus1rhosqdcden_vsr[ii]=timeavg(vus1rhosqdcden[:,ii],ts,fti,ftf)
    #
    # figure out where v^{x^1} passes through zero (if anywhere)
    ioutlist=ti[:,0,0][vus1rhosqdcden_vsr>0]
    print("ioutlistsize")
    print(len(ioutlist))
    if len(ioutlist)>0:
        iout=ioutlist[0]
        istagfromvus1rhosqdcden=iout
        rstagfromvus1rhosqdcden=r[iout,ny/2,0]
    else:
        iout=nx
        istagfromvus1rhosqdcden=iout
        rstagfromvus1rhosqdcden=Rout
    #
    print("istagfromvus1rhosqdcden=%d rstagfromvus1rhosqdcden=%g" % (istagfromvus1rhosqdcden,rstagfromvus1rhosqdcden))
    #
    #
    #####################################################
    # get time-averaged v^{x^1} weighted by density
    vus1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
    for ii in np.arange(0,nx):
        vus1rhosqdc_vsr[ii]=timeavg(vus1rhosqdc[:,ii],ts,fti,ftf)
    #
    # figure out where v^{x^1} passes through zero (if anywhere)
    ioutlist=ti[:,0,0][vus1rhosqdc_vsr>0]
    iout=ioutlist[0]
    if len(ioutlist)>0:
        iout=ioutlist[0]
        istagfromvus1rhosqdc=iout
        rstagfromvus1rhosqdc=r[iout,ny/2,0]
    else:
        iout=nx
        istagfromvus1rhosqdc=iout
        rstagfromvus1rhosqdc=Rout
    #
    #
    print("istagfromvus1rhosqdc=%d rstagfromvus1rhosqdc=%g" % (istagfromvus1rhosqdc,rstagfromvus1rhosqdc)) ; sys.stdout.flush()
    #
    #####################################################
    # get stag for average of simulation data using mdot over whole flow
    istageq=nx-1
    rstageq=Rout
    # ok, use bsqorho<5 part of flow to exclude jet at large radii
    # already have mdotfinavgvsr5 computed above
    #
    sizet=len(ts)
    #print("sizet")
    #print(sizet)
    mdot5vsr=np.zeros(nx,dtype=ldma.dtype)
    reqstagvst=np.zeros(sizet,dtype=ldma.dtype)
    istageqtemp1=np.zeros(nx,dtype=ldma.dtype)
    #
    #
    #print("tsnew"); sys.stdout.flush()
    #print(ts); sys.stdout.flush()
    #
    for tic in ts:
        tici=np.where(ts==tic)[0]
        #print("tici") ; sys.stdout.flush()
        #print(tici) ; sys.stdout.flush()
        #print("tic") ; sys.stdout.flush()
        #print(tic) ; sys.stdout.flush()
        print("lenchecks: %d %d %d" % (len(mdot5vsr[:]),len(mdtot[tici,:]),len(md5[tici,:]))) ; sys.stdout.flush()
        mdot5vsr[:]=mdtot[tici,:] # no longer need md5 since mdtot has floor correction
        #print("mdtot")
        #print(mdtot)
        #print("fuck: %d" % (tici) )
        #print(len(mdot5vsr))
        #print(mdot5vsr)
        istageqtemp1=ti[:,0,0][mdot5vsr<0]
        #print("istageqtemp1")
        #print(istageqtemp1)
        # first stagnation starting from inner radius
        if len(istageqtemp1)>0:
            istageqtemp=istageqtemp1[0]
        else:
            istageqtemp=nx-1
        #
        if istageqtemp<0:
            istageqtemp=0
        if istageqtemp>nx-1:
            istageqtemp=nx-1
        #
        reqstagvst[tici]=r[istageqtemp,0,0]
    #
    #
    #
    #
    print("lenmdotfinavgvsr5=%d" % (len(mdotfinavgvsr5))) ; sys.stdout.flush()
    indiceseq=ti[:,0,0][mdotfinavgvsr5<0]
    print("indiceseq") ; sys.stdout.flush()
    print(indiceseq) ; sys.stdout.flush()
    #
    problem1=0
    problem2a=0
    if len(indiceseq)>0:
        # if pick first such zero (using indiceseq[0] below), then if inner-region oscillates (as occurs for 2D MAD models), then picks out region that already filled-up with lots of flux long ago.
        istageq=indiceseq[0]
        if istageq>0 and istageq<nx:
            rstageq=r[istageq,0,0]
            print("istageq=%d rstageq=%g" % (istageq,rstageq) ) ; sys.stdout.flush()
        else:
            print("istageq=%d len=%d PROBLEM1" % (istageq,len(indiceseq)) ) ; sys.stdout.flush()
            problem1=1
    else:
        print("indicieseq PROBLEM2") ; sys.stdout.flush()
        problem2a=1
    #
    # get stag for very near the end of the simulation data
    istageqnearfin=nx-1
    rstageqnearfin=Rout
    print("fti=%g ftf=%g other=%g" % (fti,ftf,0.85*ftf) ) ; sys.stdout.flush()
    if ts[0]>fti:
        truefti=ts[0]
    else:
        truefti=fti
    if ts[-1]<ftf:
        trueftf=ts[-1]
    else:
        trueftf=ftf
    #
    nearfinti=(trueftf-truefti)*0.85 + truefti
    # ok, use bsqorho<5 part of flow to exclude jet at large radii
    mdotnearfinavgvsr5 = timeavg(mdtot[:,:],ts,nearfinti,trueftf)
    print("lenmdotnearfinavgvsr5=%d" % (len(mdotnearfinavgvsr5))) ; sys.stdout.flush()
    indiceseqnearfin=ti[:,0,0][mdotnearfinavgvsr5<0]
    print("indiceseqnearfin") ; sys.stdout.flush()
    print(indiceseqnearfin) ; sys.stdout.flush()
    #
    problem1b=0
    problem2b=0
    if len(indiceseqnearfin)>0:
        # if pick first such zero (using indiceseq[0] below), then if inner-region oscillates (as occurs for 2D MAD models), then picks out region that already filled-up with lots of flux long ago.
        istageqnearfin=indiceseqnearfin[0]
        if istageqnearfin>0 and istageqnearfin<nx:
            rstageqnearfin=r[istageqnearfin,0,0]
            print("istageqnearfin=%d rstageqnearfin=%g" % (istageqnearfin,rstageqnearfin) ) ; sys.stdout.flush()
        else:
            print("istageqnearfin=%d len=%d PROBLEM1" % (istageqnearfin,len(indiceseqnearfin)) ) ; sys.stdout.flush()
            problem1b=1
    else:
        print("indicieseqnearfin PROBLEM2") ; sys.stdout.flush()
        problem2b=1
    #
    #
    #
    print("ts") ; sys.stdout.flush()
    print(ts) ; sys.stdout.flush()
    #
    sizet=len(ts)
    print("sizet=%d" % (sizet) ) ; sys.stdout.flush()
    blob=np.zeros(len(mdotfinavgvsr5),dtype=mdotfinavgvsr5.dtype)
    indicesvst=np.zeros(sizet,dtype=ti.dtype)
    for tic in ts:
        tici=np.where(ts==tic)[0]
        #print("tic=%g %d tici=%d" % (tic,len(tic==ts),tici) )
        blob[:]=mdtot[tici,:]
        #print("lenblob=%d" % (len(blob)))
        indices=ti[:,0,0][blob<0]
        #print("indices")
        #print(indices)
        if len(indices)>0:
            indicesvst[tici]=indices[0]
        else:
            indicesvst[tici]=nx-1
    #
    print("indicesvst") ; sys.stdout.flush()
    print(indicesvst) ; sys.stdout.flush()
    #
    #################################
    #
    #radius of stagnation point (Pjmabsqorho5(rstag) = 0)
    #
    #################################
    indices=ti[:,0,0][pjmafinavgvsr5>0]
    # problem with out of bounds on iofr(2*rstag) or then max for thickdisk5 for no apparent reason
    if 0 and indices.shape[0]>0:
        istag=indices[0]
        rstag=r[istag,0,0]
        print("istag=%d rstag=%g" % (istag,rstag) ) ; sys.stdout.flush()
        if rstag>20:
            rstag=20
        # issue with out of bounds in iofr, so keep rstag outside Rin
        print("rstag=%g Rin=%g Rout=%g" % (rstag, Rin, Rout) ) ; sys.stdout.flush()
        rstag=np.max(rstag,Rin*1.05)
        rstag=np.max(rstag,Rout*0.99)
        i2stag=iofr(2*rstag)
        i4stag=iofr(4*rstag)
        i8stag=iofr(8*rstag)
        pjtotfinavgvsr5max    = np.max(pjtotfinavgvsr5)
        pjtotfinavgvsr5rstag  = pjtotfinavgvsr5[istag]
        pjtotfinavgvsr5r2stag = pjtotfinavgvsr5[i2stag]
        pjtotfinavgvsr5r4stag = pjtotfinavgvsr5[i4stag]
        pjtotfinavgvsr5r8stag = pjtotfinavgvsr5[i8stag]
    else:
        istag=0
        rstag=0
        i2stag=0
        i4stag=0
        i8stag=0
        pjtotfinavgvsr5max    = np.max(pjtotfinavgvsr5)
        pjtotfinavgvsr5rstag  = 0
        pjtotfinavgvsr5r2stag = 0
        pjtotfinavgvsr5r4stag = 0
        pjtotfinavgvsr5r8stag = 0
    #
    ######################################
    # END equatorial stagnation calculation
    ######################################
    #
    ######################################
    # BEGIN PART1 of COMPUTE JON WHICHPLOT==5
    ######################################
    print("Part1 whichplot==5" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    ##############
    # true total flux (including BH+disk @ equator) vs. time and radius
    feqtot[:,ti[:,0,0]<ihor]=0
    ftruetot=np.copy(feqtot)
    for tic in ts:
        tici=np.where(ts==tic)[0]
        # fstot doesn't account for sign as required
        #ftruetot[tici,:]=ftruetot[tici,:] + (-fstot[tici,ihor]/2)
        # fsmaxtot accounts for sign as required
        #ftruetot[tici,:]=ftruetot[tici,:] - fsmaxtot[tici,ihor]
        # fsuphalf accounts for sign as required and is correct hemisphere to add to equatorial value
        ftruetot[tici,:]=ftruetot[tici,:] - fsuphalf[tici,ihor]
    #
    ############
    #
    # get zero point in total flux and then find where max same-signed flux is
    #
    blobf=np.zeros(len(mdotfinavgvsr5),dtype=mdotfinavgvsr5.dtype)
    ifmaxvst=np.zeros(sizet,dtype=int)
    fmaxvst=np.zeros(sizet,dtype=float)
    #
    filefmax = open( "fmax.txt" , "w" )
    #
    for tic in ts:
        tici=np.where(ts==tic)[0]
        print("tic=%g %d tici=%d" % (tic,len(tic==ts),tici) ) ; sys.stdout.flush()
        blobf[:]=ftruetot[tici,:]
        #print("lenblobf=%d" % (len(blobf)))
        #print("blobf")
        #print(blobf)
        # DEBUG:
        if tici==len(ts)-1:
            print("blobf=%g",blobf) ; sys.stdout.flush()
            for ii in np.arange(0,len(blobf)):
                filefmax.write( "%d %g   %g  %g %g %g  %g\n" % (ti[ii,0,0],r[ii,0,0],blobf[ii],feqtot[tici,ii],fsmaxtot[tici,ii],fsuphalf[tici,ii],fstot[tici,ii]/2.0)); filefmax.flush()
        #
        #
        # first get where total vertical flux at equator (including horizon) reaches zero.
        condition=(ti[:,0,0]>ihor)
        condition=condition*(np.sign(blobf)!=np.sign(blobf[ihor]))
        fzeroO=ti[:,0,0][condition==1]
        fzero=fzeroO.astype(np.integer)
        izero=-1
        # see if ever got zero
        if len(fzero)==0:
            izero=nx-1
        else:
            izero=fzero[0]
            # back-up to first same-signed value
            if izero!=ihor:
                izero=izero-1
            #
        #
        # get max of flux inside of zeroing, so that max corresponds to field reversal location
        print("ihor=%d izero=%d" % (ihor, izero) ) ; sys.stdout.flush()
        #
        if izero!=-1:
            #print("blobfihor=%g blobfizero=%g" % (blobf[ihor],blobf[izero]) )
            condition=ti[:,0,0]>=ihor
            condition=condition*(ti[:,0,0]<=izero)
            # only do max over relevant range
            newblobf=np.copy(blobf)
            newblobf[ti[:,0,0]<ihor]=0
            newblobf[ti[:,0,0]>izero]=0
            condition=condition*(np.fabs(newblobf[:])==np.max(np.fabs(newblobf[:])))
            #print("condition")
            #print(condition)
            imax=np.where(condition==1)[0]
            #print("imax")
            #print(imax)
            #
            if(len(imax)>1):
                imax=imax[0]
                #print("imax2")
                #print(imax)
            #
            ifmax=ftruetot[tici,imax]
            #print("ifmax")
            #print(ifmax)
            #print("imax=%d ifmax=%g" % (imax,ifmax) )
            ifmaxvst[tici]=imax
        else:
            ifmaxvst[tici]=ihor
        #
        fmaxvst[tici]=ftruetot[tici,ifmaxvst[tici]]
        #print("fmax=%g" % (fmaxvst[tici]) )
    #
    #
    filefmax.close()
    #
    print("ifmaxvst") ; sys.stdout.flush()
    print(ifmaxvst) ; sys.stdout.flush()
    print("fmaxvst") ; sys.stdout.flush()
    print(fmaxvst) ; sys.stdout.flush()
    #
    # time-averaged flux at the max flux relevant for the hole flux
    # use this rather than t=0 max flux for hole ratio calculation because flux can degrade over time on domain.
    # So want to know what the flux is on the hole relative to similar signed flux available to the hole at any time, not just predegraded value at t=0
    ftruetot_avg = timeavg(fmaxvst,ts,fti,ftf)
    print("ftruetot_avg=%g fmaxvst_end=%g" % (ftruetot_avg,fmaxvst[-1]) ) ; sys.stdout.flush()
    #
    #
    #
    # kinda odd use of average whichistageq inside time-dependent thing, but done for simplicity
    feqstag=feqtot[:,istageq]
    # need t=0 value since want full possible source of flux, not just average or current flux available
    feqstagt0=feqtot[0,istageq]
    feqstag_avg1 = timeavg(feqstag,ts,fti,ftf)
    feqstag_avg2 = timeavg(feqstag**2,ts,fti,ftf)**0.5
    feqstagB_avg1 = timeavg(feqstag,ts,0,fti)
    feqstagB_avg2 = timeavg(feqstag**2,ts,0,fti)**0.5
    feqstagC_avg1 = timeavg(feqstag,ts,iti,itf)
    feqstagC_avg2 = timeavg(feqstag**2,ts,iti,itf)**0.5
    print("feqstagt0=%g" % (feqstagt0) )
    print("feqstag_avg1=%g feqstag_avg2=%g" % (feqstag_avg1, feqstag_avg2) )
    print("feqstagB_avg1=%g feqstagB_avg2=%g" % (feqstagB_avg1, feqstagB_avg2) )
    print("feqstagC_avg1=%g feqstagC_avg2=%g" % (feqstagC_avg1, feqstagC_avg2) )
    sys.stdout.flush()
    #
    # kinda odd use of average istageq inside time-dependent thing, but done for simplicity
    feqstagnearfin=feqtot[:,istageqnearfin]
    # need t=0 value since want full possible source of flux, not just average or current flux available
    feqstagnearfint0=feqtot[0,istageqnearfin]
    feqstagnearfin_avg1 = timeavg(feqstagnearfin,ts,fti,ftf)
    feqstagnearfin_avg2 = timeavg(feqstagnearfin**2,ts,fti,ftf)**0.5
    feqstagnearfinB_avg1 = timeavg(feqstagnearfin,ts,0,fti)
    feqstagnearfinB_avg2 = timeavg(feqstagnearfin**2,ts,0,fti)**0.5
    feqstagnearfinC_avg1 = timeavg(feqstagnearfin,ts,iti,itf)
    feqstagnearfinC_avg2 = timeavg(feqstagnearfin**2,ts,iti,itf)**0.5
    print("feqstagnearfint0=%g" % (feqstagnearfint0) )
    print("feqstagnearfin_avg1=%g feqstagnearfin_avg2=%g" % (feqstagnearfin_avg1, feqstagnearfin_avg2) )
    print("feqstagnearfinB_avg1=%g feqstagnearfinB_avg2=%g" % (feqstagnearfinB_avg1, feqstagnearfinB_avg2) )
    print("feqstagnearfinC_avg1=%g feqstagnearfinC_avg2=%g" % (feqstagnearfinC_avg1, feqstagnearfinC_avg2) )
    sys.stdout.flush()
    #
    # choose which istageq to use
    #chosenfeqstag=feqstagt0
    #chosenfeqstag=feqstagnearfint0
    if problem2a==0:
        chosenfeqstag=feqstagt0
        istagequse=istageq
    elif problem2a==0 and problem2b==0:
        if np.fabs(feqstagnearfint0)>np.fabs(feqstagt0):
            chosenfeqstag=feqstagnearfint0
            istagequse=istageqnearfin
        else:
            chosenfeqstag=feqstagt0
            istagequse=istageq
    else:
        if problem2a==0:
            chosenfeqstag=feqstagt0
            istagequse=istageq
        elif problem2b==0:
            chosenfeqstag=feqstagnearfint0
            istagequse=istageqnearfin
        else:
            print("Major problem2") ; sys.stdout.flush()
            chosenfeqstag=feqstagnearfint0
            istagequse=istageqnearfin
    #
    rstagequse=r[istagequse,0,0]
    print("rstagequse=%g istagequse=%d" % (rstagequse,istagequse)) ; sys.stdout.flush()
    #
    istagreport=min(istagequse,istagfromvus1rhosqdcden)
    rstagreport=min(rstagequse,rstagfromvus1rhosqdcden)
    print("rstagreport=%g istagreport=%d" % (rstagreport,istagreport)) ; sys.stdout.flush()
    #
    ######################################
    # END PART1 of COMPUTE JON WHICHPLOT==5
    ######################################
    #
    #################################
    # BEGIN compute h/r stuff (can't depend upon rdiskin or rdiskout -- although could make some of them depend if put some of them later)
    #################################
    print("h/r stuff" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    hoverrhor=hoverr[:,ihor]
    hoverr2=hoverr[:,iofr(2)]
    hoverr5=hoverr[:,iofr(5)]
    hoverr10=hoverr[:,iofr(10)]
    hoverr12=hoverr[:,iofr(12)]
    hoverr20=hoverr[:,iofr(20)]
    if modelname=="blandford3d_new":
        # so really at r=30 not 100
        hoverr100=hoverr[:,iofr(30)]
    else:
        hoverr100=hoverr[:,iofr(100)]
    #
    #print("hoverr100") ; sys.stdout.flush()
    #print(hoverr100) ; sys.stdout.flush()
    #for ii in np.arange(0,len(hoverr100)):
    #    print("ii=%d hoverr100=%g" % (ii,hoverr100[ii]))
    #
    hoverrhor_t0 = hoverrhor[0]
    hoverr2_t0 = hoverr2[0]
    hoverr5_t0 = hoverr5[0]
    hoverr10_t0 = hoverr10[0]
    hoverr12_t0 = hoverr12[0]
    hoverr20_t0 = hoverr20[0]
    hoverr100_t0 = hoverr100[0]
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        hoverr12=hoverr[:,iofr(12)]
        hoverratrmax_t0=hoverr12[0]
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        hoverr34=hoverr[:,iofr(34)]
        hoverratrmax_t0=hoverr34[0]
    else:
        hoverratrmax_t0=hoverr100[0]
    #
    #
    hoverrcoronahor=hoverrcorona[:,ihor]
    hoverrcorona2=hoverrcorona[:,iofr(2)]
    hoverrcorona5=hoverrcorona[:,iofr(5)]
    hoverrcorona10=hoverrcorona[:,iofr(10)]
    hoverrcorona20=hoverrcorona[:,iofr(20)]
    if modelname=="blandford3d_new":
        # so really at r=30 not 100
        hoverrcorona100=hoverrcorona[:,iofr(30)]
    else:
        hoverrcorona100=hoverrcorona[:,iofr(100)]
    #
    #
    hoverrcoronahor_t0 = hoverrcoronahor[0]
    hoverrcorona2_t0 = hoverrcorona2[0]
    hoverrcorona5_t0 = hoverrcorona5[0]
    hoverrcorona10_t0 = hoverrcorona10[0]
    hoverrcorona20_t0 = hoverrcorona20[0]
    hoverrcorona100_t0 = hoverrcorona100[0]
    #
    #
    hoverr_jethor=hoverr_jet[:,ihor]
    hoverr_jet2=hoverr_jet[:,iofr(2)]
    hoverr_jet5=hoverr_jet[:,iofr(5)]
    hoverr_jet10=hoverr_jet[:,iofr(10)]
    hoverr_jet20=hoverr_jet[:,iofr(20)]
    if modelname=="blandford3d_new":
        # so really at r=30 not 100
        hoverr_jet100=hoverr_jet[:,iofr(30)]
    else:
        hoverr_jet100=hoverr_jet[:,iofr(100)]
    #
    hoverr_jethor_t0 = hoverr_jethor[0]
    hoverr_jet2_t0 = hoverr_jet2[0]
    hoverr_jet5_t0 = hoverr_jet5[0]
    hoverr_jet10_t0 = hoverr_jet10[0]
    hoverr_jet20_t0 = hoverr_jet20[0]
    hoverr_jet100_t0 = hoverr_jet100[0]
    #
    #
    betamin_t0=betamin[0,0]
    betaavg_t0=betaavg[0,0]
    betaratofavg_t0=betaratofavg[0,0]
    betaratofmax_t0=betaratofmax[0,0]
    print("betamin_t0=%g ,betaavg_t0=%g , betaratofavg_t0=%g , betaratofmax_t0=%g" % (betamin_t0, betaavg_t0, betaratofavg_t0, betaratofmax_t0) ) ; sys.stdout.flush()
    #
    if dotavg:
        hoverrhor_avg = timeavg(hoverrhor,ts,fti,ftf)
        hoverr2_avg = timeavg(hoverr2,ts,fti,ftf)
        hoverr5_avg = timeavg(hoverr5,ts,fti,ftf)
        hoverr10_avg = timeavg(hoverr10,ts,fti,ftf)
        hoverr12_avg = timeavg(hoverr12,ts,fti,ftf)
        hoverr20_avg = timeavg(hoverr20,ts,fti,ftf)
        hoverr100_avg = timeavg(hoverr100,ts,fti,ftf)

        print("hoverr100_avg=%g %d %d" % (hoverr100_avg,fti,ftf)) ; sys.stdout.flush()
        #
        # hoverr10 is function of time.  Unsure what time to choose.
        # ts: carray of times of data
        # fti: start avg time
        # ftf: end avg time
        # use end time by choosing -1 that wraps
        if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
            hoverri=hoverr10_avg
            hoverro=hoverr12_avg
        else:
            hoverri=hoverr20_avg
            hoverro=hoverr100_avg            
        #
        hoverrcoronahor_avg = timeavg(hoverrcoronahor,ts,fti,ftf)
        hoverrcorona2_avg = timeavg(hoverrcorona2,ts,fti,ftf)
        hoverrcorona5_avg = timeavg(hoverrcorona5,ts,fti,ftf)
        hoverrcorona10_avg = timeavg(hoverrcorona10,ts,fti,ftf)
        hoverrcorona20_avg = timeavg(hoverrcorona20,ts,fti,ftf)
        hoverrcorona100_avg = timeavg(hoverrcorona100,ts,fti,ftf)
        #
        hoverr_jethor_avg = timeavg(hoverr_jethor,ts,fti,ftf)
        hoverr_jet2_avg = timeavg(hoverr_jet2,ts,fti,ftf)
        hoverr_jet5_avg = timeavg(hoverr_jet5,ts,fti,ftf)
        hoverr_jet10_avg = timeavg(hoverr_jet10,ts,fti,ftf)
        hoverr_jet20_avg = timeavg(hoverr_jet20,ts,fti,ftf)
        hoverr_jet100_avg = timeavg(hoverr_jet100,ts,fti,ftf)
        if(iti>fti):
            #
            hoverrhor2_avg = timeavg(hoverrhor,ts,iti,itf)
            hoverr22_avg = timeavg(hoverr2,ts,iti,itf)
            hoverr52_avg = timeavg(hoverr5,ts,iti,itf)
            hoverr102_avg = timeavg(hoverr10,ts,iti,itf)
            hoverr202_avg = timeavg(hoverr20,ts,iti,itf)
            hoverr1002_avg = timeavg(hoverr100,ts,iti,itf)
            #
            hoverrcoronahor2_avg = timeavg(hoverrcoronahor,ts,iti,itf)
            hoverrcorona22_avg = timeavg(hoverrcorona2,ts,iti,itf)
            hoverrcorona52_avg = timeavg(hoverrcorona5,ts,iti,itf)
            hoverrcorona102_avg = timeavg(hoverrcorona10,ts,iti,itf)
            hoverrcorona202_avg = timeavg(hoverrcorona20,ts,iti,itf)
            hoverrcorona1002_avg = timeavg(hoverrcorona100,ts,iti,itf)
            #
            hoverr_jethor2_avg = timeavg(hoverr_jethor,ts,iti,itf)
            hoverr_jet22_avg = timeavg(hoverr_jet2,ts,iti,itf)
            hoverr_jet52_avg = timeavg(hoverr_jet5,ts,iti,itf)
            hoverr_jet102_avg = timeavg(hoverr_jet10,ts,iti,itf)
            hoverr_jet202_avg = timeavg(hoverr_jet20,ts,iti,itf)
            hoverr_jet1002_avg = timeavg(hoverr_jet100,ts,iti,itf)
            #
            #
    #################################
    # END compute h/r stuff
    #################################
    #
    #
    #
    #
    #################################
    # BEGIN determine iin and iout
    #################################
    print("determine iin iout" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    for rieiter in np.arange(0,2):
        # r\sim risco is beyond ISCO in all models where GR doesn't matter much
        rrangestart=12.0
        risco=Risco(a)
        iin=iofr(risco)
        iinalt=iofr(rrangestart)
        if iin<iinalt:
            iin=iinalt
        #
        # determine iout0 through a bit of iteration
        alphatest=0.05
        # back off 6 cells from stagnation surface (i.e. things are certainly not in eq at stag, and see (e.g. sasha99) that not power-law beyond 1-2 viscous radii
        iout0=istagreport-6
        iout=iout0
        #
        for iiter in np.arange(0,5):
            #
            #
            if iin+2>=iout:
                iout=iin+3
            # limit to inflow equilibrium region
            #hortest=hoverro
            # use time-averaged H/R and averaged over iin:iout in radius
            hortest=np.average(timeavg_vstvsr(hoverr[:,iin:iout],ts,fti,ftf))
            print("iin=%d iout=%d : iiter=%d hortest=%g" % (iin,iout,iiter,hortest))
            # use final time
            timetest=ts[-1]
            #
            if rieiter==0:
                # for wind
                timetest*=(1.0)
            elif rieiter==1:
                # for disk
                timetest*=(0.5)
            #
            rie=(alphatest*hortest**2.0*timetest)**(2.0/3.0)
            if rie>0.95*Rout:
                rie=0.95*Rout
            if rie<max(risco,3):
               rie=max(risco,3)
            print("rie=%g" % (rie)) ; sys.stdout.flush()
            iie=iofr(rie)
            # update iout
            iout=iie
            #
            #
            # not too close to stagnation
            if iout>iout0:
                print("inside loop: Changed iout=%d to iout0=%d" % (iout,iout0)) ; sys.stdout.flush()
                iout=iout0
            #
            if iout>nx-1:
                print("inside loop: Changed iout=%d to nx-1=%d" % (iout,nx-1)) ; sys.stdout.flush()
                iout=nx-1
            #
            if iout<=iin:
                # only happens with runlocaldipole3dfiducial
                print("inside loop: Changed iin=%d to iofr(6.0)=%d" % (iin,iofr(6.0))) ; sys.stdout.flush()
                print("inside loop: Changed iout=%d to iofr(12.0)=%d" % (iout,iofr(12.0))) ; sys.stdout.flush()
                iin=iofr(6.0)
                iout=iofr(12.0)
            #
            if iin+2>=iout:
                iout=iin+3
            #
            # get fit so can extract average value over interesting radial range
            print("alphamag fits: iin=%d iout=%d" % (iin,iout))
            alphamag1_vsr_avg=np.average(np.fabs(alphamag1_vsr[iin:iout]))
            alphamag2_vsr_avg=np.average(np.fabs(alphamag2_vsr[iin:iout]))
            alphamag3_vsr_avg=np.average(np.fabs(alphamag3_vsr[iin:iout]))
            #
            # fabs in case small like early times or when testing script
            alphatest=np.fabs(alphamag2_vsr_avg)
            #
            print("rieiter=%d iiter=%d : iin=%d rie=%g iie=%d iout=%d alphatest=%g" % (rieiter,iiter,iin,rie,iie,iout,alphatest)) ; sys.stdout.flush()
        #
        # radius of iin and iout
        rfitin0=r[iin,0,0]
        if np.fabs(rfitin0-rrangestart)<1:
            rfitin0=rrangestart
            iin=iofr(rfitin0)
        #
        # GODMARK: can't limit this model yet
        if modelname!="runlocaldipole3dfiducial":
            if iout>iout0:
                print("Changed iout=%d to iout0=%d" % (iout,iout0)) ; sys.stdout.flush()
                iout=iout0
        #
        rfitout0=r[iout,0,0]
        #
        if rieiter==0:
            # wind
            iin1=iin
            iout1=iout
            rfitin1=rfitin0
            rfitout1=rfitout0
        if rieiter==1:
            # disk
            iin2=iin
            iout2=iout
            rfitin2=rfitin0
            rfitout2=rfitout0
        print("rieiter=%d iin=%d rfitin=%g iout=%d rfitout=%g" % (rieiter,iin,rfitin0,iout,rfitout0)) ; sys.stdout.flush()
    #
    print("iin1=%d rfitin1=%g iout1=%d rfitout1=%g" % (iin1,rfitin1,iout1,rfitout1)) ; sys.stdout.flush()
    print("iin2=%d rfitin2=%g iout2=%d rfitout2=%g" % (iin2,rfitin2,iout2,rfitout2)) ; sys.stdout.flush()
    #
    #################################
    # BEGIN determine true iin and iout
    #################################
    print("determine true iin iout" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    # based upon integration of -v_r:
    globalbadfit=0
    for rieiter in np.arange(0,4):
        # r\sim risco is beyond ISCO in all models where GR doesn't matter much
        rrangestart=12.0 # 10 still too close and smooth profile is not yet power-law
        risco=Risco(a)
        iin=iofr(risco)
        iinalt=iofr(rrangestart)
        if iin<iinalt:
            iin=iinalt
        #
        # (maybe) step back a bit
        iout=istagfromvus1rhosqdcden-0
        print("starting stag version of iout=%d which is rout=%g" % (iout,rstagfromvus1rhosqdcden))
        #
        # check if iout is good, or else force iin and iout result
        if iout<iin:
            iin=iofr(12.0)
            iout=iofr(16.0)
            globalbadfit=1
        else:
            globalbadfit=0
            # good iin and iout, so integrate out in 
            drvsr=dxdxp[1,1][:,ny/2,0]*_dx1
            print("shapes")
            print(drvsr.shape)
            print(vus1rhosqdcden_vsr.shape)
            dtgrand=-drvsr[iin:iout]/vus1rhosqdcden_vsr[iin:iout]
            Tcum = dtgrand.cumsum()
            # number of inflow time scales to wait for at a given radius (as if velocity was numinflowtimes slower)
            if rieiter==0:
                # for wind and other things (do 1 times as well)
                numinflowtimes=3.0
                #
                #Tcumcut=ts[-1]
                # most conservative using initial time for averaging period
                Tcumcut=fti
            elif rieiter==1:
                # for disk  part
                numinflowtimes=3.0
                #
                #Tcumcut=ts[-1]
                # most conservative using initial time for averaging period
                Tcumcut=fti
            elif rieiter==2:
                # just for computing 1 inflow time
                numinflowtimes=1.0
                # non-conservative using final time for averaging
                Tcumcut=ftf
            elif rieiter==3:
                # just for computing 1 inflow time
                numinflowtimes=1.0
                # conservative using initial time for averaging
                Tcumcut=fti
            #
            iouttestlist=ti[iin:iout,0,0][Tcum*numinflowtimes-Tcumcut>0]
            if len(iouttestlist)>0:
                iout=iouttestlist[0]
                print("new iout=%d" % (iout))
            else:
                print("Couldn't find new iout, using largest iout given by istag such that iout=%d" % (iout))
        #
        # avoid degenerate condition using 2 cells for fitting purposes
        if iin+2>=iout:
            iout=iin+3
        #
        # RADIUS AND I CORRECTIONS
        rfitin0=r[iin,0,0]
        iin=iofr(rfitin0)
        #
        # fix-up grid-level error in starting position so table not complicated looking
        if(np.fabs(rrangestart-rfitin0)<1.0):
            rfitin0=rrangestart
            iin=iofr(rfitin0)
        #
        rfitout0=r[iout,0,0]
        iout=iofr(rfitout0)
        #
        if rieiter<=1:
            # limit fit to out to 100 (where pressure maximum is in thickdisk models and always begins to contaminate fits)
            # even beyond 30 things oscillate for some models (e.g. thickdisk3 and thickdiskhr3)
            rfitout0=min(30.0,rfitout0)
            iout=iofr(rfitout0)
        #
        # avoid i->r rounding error
        if np.fabs(16.0-rfitout0)<1E-3:
            rfitout0=16.0
        #
        if rieiter==0:
            iin1=iin
            iout1=iout
            rfitin1=rfitin0
            rfitout1=rfitout0
        if rieiter==1:
            iin2=iin
            iout2=iout
            rfitin2=rfitin0
            rfitout2=rfitout0
        if rieiter==2:
            iin6=iin
            iout6=iout
            rfitin6=rfitin0
            rfitout6=rfitout0
        if rieiter==3:
            iin7=iin
            iout7=iout
            rfitin7=rfitin0
            rfitout7=rfitout0
        #
        #
        #
        print("true rieiter=%d iin=%d rfitin=%g iout=%d rfitout=%g" % (rieiter,iin,rfitin0,iout,rfitout0)) ; sys.stdout.flush()
    #
    print("true iin1=%d rfitin1=%g iout1=%d rfitout1=%g" % (iin1,rfitin1,iout1,rfitout1)) ; sys.stdout.flush()
    print("true iin2=%d rfitin2=%g iout2=%d rfitout2=%g" % (iin2,rfitin2,iout2,rfitout2)) ; sys.stdout.flush()
    print("true iin6=%d rfitin6=%g iout6=%d rfitout6=%g" % (iin6,rfitin6,iout6,rfitout6)) ; sys.stdout.flush()
    print("true iin7=%d rfitin7=%g iout7=%d rfitout7=%g" % (iin7,rfitin7,iout7,rfitout7)) ; sys.stdout.flush()
    #
    # detect whether should even attempt fit for power-law or not
    if rfitout1<14.0:
        globalbadfit=1
    else:
        globalbadfit=0        
    #
    # override to see some result over short span
    if modelname=="runlocaldipole3dfiducial":
        globalbadfit=0
    #
    # for Mdotin-MdotBH and other fits -- 20 a bit too soon for good fits for letaw and letamw and eta's a tad.
    rfitin3=20.0
    iin3=iofr(rfitin3)
    iout3=iout7 # try to use normal single inflow time at *start* of averaging period
    rfitout3=r[iout3,ny/2,0]
    # limit outer wind to under 100
    rfitout3=max(40.0,min(100.0,rfitout3))
    iout3=iofr(rfitout3)
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        rfitin3=6.0
        iin3=iofr(rfitin3)
        iout3=iout7 # try to use normal single inflow time at *start* of averaging period
        rfitout3=r[iout3,ny/2,0]
        # limit outer wind to under 100
        rfitout3=max(15.0,min(100.0,rfitout3))
        iout3=iofr(rfitout3)
    #
    #
    # for Mdotmw
    rfitin4=rfitin3
    iin4=iin3
    rfitout4=rfitout3
    iout4=iout3
    #
    # for Mdotw (should be same as #3) for consistent power-law fits
    rfitin5=rfitin3
    iin5=iin3
    rfitout5=rfitout3
    iout5=iout3
    #
    print("true iin3=%d rfitin3=%g iout3=%d rfitout3=%g" % (iin3,rfitin3,iout3,rfitout3)) ; sys.stdout.flush()
    print("true iin4=%d rfitin4=%g iout4=%d rfitout4=%g" % (iin4,rfitin4,iout4,rfitout4)) ; sys.stdout.flush()
    print("true iin5=%d rfitin5=%g iout5=%d rfitout5=%g" % (iin5,rfitin5,iout5,rfitout5)) ; sys.stdout.flush()
    #
    #
    #
    # just set as fixed so scaling and comparisons more obvious.  rjetout=50 should be good enough as approximately viscous time
    # these need to be the same for division by mdot's to be consistent to get consistent etawinds
    rdiskin=rjetin
    rdiskout=rjetout
    # set rdiskin to be either 10 or no smaller than where iin1 is set
    #rdiskin=max(rrangestart,r[iin1,0,0])
    idiskin=iofr(rdiskin)
    # set rdiskout to be either 100 or no larger than inflow equilibrium range
    #rdiskout=min(rjetout,r[iout,0,0])
    #rdiskout=r[iout,0,0]
    idiskout=iofr(rdiskout)
    print("idiskin=%d rdiskin=%g idiskout=%d rdiskout=%g" % (idiskin,rdiskin,idiskout,rdiskout)) ; sys.stdout.flush()
    #
    #################################
    # END determine iin and iout
    #################################
    #
    #################################
    # BEGIN compute aspect ratio grid stuff
    #################################
    #
    #
    print("A stuff" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    # get time-averaged hoverr vs. r so can use that for various calculations
    hoverr_vsr=timeavg(hoverr,ts,fti,ftf)
    hoverrvsr3d=np.zeros((nx,ny,nz),dtype=h.dtype)
    for jj in np.arange(0,ny):
        for kk in np.arange(0,nz):
            hoverrvsr3d[:,jj,kk] = hoverr_vsr[:]
    #
    #drnormvsr,dHnormvsr,dPnormvsr=gridcalc(hoverr10[-1])
    # run.liker2butbeta40 has issues with hoverr10[-1]
    #drnormvsr,dHnormvsr,dPnormvsr=gridcalc(hoverr10_avg)
    # SUPERNOTEMARK: gridcalc() below uses 2D or 3D grid data not qty data
    #drvsr,dHvsr,dPvsr,drnormvsr,dHnormvsr,dPnormvsr=gridcalc(hoverrconst=hoverro)
    # makes no sense to use hoverro for all radii.  Use hoverr_vsr instead.
    drvsr,dHvsr,dPvsr,drnormvsr,dHnormvsr,dPnormvsr=gridcalc(hoverr=hoverrvsr3d)
    #
    fgrid = open('datavsrgrid.txt', 'w')
    for ii in np.arange(0,nx):
        fgrid.write("%d %g  %g %g %g\n" % (ii,r[ii,ny/2,0],drnormvsr[ii],dHnormvsr[ii],dPnormvsr[ii]))
    fgrid.close()
    #
    drnormvsrhor=drnormvsr[ihor]
    dHnormvsrhor=dHnormvsr[ihor]
    dPnormvsrhor=dPnormvsr[ihor]
    drnormvsr10=drnormvsr[iofr(10)]
    dHnormvsr10=dHnormvsr[iofr(10)]
    dPnormvsr10=dPnormvsr[iofr(10)]
    drnormvsr20=drnormvsr[iofr(20)]
    dHnormvsr20=dHnormvsr[iofr(20)]
    dPnormvsr20=dPnormvsr[iofr(20)]
    if modelname=="blandford3d_new":
        # so really at r=30 not 100
        drnormvsr100=drnormvsr[iofr(30)]
        dHnormvsr100=dHnormvsr[iofr(30)]
        dPnormvsr100=dPnormvsr[iofr(30)]
    else:
        drnormvsr100=drnormvsr[iofr(100)]
        dHnormvsr100=dHnormvsr[iofr(100)]
        dPnormvsr100=dPnormvsr[iofr(100)]
    #
    #
    nzreal=nz
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        drnormh=drnormvsrhor
        dHnormh=dHnormvsrhor
        dPnormh=dPnormvsrhor
        drnormi=drnormvsr10
        dHnormi=dHnormvsr10
        dPnormi=dPnormvsr10
        drnormo=drnormvsr20
        dHnormo=dHnormvsr20
        dPnormo=dPnormvsr20
        #
    else:
        drnormh=drnormvsrhor
        dHnormh=dHnormvsrhor
        dPnormh=dPnormvsrhor
        drnormi=drnormvsr20
        dHnormi=dHnormvsr20
        dPnormi=dPnormvsr20
        drnormo=drnormvsr100
        dHnormo=dHnormvsr100
        dPnormo=dPnormvsr100
        #
        # only sasha99 model (at late times!) should do the below
        if modelname=="sasha99":
            dPnormh/=2
            dPnormi/=2
            dPnormo/=2
            nzreal=nz*2
        #
    #################################
    # END compute A stuff
    #################################
    #################################
    # BEGIN compute qMRI stuff
    #################################
    print("qMRI stuff" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #############################################
    # get radius when Q2mri=1 first unless Q2mri>1 at r=rh
    #
    # original Q1,Q2 calculations used Omega_{Keplerian} while should be Omega, so fix the vs. radius quantities at least (so only have to re-"plot", not recompute everything)
    # Q1\propto lambdamri\propto 1/Omega
    # Q2\propto 1/lambdamri and lambdamri\propto 1/\Omega so Q2\propto Omega
    OMEGAFIX=1
    #
    R_vsr=r[:,ny/2,0]*np.sin(h[:,ny/2,0])
    vuas3rhosqdcdenkep_vsr=R_vsr/(a + R_vsr**(1.5))
    #
    # create kep v_\phi for every time
    vuas3rhosqdcdenkep=np.copy(vuas3rhosqdcden)*0.0
    for ttii in np.arange(0,len(ts)):
            vuas3rhosqdcdenkep[ttii,:] = vuas3rhosqdcdenkep_vsr[:]
    #
    # GODMARK: Should really use (|b|\rho_0)^{1/2} weighting for qmridisk and iq2mridisk, but if anything more sub-Keplerian than dcden version so if anyting MRI suppressed over large radial range.
    if OMEGAFIX==1:
        omegafixrat=vuas3rhosqdcden/vuas3rhosqdcdenkep
    else:
        omegafixrat=1.0 + 0*vuas3rhosqdcden
    #
    # fix
    global qmridisk,iq2mridisk,qmridiskweak,iq2mridiskweak
    qmridisk=qmridisk/omegafixrat
    iq2mridisk=iq2mridisk/omegafixrat
    qmridiskweak=qmridiskweak/omegafixrat
    iq2mridiskweak=iq2mridiskweak/omegafixrat
    #
    # now can use these as usually do ....
    #
    ##########################
    iq2mridisk_vsr=timeavg(iq2mridisk,ts,fti,ftf)
    q2mridisk_avg=hoverr_vsr/iq2mridisk_vsr
    print("q2mridisk_avg") ; sys.stdout.flush()
    print(q2mridisk_avg) ; sys.stdout.flush()
    print("r") ; sys.stdout.flush()
    print(r[:,ny/2,0]) ; sys.stdout.flush()
    #
    iq2mridiskweak_vsr=timeavg(iq2mridiskweak,ts,fti,ftf)
    q2mridiskweak_avg=hoverr_vsr/iq2mridiskweak_vsr
    print("q2mridiskweak_avg") ; sys.stdout.flush()
    print(q2mridiskweak_avg) ; sys.stdout.flush()
    print("r") ; sys.stdout.flush()
    print(r[:,ny/2,0]) ; sys.stdout.flush()
    ####################
    #
    #rq2mri1cut=min(5.0,Risco(a)) # some allowance for smaller than isco, but doesn't help thickdiskrr2 that's still not hitting q2=1 near BH.
    rq2mri1cut=4.0
    iq2mri1cut=iofr(rq2mri1cut)
    rq2mri1cut=r[iq2mri1cut,ny/2,0] # to get consistency for checks to work
    print("iq2mri1cut=%d" % (iq2mri1cut)) ; sys.stdout.flush()
    # skip i<iq2mri1cut due to boundary condition influence modifying Q2 to be >1/2 just in a few cells
    indicesiq2mri1=ti[iq2mri1cut:nx,0,0][q2mridisk_avg[iq2mri1cut:nx]>=0.5] # use 0.5 because 1.0 too close to possibly allowing MRI
    print("indicesiq2mri1") ; sys.stdout.flush()
    print(indicesiq2mri1) ; sys.stdout.flush()
    iq2mri1=indicesiq2mri1[0] # first instance vs. radius
    print("iq2mri1") ; sys.stdout.flush()
    print(iq2mri1) ; sys.stdout.flush()
    rq2mri1=r[iq2mri1,ny/2,0] # radius
    print("rq2mri1") ; sys.stdout.flush()
    print(rq2mri1) ; sys.stdout.flush()
    #
    #rq2mri2cut=min(5.0,Risco(a)) # some allowance for smaller than isco, but doesn't help thickdiskrr2 that's still not hitting q2=1 near BH.
    rq2mri2cut=4.0
    iq2mri2cut=iofr(rq2mri2cut)
    rq2mri2cut=r[iq2mri2cut,ny/2,0] # to get consistency for checks to work
    print("iq2mri2cut=%d" % (iq2mri2cut)) ; sys.stdout.flush()
    # skip i<iq2mri2cut due to boundary condition influence modifying Q2 to be >1/2 just in a few cells
    indicesiq2mri2=ti[iq2mri2cut:nx,0,0][q2mridiskweak_avg[iq2mri2cut:nx]>=0.5] # use 0.5 because 1.0 too close to possibly allowing MRI
    print("indicesiq2mri2") ; sys.stdout.flush()
    print(indicesiq2mri2) ; sys.stdout.flush()
    iq2mri2=indicesiq2mri2[0] # first instance vs. radius
    print("iq2mri2") ; sys.stdout.flush()
    print(iq2mri2) ; sys.stdout.flush()
    rq2mri2=r[iq2mri2,ny/2,0] # radius
    print("rq2mri2") ; sys.stdout.flush()
    print(rq2mri2) ; sys.stdout.flush()
    #
    ##############################################
    #
    ##############################################
    # dc: over disk+corona but bsq/rho<1 only: Doesn't work -- no r_m present!
    # dcden:  over disk only (high density disk): Doesn't work -- no r_m present!
    # use full flow that includes jet : required to get r_m -- makes sense since jet is what pushes down on disk!
    # look at 1/\beta since more stable since b=0 is more common than ug=0
    #ibetarm1=(bsqrhosq/2.0)/(rhosrhosq*(vus1rhosq**2) + ugsrhosq*(gam-1.0))
    pbrm1=(bsqrhosq/2.0)
    pgrm1=ugsrhosq*(gam-1.0)
    rhovsqrm1=(rhosrhosq+pgrm1+ugsrhosq)*(uu0rhosq*vus1rhosq)**2
    ibetarm1=pbrm1/(rhovsqrm1 + pgrm1)
    ibetarm1_avg = timeavg_vstvsr(ibetarm1,ts,fti,ftf)
    print("ibetarm1_avg") ; sys.stdout.flush()
    print(ibetarm1_avg) ; sys.stdout.flush()
    print("r") ; sys.stdout.flush()
    print(r[:,ny/2,0]) ; sys.stdout.flush()
    #
    if modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2":
        rm1cut=20.0
    else:
        rm1cut=4.0
    #
    irm1cut=iofr(rm1cut)
    rm1cut=r[irm1cut,ny/2,0] # to get consistency for checks to work
    print("irm1cut=%d" % (irm1cut)) ; sys.stdout.flush()
    indicesirm1=ti[irm1cut:nx,0,0][ibetarm1_avg[irm1cut:nx]<=1.0] # 1/\betarm=1 is where \betarm=1
    print("indicesirm1") ; sys.stdout.flush()
    print(indicesirm1) ; sys.stdout.flush()
    irm1=indicesirm1[0] # first instance vs. radius
    print("irm1") ; sys.stdout.flush()
    print(irm1) ; sys.stdout.flush()
    rm1=r[irm1,ny/2,0] # radius
    print("rm1") ; sys.stdout.flush()
    print(rm1) ; sys.stdout.flush()
    #
    ###############
    # get rm1 vs. time
    rm1vstcut=2.1
    irm1vstcut=iofr(rm1vstcut)
    rm1vstcut=r[irm1vstcut,ny/2,0] # to get consistency for checks to work
    rm1vst=ibetarm1[:,0]*0.0
    for ttii in np.arange(0,len(ts)):
        indicesirm1ttii=ti[irm1vstcut:nx,0,0][ibetarm1[ttii,irm1vstcut:nx]<=1.0] # 1/\betarm=1 is where \betarm=1
        if len(indicesirm1ttii)>0:
            irm1ttii=indicesirm1ttii[0] # first instance vs. radius
            rm1vst[ttii]=r[irm1ttii,ny/2,0] # radius
        else:
            irm1ttii=nx-1 # never got small ibeta or large beta
            rm1vst[ttii]=r[irm1ttii,ny/2,0] # radius
    #
    print("rm1vst") ; sys.stdout.flush()
    print(rm1vst) ; sys.stdout.flush()
    frm1 = open('datavsrrm1.txt', 'w')
    frm1.write("#%s %s %s \n" % ("tici","ts","rm1" ) )
    for ttii in np.arange(0,len(ts)):
        frm1.write("%d %g %g\n" % (ttii,ts[ttii],rm1vst[ttii] ) )
        #
    frm1.close()
    #
    #
    #####################
    ibetarm2=(bsqrhosqdc/2.0)/(rhosrhosqdc*(uu0rhosqdc*vus1rhosqdc)**2 + ugsrhosqdc*(gam-1.0))
    ibetarm2_avg = timeavg_vstvsr(ibetarm2,ts,fti,ftf)
    print("ibetarm2_avg") ; sys.stdout.flush()
    print(ibetarm2_avg) ; sys.stdout.flush()
    print("r") ; sys.stdout.flush()
    print(r[:,ny/2,0]) ; sys.stdout.flush()
    #
    rm2cut=4.0
    irm2cut=iofr(rm2cut)
    print("irm2cut=%d" % (irm2cut)) ; sys.stdout.flush()
    indicesirm2=ti[irm2cut:nx,0,0][ibetarm2_avg[irm2cut:nx]<=1.0] # 1/\betarm=1 is where \betarm=1
    print("indicesirm2") ; sys.stdout.flush()
    print(indicesirm2) ; sys.stdout.flush()
    irm2=indicesirm2[0] # first instance vs. radius
    print("irm2") ; sys.stdout.flush()
    print(irm2) ; sys.stdout.flush()
    rm2=r[irm2,ny/2,0] # radius
    print("rm2") ; sys.stdout.flush()
    print(rm2) ; sys.stdout.flush()
    # 
    #####################
    ibetarm3=(bsqrhosqdcden/2.0)/(rhosrhosqdcden*(uu0rhosqdcden*vus1rhosqdcden)**2 + ugsrhosqdcden*(gam-1.0))
    #ibetarm3=(bsqrhosqdcden/2.0)/(rhosrhosqdcden*(vus1rhosqdcden**2) + ugsrhosqdcden*(gam-1.0))
    ibetarm3_avg = timeavg_vstvsr(ibetarm3,ts,fti,ftf)
    print("ibetarm3_avg") ; sys.stdout.flush()
    print(ibetarm3_avg) ; sys.stdout.flush()
    print("r") ; sys.stdout.flush()
    print(r[:,ny/2,0]) ; sys.stdout.flush()
    #
    rm3cut=4.0
    irm3cut=iofr(rm3cut)
    print("irm3cut=%d" % (irm3cut)) ; sys.stdout.flush()
    indicesirm3=ti[irm3cut:nx,0,0][ibetarm3_avg[irm3cut:nx]<=1.0] # 1/\betarm=1 is where \betarm=1
    print("indicesirm3") ; sys.stdout.flush()
    print(indicesirm3) ; sys.stdout.flush()
    irm3=indicesirm3[0] # first instance vs. radius
    print("irm3") ; sys.stdout.flush()
    print(irm3) ; sys.stdout.flush()
    rm3=r[irm3,ny/2,0] # radius
    print("rm3") ; sys.stdout.flush()
    print(rm3) ; sys.stdout.flush()
    # 
    ############################################### t=0 qmri's
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        qmrir1=10.0
        qmrir2=15.0
        qmrir3=20.0
    else:
        qmrir1=20.0
        qmrir2=50.0
        qmrir3=100.0
    #
    spreadrat=0.2
    qrin=qmrir1*(1.0-spreadrat)
    qrout=qmrir1*(1.0+spreadrat)
    iqrin20=iofr(qrin)
    iqrout20=iofr(qrout)
    print("qrin=%g iqrin20=%d qrout=%g iqrout20=%d" % (qrin,iqrin20,qrout,iqrout20)) ; sys.stdout.flush()
    qcondition=(r[:,0,0]>qrin)
    qcondition=qcondition*(r[:,0,0]<qrout)
    qcondition2=qcondition
    #
    qmridisk20=np.copy(qmridisk)
    qmridisk20[:,qcondition2==False]=0
    qmridisk20=((qmridisk20[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    iq2mridisk20=np.copy(iq2mridisk)
    iq2mridisk20[:,qcondition2==False]=0
    iq2mridisk20=((iq2mridisk20[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    #
    #wtf1=np.sum(iq2mridisk20[:,qcondition2]*normmridisk[:,qcondition2],axis=1)
    #wtf2=np.sum(iq2mridisk20[:,qcondition2],axis=1)
    #wtf3=np.sum(normmridisk[:,qcondition2],axis=1)
    #wtf4=np.sum(qcondition)
    #print("god=%g %g %g %g" % ( wtf1[0],wtf2[0],wtf3[0],wtf4 ) )
    #print("god1=%g %g %g %g" % ( wtf1[1],wtf2[1],wtf3[1],wtf4 ) )
    #print("god2=%g %g %g %g" % ( wtf1[2],wtf2[2],wtf3[2],wtf4 ) )
    #
    qmridiskweak20=np.copy(qmridiskweak)
    qmridiskweak20[:,qcondition2==False]=0
    qmridiskweak20=((qmridiskweak20[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    iq2mridiskweak20=np.copy(iq2mridiskweak)
    iq2mridiskweak20[:,qcondition2==False]=0
    iq2mridiskweak20=((iq2mridiskweak20[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    #
    #
    qrin=qmrir2*(1.0-spreadrat)
    qrout=qmrir2*(1.0+spreadrat)
    iqrin50=iofr(qrin)
    iqrout50=iofr(qrout)
    print("qrin=%g iqrin50=%d qrout=%g iqrout50=%d" % (qrin,iqrin50,qrout,iqrout50)) ; sys.stdout.flush()
    qcondition=(r[:,0,0]>qrin)
    qcondition=qcondition*(r[:,0,0]<qrout)
    qcondition2=qcondition
    #
    qmridisk50=np.copy(qmridisk)
    qmridisk50[:,qcondition2==False]=0
    qmridisk50=((qmridisk50[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    iq2mridisk50=np.copy(iq2mridisk)
    iq2mridisk50[:,qcondition2==False]=0
    iq2mridisk50=((iq2mridisk50[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    #
    qmridiskweak50=np.copy(qmridiskweak)
    qmridiskweak50[:,qcondition2==False]=0
    qmridiskweak50=((qmridiskweak50[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    iq2mridiskweak50=np.copy(iq2mridiskweak)
    iq2mridiskweak50[:,qcondition2==False]=0
    iq2mridiskweak50=((iq2mridiskweak50[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    #
    #
    qrin=qmrir3*(1.0-spreadrat)
    qrout=qmrir3*(1.0+spreadrat)
    iqrin100=iofr(qrin)
    iqrout100=iofr(qrout)
    print("qrin=%g iqrin100=%d qrout=%g iqrout100=%d" % (qrin,iqrin100,qrout,iqrout100)) ; sys.stdout.flush()
    qcondition=(r[:,0,0]>qrin)
    qcondition=qcondition*(r[:,0,0]<qrout)
    qcondition2=qcondition
    #
    qmridisk100=np.copy(qmridisk)
    qmridisk100[:,qcondition2==False]=0
    qmridisk100=((qmridisk100[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    iq2mridisk100=np.copy(iq2mridisk)
    iq2mridisk100[:,qcondition2==False]=0
    iq2mridisk100=((iq2mridisk100[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    #
    #
    qmridiskweak100=np.copy(qmridiskweak)
    qmridiskweak100[:,qcondition2==False]=0
    qmridiskweak100=((qmridiskweak100[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    iq2mridiskweak100=np.copy(iq2mridiskweak)
    iq2mridiskweak100[:,qcondition2==False]=0
    iq2mridiskweak100=((iq2mridiskweak100[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    #
    #
    ################################ initial Q's
    qmridisk20_t0 = qmridisk20[0]
    qmridisk50_t0 = qmridisk50[0]
    qmridisk100_t0 = qmridisk100[0]
    print("qmridisk20_t0=%g" % (qmridisk20_t0) )
    print("qmridisk50_t0=%g" % (qmridisk50_t0) )
    print("qmridisk100_t0=%g" % (qmridisk100_t0) )
    sys.stdout.flush()
    #
    hoverr20_t0 = np.average(hoverr[0,iqrin20:iqrout20])
    hoverr50_t0 = np.average(hoverr[0,iqrin50:iqrout50])
    hoverr100_t0 = np.average(hoverr[0,iqrin100:iqrout100])
    print("hoverr20_t0=%g" % (hoverr20_t0) )
    print("hoverr50_t0=%g" % (hoverr50_t0) )
    print("hoverr100_t0=%g" % (hoverr100_t0) )
    sys.stdout.flush()
    #
    iq2mridisk20_t0 = iq2mridisk20[0]/hoverr20_t0
    iq2mridisk50_t0 = iq2mridisk50[0]/hoverr50_t0
    iq2mridisk100_t0 = iq2mridisk100[0]/hoverr100_t0
    print("iq2mridisk20_t0=%g iq2mridisk20_t0=%g" % (iq2mridisk20_t0,iq2mridisk20_t0) )
    print("iq2mridisk50_t0=%g iq2mridisk50_t0=%g" % (iq2mridisk50_t0,iq2mridisk50_t0) )
    print("iq2mridisk100_t0=%g iq2mridisk100_t0=%g" % (iq2mridisk100_t0,iq2mridisk100_t0) )
    sys.stdout.flush()
    #
    # get initial values for weak Q's
    qmridiskweak20_t0 = qmridiskweak20[0]
    qmridiskweak50_t0 = qmridiskweak50[0]
    qmridiskweak100_t0 = qmridiskweak100[0]
    print("qmridiskweak20_t0=%g qmridiskweak20_t0=%g" % (qmridiskweak20_t0,qmridiskweak20_t0) )
    print("qmridiskweak50_t0=%g qmridiskweak50_t0=%g" % (qmridiskweak50_t0,qmridiskweak50_t0) )
    print("qmridiskweak100_t0=%g qmridiskweak100_t0=%g" % (qmridiskweak100_t0,qmridiskweak100_t0) )
    sys.stdout.flush()
    #
    iq2mridiskweak20_t0 = iq2mridiskweak20[0]/hoverr20_t0
    iq2mridiskweak50_t0 = iq2mridiskweak50[0]/hoverr50_t0
    iq2mridiskweak100_t0 = iq2mridiskweak100[0]/hoverr100_t0
    print("iq2mridiskweak20_t0=%g iq2mridiskweak20_t0=%g" % (iq2mridiskweak20_t0,iq2mridiskweak20_t0) )
    print("iq2mridiskweak50_t0=%g iq2mridiskweak50_t0=%g" % (iq2mridiskweak50_t0,iq2mridiskweak50_t0) )
    print("iq2mridiskweak100_t0=%g iq2mridiskweak100_t0=%g" % (iq2mridiskweak100_t0,iq2mridiskweak100_t0) )
    sys.stdout.flush()
    #
    #
    ################################ time-average qmri's
    #
    qrin=rfitin2*(1.0-spreadrat)
    qrout=rfitin2*(1.0+spreadrat)
    iqrinrfitin2=iofr(qrin)
    iqroutrfitin2=iofr(qrout)
    qcondition=(r[:,0,0]>qrin)
    qcondition=qcondition*(r[:,0,0]<qrout)
    qcondition2=qcondition
    #
    qmridiskrfitin2=np.copy(qmridisk)
    qmridiskrfitin2[:,qcondition2==False]=0
    qmridiskrfitin2=((qmridiskrfitin2[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    iq2mridiskrfitin2=np.copy(iq2mridisk)
    iq2mridiskrfitin2[:,qcondition2==False]=0
    iq2mridiskrfitin2=((iq2mridiskrfitin2[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    #
    #wtf1=np.sum(iq2mridiskrfitin2[:,qcondition2]*normmridisk[:,qcondition2],axis=1)
    #wtf2=np.sum(iq2mridiskrfitin2[:,qcondition2],axis=1)
    #wtf3=np.sum(normmridisk[:,qcondition2],axis=1)
    #wtf4=np.sum(qcondition)
    #print("god=%g %g %g %g" % ( wtf1[0],wtf2[0],wtf3[0],wtf4 ) )
    #print("god1=%g %g %g %g" % ( wtf1[1],wtf2[1],wtf3[1],wtf4 ) )
    #print("god2=%g %g %g %g" % ( wtf1[2],wtf2[2],wtf3[2],wtf4 ) )
    #
    qmridiskweakrfitin2=np.copy(qmridiskweak)
    qmridiskweakrfitin2[:,qcondition2==False]=0
    qmridiskweakrfitin2=((qmridiskweakrfitin2[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    iq2mridiskweakrfitin2=np.copy(iq2mridiskweak)
    iq2mridiskweakrfitin2[:,qcondition2==False]=0
    iq2mridiskweakrfitin2=((iq2mridiskweakrfitin2[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    #
    #
    qrin=rfitout2*(1.0-spreadrat)
    qrout=rfitout2*(1.0+spreadrat)
    iqrinrfitout2=iofr(qrin)
    iqroutrfitout2=iofr(qrout)
    qcondition=(r[:,0,0]>qrin)
    qcondition=qcondition*(r[:,0,0]<qrout)
    qcondition2=qcondition
    #
    qmridiskrfitout2=np.copy(qmridisk)
    qmridiskrfitout2[:,qcondition2==False]=0
    qmridiskrfitout2=((qmridiskrfitout2[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    iq2mridiskrfitout2=np.copy(iq2mridisk)
    iq2mridiskrfitout2[:,qcondition2==False]=0
    iq2mridiskrfitout2=((iq2mridiskrfitout2[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    #
    qmridiskweakrfitout2=np.copy(qmridiskweak)
    qmridiskweakrfitout2[:,qcondition2==False]=0
    qmridiskweakrfitout2=((qmridiskweakrfitout2[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    iq2mridiskweakrfitout2=np.copy(iq2mridiskweak)
    iq2mridiskweakrfitout2[:,qcondition2==False]=0
    iq2mridiskweakrfitout2=((iq2mridiskweakrfitout2[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    #
    #
    qrin=rfitout6*(1.0-spreadrat)
    qrout=rfitout6*(1.0+spreadrat)
    iqrinrfitout6=iofr(qrin)
    iqroutrfitout6=iofr(qrout)
    qcondition=(r[:,0,0]>qrin)
    qcondition=qcondition*(r[:,0,0]<qrout)
    qcondition2=qcondition
    #
    qmridiskrfitout6=np.copy(qmridisk)
    qmridiskrfitout6[:,qcondition2==False]=0
    qmridiskrfitout6=((qmridiskrfitout6[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    iq2mridiskrfitout6=np.copy(iq2mridisk)
    iq2mridiskrfitout6[:,qcondition2==False]=0
    iq2mridiskrfitout6=((iq2mridiskrfitout6[:,qcondition2]*normmridisk[:,qcondition2]).sum(axis=1))/((normmridisk[:,qcondition2]).sum(axis=1))
    #
    #
    qmridiskweakrfitout6=np.copy(qmridiskweak)
    qmridiskweakrfitout6[:,qcondition2==False]=0
    qmridiskweakrfitout6=((qmridiskweakrfitout6[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    iq2mridiskweakrfitout6=np.copy(iq2mridiskweak)
    iq2mridiskweakrfitout6[:,qcondition2==False]=0
    iq2mridiskweakrfitout6=((iq2mridiskweakrfitout6[:,qcondition2]*normmridiskweak[:,qcondition2]).sum(axis=1))/((normmridiskweak[:,qcondition2]).sum(axis=1))
    #
    ################################# time-averaged Q's
    hoverrrfitin2_avg = np.average(hoverr[:,iqrinrfitin2:iqroutrfitin2])
    hoverrrfitout2_avg = np.average(hoverr[:,iqrinrfitout2:iqroutrfitout2])
    hoverrrfitout6_avg = np.average(hoverr[:,iqrinrfitout6:iqroutrfitout6])
    #
    print("hoverrrfitin2_avg=%g" % (hoverrrfitin2_avg) )
    print("hoverrrfitout2_avg=%g" % (hoverrrfitout2_avg) )
    print("hoverrrfitout6_avg=%g" % (hoverrrfitout6_avg) )
    sys.stdout.flush()
    #
    if dotavg:
        qmridiskrfitin2_avg = timeavg(qmridiskrfitin2,ts,fti,ftf)
        qmridiskrfitout2_avg = timeavg(qmridiskrfitout2,ts,fti,ftf)
        qmridiskrfitout6_avg = timeavg(qmridiskrfitout6,ts,fti,ftf)
        #
        iq2mridiskrfitin2_avg = timeavg(iq2mridiskrfitin2,ts,fti,ftf)/hoverrrfitin2_avg
        iq2mridiskrfitout2_avg = timeavg(iq2mridiskrfitout2,ts,fti,ftf)/hoverrrfitout2_avg
        iq2mridiskrfitout6_avg = timeavg(iq2mridiskrfitout6,ts,fti,ftf)/hoverrrfitout6_avg
        #
        qmridiskweakrfitin2_avg = timeavg(qmridiskweakrfitin2,ts,fti,ftf)
        qmridiskweakrfitout2_avg = timeavg(qmridiskweakrfitout2,ts,fti,ftf)
        qmridiskweakrfitout6_avg = timeavg(qmridiskweakrfitout6,ts,fti,ftf)
        #
        iq2mridiskweakrfitin2_avg = timeavg(iq2mridiskweakrfitin2,ts,fti,ftf)/hoverrrfitin2_avg
        iq2mridiskweakrfitout2_avg = timeavg(iq2mridiskweakrfitout2,ts,fti,ftf)/hoverrrfitout2_avg
        iq2mridiskweakrfitout6_avg = timeavg(iq2mridiskweakrfitout6,ts,fti,ftf)/hoverrrfitout6_avg
        #
        if(iti>fti):
            qmridiskrfitin22_avg = timeavg(qmridiskrfitin2,ts,iti,itf)
            qmridiskrfitout22_avg = timeavg(qmridiskrfitout2,ts,iti,itf)
            qmridiskrfitout62_avg = timeavg(qmridiskrfitout6,ts,iti,itf)
            #
            iq2mridiskrfitin22_avg = timeavg(iq2mridiskrfitin2,ts,iti,itf)/hoverrrfitin2_avg
            iq2mridiskrfitout22_avg = timeavg(iq2mridiskrfitout2,ts,iti,itf)/hoverrrfitout2_avg
            iq2mridiskrfitout62_avg = timeavg(iq2mridiskrfitout6,ts,iti,itf)/hoverrrfitout6_avg
            #
            qmridiskweakrfitin22_avg = timeavg(qmridiskweakrfitin2,ts,iti,itf)
            qmridiskweakrfitout22_avg = timeavg(qmridiskweakrfitout2,ts,iti,itf)
            qmridiskweakrfitout62_avg = timeavg(qmridiskweakrfitout6,ts,iti,itf)
            #
            iq2mridiskweakrfitin22_avg = timeavg(iq2mridiskweakrfitin2,ts,iti,itf)/hoverrrfitin2_avg
            iq2mridiskweakrfitout22_avg = timeavg(iq2mridiskweakrfitout2,ts,iti,itf)/hoverrrfitout2_avg
            iq2mridiskweakrfitout62_avg = timeavg(iq2mridiskweakrfitout6,ts,iti,itf)/hoverrrfitout6_avg
        #
    #
    #################################
    # END compute qMRI stuff
    #################################
    #################################
    # BEGIN PART2 of compute vsr (things that can depend upon rdiskin or rdiskout)
    #################################
    print("Part2 vsr" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    mdotwininiavg = timeavg(np.abs(mdwind[:,iofr(rdiskin)]),ts,iti,itf)
    mdotwinfinavg = timeavg(np.abs(mdwind[:,iofr(rdiskin)]),ts,fti,ftf)
    mdotwoutiniavg = timeavg(np.abs(mdwind[:,iofr(rdiskout)]),ts,iti,itf)
    mdotwoutfinavg = timeavg(np.abs(mdwind[:,iofr(rdiskout)]),ts,fti,ftf)
    #
    mdotmwininiavg = timeavg(np.abs(mdmwind[:,iofr(rjetin)]),ts,iti,itf)
    mdotmwinfinavg = timeavg(np.abs(mdmwind[:,iofr(rjetin)]),ts,fti,ftf)
    mdotmwoutiniavg = timeavg(np.abs(mdmwind[:,iofr(rjetout)]),ts,iti,itf)
    mdotmwoutfinavg = timeavg(np.abs(mdmwind[:,iofr(rjetout)]),ts,fti,ftf)
    #
    # use md10 since at large radii don't reach bsq/rho>30 too easily and still approximately accurate for floor-dominated region
    # don't use horizon values for jet or wind since very different mdot, etc. there
    # handle md10 issue inside mdjet and mdwind calculation, so keep to consistent cells chosen instead of subtracting off contributions from different masked cells in integration
    mdotjetiniavg = timeavg(np.abs(mdjet[:,iofr(rjetout)]),ts,iti,itf)
    mdotjetfinavg = timeavg(np.abs(mdjet[:,iofr(rjetout)]),ts,fti,ftf)
    #
    # handle md10 issue inside computation for mdin (i.e. avoid including bsq/rho>30)
    mdotinrdiskininiavg = timeavg(np.abs(mdin[:,iofr(rdiskin)]),ts,iti,itf)
    mdotinrdiskinfinavg = timeavg(np.abs(mdin[:,iofr(rdiskin)]),ts,fti,ftf)
    mdotinrdiskoutiniavg = timeavg(np.abs(mdin[:,iofr(rdiskout)]),ts,iti,itf)
    mdotinrdiskoutfinavg = timeavg(np.abs(mdin[:,iofr(rdiskout)]),ts,fti,ftf)
    #
    #
    #
    #################################
    # END PART2 of compute vsr (things that can depend upon rdiskin or rdiskout)
    #################################
    #
    print("Sasha stuff" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    fc=0
    if showextra:
        ofc = 1
        clr = 'r'
    else:
        ofc = 0
        clr = 'k'

    if epsFm is not None and epsFke is not None:
        FMraw    = mdtot[:,ihor]
        FM       = epsFm * mdtot[:,ihor]
        FMavg    = epsFm * timeavg(mdtot,ts,fti,ftf)[ihor]
        FMiniavg = epsFm * timeavg(mdtot,ts,iti,itf)[ihor] 
        FEraw = -edtot[:,ihor]
        FE= epsFke*(FMraw-FEraw)
    else:
        FMraw    = mdtot[:,ihor]
        FM       = mdtot[:,ihor]
        FMavg    = timeavg(mdtot,ts,fti,ftf)[ihor]
        FMiniavg = timeavg(mdtot,ts,iti,itf)[ihor] 
        FEraw = -edtot[:,ihor]
        FE= (FMraw-FEraw)
        #FMiniavg = mdotiniavg
        #FMavg = mdotfinavg
        #FM = mdtot[:,ihor]
        #FE = pjemtot[:,ihor]
    if showextra:
        lst = 'solid'
    else:
        lst = 'dashed'
    #
    #
    #
    ######################################
    # BEGIN COMPUTE JON WHICHPLOT==4
    ######################################
    print("whichplot==4" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    # mdotmwinfinavg mdotmwoutfinavg
    # mdotwinfinavg mdotwoutfinavg
    # mdotinrdiskfinniavg  mdotinrdiskoutfinavg
    #
    etabhEM = prefactor*pjemtot[:,ihor]/mdotfinavg
    etabhMAKE = prefactor*pjmaketot[:,ihor]/mdotfinavg
    etabh = etabhEM + etabhMAKE
    etajEM = prefactor*pjem_mu1[:,iofr(rjetout)]/mdotfinavg
    etajMAKE = prefactor*pjmake_mu1[:,iofr(rjetout)]/mdotfinavg
    etaj = etajEM + etajMAKE
    etajlocal = etaj*(mdotfinavg/mdotinrdiskoutfinavg)
    etamwinEM = prefactor*pjem_mumax1m[:,iofr(rjetin)]/mdotfinavg
    etamwinMAKE = prefactor*pjmake_mumax1m[:,iofr(rjetin)]/mdotfinavg
    etamwin = etamwinEM + etamwinMAKE
    etamwinlocal = etamwin*(mdotfinavg/mdotinrdiskinfinavg)
    etamwoutEM = prefactor*pjem_mumax1m[:,iofr(rjetout)]/mdotfinavg
    etamwoutMAKE = prefactor*pjmake_mumax1m[:,iofr(rjetout)]/mdotfinavg
    etamwout = etamwoutEM + etamwoutMAKE
    etamwoutlocal = etamwout*(mdotfinavg/mdotinrdiskoutfinavg)
    etawinEM = prefactor*pjem_mumax1[:,iofr(rdiskin)]/mdotfinavg
    etawinMAKE = prefactor*pjmake_mumax1[:,iofr(rdiskin)]/mdotfinavg
    etawin = etawinEM + etawinMAKE
    etawinlocal = etawin*(mdotfinavg/mdotinrdiskinfinavg)
    etawoutEM = prefactor*pjem_mumax1[:,iofr(rdiskout)]/mdotfinavg
    etawoutMAKE = prefactor*pjmake_mumax1[:,iofr(rdiskout)]/mdotfinavg
    etawout = etawoutEM + etawoutMAKE
    etawoutlocal = etawout*(mdotfinavg/mdotinrdiskoutfinavg)
    #
    etabhEM2 = prefactor*pjemtot[:,ihor]/mdotiniavg
    etabhMAKE2 = prefactor*pjmaketot[:,ihor]/mdotiniavg
    etabh2 = etabhEM2 + etabhMAKE2
    etajEM2 = prefactor*pjem_mu1[:,iofr(rjetout)]/mdotiniavg
    etajMAKE2 = prefactor*pjmake_mu1[:,iofr(rjetout)]/mdotiniavg
    etaj2 = etajEM2 + etajMAKE2
    etaj2local = etaj2*(mdotiniavg/mdotinrdiskoutiniavg)
    etamwinEM2 = prefactor*pjem_mumax1m[:,iofr(rjetin)]/mdotiniavg
    etamwinMAKE2 = prefactor*pjmake_mumax1m[:,iofr(rjetin)]/mdotiniavg
    etamwin2 = etamwinEM2 + etamwinMAKE2
    etamwin2local = etamwin2*(mdotiniavg/mdotinrdiskininiavg)
    etamwoutEM2 = prefactor*pjem_mumax1m[:,iofr(rjetout)]/mdotiniavg
    etamwoutMAKE2 = prefactor*pjmake_mumax1m[:,iofr(rjetout)]/mdotiniavg
    etamwout2 = etamwoutEM2 + etamwoutMAKE2
    etamwout2local = etamwout2*(mdotiniavg/mdotinrdiskoutiniavg)
    etawinEM2 = prefactor*pjem_mumax1[:,iofr(rdiskin)]/mdotiniavg
    etawinMAKE2 = prefactor*pjmake_mumax1[:,iofr(rdiskin)]/mdotiniavg
    etawin2 = etawinEM2 + etawinMAKE2
    etawin2local = etawin2*(mdotiniavg/mdotinrdiskininiavg)
    etawoutEM2 = prefactor*pjem_mumax1[:,iofr(rdiskout)]/mdotiniavg
    etawoutMAKE2 = prefactor*pjmake_mumax1[:,iofr(rdiskout)]/mdotiniavg
    etawout2 = etawoutEM2 + etawoutMAKE2
    etawout2local = etawout2*(mdotiniavg/mdotinrdiskoutiniavg)
    #
    # lj = angular momentum flux
    letabhEM = prefactor*ljemtot[:,ihor]/mdotfinavg
    letabhMAKE = prefactor*ljmaketot[:,ihor]/mdotfinavg
    letabh = letabhEM + letabhMAKE
    letajEM = prefactor*ljem_mu1[:,iofr(rjetout)]/mdotfinavg
    letajMAKE = prefactor*ljmake_mu1[:,iofr(rjetout)]/mdotfinavg
    letaj = letajEM + letajMAKE
    letajlocal = letaj*(mdotfinavg/mdotinrdiskoutfinavg)
    letamwinEM = prefactor*ljem_mumax1m[:,iofr(rjetin)]/mdotfinavg
    letamwinMAKE = prefactor*ljmake_mumax1m[:,iofr(rjetin)]/mdotfinavg
    letamwin = letamwinEM + letamwinMAKE
    letamwinlocal = letamwin*(mdotfinavg/mdotinrdiskinfinavg)
    letamwoutEM = prefactor*ljem_mumax1m[:,iofr(rjetout)]/mdotfinavg
    letamwoutMAKE = prefactor*ljmake_mumax1m[:,iofr(rjetout)]/mdotfinavg
    letamwout = letamwoutEM + letamwoutMAKE
    letamwoutlocal = letamwout*(mdotfinavg/mdotinrdiskoutfinavg)
    letawinEM = prefactor*ljem_mumax1[:,iofr(rdiskin)]/mdotfinavg
    letawinMAKE = prefactor*ljmake_mumax1[:,iofr(rdiskin)]/mdotfinavg
    letawin = letawinEM + letawinMAKE
    letawinlocal = letawin*(mdotfinavg/mdotinrdiskinfinavg)
    letawoutEM = prefactor*ljem_mumax1[:,iofr(rdiskout)]/mdotfinavg
    letawoutMAKE = prefactor*ljmake_mumax1[:,iofr(rdiskout)]/mdotfinavg
    letawout = letawoutEM + letawoutMAKE
    letawoutlocal = letawout*(mdotfinavg/mdotinrdiskoutfinavg)
    #
    letabhEM2 = prefactor*ljemtot[:,ihor]/mdotiniavg
    letabhMAKE2 = prefactor*ljmaketot[:,ihor]/mdotiniavg
    letabh2 = letabhEM2 + letabhMAKE2
    letajEM2 = prefactor*ljem_mu1[:,iofr(rjetout)]/mdotiniavg
    letajMAKE2 = prefactor*ljmake_mu1[:,iofr(rjetout)]/mdotiniavg
    letaj2 = letajEM2 + letajMAKE2
    letaj2local = letaj2*(mdotiniavg/mdotinrdiskoutiniavg)
    letamwinEM2 = prefactor*ljem_mumax1m[:,iofr(rjetin)]/mdotiniavg
    letamwinMAKE2 = prefactor*ljmake_mumax1m[:,iofr(rjetin)]/mdotiniavg
    letamwin2 = letamwinEM2 + letamwinMAKE2
    letamwin2local = letamwin2*(mdotiniavg/mdotinrdiskininiavg)
    letamwoutEM2 = prefactor*ljem_mumax1m[:,iofr(rjetout)]/mdotiniavg
    letamwoutMAKE2 = prefactor*ljmake_mumax1m[:,iofr(rjetout)]/mdotiniavg
    letamwout2 = letamwoutEM2 + letamwoutMAKE2
    letamwout2local = letamwout2*(mdotiniavg/mdotinrdiskoutiniavg)
    letawinEM2 = prefactor*ljem_mumax1[:,iofr(rdiskin)]/mdotiniavg
    letawinMAKE2 = prefactor*ljmake_mumax1[:,iofr(rdiskin)]/mdotiniavg
    letawin2 = letawinEM2 + letawinMAKE2
    letawin2local = letawin2*(mdotiniavg/mdotinrdiskininiavg)
    letawoutEM2 = prefactor*ljem_mumax1[:,iofr(rdiskout)]/mdotiniavg
    letawoutMAKE2 = prefactor*ljmake_mumax1[:,iofr(rdiskout)]/mdotiniavg
    letawout2 = letawoutEM2 + letawoutMAKE2
    letawout2local = letawout2*(mdotiniavg/mdotinrdiskoutiniavg)
    #
    #
    #
    #
    #
    #
    if(1 and iti>fti):
        #use mdot averaged over the same time interval for iti<t<=itf
        icond=(ts>=iti)*(ts<=itf)
        #
        etabh[icond]=etabh2[icond]
        etabhEM[icond]=etabhEM2[icond]
        etabhMAKE[icond]=etabhMAKE2[icond]
        etaj[icond]=etaj2[icond]
        etajlocal[icond]=etaj2local[icond]
        etajEM[icond]=etajEM2[icond]
        etajMAKE[icond]=etajMAKE2[icond]
        etamwin[icond]=etamwin2[icond]
        etamwinlocal[icond]=etamwin2local[icond]
        etamwinEM[icond]=etamwinEM2[icond]
        etamwinMAKE[icond]=etamwinMAKE2[icond]
        etamwout[icond]=etamwout2[icond]
        etamwoutlocal[icond]=etamwout2local[icond]
        etamwoutEM[icond]=etamwoutEM2[icond]
        etamwoutMAKE[icond]=etamwoutMAKE2[icond]
        etawin[icond]=etawin2[icond]
        etawinlocal[icond]=etawin2local[icond]
        etawinEM[icond]=etawinEM2[icond]
        etawinMAKE[icond]=etawinMAKE2[icond]
        etawout[icond]=etawout2[icond]
        etawoutlocal[icond]=etawout2local[icond]
        etawoutEM[icond]=etawoutEM2[icond]
        etawoutMAKE[icond]=etawoutMAKE2[icond]
        #
        letabh[icond]=letabh2[icond]
        letabhEM[icond]=letabhEM2[icond]
        letabhMAKE[icond]=letabhMAKE2[icond]
        letaj[icond]=letaj2[icond]
        letajlocal[icond]=letaj2local[icond]
        letajEM[icond]=letajEM2[icond]
        letajMAKE[icond]=letajMAKE2[icond]
        letamwin[icond]=letamwin2[icond]
        letamwinlocal[icond]=letamwin2local[icond]
        letamwinEM[icond]=letamwinEM2[icond]
        letamwinMAKE[icond]=letamwinMAKE2[icond]
        letamwout[icond]=letamwout2[icond]
        letamwoutlocal[icond]=letamwout2local[icond]
        letamwoutEM[icond]=letamwoutEM2[icond]
        letamwoutMAKE[icond]=letamwoutMAKE2[icond]
        letawin[icond]=letawin2[icond]
        letawinlocal[icond]=letawin2local[icond]
        letawinEM[icond]=letawinEM2[icond]
        letawinMAKE[icond]=letawinMAKE2[icond]
        letawout[icond]=letawout2[icond]
        letawoutlocal[icond]=letawout2local[icond]
        letawoutEM[icond]=letawoutEM2[icond]
        letawoutMAKE[icond]=letawoutMAKE2[icond]
        #
    if dotavg:
        etabh_avg = timeavg(etabh,ts,fti,ftf)
        etabhEM_avg = timeavg(etabhEM,ts,fti,ftf)
        etabhMAKE_avg = timeavg(etabhMAKE,ts,fti,ftf)
        etaj_avg = timeavg(etaj,ts,fti,ftf)
        etajlocal_avg = timeavg(etajlocal,ts,fti,ftf)
        etajEM_avg = timeavg(etajEM,ts,fti,ftf)
        etajMAKE_avg = timeavg(etajMAKE,ts,fti,ftf)
        etamwin_avg = timeavg(etamwin,ts,fti,ftf)
        etamwinlocal_avg = timeavg(etamwinlocal,ts,fti,ftf)
        etamwinEM_avg = timeavg(etamwinEM,ts,fti,ftf)
        etamwinMAKE_avg = timeavg(etamwinMAKE,ts,fti,ftf)
        etamwout_avg = timeavg(etamwout,ts,fti,ftf)
        etamwoutlocal_avg = timeavg(etamwoutlocal,ts,fti,ftf)
        etamwoutEM_avg = timeavg(etamwoutEM,ts,fti,ftf)
        etamwoutMAKE_avg = timeavg(etamwoutMAKE,ts,fti,ftf)
        etawin_avg = timeavg(etawin,ts,fti,ftf)
        etawinlocal_avg = timeavg(etawinlocal,ts,fti,ftf)
        etawinEM_avg = timeavg(etawinEM,ts,fti,ftf)
        etawinMAKE_avg = timeavg(etawinMAKE,ts,fti,ftf)
        etawout_avg = timeavg(etawout,ts,fti,ftf)
        etawoutlocal_avg = timeavg(etawoutlocal,ts,fti,ftf)
        etawoutEM_avg = timeavg(etawoutEM,ts,fti,ftf)
        etawoutMAKE_avg = timeavg(etawoutMAKE,ts,fti,ftf)
        pemtot_avg = timeavg(pjemtot[:,ihor],ts,fti,ftf)
        #
        letabh_avg = timeavg(letabh,ts,fti,ftf)
        letabhEM_avg = timeavg(letabhEM,ts,fti,ftf)
        letabhMAKE_avg = timeavg(letabhMAKE,ts,fti,ftf)
        letaj_avg = timeavg(letaj,ts,fti,ftf)
        letajlocal_avg = timeavg(letajlocal,ts,fti,ftf)
        letajEM_avg = timeavg(letajEM,ts,fti,ftf)
        letajMAKE_avg = timeavg(letajMAKE,ts,fti,ftf)
        letamwin_avg = timeavg(letamwin,ts,fti,ftf)
        letamwinlocal_avg = timeavg(letamwinlocal,ts,fti,ftf)
        letamwinEM_avg = timeavg(letamwinEM,ts,fti,ftf)
        letamwinMAKE_avg = timeavg(letamwinMAKE,ts,fti,ftf)
        letamwout_avg = timeavg(letamwout,ts,fti,ftf)
        letamwoutlocal_avg = timeavg(letamwoutlocal,ts,fti,ftf)
        letamwoutEM_avg = timeavg(letamwoutEM,ts,fti,ftf)
        letamwoutMAKE_avg = timeavg(letamwoutMAKE,ts,fti,ftf)
        letawin_avg = timeavg(letawin,ts,fti,ftf)
        letawinlocal_avg = timeavg(letawinlocal,ts,fti,ftf)
        letawinEM_avg = timeavg(letawinEM,ts,fti,ftf)
        letawinMAKE_avg = timeavg(letawinMAKE,ts,fti,ftf)
        letawout_avg = timeavg(letawout,ts,fti,ftf)
        letawoutlocal_avg = timeavg(letawoutlocal,ts,fti,ftf)
        letawoutEM_avg = timeavg(letawoutEM,ts,fti,ftf)
        letawoutMAKE_avg = timeavg(letawoutMAKE,ts,fti,ftf)
        lemtot_avg = timeavg(ljemtot[:,ihor],ts,fti,ftf)
        #
        #
        #
        if(iti>fti):
            etabh2_avg = timeavg(etabh2,ts,iti,itf)
            etabhEM2_avg = timeavg(etabhEM2,ts,iti,itf)
            etabhMAKE2_avg = timeavg(etabhMAKE2,ts,iti,itf)
            etaj2_avg = timeavg(etaj2,ts,iti,itf)
            etaj2local_avg = timeavg(etaj2local,ts,iti,itf)
            etajEM2_avg = timeavg(etajEM2,ts,iti,itf)
            etajMAKE2_avg = timeavg(etajMAKE2,ts,iti,itf)
            etamwin2_avg = timeavg(etamwin2,ts,iti,itf)
            etamwin2local_avg = timeavg(etamwin2local,ts,iti,itf)
            etamwinEM2_avg = timeavg(etamwinEM2,ts,iti,itf)
            etamwinMAKE2_avg = timeavg(etamwinMAKE2,ts,iti,itf)
            etamwout2_avg = timeavg(etamwout2,ts,iti,itf)
            etamwout2local_avg = timeavg(etamwout2local,ts,iti,itf)
            etamwoutEM2_avg = timeavg(etamwoutEM2,ts,iti,itf)
            etamwoutMAKE2_avg = timeavg(etamwoutMAKE2,ts,iti,itf)
            etawin2_avg = timeavg(etawin2,ts,iti,itf)
            etawin2local_avg = timeavg(etawin2local,ts,iti,itf)
            etawinEM2_avg = timeavg(etawinEM2,ts,iti,itf)
            etawinMAKE2_avg = timeavg(etawinMAKE2,ts,iti,itf)
            etawout2_avg = timeavg(etawout2,ts,iti,itf)
            etawout2local_avg = timeavg(etawout2local,ts,iti,itf)
            etawoutEM2_avg = timeavg(etawoutEM2,ts,iti,itf)
            etawoutMAKE2_avg = timeavg(etawoutMAKE2,ts,iti,itf)
            pemtot2_avg = timeavg(pjemtot[:,ihor],ts,iti,itf)
            #
            letabh2_avg = timeavg(letabh2,ts,iti,itf)
            letabhEM2_avg = timeavg(letabhEM2,ts,iti,itf)
            letabhMAKE2_avg = timeavg(letabhMAKE2,ts,iti,itf)
            letaj2_avg = timeavg(letaj2,ts,iti,itf)
            letaj2local_avg = timeavg(letaj2local,ts,iti,itf)
            letajEM2_avg = timeavg(letajEM2,ts,iti,itf)
            letajMAKE2_avg = timeavg(letajMAKE2,ts,iti,itf)
            letamwin2_avg = timeavg(letamwin2,ts,iti,itf)
            letamwin2local_avg = timeavg(letamwin2local,ts,iti,itf)
            letamwinEM2_avg = timeavg(letamwinEM2,ts,iti,itf)
            letamwinMAKE2_avg = timeavg(letamwinMAKE2,ts,iti,itf)
            letamwout2_avg = timeavg(letamwout2,ts,iti,itf)
            letamwout2local_avg = timeavg(letamwout2local,ts,iti,itf)
            letamwoutEM2_avg = timeavg(letamwoutEM2,ts,iti,itf)
            letamwoutMAKE2_avg = timeavg(letamwoutMAKE2,ts,iti,itf)
            letawin2_avg = timeavg(letawin2,ts,iti,itf)
            letawin2local_avg = timeavg(letawin2local,ts,iti,itf)
            letawinEM2_avg = timeavg(letawinEM2,ts,iti,itf)
            letawinMAKE2_avg = timeavg(letawinMAKE2,ts,iti,itf)
            letawout2_avg = timeavg(letawout2,ts,iti,itf)
            letawout2local_avg = timeavg(letawout2local,ts,iti,itf)
            letawoutEM2_avg = timeavg(letawoutEM2,ts,iti,itf)
            letawoutMAKE2_avg = timeavg(letawoutMAKE2,ts,iti,itf)
            lemtot2_avg = timeavg(ljemtot[:,ihor],ts,iti,itf)
            #
        #
    #
    lbh_avg=letabh_avg/prefactor
    lbhEM_avg=letabhEM_avg/prefactor
    lbhMAKE_avg=letabhMAKE_avg/prefactor
    ljmwout_avg=(letaj_avg + letamwout_avg)/prefactor
    ljmwoutlocal_avg=(letaj_avg + letamwoutlocal_avg)/prefactor
    ljwout_avg=(letaj_avg + letawout_avg)/prefactor
    ljwoutlocal_avg=(letaj_avg + letawoutlocal_avg)/prefactor
    lj_avg=letaj_avg/prefactor
    ljlocal_avg=letajlocal_avg/prefactor
    ljEM_avg=letajEM_avg/prefactor
    ljMAKE_avg=letajMAKE_avg/prefactor
    lmwin_avg=letamwin_avg/prefactor
    lmwinlocal_avg=letamwinlocal_avg/prefactor
    lmwinEM_avg=letamwinEM_avg/prefactor
    lmwinMAKE_avg=letamwinMAKE_avg/prefactor
    lmwout_avg=letamwout_avg/prefactor
    lmwoutlocal_avg=letamwoutlocal_avg/prefactor
    lmwoutEM_avg=letamwoutEM_avg/prefactor
    lmwoutMAKE_avg=letamwoutMAKE_avg/prefactor
    lwin_avg=letawin_avg/prefactor
    lwinlocal_avg=letawinlocal_avg/prefactor
    lwinEM_avg=letawinEM_avg/prefactor
    lwinMAKE_avg=letawinMAKE_avg/prefactor
    lwout_avg=letawout_avg/prefactor
    lwoutlocal_avg=letawoutlocal_avg/prefactor
    lwoutEM_avg=letawoutEM_avg/prefactor
    lwoutMAKE_avg=letawoutMAKE_avg/prefactor
    #
    sbh_avg  = (-lbh_avg) - 2.0*a*(1.0-etabh_avg/prefactor)
    sbhEM_avg  = (-lbhEM_avg) - 2.0*a*(1.0-etabhEM_avg/prefactor)
    sbhMAKE_avg  = (-lbhMAKE_avg) - 2.0*a*(1.0-etabhMAKE_avg/prefactor)
    sj_avg   = (-lj_avg)  - 2.0*a*(1.0-etaj_avg/prefactor)
    sjlocal_avg   = (-ljlocal_avg)  - 2.0*a*(1.0-etajlocal_avg/prefactor)
    sjEM_avg   = (-ljEM_avg)  - 2.0*a*(1.0-etajEM_avg/prefactor)
    sjMAKE_avg   = (-ljMAKE_avg)  - 2.0*a*(1.0-etajMAKE_avg/prefactor)
    smwin_avg   = (-lmwin_avg)  - 2.0*a*(1.0-etamwin_avg/prefactor)
    smwinlocal_avg   = (-lmwinlocal_avg)  - 2.0*a*(1.0-etamwinlocal_avg/prefactor)
    smwinEM_avg   = (-lmwinEM_avg)  - 2.0*a*(1.0-etamwinEM_avg/prefactor)
    smwinMAKE_avg   = (-lmwinMAKE_avg)  - 2.0*a*(1.0-etamwinMAKE_avg/prefactor)
    smwout_avg   = (-lmwout_avg)  - 2.0*a*(1.0-etamwout_avg/prefactor)
    smwoutlocal_avg   = (-lmwoutlocal_avg)  - 2.0*a*(1.0-etamwoutlocal_avg/prefactor)
    smwoutEM_avg   = (-lmwoutEM_avg)  - 2.0*a*(1.0-etamwoutEM_avg/prefactor)
    smwoutMAKE_avg   = (-lmwoutMAKE_avg)  - 2.0*a*(1.0-etamwoutMAKE_avg/prefactor)
    swin_avg   = (-lwin_avg)  - 2.0*a*(1.0-etawin_avg/prefactor)
    swinlocal_avg   = (-lwinlocal_avg)  - 2.0*a*(1.0-etawinlocal_avg/prefactor)
    swinEM_avg   = (-lwinEM_avg)  - 2.0*a*(1.0-etawinEM_avg/prefactor)
    swinMAKE_avg   = (-lwinMAKE_avg)  - 2.0*a*(1.0-etawinMAKE_avg/prefactor)
    swout_avg   = (-lwout_avg)  - 2.0*a*(1.0-etawout_avg/prefactor)
    swoutlocal_avg   = (-lwoutlocal_avg)  - 2.0*a*(1.0-etawoutlocal_avg/prefactor)
    swoutEM_avg   = (-lwoutEM_avg)  - 2.0*a*(1.0-etawoutEM_avg/prefactor)
    swoutMAKE_avg   = (-lwoutMAKE_avg)  - 2.0*a*(1.0-etawoutMAKE_avg/prefactor)
    #
    #
    einf,linf=elinfcalc(a)
    etant=prefactor*(1.0-einf)
    lnt=-linf
    snt  = linf       - 2.0*a*einf
    #
    # Jon's whichplot==4 Plot:
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        windplotfactor=1.0
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        windplotfactor=1.0
    else:
        windplotfactor=0.1
    #
    #
    #
    global gridtype
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        gridtype="ExpOld"
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        gridtype="TNM11"
    elif Rout==26000:
        gridtype="HypExp"
    elif Rout==1000:
        gridtype="Exp"
    else:
        gridtype="UnknownModelGridType"
    #
    if modelname=="thickdisk7":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN40"
    elif modelname=="thickdisk8":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN100c1"
    elif modelname=="thickdisk11":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN100c2"
    elif modelname=="thickdisk12":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN100c3"
    elif modelname=="thickdisk13":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN100c4"
    elif modelname=="run.like8":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN40c5$^*$"
    elif modelname=="thickdiskrr2":
        fieldtype="PoloidalFlip"
        truemodelname="A-0.94BfN30"
    elif modelname=="run.liker2butbeta40":
        fieldtype="PoloidalFlip"
        truemodelname="A-0.94BfN40c1$^*$"
    elif modelname=="run.liker2":
        fieldtype="PoloidalFlip"
        truemodelname="A-0.94BfN10c2$^*$"
    elif modelname=="thickdisk16":
        fieldtype="PoloidalFlip"
        truemodelname="A-0.5BfN30"
    elif modelname=="thickdisk5":
        fieldtype="PoloidalFlip"
        truemodelname="A0.0BfN10"
    elif modelname=="thickdisk14":
        fieldtype="PoloidalFlip"
        truemodelname="A0.5BfN30"
    elif modelname=="thickdiskr1":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN30"
    elif modelname=="thickdiskr2":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN30r"
    elif modelname=="run.liker1":
        fieldtype="PoloidalFlip"
        truemodelname="A0.94BfN10c$^*$"
    elif modelname=="thickdisk9":
        fieldtype="Poloidal"
        truemodelname="A0.94BpN100"
    elif modelname=="thickdiskr3":
        fieldtype="Toroidal"
        truemodelname="A-0.94BtN10"
    elif modelname=="thickdisk17":
        fieldtype="Toroidal"
        truemodelname="A-0.5BtN10"
    elif modelname=="thickdisk10":
        fieldtype="Toroidal"
        truemodelname="A0.0BtN10"
    elif modelname=="thickdisk15":
        fieldtype="Toroidal"
        truemodelname="A0.5BtN5300"
    elif modelname=="thickdiskr15":
        fieldtype="Toroidal"
        truemodelname="A0.5BtN10"
    elif modelname=="thickdisk2":
        fieldtype="Toroidal"
        truemodelname="A0.94BtN10r"
    elif modelname=="thickdisk3":
        fieldtype="Toroidal"
        truemodelname="A0.94BtN10"
    elif modelname=="thickdiskhr3":
        fieldtype="Toroidal"
        truemodelname="A0.94BtN10HR"
    elif modelname=="runlocaldipole3dfiducial":
        fieldtype="PoloidalOld"
        truemodelname="MB09D"
    elif modelname=="blandford3d_new":
        fieldtype="LSQuad"
        truemodelname="MB09Q"
    elif modelname=="sasham9":
        fieldtype="Poloidal2"
        truemodelname="A-0.9N100halfpi"
    elif modelname=="sasham9full2pi":
        fieldtype="Poloidal2"
        truemodelname="A-0.9N100"
    elif modelname=="sasham5":
        fieldtype="Poloidal2"
        truemodelname="A-0.5N100"
    elif modelname=="sasha0":
        fieldtype="Poloidal2"
        truemodelname="A0.0N100"
    elif modelname=="sasha1":
        fieldtype="Poloidal2"
        truemodelname="A0.1N100"
    elif modelname=="sasha2":
        fieldtype="Poloidal2"
        truemodelname="A0.2N100"
    elif modelname=="sasha5":
        fieldtype="Poloidal2"
        truemodelname="A0.5N100"
    elif modelname=="sasha9b25":
        fieldtype="Poloidal2"
        truemodelname="A0.9N25"
    elif modelname=="sasha9b50":
        fieldtype="Poloidal2"
        truemodelname="A0.9N50"
    elif modelname=="sasha9b100":
        fieldtype="Poloidal2"
        truemodelname="A0.9N100"
    elif modelname=="sasha9b200":
        fieldtype="Poloidal2"
        truemodelname="A0.9N200"
    elif modelname=="sasha99":
        fieldtype="Poloidal2"
        truemodelname="A0.99N100"
    else:
        fieldtype="UnknownModelFieldType"
    #
    #
    #
    ######################################
    # END COMPUTE JON WHICHPLOT==4
    ######################################
    #
    #
    #
    ######################################
    # BEGIN PART2 of COMPUTE JON WHICHPLOT==5
    ######################################
    print("part2 whichplot==5" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    # get initial extrema
    # get equatorial flux extrema at t=0 to normalize new flux on hole
    feqtot0extrema=extrema(feqtot[0,:],withendf=True)
    feqtot0extremai=feqtot0extrema[0]
    numextrema0=len(feqtot0extremai)
    # first value is probably 0, so avoid it later below
    feqtot0extremaval=feqtot0extrema[1]
    print("feqtot0extrema at t=0: numextrema0=%d" % (numextrema0) ) ; sys.stdout.flush()
    print(feqtot0extrema) ; sys.stdout.flush()
    #
    #
    # now replace with desired extrema (avoid values that are just close in value)
    feqtotextremai=0*np.copy(feqtot0extremai)
    feqtotextremaval=0*np.copy(feqtot0extremaval)
    newtic=0
    # at least sepi cells apart to avoid capturing noise
    sepi=3
    for tic in np.arange(0,numextrema0-1+1):
        #print("tic=%d" % (tic) )
        # avoid t=0 regions that are much less than initial maximum density to avoid noise (or interpolated-generated noise)
        if np.fabs(rhosrhosqeq[0,feqtot0extremai[tic]])>maxrho*1E-6:
            goodtic=(tic==0 and feqtot0extremai[tic]<sepi+feqtot0extremai[tic+1]) or (tic==numextrema0-1 and feqtot0extremai[tic]>feqtot0extremai[tic-1]+sepi) or (tic>0 and tic<numextrema0-1 and feqtot0extremai[tic]<sepi+feqtot0extremai[tic+1] and feqtot0extremai[tic]>feqtot0extremai[tic-1]+sepi)
            #
            if(newtic==0) and np.fabs(feqtot0extremaval[tic])>1E-15 and goodtic:
                feqtotextremai[newtic]=feqtot0extremai[tic]
                feqtotextremaval[newtic]=feqtot0extremaval[tic]
                newtic=newtic+1
            #
            if(newtic>0) and np.fabs(feqtot0extremaval[tic])>1E-15 and goodtic:
                error=np.fabs(feqtotextremaval[newtic-1]-feqtot0extremaval[tic])/(np.fabs(feqtotextremaval[newtic-1])+np.fabs(feqtot0extremaval[tic]))
                #print("prior new=%g current old=%g error=%g" % (feqtotextremaval[newtic-1],feqtot0extremaval[tic],error) )
                if error>0.4:
                    feqtotextremai[newtic]=feqtot0extremai[tic]
                    feqtotextremaval[newtic]=feqtot0extremaval[tic]
                    newtic=newtic+1
                # else add nothing
            #
    numextrema=newtic
    print("feqtotextrema at t=0: numextrema=%d" % (numextrema) )
    print(feqtotextremai)
    print(feqtotextremaval)
    sys.stdout.flush()
    #
    #
    # model overrides for smallish \Psi at larger radii in Sasha's model
    if modelname=="runlocaldipole3dfiducial":
        # real value
        if numextrema>1:
            numextrema=1
        #
    elif modelname=="blandford3d_new":
        # real value
        if numextrema>1:
            numextrema=1
        #
        # know flux is really zero, but use of centered field messes that up
        feqtotextremaval[0]=1E-30
        #
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        # real value
        if numextrema>1:
            numextrema=1
        #
    #
    # also get final extrema
    feqtotextremafinal=extrema(feqtot[-1,:],withendf=True)
    feqtotextremaifinal=feqtotextremafinal[0]
    numextremafinal=len(feqtotextremaifinal)
    # first value is probably 0, so avoid it later below
    feqtotextremavalfinal=feqtotextremafinal[1]
    print("feqtotextremafinal at t=tfinal: numextremafinal=%d" % (numextremafinal) )
    print(feqtotextremafinal)
    sys.stdout.flush()
    #
    # fstot is absolute flux, so for split-mono gives 2X potential near equator
    # positive fluxvsr means flux points towards \theta=\pi pole, so points in z-direction.
    # positive fluxvsh starting at \theta=0 would come from negative fluxvsr, so flip sign for comparison of origin of field on BH
    # So  fluxvsh=-fluxvsr
    # once sign is fixed, and assuming j=0 is theta=0 is theta=0 pole:
    #
    # A : measured relative to t=0 fluxes
    # B : measured relative to flux at stagnation surface
    # C : measured relative to flux (vs. t) on hole+equator that is available to hole of same-signed flux
    #
    #
    sumextreme=0
    abssumextreme=0
    if modelname=="blandford3d_new":
        starteval=0
    else:
        starteval=0
    #
    testnum=starteval
    #
    firstlimited=starteval
    whichfirstlimited=-1
    everfirstlimited=0
    #
    # memory accesses at least index=2, even if just zero value
    bigextrema=max(numextrema,3)
    fstotnormA=np.zeros( ( bigextrema ,sizet ),dtype=float)
    fstotnormB=np.zeros( ( bigextrema ,sizet ),dtype=float)
    fstotnormA_avg=np.zeros( bigextrema ,dtype=float)
    fstotnormB_avg=np.zeros( bigextrema ,dtype=float)
    #
    for testnum in np.arange(0,numextrema):
      if numextrema>testnum:
        if feqtotextremai[testnum]>istagreport:
            trueieq=istagreport
            if everfirstlimited==0:
                everfirstlimited=1
                whichfirstlimited=testnum
                # not feqstag_avg2 or feqstag_avg1
                if testnum>=1:
                    if np.fabs(chosenfeqstag)>np.fabs(feqtotextremaval[testnum-1]):
                        firstlimited=chosenfeqstag
                    else:
                        firstlimited=feqtotextremaval[testnum-1]
                    #
                else:
                    firstlimited=chosenfeqstag
                #
            #
            truefeq=firstlimited
            #
            print("limited trueieq=%d truefeq=%g" % (trueieq,truefeq) ) ; sys.stdout.flush()
        else:
            trueieq=feqtotextremai[testnum]
            truefeq=feqtotextremaval[testnum]
            print("unlimited trueieq=%d truefeq=%g" % (trueieq,truefeq) ) ; sys.stdout.flush()
        #
        # fstot has no sign information
        #fstotnormA[testnum]=(-fstot[:,ihor]/2.0)/(feqtotextremaval[testnum]+(-fstot[0,ihor]/2.0))
        #fstotnormB[testnum]=(-fstot[:,ihor]/2.0)/(truefeq+(-fstot[:,ihor]/2.0))
        fstotnormA[testnum]=(-fsuphalf[:,ihor])/(feqtotextremaval[testnum]+(-fsuphalf[0,ihor]))
        print("testnum=%d : fstotnormAden=%g  %g %g" % (testnum,feqtotextremaval[testnum]+(-fsuphalf[0,ihor]),feqtotextremaval[testnum],-fsuphalf[0,ihor])) ; sys.stdout.flush()
        #
        fstotnormB[testnum]=(-fsuphalf[:,ihor])/(truefeq+(-fsuphalf[:,ihor]))
        #
        print("rext%d=%g" % (testnum,r[trueieq,0,0]) ) ; sys.stdout.flush()
        print("rexttrue=%g" % (r[trueieq,0,0]) ) ; sys.stdout.flush()
        sumextreme+=feqtotextremaval[testnum]
        abssumextreme+=np.fabs(feqtotextremaval[testnum])
        #
        if dotavg:
            fstotnormA_avg[testnum] = timeavg(fstotnormA[testnum]**2,ts,fti,ftf)**0.5
            print("fstotnormA_avg[%d]=%g" % (testnum,fstotnormA_avg[testnum]))
            fstotnormB_avg[testnum] = timeavg(fstotnormB[testnum]**2,ts,fti,ftf)**0.5
        #
        print("it=%d %d %d" % (numextrema,testnum,istagreport) ) ; sys.stdout.flush()
    #
    #
    if whichfirstlimited==-1 or everfirstlimited==0:
        print("Never found limited: feqtotextremai[starteval]=%d numextrema=%d istagreport=%d" % (feqtotextremai[starteval],numextrema,istagreport) ) ; sys.stdout.flush()
        # just choose outermost extrema
        whichfirstlimited=numextrema-1
        testnum=numextrema-1
        firstlimited=feqtotextremaval[numextrema-1]
        truefeq=firstlimited
        #fstotnormB[testnum]=(-fstot[:,ihor]/2.0)/(truefeq+(-fstot[:,ihor]/2.0))
        fstotnormB[testnum]=(-fsuphalf[:,ihor])/(truefeq+(-fsuphalf[:,ihor]))
        fstotnormB_avg[testnum]=timeavg(fstotnormB[testnum]**2,ts,fti,ftf)**0.5
        print("self-chosen whichfirstlimited=%d firstlimited=%g" % (whichfirstlimited,firstlimited) ) ; sys.stdout.flush()
    #
    #
    # below can be used to detect poloidal flips vs. poloidal (but not really vs. toroidal)
    fracdiffabs=np.fabs(np.fabs(sumextreme)-abssumextreme)/((np.fabs(sumextreme)+abssumextreme))
    #                           
    #
    # choose for B the first limited case
    fstotnormgenB_avg = fstotnormB_avg[whichfirstlimited]
    print("fstotnormgenB_avg=%g" % (fstotnormgenB_avg) ) ; sys.stdout.flush()
    #
    # find max absolute flux BH+eq up to stagnation surface:
    #blobf=np.zeros(len(mdotfinavgvsr5),dtype=mdotfinavgvsr5.dtype)
    ifstagmaxvst=np.zeros(sizet,dtype=int)
    fstagmaxvst=np.zeros(sizet,dtype=float)
    #
    for tic in ts:
        tici=np.where(ts==tic)[0]
        #print("tic=%g %d tici=%d" % (tic,len(tic==ts),tici) )
        blobf[:]=ftruetot[tici,:]
        condition=ti[:,0,0]>=ihor
        condition=condition*(ti[:,0,0]<=istagreport)
        # only do max over relevant range
        newblobf=np.copy(blobf)
        newblobf[ti[:,0,0]<ihor]=0
        newblobf[ti[:,0,0]>istagreport]=0
        condition=condition*(np.fabs(newblobf[:])==np.max(np.fabs(newblobf[:])))
        imax=np.where(condition==1)[0]
        #
        if(len(imax)>1):
            imax=imax[0]
        #
        ifmax=ftruetot[tici,imax]
        ifstagmaxvst[tici]=imax
        #
        fstagmaxvst[tici]=ftruetot[tici,ifstagmaxvst[tici]]
    #
    # 
    # time-averaged flux at the max flux relevant for the hole flux
    # use this rather than t=0 max flux for hole ratio calculation because flux can degrade over time on domain.
    # So want to know what the flux is on the hole relative to similar signed flux available to the hole at any time, not just predegraded value at t=0
    fstagtruetot_avg = timeavg(fstagmaxvst,ts,fti,ftf)
    print("fstagtruetot_avg=%g fstagmaxvst_end=%g" % (fstagtruetot_avg,fstagmaxvst[-1]) ) ; sys.stdout.flush()
    #
    #####################
    # measure based upon flux currently available (up to stagnation surface) to the hole
    fstotnormE=(-fsuphalf[:,ihor])/(fstagtruetot_avg)
    fstotnormE2=(-fsuphalf[:,ihor])/(fstagmaxvst[:]) # more instantaneous version of above
    #
    # ratio of averages for stable average value
    fstotnormgenE_avg = timeavg(fstotnormE**2,ts,fti,ftf)**0.5
    print("fstotnormgenE_avg=%g" % (fstotnormgenE_avg) ) ; sys.stdout.flush()
    #
    #
    #####################
    # measure based upon flux currently available to the hole
    fstotnormC=(-fsuphalf[:,ihor])/(ftruetot_avg)
    fstotnormC2=(-fsuphalf[:,ihor])/(fmaxvst[:]) # more instantaneous version of above
    #
    # ratio of averages for stable average value
    fstotnormgenC_avg = timeavg(fstotnormC**2,ts,fti,ftf)**0.5
    print("fstotnormgenC_avg=%g" % (fstotnormgenC_avg) ) ; sys.stdout.flush()
    #
    # actual max absolute flux on horizon
    fsmaxtot_avg1 = timeavg(fsmaxtot[:,ihor]**2,ts,fti,ftf)**0.5
    print("fsmaxtot_avg1=%g" % (fsmaxtot_avg1) )
    fsmaxtot_avg2 = timeavg(fsmaxtot[:,ihor],ts,fti,ftf)
    print("fsmaxtot_avg2=%g" % (fsmaxtot_avg2) )
    #
    # upperhalf-hemisphere flux on horizon
    fsuphalf_avg1 = timeavg(fsuphalf[:,ihor]**2,ts,fti,ftf)**0.5
    print("fsuphalf_avg1=%g" % (fsuphalf_avg1) )
    fsuphalf_avg2 = timeavg(fsuphalf[:,ihor],ts,fti,ftf)
    print("fsuphalf_avg2=%g" % (fsuphalf_avg2) )
    #fstotnormD=(-fstot[:,ihor]/2.0)/(fsmaxtot_avg)
    # actually, since local, want direct ratio of values(t) since directly related to each other and want high accuracy
    # want fstot in numerator below so can see sign as result
    # below should really be fxmaxtot and not fsuphalf
    fstotnormD=(-fstot[:,ihor]/2.0)/(fsmaxtot[:,ihor])
    fstotnormgenD_avg1 = timeavg(fstotnormD**2,ts,fti,ftf)**0.5
    print("fstotnormgenD_avg1=%g" % (fstotnormgenD_avg1) )
    fstotnormgenD_avg2 = timeavg(fstotnormD,ts,fti,ftf)
    print("fstotnormgenD_avg2=%g" % (fstotnormgenD_avg2) )
    # use sum of absolute value of ratio because if flux switches poles or otherwise varies, then sum can be small even if absolute flux on hole is large.
    fstotnormgenD_avg = np.fabs(fstotnormgenD_avg1)
    print("fstotnormgenD_avg=%g" % (fstotnormgenD_avg) )
    sys.stdout.flush()    
    #
    # want fstot in numerator below so can see sign as result
    fstotnormF=(-fstot[:,ihor]/2.0)/(fsuphalf[:,ihor])
    fstotnormgenF_avg1 = timeavg(fstotnormF**2,ts,fti,ftf)**0.5
    print("fstotnormgenF_avg1=%g" % (fstotnormgenF_avg1) )
    fstotnormgenF_avg2 = timeavg(fstotnormF,ts,fti,ftf)
    print("fstotnormgenF_avg2=%g" % (fstotnormgenF_avg2) )
    # use sum of absolute value of ratio because if flux switches poles or otherwise varies, then sum can be small even if absolute flux on hole is large.
    fstotnormgenF_avg = np.fabs(fstotnormgenF_avg1)
    print("fstotnormgenF_avg=%g" % (fstotnormgenF_avg) )
    sys.stdout.flush()    
    #
    # New conversion from phibh[HL] (old had 1/(2\pi) bug) to phibh[Gaussian] to Upsilon
    # (fstot/2) corresponds to half-flux on hole
    # the sqrt(4\pi) converts flux from HL units to Gaussian units
    # Finally, we really want to show Upsilon, which is \approx 0.2 \phibh[Gaussian], so go ahead and do that here and so redefine phibh
    #
    # For whichplot==5 Computation:
    omh = a / (2*(1+(1-a**2)**0.5))
    #
    # THESE ARE NOW UPSILON RATHER THAN phibh[Gaussian,halfflux] due to factor of 0.2
    # normalized to local Mdot
    # choose fstot below so no effect of sign on flux as wanted for Upsilon since sign has no physical effect except through reconnection issues
    phibh=(fstot[:,ihor]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotfinavg**0.5
    #
    phirdiskin=(fsin[:,iofr(rdiskin)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotinrdiskinfinavg**0.5
    phirdiskout=(fsin[:,iofr(rdiskout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotinrdiskoutfinavg**0.5
    #
    # normalized to BH Mdot (so kinda non-local, but magnetic flux in jet mostly conserved from hole to large radii)
    phij=(phiabsj_mu1[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotfinavg**0.5
    #
    # normalize wind by its own Mdotout so always well-defined and co-spatial-local normalization
    phimwin=(phiabsj_mumax1m[:,iofr(rjetin)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotmwinfinavg**0.5    #mdotfinavg**0.5
    phimwout=(phiabsj_mumax1m[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotmwoutfinavg**0.5    #mdotfinavg**0.5
    #mdotmwinfinavg mdotmwoutfinavg
    #mdotwinfinavg mdotwoutfinavg
    # mdotinrdiskininiavg  mdotinrdiskoutiniavg
    #
    #
    phiwin=(phiabsj_mumax1[:,iofr(rdiskin)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotwinfinavg**0.5    #mdotfinavg**0.5
    phiwout=(phiabsj_mumax1[:,iofr(rdiskout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotwoutfinavg**0.5  #mdotfinavg**0.5
    #
    phijn=(phiabsj_n_mu1[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotfinavg**0.5
    phijs=(phiabsj_s_mu1[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotfinavg**0.5
    #
    phibh2=(fstot[:,ihor]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotiniavg**0.5
    phirdiskin2=(fsin[:,iofr(rdiskin)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotinrdiskininiavg**0.5
    phirdiskout2=(fsin[:,iofr(rdiskout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotinrdiskoutiniavg**0.5
    #
    phij2=(phiabsj_mu1[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotiniavg**0.5
    phimwin2=(phiabsj_mumax1m[:,iofr(rjetin)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotmwininiavg**0.5    #mdotiniavg**0.5
    phimwout2=(phiabsj_mumax1m[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotmwoutiniavg**0.5 #mdotiniavg**0.5
    phiwin2=(phiabsj_mumax1[:,iofr(rdiskin)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotwininiavg**0.5    #mdotiniavg**0.5
    phiwout2=(phiabsj_mumax1[:,iofr(rdiskout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotwoutiniavg**0.5 #mdotiniavg**0.5
    #
    #phijn2=(phiabsj_n_mu2[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotiniavg**0.5
    #phijs2=(phiabsj_s_mu2[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotiniavg**0.5
    phijn2=(phiabsj_n_mu1[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotiniavg**0.5
    phijs2=(phiabsj_s_mu1[:,iofr(rjetout)]/2.0)*(0.2*np.sqrt(4.0*np.pi))/mdotiniavg**0.5
    #
    if(1 and iti>fti):
        #use phi averaged over the same time interval for iti<t<=itf
        icond=(ts>=iti)*(ts<=itf)
        phibh[icond]=phibh2[icond]
        phirdiskin[icond]=phirdiskin2[icond]
        phirdiskout[icond]=phirdiskout2[icond]
        phij[icond]=phij2[icond]
        phijs[icond]=phijs2[icond]
        phijn[icond]=phijn2[icond]
        phimwin[icond]=phimwin2[icond]
        phimwout[icond]=phimwout2[icond]
        phiwin[icond]=phiwin2[icond]
        phiwout[icond]=phiwout2[icond]
    if dotavg:
        phibh_avg = timeavg(phibh**2,ts,fti,ftf)**0.5
        phirdiskin_avg = timeavg(phirdiskin**2,ts,fti,ftf)**0.5
        phirdiskout_avg = timeavg(phirdiskout**2,ts,fti,ftf)**0.5
        phij_avg = timeavg(phij**2,ts,fti,ftf)**0.5
        phimwin_avg = timeavg(phimwin**2,ts,fti,ftf)**0.5
        phimwout_avg = timeavg(phimwout**2,ts,fti,ftf)**0.5
        phiwin_avg = timeavg(phiwin**2,ts,fti,ftf)**0.5
        phiwout_avg = timeavg(phiwout**2,ts,fti,ftf)**0.5
        fstot_avg = timeavg(fstot[:,ihor]**2,ts,fti,ftf)**0.5
        fsmaxtot_avg = timeavg(fsmaxtot[:,ihor]**2,ts,fti,ftf)**0.5
        fsuphalf_avg = timeavg(fsuphalf[:,ihor]**2,ts,fti,ftf)**0.5
        #
        phijn_avg = timeavg(phijn**2,ts,fti,ftf)**0.5
        phijs_avg = timeavg(phijn**2,ts,fti,ftf)**0.5
        #
    if(iti>fti):
        phibh2_avg = timeavg(phibh2**2,ts,iti,itf)**0.5
        fstot2_avg = timeavg(fstot[:,ihor]**2,ts,iti,itf)**0.5
        fsmaxtot2_avg = timeavg(fsmaxtot[:,ihor]**2,ts,iti,itf)**0.5
        fsuphalf2_avg = timeavg(fsuphalf[:,ihor]**2,ts,iti,itf)**0.5
    #
    # use disk-type iin2:iout2
    # NO: fix always to be from r=15 to r=30 so can compare across simulations
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        iinalt=iofr(10.0)
        ioutalt=iofr(12.0)
    else:
        iinalt=iofr(12.0)
        ioutalt=iofr(20.0)
    #
    # get fit so can extract average value over interesting radial range
    numfit=1
    (alphamag1_vsr_fit0,alphamag1_vsr_fitsigma0,alphamag1_vsr_fitgoodness0)=jonpolyfit((np.fabs(r[iinalt:ioutalt,0,0])),(np.fabs(alphamag1_vsr[iinalt:ioutalt])),1,dologx=0,dology=0,doabs=1,num=numfit) ; numfit+=1
    alphamag1_vsr_avg=np.average(np.fabs(alphamag1_vsr[iinalt:ioutalt]))    
    (alphamag2_vsr_fit0,alphamag2_vsr_fitsigma0,alphamag2_vsr_fitgoodness0)=jonpolyfit((np.fabs(r[iinalt:ioutalt,0,0])),(np.fabs(alphamag2_vsr[iinalt:ioutalt])),1,dologx=0,dology=0,doabs=1,num=numfit) ; numfit+=1
    alphamag2_vsr_avg=np.average(np.fabs(alphamag2_vsr[iinalt:ioutalt]))    
    (alphamag3_vsr_fit0,alphamag3_vsr_fitsigma0,alphamag3_vsr_fitgoodness0)=jonpolyfit((np.fabs(r[iinalt:ioutalt,0,0])),(np.fabs(alphamag3_vsr[iinalt:ioutalt])),1,dologx=0,dology=0,doabs=1,num=numfit) ; numfit+=1
    alphamag3_vsr_avg=np.average(np.fabs(alphamag3_vsr[iinalt:ioutalt]))    
    #
    ######################################
    # END PART2 of COMPUTE JON WHICHPLOT==5
    ######################################
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #######################################
    # Begin some plots
    #######################################
    print("Some plots" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    #
    #
    #
    #
    #
    #
    #######################
    #
    # Mdot ***
    #
    #######################
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        windplotfactor=1.0
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        windplotfactor=1.0
    else:
        #windplotfactor=0.1
        # with only showing magnetized wind, 1.0 factor best
        windplotfactor=1.0
    #
    sashaplot1=0
    #
    #####################################
    # Sasha's version of Mdot plot
    if whichplot == 1 and sashaplot1 == 1:
        if dotavg:
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+FMavg,color=(ofc,fc,fc),linestyle=lst)
            if(iti>fti):
                ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+mdotiniavg,color=(ofc,fc,fc))
                
        ax.plot(ts,np.abs(FM),clr,label=r'$\dot Mc^2$')
        if findex != None:
            if not isinstance(findex,tuple):
                ax.plot(ts[findex],np.abs(FM)[findex],'o',mfc='r')
            else:
                for fi in findex:
                    ax.plot(ts[fi],np.abs(FM)[fi],'o',mfc='r')#,label=r'$\dot M$')
        #ax.legend(loc='upper left')
        ax.set_ylabel(r'$\dot Mc^2$',fontsize=16,labelpad=9)
        plt.setp( ax.get_xticklabels(), visible=False)
        ax.set_xlim(ts[0],ts[-1])
        if showextra:
            plt.legend(loc='upper left',bbox_to_anchor=(0.05,0.95),ncol=1,borderaxespad=0,frameon=True,labelspacing=0)
    #
    #####################################
    # Jon's version of Mdot plot
    if whichplot == 1 and sashaplot1 == 0:
        if dotavg:
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+mdotfinavg,color=(ofc,fc,fc))
            if showextra:
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+mdotjetfinavg,'--',color=(fc,fc+0.5*(1-fc),fc))
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+mdotmwoutfinavg*windplotfactor,'-.',color=(fc,fc,1))
            if(iti>fti):
                ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+mdotiniavg,color=(ofc,fc,fc))
                if showextra:
                    ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+mdotjetiniavg,color=(fc,fc+0.5*(1-fc),fc))
                    ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+mdotmwoutiniavg*windplotfactor,color=(fc,fc,1))
        #
        print("before ax.plot1") ; sys.stdout.flush()
        ax.plot(ts,np.abs(mdtot[:,ihor]),clr,label=r'$\dot M_{\rm H}c^2$')
        if showextra:
            print("before ax.plot2") ; sys.stdout.flush()
            ax.plot(ts,np.abs(mdjet[:,iofr(rjetout)]),'g--',label=r'$\dot M_{\rm j}c^2$')
            if windplotfactor==1.0:
                print("before ax.plot3") ; sys.stdout.flush()
                ax.plot(ts,windplotfactor*np.abs(mdmwind[:,iofr(rjetout)]),'b-.',label=r'$\dot M_{\rm mw,o}c^2$')
            elif windplotfactor==0.1:
                ax.plot(ts,windplotfactor*np.abs(mdmwind[:,iofr(rjetout)]),'b-.',label=r'$0.1\dot M_{\rm mw,o}c^2$')
        #
        if findex != None:
            if not isinstance(findex,tuple):
                ax.plot(ts[findex],np.abs(mdtot[:,ihor])[findex],'o',mfc='r')
                if showextra:
                    ax.plot(ts[findex],np.abs(mdjet[:,iofr(rjetout)])[findex],'gs')
                    ax.plot(ts[findex],windplotfactor*np.abs(mdmwind[:,iofr(rjetout)])[findex],'bv')
            else:
                for fi in findex:
                    ax.plot(ts[fi],np.abs(mdtot[:,ihor])[fi],'o',mfc='r')#,label=r'$\dot M$')
                    if showextra:
                        ax.plot(ts[fi],np.abs(mdjet[:,iofr(rjetout)])[fi],'gs')
                        ax.plot(ts[fi],windplotfactor*np.abs(mdmwind[:,iofr(rjetout)])[fi],'bv')
        #
        #ax.set_ylabel(r'$\dot Mc^2$',fontsize=16,labelpad=9)
        ax.set_ylabel(r'$\dot Mc^2$',fontsize=16,ha='left',labelpad=20)
        #
        plt.setp( ax.get_xticklabels(), visible=False)
        ax.set_xlim(ts[0],ts[-1])
        if showextra:
            # http://matplotlib.sourceforge.net/users/legend_guide.html
            # http://matplotlib.sourceforge.net/examples/pylab_examples/legend_demo.html
            print("before plt.legend") ; sys.stdout.flush()
            #
            leg=ax.legend(loc='upper left',bbox_to_anchor=(0.02,0.98),ncol=1,borderaxespad=0,frameon=True,labelspacing=0)
            #plt.legend(loc='upper left',bbox_to_anchor=(0.02,0.98),ncol=1,borderaxespad=0,frameon=True,labelspacing=0)
            print("after plt.legend") ; sys.stdout.flush()
            #
            #plt.legend(loc='upper left',ncol=1,borderaxespad=0,frameon=True,labelspacing=0)
            # set some legend properties.  All the code below is optional.  The
            # defaults are usually sensible but if you need more control, this
            # shows you how
            #leg = plt.gca().get_legend()
            ltext  = leg.get_texts()  # all the text.Text instance in the legend
            llines = leg.get_lines()  # all the lines.Line2D instance in the legend
            frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend
            # see text.Text, lines.Line2D, and patches.Rectangle for more info on
            # the settable properties of lines, text, and rectangles
            #frame.set_facecolor('0.80')      # set the frame face color to light gray
            plt.setp(ltext, fontsize=12)    # the legend text fontsize
            #plt.setp(llines, linewidth=1.5)      # the legend linewidth
            #leg.draw_frame(False)           # don't draw the legend frame
    #
    #
    #######################
    #
    # Pjet
    #
    #######################
    if whichplot == 2:
        ax.plot(ts,(pjem5[:,ihor]),label=r'P_{\rm j}$')
        #ax.legend(loc='upper left')
        if dotavg:
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+pjetfinavg)#,label=r'$\langle P_{\rm j}\rangle$')
        ax.set_ylabel(r'$P_{\rm j}$',fontsize=16)
        plt.setp( ax.get_xticklabels(), visible=False)
        ax.set_xlim(ts[0],ts[-1])
    #######################
    #
    # eta instantaneous
    #
    #######################
    if whichplot == 3:
        ax.plot(ts,(pjem5[:,ihor]/(mdtot[:,ihor])))#,label=r'$P_{\rm j}/\dot M$')
        #ax.legend(loc='upper left')
        if dotavg:
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+pjetfinavg/mdotfinavg)#,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
        ax.set_ylim(0,4)
        #ax.set_xlabel(r'$t\;(r_g/c)$')
        ax.set_ylabel(r'$P_{\rm j}/\dot M$',fontsize=16)
        ax.set_xlim(ts[0],ts[-1])
    #######################
    #
    # eta ***
    #
    #######################
    #
    sashaplot4=0
    #
    # Sasha's whichplot==4 Plot:
    if whichplot == 4 and sashaplot4 == 1:
        # Compute Sasha's version even if not plotting, so can output to file for comparison
        # Sasha's whichplot==4 Calculation:
        etabh = prefactor*FE/FMavg
        etabh2 = prefactor*FE/FMiniavg
        #etaj = prefactor*pjke_mu2[:,iofr(100)]/mdotfinavg
        #etaw = prefactor*(pjke_mu1-pjke_mu2)[:,iofr(100)]/mdotfinavg
        #etaj2 = prefactor*pjke_mu2[:,iofr(100)]/mdotiniavg
        #etaw2 = prefactor*(pjke_mu1-pjke_mu2)[:,iofr(100)]/mdotiniavg
        etajEM = prefactor*pjem_mu1[:,iofr(rjetout)]/mdotfinavg
        etajMAKE = prefactor*pjmake_mu1[:,iofr(rjetout)]/mdotfinavg
        etaj = etajEM + etajMAKE
        etawinEM = prefactor*pjem_mumax1[:,iofr(rdiskin)]/mdotfinavg
        etawinMAKE = prefactor*pjmake_mumax1[:,iofr(rdiskin)]/mdotfinavg
        etawin = etawinEM + etawinMAKE
        etawoutEM = prefactor*pjem_mumax1[:,iofr(rdiskout)]/mdotfinavg
        etawoutMAKE = prefactor*pjmake_mumax1[:,iofr(rdiskout)]/mdotfinavg
        etawout = etawoutEM + etawoutMAKE
        #
        etajEM2 = prefactor*pjem_mu1[:,iofr(rjetout)]/mdotiniavg
        etajMAKE2 = prefactor*pjmake_mu1[:,iofr(rjetout)]/mdotiniavg
        etaj2 = etajEM2 + etajMAKE2
        etawinEM2 = prefactor*pjem_mumax1[:,iofr(rdiskin)]/mdotiniavg
        etawinMAKE2 = prefactor*pjmake_mumax1[:,iofr(rdiskin)]/mdotiniavg
        etawin2 = etawinEM2 + etawinMAKE2
        etawoutEM2 = prefactor*pjem_mumax1[:,iofr(rdiskout)]/mdotiniavg
        etawoutMAKE2 = prefactor*pjmake_mumax1[:,iofr(rdiskout)]/mdotiniavg
        etawout2 = etawoutEM2 + etawoutMAKE2
        #
        if(1 and iti>fti):
            #use mdot averaged over the same time interval for iti<t<=itf
            icond=(ts>=iti)*(ts<=itf)
            etabh[icond]=etabh2[icond]
            etaj[icond]=etaj2[icond]
            etawin[icond]=etawin2[icond]
            etawout[icond]=etawout2[icond]
        if dotavg:
            etaj_avg = timeavg(etaj,ts,fti,ftf)
            etabh_avg = timeavg(etabh,ts,fti,ftf)
            etawin_avg = timeavg(etawin,ts,fti,ftf)
            etawout_avg = timeavg(etawout,ts,fti,ftf)
            ptot_avg = timeavg(pjemtot[:,ihor],ts,fti,ftf)
            if(iti>fti):
                etaj2_avg = timeavg(etaj2,ts,iti,itf)
                etabh2_avg = timeavg(etabh2,ts,iti,itf)
                etawin2_avg = timeavg(etawin2,ts,iti,itf)
                etawout2_avg = timeavg(etawout2,ts,iti,itf)
                ptot2_avg = timeavg(pjemtot[:,ihor],ts,iti,itf)
        #
        #
        if dotavg:
            if showextra:
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etaj_avg,'--',color=(fc,fc+0.5*(1-fc),fc)) 
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etabh_avg,color=(ofc,fc,fc),linestyle=lst) 
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            #ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etawout_avg,'-.',color=(fc,fc+0.5*(1-fc),fc)) 
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            if(iti>fti):
                if showextra:
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etaj2_avg,'--',color=(fc,fc+0.5*(1-fc),fc))
                ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etabh2_avg,color=(ofc,fc,fc))
                #ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etawout2_avg,'-.',color=(fc,fc+0.5*(1-fc),fc)) 
        ax.plot(ts,etabh,clr,label=r'$\eta_{\rm H}$')
        if showextra:
            ax.plot(ts,etaj,'g--',label=r'$\eta_{\rm j}$')
            ax.plot(ts,etawout,'b-.',label=r'$\eta_{\rm w}$')
        if findex != None:
            if not isinstance(findex,tuple):
                if showextra:
                    ax.plot(ts[findex],etaj[findex],'gs')
                ax.plot(ts[findex],etabh[findex],'o',mfc='r')
                if showextra:
                    ax.plot(ts[findex],etawout[findex],'bv')
            else:
                for fi in findex:
                    if showextra:
                        ax.plot(ts[fi],etawout[fi],'bv')#,label=r'$\dot M$')
                        ax.plot(ts[fi],etaj[fi],'gs')#,label=r'$\dot M$')
                    ax.plot(ts[fi],etabh[fi],'o',mfc='r')#,label=r'$\dot M$')
        #ax.legend(loc='upper left')
        #ax.set_ylim(0,2)
        ax.set_xlabel(r'$t\;[r_g/c]$',fontsize=16)
        if prefactor == 100:
            ax.set_ylabel(r'$\eta\ [\%]$',fontsize=16,ha='left',labelpad=20)
        else:
            ax.set_ylabel(r'$\eta$',fontsize=16,labelpad=16)
        ax.set_xlim(ts[0],ts[-1])
        if showextra:
            plt.legend(loc='upper left',bbox_to_anchor=(0.02,0.98),ncol=1,borderpad = 0,borderaxespad=0,frameon=True,labelspacing=0)
    #
    # Done with Sasha's whichplot==4
    # Print Sasha's result
    print( "Sasha's values: (if epsFm=epsFke=1, then FMavg=mdot30+mdot)" )
    if epsFm is not None:
        print( "epsFm  = %g, epsFke= %g" % (epsFm , epsFke) )
    else:
        print( "epsFm  = 1, epsFke= 1")
    #
    print( "eta_H = %g, eta_j = %g, eta_w = %g, eta_jw = %g, FMavg=%g, mdot = %g, mdot30 = %g" % ( etabh_avg, etaj_avg, etawout_avg, etaj_avg + etawout_avg, FMavg, mdotfinavg, mdot30finavg ) )
    if iti > fti:
        print( "eta_H2 = %g, eta_j2 = %g, eta_w2 = %g, eta_jw2 = %g, FMiniavg=%g, mdot2 = %g, mdot230=%g" % ( etabh2_avg, etaj2_avg, etawout2_avg, etaj2_avg + etawout2_avg, FMiniavg, mdotiniavg, mdot30iniavg) )
    #
    sys.stdout.flush()
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    print("plot whichplot==4" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    #
    if whichplot == 4 and sashaplot4 == 0:
        if dotavg:
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etabh_avg,color=(ofc,fc,fc)) 
            if showextra:
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etaj_avg,'--',color=(fc,fc+0.5*(1-fc),fc)) 
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etamwout_avg,'-.',color=(fc,fc,1)) 
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            if(iti>fti):
                ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etabh2_avg,color=(ofc,fc,fc))
                if showextra:
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etaj2_avg,'--',color=(fc,fc+0.5*(1-fc),fc))
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etamwout2_avg,'-.',color=(fc,fc,1))
        #
        ax.plot(ts,etabh,clr,label=r'$\eta_{\rm H}$')
        if showextra:
            ax.plot(ts,etaj,'g--',label=r'$\eta_{\rm j}$')
            ax.plot(ts,etamwout,'b-.',label=r'$\eta_{\rm mw,o}$')
        if findex != None:
            if not isinstance(findex,tuple):
                ax.plot(ts[findex],etabh[findex],'o',mfc='r')
                if showextra:
                    ax.plot(ts[findex],etaj[findex],'gs')
                    ax.plot(ts[findex],etamwout[findex],'bv')
            else:
                for fi in findex:
                    ax.plot(ts[fi],etabh[fi],'o',mfc='r')#,label=r'$\dot M$')
                    if showextra:
                        ax.plot(ts[fi],etamwout[fi],'bv')#,label=r'$\dot M$')
                        ax.plot(ts[fi],etaj[fi],'gs')#,label=r'$\dot M$')
        #ax.set_ylim(0,2)
        yminbh=np.min(etabh)
        yminj=np.min(etaj)
        yminmw=np.min(etamwout)
        ymin=min(yminbh,yminj)
        ymin=min(ymin,yminmw)
        # sasha99 at least drops-out at certain points to eta<<0  -- so force eta=0 as minimum
        if modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
            ymin=0
        #
        ymaxbh=np.max(etabh)
        ymaxj=np.max(etaj)
        ymaxmw=np.max(etamwout)
        ymax=max(ymaxbh,ymaxj)
        ymax=max(ymax,ymaxmw)
        #
        ax.set_ylim(ymin,ymax)
        #
        ax.set_xlabel(r'$t\;[r_g/c]$',fontsize=16)
        ax.set_ylabel(r'$\eta\ [\%]$',fontsize=16,ha='left',labelpad=20)
        ax.set_xlim(ts[0],ts[-1])
        if showextra:
            leg=ax.legend(loc='upper left',bbox_to_anchor=(0.02,0.98),ncol=1,borderpad = 0,borderaxespad=0,frameon=True,labelspacing=0)
            # set some legend properties.  All the code below is optional.  The
            # defaults are usually sensible but if you need more control, this
            # shows you how
            #leg = plt.gca().get_legend()
            ltext  = leg.get_texts()  # all the text.Text instance in the legend
            llines = leg.get_lines()  # all the lines.Line2D instance in the legend
            frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend
            # see text.Text, lines.Line2D, and patches.Rectangle for more info on
            # the settable properties of lines, text, and rectangles
            #frame.set_facecolor('0.80')      # set the frame face color to light gray
            plt.setp(ltext, fontsize=12)    # the legend text fontsize
            #plt.setp(llines, linewidth=1.5)      # the legend linewidth
            #leg.draw_frame(False)           # don't draw the legend frame
    #
    # End Jon's whichplot==4 Plot
    #
    # Print's Jon's whichplot==4 Values:
    #
    #
    #
    ######################################
    # BEGIN PRINT JON WHICHPLOT==4
    ######################################
    print("print whichplot==4" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    print( "Jon's values: (recall mdotorig = mdot + mdot30 should be =FMavg)" )
    #
    print( "ihor = %d ihorpole = %d ihoreq = %d rhor = %g rjetin=%g rjetout=%g rdiskin=%g rdiskout=%g" % (ihor,iofrpole(rhor),iofreq(rhor),rhor,rjetin,rjetout,rdiskin,rdiskout))
    #
    print( "mdot = %g, mdot10 = %g, mdot30 = %g, mdotinin = %g, mdotinout=%g, mdotjet = %g, mdotmwin = %g, mdotmwout = %g, mdotwin = %g, mdotwout = %g" % ( mdotfinavg, mdot10finavg, mdot30finavg, mdotinrdiskinfinavg, mdotinrdiskoutfinavg, mdotjetfinavg, mdotmwinfinavg, mdotmwoutfinavg, mdotwinfinavg, mdotwoutfinavg) )
    #
    print( "hoverrhor_t0 = %g, hoverr2_t0 = %g, hoverr5_t0 = %g, hoverr10_t0 = %g, hoverr20_t0 = %g, hoverr100_t0 = %g" % ( hoverrhor_t0 ,  hoverr2_t0 , hoverr5_t0 , hoverr10_t0 ,  hoverr20_t0 ,  hoverr100_t0 ) )
    print( "hoverrcoronahor_t0 = %g, hoverrcorona2_t0 = %g, hoverrcorona5_t0 = %g, hoverrcorona10_t0 = %g, hoverrcorona20_t0 = %g, hoverrcorona100_t0 = %g" % ( hoverrcoronahor_t0 ,  hoverrcorona2_t0 , hoverrcorona5_t0 , hoverrcorona10_t0 ,  hoverrcorona20_t0 ,  hoverrcorona100_t0 ) )
    print( "hoverr_jethor_t0 = %g, hoverr_jet2_t0 = %g, hoverr_jet5_t0 = %g, hoverr_jet10_t0 = %g, hoverr_jet20_t0 = %g, hoverr_jet100_t0 = %g" % ( hoverr_jethor_t0 ,  hoverr_jet2_t0 , hoverr_jet5_t0 , hoverr_jet10_t0 ,  hoverr_jet20_t0 ,  hoverr_jet100_t0 ) )
    #
    print( "hoverrhor_avg = %g, hoverr2_avg = %g, hoverr5_avg = %g, hoverr10_avg = %g, hoverr20_avg = %g, hoverr100_avg = %g" % ( hoverrhor_avg ,  hoverr2_avg , hoverr5_avg , hoverr10_avg ,  hoverr20_avg ,  hoverr100_avg ) )
    print( "hoverrcoronahor_avg = %g, hoverrcorona2_avg = %g, hoverrcorona5_avg = %g, hoverrcorona10_avg = %g, hoverrcorona20_avg = %g, hoverrcorona100_avg = %g" % ( hoverrcoronahor_avg ,  hoverrcorona2_avg , hoverrcorona5_avg , hoverrcorona10_avg ,  hoverrcorona20_avg ,  hoverrcorona100_avg ) )
    print( "hoverr_jethor_avg = %g, hoverr_jet2_avg = %g, hoverr_jet5_avg = %g, hoverr_jet10_avg = %g, hoverr_jet20_avg = %g, hoverr_jet100_avg = %g" % ( hoverr_jethor_avg ,  hoverr_jet2_avg , hoverr_jet5_avg , hoverr_jet10_avg ,  hoverr_jet20_avg ,  hoverr_jet100_avg ) )
    #
    #iq2mridisk20/50/100_t0
    print( "qmridisk20_t0 = %g, qmridisk50_t0 = %g, qmridisk100_t0 = %g" % (  qmridisk20_t0 ,  qmridisk50_t0 ,  qmridisk100_t0 ) )
    print( "q2mridisk20_t0 = %g, q2mridisk50_t0 = %g, q2mridisk100_t0 = %g" % (  1.0/iq2mridisk20_t0 ,  1.0/iq2mridisk50_t0 ,  1.0/iq2mridisk100_t0 ) )
    #
    #iq2mridiskrfitin2/rfitout2/rfitout6
    print( "qmridiskrfitin2 = %g, qmridiskrfitout2 = %g, qmridiskrfitout6 = %g" % (  qmridiskrfitin2_avg ,  qmridiskrfitout2_avg ,  qmridiskrfitout6_avg ) )
    print( "q2mridiskrfitin2 = %g, q2mridiskrfitout2 = %g, q2mridiskrfitout6 = %g" % (  1.0/iq2mridiskrfitin2_avg ,  1.0/iq2mridiskrfitout2_avg ,  1.0/iq2mridiskrfitout6_avg ) )
    #
    print( "qmridiskweak20_t0 = %g, qmridiskweak50_t0 = %g, qmridiskweak100_t0 = %g" % (  qmridiskweak20_t0 ,  qmridiskweak50_t0 ,  qmridiskweak100_t0 ) )
    print( "q2mridiskweak20_t0 = %g, q2mridiskweak50_t0 = %g, q2mridiskweak100_t0 = %g" % (  1.0/iq2mridiskweak20_t0 ,  1.0/iq2mridiskweak50_t0 ,  1.0/iq2mridiskweak100_t0 ) )
    #
    print( "qmridiskweakrfitin2 = %g, qmridiskweakrfitout2 = %g, qmridiskweakrfitout6 = %g" % (  qmridiskweakrfitin2_avg ,  qmridiskweakrfitout2_avg ,  qmridiskweakrfitout6_avg ) )
    print( "q2mridiskweakrfitin2 = %g, q2mridiskweakrfitout2 = %g, q2mridiskweakrfitout6 = %g" % (  1.0/iq2mridiskweakrfitin2_avg ,  1.0/iq2mridiskweakrfitout2_avg ,  1.0/iq2mridiskweakrfitout6_avg ) )
    #
    #
    print( "asphor = %g:%g:%g, asp10 = %g:%g:%g, asp20 = %g:%g:%g, asp100 = %g:%g:%g" % ( drnormvsrhor, dHnormvsrhor, dPnormvsrhor, drnormvsr10, dHnormvsr10, dPnormvsr10, drnormvsr20, dHnormvsr20, dPnormvsr20, drnormvsr100, dHnormvsr100, dPnormvsr100 ) )
    #
    print( "eta_H = %g, eta_HEM = %g, eta_HMAKE = %g, eta_jwout = %g, eta_j = %g, eta_jEM = %g, eta_jMAKE = %g, eta_mwin = %g, eta_mwinEM = %g, eta_mwinMAKE = %g, eta_mwout = %g, eta_mwoutEM = %g, eta_mwoutMAKE = %g, eta_win = %g, eta_winEM = %g, eta_winMAKE = %g, eta_wout = %g, eta_woutEM = %g, eta_woutMAKE = %g, pemtot_H = %g" % ( etabh_avg, etabhEM_avg, etabhMAKE_avg, etaj_avg + etawout_avg, etaj_avg, etajEM_avg, etajMAKE_avg, etamwin_avg, etamwinEM_avg, etamwinMAKE_avg, etamwout_avg, etamwoutEM_avg, etamwoutMAKE_avg, etawin_avg, etawinEM_avg, etawinMAKE_avg, etawout_avg, etawoutEM_avg, etawoutMAKE_avg, pemtot_avg ) )
    #
    print( "leta_H = %g, leta_HEM = %g, leta_HMAKE = %g, leta_jwout = %g, leta_j = %g, leta_jEM = %g, leta_jMAKE = %g, leta_mwin = %g, leta_mwinEM = %g, leta_mwinMAKE = %g, leta_mwout = %g, leta_mwoutEM = %g, leta_mwoutMAKE = %g, leta_win = %g, leta_winEM = %g, leta_winMAKE = %g, leta_wout = %g, leta_woutEM = %g, leta_woutMAKE = %g, lemtot_H = %g" % ( letabh_avg, letabhEM_avg, letabhMAKE_avg, letaj_avg + letawout_avg, letaj_avg, letajEM_avg, letajMAKE_avg, letamwin_avg, letamwinEM_avg, letamwinMAKE_avg, letamwout_avg, letamwoutEM_avg, letamwoutMAKE_avg, letawin_avg, letawinEM_avg, letawinMAKE_avg, letawout_avg, letawoutEM_avg, letawoutMAKE_avg, lemtot_avg ) )
    #
    if iti > fti:
        print( "incomplete output: %g %g" % (iti, fti) )
    #
    # 6:
    print( "HLatex5: ModelName & $\\dot{M}_{\\rm{}H}$  & $\\dot{M}_{\\rm{}in,i}-\\dot{M}_{\\rm{}H}$ & $\\dot{M}_{\\rm{}in,o}-\\dot{M}_{\\rm{}H}$     & $\\dot{M}_{\\rm{}j}$    & $\\dot{M}_{\\rm{}mw,i}$ & $\\dot{M}_{\\rm{}mw,o}$    & $\\dot{M}_{\\rm{}w,i}$ & $\\dot{M}_{\\rm{}w,o}$ \\\\" )
    print( "VLatex5: %s         & %g & %g & %g    & %g    & %g & %g   & %g & %g \\\\ %% %s" % (truemodelname, roundto2(mdotfinavg), roundto2(mdotinrdiskinfinavg-mdotfinavg), roundto2(mdotinrdiskoutfinavg-mdotfinavg), roundto2(mdotjetfinavg),    roundto2(mdotmwinfinavg), roundto2(mdotmwoutfinavg),     roundto2(mdotwinfinavg), roundto2(mdotwoutfinavg),    modelname ) )
    #
    # 12:
    print( "HLatex95: $\\delta r:r \\delta\\theta:r\\sin\\theta \\delta\\phi$" )
    print( "HLatex95: ModelName & $r_{\\rm{}H}$ & $r_i$ & $r_o$ \\\\" )
    print( "VLatex95: %s         & %g:%g:%g & %g:%g:%g & %g:%g:%g \\\\ %% %s" % (truemodelname, roundto2(drnormh), roundto2(dHnormh), roundto2(dPnormh), roundto2(drnormi), roundto2(dHnormi), roundto2(dPnormi), roundto2(drnormo), roundto2(dHnormo), roundto2(dPnormo), modelname ) )
    #
    # 8:
    # below use of ts[-1] for T_f assumes always add last file to file list, which currently do.
    print("HLatex1: ModelName & $a/M$ & FieldType & $\\beta_{\\rm{}min}$ & $\\beta_{\\rm{}rat-of-avg} & $\\beta_{\\rm{}rat-of-max} & $\\theta^d_{r_{\\rm{}max}}$ & $Q_{2,t=0,\\rm{}MRI,\\{i,  o\\}}$ & $T_f$  \\\\")
    print("VLatex1: %s        & %g  &  %s       & %g                   & %g                         & %g                         & %g                          & %g,  %g                         & %g     \\\\ %% %s" % (truemodelname,a,fieldtype,roundto2(betamin_t0),roundto2(betaratofavg_t0),roundto2(betaratofmax_t0),roundto2(hoverratrmax_t0), roundto2(1.0/iq2mridisk20_t0), roundto2(1.0/iq2mridisk50_t0), ts[-1], modelname ) )
    #
    # 16:
    print("HLatex2: ModelName  & GridType & $N_r$ & $N_\\theta$ & $N_\\phi$ & $R_{\\rm{}in}$ & $R_{\\rm{}out}$  & $\\Delta\\phi$ & $A_{r=r_{\\rm{}H}}$ & $A_{r_i}$ & $A_{r_o}$ & $Q_{1,t=0,\\rm{}MRI,\{i,  o\}}$  & $T^a_i$--$T^a_f$  \\\\")
    #
    checkf=4.0
    if np.fabs(ph[0,0,-1]-2.0*np.pi)<checkf*ph[0,0,-1]/nz:
        stringdeltaphi="$2\\pi$"
    elif np.fabs(ph[0,0,-1]-np.pi)<checkf*ph[0,0,-1]/nz:
        stringdeltaphi="$\\pi$"
    elif np.fabs(ph[0,0,-1]-np.pi*0.5)<checkf*ph[0,0,-1]/nz:
        stringdeltaphi="$\\pi/2$"
    elif np.fabs(ph[0,0,-1]-np.pi*0.25)<checkf*ph[0,0,-1]/nz:
        stringdeltaphi="$\\pi/4$"
    else:
        stringdeltaphi="?"
    #
    if nz==1:
        stringdeltaphi="$2\\pi$"
    #
    #qmridisk20_t0 ,  qmridisk50_t0
    print("VLatex2: %s         & %s       &  %g   & %g          & %g        & %g             & %g               & %s          & %g:%g:%g    & %g:%g:%g  & %g:%g:%g  & %g,  %g                          & %g--%g            \\\\ %% %s" % (truemodelname,gridtype,nx,ny,nzreal,roundto3(Rin),Rout,stringdeltaphi,roundto2(drnormh), roundto2(dHnormh), roundto2(dPnormh), roundto2(drnormi), roundto2(dHnormi), roundto2(dPnormi), roundto2(drnormo), roundto2(dHnormo), roundto2(dPnormo),roundto2(qmridisk20_t0), roundto2(qmridisk50_t0),truetmin,truetmax, modelname ) )
    #
    # 8:
    print( "HLatex99: ModelName & $Q_{1,t=0,\\rm{}MRI,i}$ & $Q_{1,t=0,\\rm{}MRI,o}$  & $Q_{1,t=0,\\rm{}MRI,fo}$ & $Q_{2,t=0,\\rm{}MRI,i}$ & $Q_{2,t=0,\\rm{}MRI,o}$ & $Q_{2,t=0,\\rm{}MRI,fo}$  \\\\" )
    print( "VLatex99: %s         & %g & %g & %g & %g & %g & %g \\\\ %% %s" % (truemodelname, roundto2(qmridisk20_t0), roundto2(qmridisk50_t0), roundto2(qmridisk100_t0), roundto2(1.0/iq2mridisk20_t0), roundto2(1.0/iq2mridisk50_t0), roundto2(1.0/iq2mridisk100_t0), modelname ) )
    #
    # alphamag?_vsr_fit[1] gives average value over fitted range
    # rq2mri1
    #
    # determine how to report rm
    if nz==1:
        # 2D models can stagnate at small radii, but still want to know where rm is
        fakerstagreport=1E30
    else:
        #fakerstagreport=rstagreport
        fakerstagreport=rfitout6
        # no, sasha1 does have 1/betamod>1 out to large radii, just not much above 1.
        #fakerstagreport=1E30
        #fakerstagreport
    #
    print( "HLatex4: ModelName & $\\alpha_a$ & $\\alpha_b$ & $\\alpha_c$ & $Q_{1,\\rm{}MRI,i}$ & $Q_{1,\\rm{}MRI,o}$  & $Q_{2,\\rm{}MRI,i}$ & $Q_{2,\\rm{}MRI,o}$ & $r_{Q_{2,\\rm{}MRI}=1/2}$ & $r_{Q_{2\\rm{}weak,MRI}=1/2}$ & $r_m$ \\\\" )
    print( "VLatex4: %s        & %g          & %g          & %g          & %g                  & %g                   & %g                  & %g                  & %s                        & %s                                 & %s                       \\\\ %% %s" % (truemodelname, roundto2(alphamag1_vsr_avg), roundto2(alphamag2_vsr_avg), roundto2(alphamag3_vsr_avg), roundto2(qmridiskrfitin2_avg), roundto2(qmridiskrfitout2_avg), roundto2(1.0/iq2mridiskrfitin2_avg), roundto2(1.0/iq2mridiskrfitout2_avg), roundto2_rq2mri1(rq2mri1,rq2mri1cut,fakerstagreport), roundto2_rq2mri1(rq2mri2,rq2mri2cut,fakerstagreport), roundto2_rq2mri1(rm1,rm1cut,fakerstagreport), modelname ) )
    #
    # 8:
    print( "HLatex97: ModelName & $Q_{1,t=0,\\rm{}MRI,i,w}$ & $Q_{1,t=0,\\rm{}MRI,o,w}$  & $Q_{1,t=0,\\rm{}MRI,fo,w}$ & $Q_{2,t=0,\\rm{}MRI,i,w}$ & $Q_{2,t=0,\\rm{}MRI,o,w}$ & $Q_{2,t=0,\\rm{}MRI,fo,w}$ & rm1 & rm2 & rm3  \\\\" )
    print( "VLatex97: %s         & %g & %g & %g & %g & %g & %g & %s & %s & %s \\\\ %% %s" % (truemodelname, roundto2(qmridiskweak20_t0), roundto2(qmridiskweak50_t0), roundto2(qmridiskweak100_t0), roundto2(1.0/iq2mridiskweak20_t0), roundto2(1.0/iq2mridiskweak50_t0), roundto2(1.0/iq2mridiskweak100_t0), roundto2_rq2mri1(rm1,rm1cut,fakerstagreport), roundto2_rq2mri1(rm2,rm2cut,fakerstagreport), roundto2_rq2mri1(rm3,rm3cut,fakerstagreport), modelname ) )
    #
    print( "HLatex96: ModelName & $Q_{1,\\rm{}MRI,i,w}$ & $Q_{1,\\rm{}MRI,o,w}$  & $Q_{1,\\rm{}MRI,fo,w}$ & $Q_{2,\\rm{}MRI,i,w}$ & $Q_{2,\\rm{}MRI,o,w}$ & $Q_{2,\\rm{}MRI,fo,w}$  \\\\" )
    print( "VLatex96: %s         & %g & %g & %g & %g & %g & %g \\\\ %% %s" % (truemodelname, roundto2(qmridiskweakrfitin2_avg), roundto2(qmridiskweakrfitout2_avg), roundto2(qmridiskweakrfitout6_avg), roundto2(1.0/iq2mridiskweakrfitin2_avg), roundto2(1.0/iq2mridiskweakrfitout2_avg), roundto2(1.0/iq2mridiskweakrfitout6_avg), modelname ) )
    #
    # for ratio of disk thickness to grid cell thickness at horizon, account for actual thickness and count number of cells, rather than just using equatorial value
    #dthetaihor=dxdxp[2][2][ihor,:,0]*_dx2
    #numcellsdiskihor=hoverrhor_avg/(dxdxp[2][2][ihor,ny/2,0]*_dx2)
    numcellsdiskihor=jofhfloat(np.pi*0.5+hoverrhor_avg,ihor) - ny*0.5
    # 
    print( "HLatex3: ModelName & $N^d_{\\theta,{\\rm{}H}}$  & $\\theta^d_{\\rm{}H}$  & $\\theta^d_{5}$ & $\\theta^d_{20}$ & $\\theta^d_{100}$ & $\\theta^{dc}_{\\rm{}H}$  & $\\theta^{dc}_{5}$ & $\\theta^{dc}_{20}$ & $\\theta^{dc}_{100}$ & $\\theta^{cj}_{\\rm{}H}$  & $\\theta^{cj}_{5}$ & $\\theta^{cj}_{20}$ & $\\theta^{cj}_{100}$ \\\\" )
    print( "VLatex3: %s         & %g & %g & %g & %g & %g & %g & %g & %g & %g & %g & %g & %g & %g  \\\\ %% %s" % (truemodelname, roundto2(numcellsdiskihor), roundto2(hoverrhor_avg), roundto2( hoverr5_avg), roundto2(hoverr20_avg), roundto2(hoverr100_avg), roundto2(hoverrcoronahor_avg), roundto2( hoverrcorona5_avg), roundto2(hoverrcorona20_avg), roundto2(hoverrcorona100_avg), roundto2(hoverr_jethor_avg), roundto2( hoverr_jet5_avg), roundto2(hoverr_jet20_avg), roundto2(hoverr_jet100_avg), modelname ) )
    #
    #
    #
    # 9:
    print( "HLatex6: ModelName & $\\eta_{\\rm{}H}$ & $\\eta^{\\rm{}EM}_{\\rm{}H}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}H}$ & $\\eta_{\\rm{}j}$ & $\\eta^{\\rm{}EM}_j$ & $\\eta^{\\rm{}MAKE}_{\\rm{}j}$ & $\\eta^{\\rm{}local}_{\\rm{}j,o}$ & $\\eta_{\\rm{}j+mw,o}$ & $\\eta^{\\rm{}local}_{\\rm{}j+mw,o}$ & $\\eta_{\\rm{}j+w,o}$ & $\\eta^{\\rm{}local}_{\\rm{}j+w,o}$ & $\\eta_{\\rm{}NT}$ \\\\" )
    print( "VLatex6: %s         & %g               & %g                           & %g                             & %g                & %g                   & %g                             & %g                                & %g                     & %g                                   & %g &                  %g                                    & %g                 \\\\ %% %s" % (truemodelname, roundto3foreta(etabh_avg), roundto3foreta(etabhEM_avg), roundto3foreta(etabhMAKE_avg), roundto3foreta(etaj_avg), roundto3foreta(etajEM_avg), roundto3foreta(etajMAKE_avg), roundto3foreta(etajlocal_avg), roundto3foreta(etaj_avg + etamwout_avg), roundto3foreta(etajlocal_avg + etamwoutlocal_avg), roundto3foreta(etaj_avg + etawout_avg), roundto3foreta(etajlocal_avg + etawoutlocal_avg), roundto3foreta(etant), modelname ) )
    #
    # 12:
    print( "HLatex7: ModelName & $\\eta_{\\rm{}mw,i}$ & $\\eta^{\\rm{}EM}_{\\rm{}mw,i}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}mw,i}$ & $\\eta_{\\rm{}mw,o}$ & $\\eta^{\\rm{}EM}_{\\rm{}mw,o}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}mw,o}$ & $\\eta_{\\rm{}w,i}$ & $\\eta^{\\rm{}EM}_{\\rm{}w,i}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}w,i}$ & $\\eta_{\\rm{}w,o}$ & $\\eta^{\\rm{}EM}_{\\rm{}w,o}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}w,o}$ \\\\" )
    print( "VLatex7: %s        & %g & %g & %g    & %g & %g & %g   & %g & %g & %g    & %g & %g & %g  \\\\ %% %s" % (truemodelname, roundto3foreta(etamwin_avg), roundto3foreta(etamwinEM_avg), roundto3foreta(etamwinMAKE_avg), roundto3foreta(etamwout_avg), roundto3foreta(etamwoutEM_avg), roundto3foreta(etamwoutMAKE_avg), roundto3foreta(etawin_avg), roundto3foreta(etawinEM_avg), roundto3foreta(etawinMAKE_avg), roundto3foreta(etawout_avg), roundto3foreta(etawoutEM_avg), roundto3foreta(etawoutMAKE_avg), modelname ) )
    #
    #
    #
    # 9:
    # 9:
    print( "HLatex8: ModelName & $l_{\\rm{}H}$ & $l^{\\rm{}EM}_{\\rm{}H}$ & $l^{\\rm{}MAKE}_{\\rm{}H}$ & $l_{\\rm{}j}$ & $l^{\\rm{}EM}_j$ & $l^{\\rm{}MAKE}_{\\rm{}j}$ & $l^{\\rm{}local}_{\\rm{}j,o}$ & $l_{\\rm{}j+mw,o}$ & $l^{\\rm{}local}_{\\rm{}j+mw,o}$ & $l_{\\rm{}j+w,o}$ & $l^{\\rm{}local}_{\\rm{}j+w,o}$ & $l_{\\rm{}NT}$ \\\\" )
    print( "VLatex8: %s         & %g               & %g                           & %g                             & %g                & %g                   & %g                             & %g                                & %g                     & %g                                   & %g &                  %g                                    & %g                 \\\\ %% %s" % (truemodelname, roundto3forl(lbh_avg), roundto3forl(lbhEM_avg), roundto3forl(lbhMAKE_avg), roundto3forl(lj_avg), roundto3forl(ljEM_avg), roundto3forl(ljMAKE_avg), roundto3forl(ljlocal_avg), roundto3forl(lj_avg + lmwout_avg), roundto3forl(ljlocal_avg + lmwoutlocal_avg), roundto3forl(lj_avg + lwout_avg), roundto3forl(ljlocal_avg + lwoutlocal_avg), roundto3forl(lnt), modelname ) )
    #
    # s-version of Latex8 gives this Latex15 version -- replaces need for Latex8 and Latex9
    print( "HLatex15: ModelName & $s_{\\rm{}H}$ & $s^{\\rm{}EM}_{\\rm{}H}$ & $s^{\\rm{}MAKE}_{\\rm{}H}$ & $s_{\\rm{}j}$ & $s^{\\rm{}EM}_j$ & $s^{\\rm{}MAKE}_{\\rm{}j}$ & $s^{\\rm{}local}_{\\rm{}j,o}$ & $s_{\\rm{}j+mw,o}$ & $s^{\\rm{}local}_{\\rm{}j+mw,o}$ & $s_{\\rm{}j+w,o}$ & $s^{\\rm{}local}_{\\rm{}j+w,o}$ & $s_{\\rm{}NT}$ \\\\" )
    print( "VLatex15: %s         & %g               & %g                           & %g                             & %g                & %g                   & %g                             & %g                                & %g                     & %g                                   & %g &                  %g                                    & %g                 \\\\ %% %s" % (truemodelname, roundto3forl(sbh_avg), roundto3forl(sbhEM_avg), roundto3forl(sbhMAKE_avg), roundto3forl(sj_avg), roundto3forl(sjEM_avg), roundto3forl(sjMAKE_avg), roundto3forl(sjlocal_avg), roundto3forl(sj_avg + smwout_avg), roundto3forl(sjlocal_avg + smwoutlocal_avg), roundto3forl(sj_avg + swout_avg), roundto3forl(sjlocal_avg + swoutlocal_avg), roundto3forl(snt), modelname ) )
    #
    #
    # 12:
    print( "HLatex9: ModelName & $l_{\\rm{}mw,i}$ & $l^{\\rm{}EM}_{\\rm{}mw,i}$ & $l^{\\rm{}MAKE}_{\\rm{}mw,i}$ & $l_{\\rm{}mw,o}$ & $l^{\\rm{}EM}_{\\rm{}mw,o}$ & $l^{\\rm{}MAKE}_{\\rm{}mw,o}$ & $l_{\\rm{}w,i}$ & $l^{\\rm{}EM}_{\\rm{}w,i}$ & $l^{\\rm{}MAKE}_{\\rm{}w,i}$ & $l_{\\rm{}w,o}$ & $l^{\\rm{}EM}_{\\rm{}w,o}$ & $l^{\\rm{}MAKE}_{\\rm{}w,o}$ \\\\" )
    print( "VLatex9: %s        & %g & %g & %g    & %g & %g & %g   & %g & %g & %g    & %g & %g & %g  \\\\ %% %s" % (truemodelname, roundto3forl(lmwin_avg), roundto3forl(lmwinEM_avg), roundto3forl(lmwinMAKE_avg), roundto3forl(lmwout_avg), roundto3forl(lmwoutEM_avg), roundto3forl(lmwoutMAKE_avg), roundto3forl(lwin_avg), roundto3forl(lwinEM_avg), roundto3forl(lwinMAKE_avg), roundto3forl(lwout_avg), roundto3forl(lwoutEM_avg), roundto3forl(lwoutMAKE_avg), modelname ) )
    #
    #
    # 7:
    print( "HLatex10: ModelName  & $s_{\\rm{}H}$ & $s_{\\rm{}j}$   & $s_{\\rm{}mw,i}$ & $s_{\\rm{}mw,o}$    & $s_{\\rm{}w,i}$ & $s_{\\rm{}w,o}$    & $s_{\\rm{}NT}$ \\\\" )
    print( "VLatex10: %s         & %g & %g   & %g & %g    & %g & %g    & %g \\\\ %% %s" % (truemodelname, roundto2(sbh_avg), roundto2(sj_avg), roundto2(smwin_avg), roundto2(smwout_avg), roundto2(swin_avg), roundto2(swout_avg), roundto2(snt), modelname ) )
    sys.stdout.flush()
    #
    #
    ######################################
    # END PRINT JON WHICHPLOT==4
    ######################################
    #
    #        
    #
    print("eta NEW" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    #######################
    #
    # eta NEW ***
    #
    #######################
    if whichplot == 6:
        etabh = prefactor*pjemtot[:,ihor]/mdotfinavg
        etaj = prefactor*pjke_mu1[:,iofr(rjetout)]/mdotfinavg
        etaw = prefactor*pjke_mumax1[:,iofr(rdiskout)]/mdotfinavg
        #
        etabh2 = prefactor*pjemtot[:,ihor]/mdotiniavg
        etaj2 = prefactor*pjke_mu1[:,iofr(rjetout)]/mdotiniavg
        etaw2 = prefactor*pjke_mumax1[:,iofr(rdiskout)]/mdotiniavg
        #
        if(1 and iti>fti):
            #use mdot averaged over the same time interval for iti<t<=itf
            icond=(ts>=iti)*(ts<=itf)
            etabh[icond]=etabh2[icond]
            etaj[icond]=etaj2[icond]
            etaw[icond]=etaw2[icond]
        if dotavg:
            etaj_avg = timeavg(etaj,ts,fti,ftf)
            etabh_avg = timeavg(etabh,ts,fti,ftf)
            etaw_avg = timeavg(etaw,ts,fti,ftf)
            ptot_avg = timeavg(pjemtot[:,ihor],ts,fti,ftf)
            #
            ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etabh_avg,color=(ofc,fc,fc)) 
            if showextra:
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etaj_avg,'--',color=(fc,fc+0.5*(1-fc),fc)) 
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+etaw_avg,'-.',color=(fc,fc+0.5*(1-fc),fc)) 
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            #,label=r'$\langle P_j\rangle/\langle\dot M\rangle$')
            if(iti>fti):
                etaj2_avg = timeavg(etaj2,ts,iti,itf)
                etabh2_avg = timeavg(etabh2,ts,iti,itf)
                etaw2_avg = timeavg(etaw2,ts,iti,itf)
                ptot2_avg = timeavg(pjemtot[:,ihor],ts,iti,itf)
                #
                ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etabh2_avg,color=(ofc,fc,fc))
                if showextra:
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etaj2_avg,'--',color=(fc,fc+0.5*(1-fc),fc))
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+etaw2_avg,'-.',color=(fc,fc+0.5*(1-fc),fc))
        #
        ax.plot(ts,etabh,clr,label=r'$\eta_{\rm H}$')
        if showextra:
            ax.plot(ts,etaj,'g--',label=r'$\eta_{\rm j}$')
            ax.plot(ts,etaw,'b-.',label=r'$\eta_{\rm w,o}$')
        if findex != None:
            if not isinstance(findex,tuple):
                ax.plot(ts[findex],etabh[findex],'o',mfc='r')
                if showextra:
                    ax.plot(ts[findex],etaj[findex],'gs')
                    ax.plot(ts[findex],etaw[findex],'bv')
            else:
                for fi in findex:
                    ax.plot(ts[fi],etabh[fi],'o',mfc='r')#,label=r'$\dot M$')
                    if showextra:
                        ax.plot(ts[fi],etaw[fi],'bv')#,label=r'$\dot M$')
                        ax.plot(ts[fi],etaj[fi],'gs')#,label=r'$\dot M$')
        #ax.set_ylim(0,2)
        ax.set_xlabel(r'$t\;[r_g/c]$',fontsize=16)
        ax.set_ylabel(r'$\eta\ [\%]$',fontsize=16,ha='left',labelpad=20)
        ax.set_xlim(ts[0],ts[-1])
        if showextra:
            leg= ax.legend(loc='upper left',bbox_to_anchor=(0.02,0.98),ncol=1,borderpad = 0,borderaxespad=0,frameon=True,labelspacing=0)
            # set some legend properties.  All the code below is optional.  The
            # defaults are usually sensible but if you need more control, this
            # shows you how
            #leg = plt.gca().get_legend()
            ltext  = leg.get_texts()  # all the text.Text instance in the legend
            llines = leg.get_lines()  # all the lines.Line2D instance in the legend
            frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend
            # see text.Text, lines.Line2D, and patches.Rectangle for more info on
            # the settable properties of lines, text, and rectangles
            #frame.set_facecolor('0.80')      # set the frame face color to light gray
            plt.setp(ltext, fontsize=12)    # the legend text fontsize
            #plt.setp(llines, linewidth=1.5)      # the legend linewidth
            #leg.draw_frame(False)           # don't draw the legend frame

        print( "whichplot==6 values" )
        print( "eta_H = %g, eta_j = %g, eta_w = %g, eta_jw = %g, mdot = %g, mdotwin=%g, mdotwout=%g, mdotjet=%g, ptot_H = %g" % ( etabh_avg, etaj_avg, etaw_avg, etaj_avg + etaw_avg, mdotfinavg, mdotwinfinavg, mdotwoutfinavg, mdotjetfinavg, ptot_avg ) )
        if iti > fti:
            print( "eta_H2 = %g, eta_j2 = %g, eta_w2 = %g, eta_jw2 = %g, mdot2 = %g, mdotwin2=%g, mdotwout2=%g , mdotjet2=%g, ptot2_H = %g" % ( etabh2_avg, etaj2_avg, etaw2_avg, etaj2_avg + etaw2_avg, mdotiniavg, mdotwininiavg, mdotwoutiniavg, mdotjetiniavg, ptot2_avg ) )

        #xxx
    #######################
    #
    # \Phi ***
    #
    #######################
    print("\Phi plot" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #        
    sashaplot5 = 0
    #
    #
    # For whichplot==5 Plot:
    if whichplot == 5:
        if dotavg:
            if sashaplot5==0:
                if showextra:
                    ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+timeavg(phij**2,ts,fti,ftf)**0.5,'--',color=(fc,fc+0.5*(1-fc),fc))
                    ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+timeavg(phimwout**2,ts,fti,ftf)**0.5,'-.',color=(fc,fc,1))
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+phibh_avg,color=(ofc,fc,fc))
            else:
                ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+phibh_avg,color=(ofc,fc,fc),linestyle=lst)
                #ax.plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+timeavg(phimwout**2,ts,fti,ftf)**0.5,'-.',color=(fc,fc,1))
            #
            if(iti>fti):
                if showextra:
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+timeavg(phij2**2,ts,iti,itf)**0.5,'--',color=(fc,fc+0.5*(1-fc),fc))
                    ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+timeavg(phimwout2**2,ts,iti,itf)**0.5,'-.',color=(fc,fc,1))
                ax.plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+phibh2_avg,color=(ofc,fc,fc))
        #To approximately get efficiency:
        #ax.plot(ts,2./3.*np.pi*omh**2*np.abs(fsj30[:,ihor]/4/np.pi)**2/mdotfinavg)
        #prefactor to get sqrt(eta): (2./3.*np.pi*omh**2)**0.5
        ax.plot(ts,phibh,clr,label=r'$\Upsilon_{\rm H}$')
        ax.set_xlim(ts[0],ts[-1])
        #
        if showextra:
            ax.plot(ts,phij,'g--',label=r'$\Upsilon_{\rm j}$')
            ax.plot(ts,phimwout,'b-.',label=r'$\Upsilon_{\rm mw,o}$')
        if findex != None:
            if not isinstance(findex,tuple):
                if showextra:
                    ax.plot(ts[findex],phij[findex],'gs')
                ax.plot(ts[findex],phibh[findex],'o',mfc='r')
                ax.plot(ts[findex],phimwout[findex],'bv')
            else:
                for fi in findex:
                    if showextra:
                        ax.plot(ts[fi],phij[fi],'gs')
                    ax.plot(ts[fi],phibh[fi],'o',mfc='r')
                    ax.plot(ts[fi],phimwout[fi],'bv')
        ax.set_ylabel(r'$\Upsilon$',fontsize=16,ha='left',labelpad=20)
        if showextra:
            leg=ax.legend(loc='upper left',bbox_to_anchor=(0.02,0.98),ncol=1,borderpad = 0,borderaxespad=0,frameon=True,labelspacing=0)
            # set some legend properties.  All the code below is optional.  The
            # defaults are usually sensible but if you need more control, this
            # shows you how
            #leg = plt.gca().get_legend()
            ltext  = leg.get_texts()  # all the text.Text instance in the legend
            llines = leg.get_lines()  # all the lines.Line2D instance in the legend
            frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend
            # see text.Text, lines.Line2D, and patches.Rectangle for more info on
            # the settable properties of lines, text, and rectangles
            #frame.set_facecolor('0.80')      # set the frame face color to light gray
            plt.setp(ltext, fontsize=12)    # the legend text fontsize
            #plt.setp(llines, linewidth=1.5)      # the legend linewidth
            #leg.draw_frame(False)           # don't draw the legend frame
        #
        plt.setp( ax.get_xticklabels(), visible=False )
    #
    # End of whichplot==5
    #
    ######################################
    # BEGIN PRINT JON WHICHPLOT==5
    ######################################
    print("Print whichplot==5" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    # Begin print-out of Upsilon (phibh[G]/5) values:
    print( "Upsilon_H = %g, Upsilon_rdiskin = %g , Upsilon_rdiskout = %g, fstot = %g, fsmaxtot = %g, fsuphalf = %g" % ( phibh_avg, phirdiskin_avg, phirdiskout_avg, fstot_avg, fsmaxtot_avg, fsuphalf_avg ) )
    print( "Upsilon_jet = %g, Upsilon_mw,i = %g, Upsilon_mw,o = %g, Upsilon_w,i = %g, Upsilon_w,o = %g" % ( phij_avg , phimwin_avg , phimwout_avg, phiwin_avg , phiwout_avg ) )
    print( "Upsilon_jetn = %g, Upsilon_jets = %g" % ( phijn_avg , phijs_avg ) )
    if iti > fti:
        print( "incomplete output: %g %g" % (iti, fti) )
    #
    #
    # 13:
    print( "HLatex11: ModelName & $\\Upsilon_{\\rm{}H}$ & $\\Upsilon_{\\rm{}in,i}$ & $\\Upsilon_{\\rm{}in,o}$ & $\\Upsilon_{\\rm{}j}$   & $\\Upsilon_{\\rm{}mw,i}$ & $\\Upsilon_{\\rm{}mw,o}$ & $\\Upsilon_{\\rm{}w,i}$ & $\\Upsilon_{\\rm{}w,o}$    &  $\\left|\\frac{\\Psi_{\\rm{}H}}{\\Psi_1(t=0)}\\right|$ & $\\left|\\frac{\\Psi_{\\rm{}H}}{\\Psi_2(t=0)}\\right|$ & $\\left|\\frac{\\Psi_{\\rm{}H}}{\\Psi_3(t=0)}\\right|$ & $\\left|\\frac{\\Psi_{\\rm{}H}}{\\Psi_a}\\right|$ & $\\left|\\frac{\\Psi_{\\rm{}H}}{\\Psi_s}\\right|$ & $\\left|\\frac{\\Phi_{\\rm{}H}}{\\Psi_{\\rm{}fH}}\\right|$ \\\\" )
    print( "VLatex11: %s         & %g    & %g & %g       & %g      & %g & %g      & %g & %g   & %s & %s & %s & %g & %g & %g  \\\\ %% %s" % (truemodelname, roundto2forupsilon(phibh_avg), roundto2forupsilon(phirdiskin_avg), roundto2forupsilon(phirdiskout_avg), roundto2forupsilon(phij_avg), roundto2forupsilon(phimwin_avg), roundto2forupsilon(phimwout_avg), roundto2forupsilon(phiwin_avg), roundto2forupsilon(phiwout_avg), roundto2forphistring(fstotnormA_avg[0]),roundto2forphistring(fstotnormA_avg[1]),roundto2forphistring(fstotnormA_avg[2]),roundto2forphi(fstotnormgenC_avg),roundto2forphi(fstotnormgenE_avg),roundto2forphi(fstotnormgenD_avg), modelname ) )
    # switched from B->E in above since E uses actual instantaneous flux (average) [rather than t=0 values of flux] to normalize the H flux.  More conservative given dissipatin can/does occur.
    sys.stdout.flush()
    #
    ######################################
    # END PRINT JON WHICHPLOT==5
    ######################################
    #
    #
    ######################################
    # BEGIN RESIDUAL PLOTS
    ######################################
    print("residual" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    #
    #
    if whichplot == -1:
        etajetavg = pjetfinavg/mdotfinavg
        foutpower = open( "pjet_power_%s.txt" %  os.path.basename(os.getcwd()), "w" )
        #foutpower.write( "#Name a Mdot   Pjet    Etajet  Psitot Psisqtot**0.5 Psijet Psisqjet**0.5 rstag Pjtotmax Pjtot1rstag Pjtot2rstag Pjtot4rstag Pjtot8rstag\n"  )
        foutpower.write( "%s %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" % (os.path.basename(os.getcwd()), a, mdotfinavg, 
                                                                       pjetfinavg, etajetavg, fstotfinavg, 
                                                                       fstotsqfinavg, fsj30finavg, fsj30sqfinavg, 
                                                                       rstag, pjtotfinavgvsr5max, pjtotfinavgvsr5rstag, 
                                                                       pjtotfinavgvsr5r2stag, pjtotfinavgvsr5r4stag, pjtotfinavgvsr5r8stag) )
        #flush to disk just in case to make sure all is written
        foutpower.flush()
        os.fsync(foutpower.fileno())
        foutpower.close()
        return( mdotfinavg, fstotfinavg, fstotsqfinavg, fsj30finavg, fsj30sqfinavg, pjemfinavgtot )

    if whichplot == -2:
        return( mdtotvsr, edtotvsr, edmavsr, ldtotvsr )

    if whichplot == -300:
        #BL metric g_rr
        rh = 1+(1-a**2)**0.5
        r1d = r[:,0,0]
        Sigma = r**2+a**2*np.cos(h)**2
        Delta = r**2-2*r+a**2
        gdrr = Sigma/Delta
        gdtt = -(1-2*r/Sigma)
        #
        uutKS = uu[0]
        uurKS = dxdxp[1,1]*uu[1]
        uuhKS = dxdxp[2,2]*uu[2] + dxdxp[2,1]*uu[1]
        uupKS = dxdxp[3,3]*uu[3]
        uurBL = uurKS
        uutBL = uutKS - 2*(r/Delta)*uurKS - (a/Delta) * uupKS
        vurBL = uurBL / uutBL
        vrBL = gdrr**0.5*vurBL 
        plt.figure(2)
        plt.loglog( r1d, -vrBL[:,ny/2].mean(-1), 'r', label=r"$t=%g$" % t )
        plt.xlim( rh, 100 )
        plt.ylim( 1e-3, 2 )
        plt.legend( loc = 'lower left' )
       
    if whichplot == -3:
        #BL metric g_rr
        rh = 1+(1-a**2)**0.5
        r1d = r[:,0,0]
        Sigma = r**2+a**2*np.cos(h)**2
        Delta = r**2-2*r+a**2
        gdrr = Sigma/Delta
        gdtt = -(1-2*r/Sigma)
        #
        uutKS = uu02h
        uurKS = dxdxp[1,1,None,:,ny/2,0]*uus12h
        uupKS = dxdxp[3,3,None,:,ny/2,0]*uus32h
        uurBL = uurKS
        uutBL = uutKS - 2*(r/Delta)[None,:,ny/2,0]*uurKS - (a/Delta)[None,:,ny/2,0] * uupKS
        vurBL = uurBL / uutBL
        vrBL = gdrr[None,:,ny/2,0]**0.5*vurBL 
        t1 = 0.5e4
        t2 = 1e4
        avg1_vr = timeavg(vrBL,ts,t1,t2) 
        t1 = 1e4
        t2 = 1.5e4
        avg2_vr = timeavg(vrBL,ts,t1,t2) 
        t1 = 1.5e4
        t2 = 2e4
        avg3_vr = timeavg(vrBL,ts,t1,t2) 
        plt.figure(1)
        plt.loglog( r1d, -avg1_vr, 'r', label=r"$5,000<t<10,000$" )
        plt.loglog( r1d, -avg2_vr, 'g', label=r"$10,000<t<15,000$" )
        plt.loglog( r1d, -avg3_vr, 'b', label=r"$15,000<t<20,000$" )
        plt.xlim( rh, 200 )
        plt.ylim( 1e-3, 2 )
        plt.grid()
        plt.ylabel( r"$v_{\hat r}$", fontsize = 20 )
        plt.xlabel( r"$r$", fontsize = 20 )
        plt.legend( loc = 'upper right' )

    if whichplot == -4:
        rh = 1+(1-a**2)**0.5
        r1d = r[:,0,0]
        plt.figure(1)
        plt.loglog( r1d, timeavg(rhos2h,ts,5000,10000), 'r', label=r"$5,000<t<10,000$" )
        plt.loglog( r1d, timeavg(rhos2h,ts,10000,15000), 'g', label=r"$10,000<t<15,000$" )
        plt.loglog( r1d, timeavg(rhos2h,ts,15000,20000), 'b', label=r"$15,000<t<20,000$" )
        plt.xlabel(r"$r$", fontsize = 15)
        plt.ylabel(r"$\rho$", fontsize = 15)
        plt.xlim( rh, 100 )
        plt.ylim( 1e-2, 15 )
        plt.grid()
        plt.legend( loc = 'lower left' )

    #if whichplot == -5:
        
    if whichplot == None:
        fig,plotlist=plt.subplots(nrows=4,ncols=1,sharex=True,figsize=(12,16),num=1)
        #plt.clf()
        plottitle = "a = %g: %s" % ( a, os.path.basename(os.getcwd()) )
        plt.suptitle( plottitle )
        plt.subplots_adjust(hspace=0.1) #increase vertical spacing to avoid crowding
        print fstot[:,ihor].shape
        plotlist[0].plot(ts,fstot[:,ihor],label=r'$\Phi_{\rm h,tot}$')
        #plotlist[0].plot(ts,fsj5[:,ihor],label=r'$\Phi_{\rm h,5}$')
        plotlist[0].plot(ts,fsj30[:,ihor],label=r'$\Phi_{\rm h,30}$')
        #plotlist[0].plot(ts,fs,'r+') #, label=r'$\Phi_{\rm h}/0.5\Phi_{\rm i}$: Data Points')
        if dotavg:
            plotlist[0].plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+fstotsqfinavg,label=r'$\langle \Phi^2_{\rm h,tot}\rangle^{1/2}$')
            plotlist[0].plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+fsj30sqfinavg,label=r'$\langle \Phi^2_{\rm h,30}\rangle^{1/2}$')
        plotlist[0].legend(loc='upper left')
        #plt.xlabel(r'$t\;(r_g/c)$')
        plotlist[0].set_ylabel(r'$\Phi_{\rm h}$',fontsize=16)
        plt.setp( plotlist[0].get_xticklabels(), visible=False)
        plotlist[0].grid(True)
        #
        #plotlist[1].subplot(212,sharex=True)
        #plotlist[1].plot(ts,np.abs(mdtot[:,ihor]),label=r'$\dot M_{\rm h,tot}$')
        #plotlist[1].plot(ts,np.abs(mdtot[:,ihor]-md5[:,ihor]),label=r'$\dot M_{\rm h,tot,bsqorho<5}$')
        plotlist[1].plot(ts,np.abs(mdtot[:,ihor]-md10[:,ihor]),label=r'$\dot M_{{\rm h,tot}, b^2/rho<10}$')
        plotlist[1].plot(ts,np.abs(mdtot[:,ihor]-md30[:,ihor]),label=r'$\dot M_{{\rm h,tot}, b^2/rho<30}$')
        if dotavg:
            #plotlist[1].plot(ts[(ts<=itf)*(ts>=iti)],0*ts[(ts<=itf)*(ts>=iti)]+mdotiniavg,label=r'$\langle \dot M_{{\rm h,tot}, b^2/\rho<10}\rangle_{i}$')
            plotlist[1].plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+mdotfinavg,label=r'$\langle \dot M_{{\rm h,tot}, b^2/\rho<10}\rangle_{f}$')
        #plotlist[1].plot(ts,np.abs(md2h[:,ihor]),label=r'$\dot M_{\rm h,2h}$')
        #plotlist[1].plot(ts,np.abs(md4h[:,ihor]),label=r'$\dot M_{\rm h,4h}$')
        #plotlist[1].plot(ts,np.abs(mdhor[:,ihor]),label=r'$\dot M_{\rm h,hor}$')
        #plotlist[1].plot(ts,np.abs(mdrhosq[:,ihor]),label=r'$\dot M_{\rm h,rhosq}$')
        #plotlist[1].plot(ts,np.abs(md5[:,ihor]),label=r'$\dot M_{\rm h,5}$')
        plotlist[1].plot(ts,np.abs(md10[:,ihor]),label=r'$\dot M_{\rm h,10}$')
        plotlist[1].plot(ts,np.abs(md30[:,ihor]),label=r'$\dot M_{\rm h,30}$')
        #plotlist[1].plot(ts,np.abs(md[:,ihor]),'r+') #, label=r'$\dot M_{\rm h}$: Data Points')
        plotlist[1].legend(loc='upper left')
        #plotlist[1].set_xlabel(r'$t\;(r_g/c)$')
        plotlist[1].set_ylabel(r'$\dot M_{\rm h}$',fontsize=16)
        plt.setp( plotlist[1].get_xticklabels(), visible=False)

        #plotlist[2].plot(ts,(pjem10[:,ihor]),label=r'$P_{\rm j,em10}$')
        #plotlist[2].plot(ts,(pjem30[:,ihor]),label=r'$P_{\rm j,em30}$')
        if dotavg:
            plotlist[2].plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+pjetfinavg,label=r'$\langle P_{{\rm j,em30}\rangle_{f}}$')
        plotlist[2].legend(loc='upper left')
        #plotlist[2].set_xlabel(r'$t\;(r_g/c)$')
        plotlist[2].set_ylabel(r'$P_{\rm j}$',fontsize=16)

        #plotlist[3].plot(ts,(pjem10[:,ihor]/mdtot[:,ihor]),label=r'$P_{\rm j,em10}/\dot M_{\rm tot}$')
        plotlist[3].plot(ts,(pjem5[:,ihor]/(mdtot[:,ihor]-md5[:,ihor])),label=r'$P_{\rm j,em5}/\dot M_{{\rm tot},b^2/\rho<5}$')
        #plotlist[3].plot(ts,(pjem30[:,ihor]/mdotfinavg),label=r'$\dot \eta_{10}=P_{\rm j,em10}/\dot M_{{\rm tot},b^2/\rho<30}$')
        if dotavg:
            #plotlist[3].plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+pjetfinavg/mdotiniavg,label=r'$\langle P_j\rangle/\langle\dot M_i\rangle_{f}$')
            plotlist[3].plot(ts[(ts<=ftf)*(ts>=fti)],0*ts[(ts<=ftf)*(ts>=fti)]+pjetfinavg/mdotfinavg,'r',label=r'$\langle P_j\rangle/\langle\dot M_f\rangle_{f}$')
        #plotlist[3].set_ylim(0,6)
        plotlist[3].legend(loc='upper left')
        plotlist[3].set_xlabel(r'$t\;(r_g/c)$')
        #plotlist[3].set_ylabel(r'$P_{\rm j}/\dot M_{\rm h}$',fontsize=16)
        plotlist[3].set_ylabel(r'$\eta_{\rm j}$',fontsize=16)

        #title("\TeX\ is Number $\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!", 
        #      fontsize=16, color='r')
        plotlist[0].grid(True)
        plotlist[1].grid(True)
        plotlist[2].grid(True)
        plotlist[3].grid(True)
        fig.savefig('pjet1_%s.pdf' % os.path.basename(os.getcwd()) )

        #density/velocity/hor figure
        #!!!rhor=1+(1-a**2)**0.5
        fig,plotlist=plt.subplots(nrows=4,ncols=1,sharex=True,figsize=(12,16),num=2)
        #plt.clf()
        plottitle = r"$\rho$,$u^r$,$h/r$: $a= $%g: %s" % ( a, os.path.basename(os.getcwd()) )
        plt.suptitle( plottitle )
        plt.subplots_adjust(hspace=0.1) #increase vertical spacing to avoid crowding
        #print fstot[:,ihor].shape
        plotlist[0].plot(ts,hoverr[:,ihor],label=r'$(h/r)_{\rm h}$')
        plotlist[0].plot(ts,hoverr[:,iofr(2)],label=r'$(h/r)_{\rm 2}$') ##### continue here
        plotlist[0].plot(ts,hoverr[:,iofr(4)],label=r'$(h/r)_{\rm 4}$')
        plotlist[0].plot(ts,hoverr[:,iofr(8)],label=r'$(h/r)_{\rm 8}$')
        #lotlist[0].plot(ts,hoverr[:,iofr(10)],label=r'$(h/r)_{\rm 10}$')
        #plotlist[0].plot(ts,hoverr[:,iofr(12)],label=r'$(h/r)_{\rm 12}$')
        #plotlist[0].plot(ts,hoverr[:,iofr(15)],label=r'$(h/r)_{\rm 15}$')
        #thetamid
        plotlist[0].plot(ts,(thetamid-np.pi/2)[:,ihor],'--',label=r'$\theta_{\rm h}$')
        plotlist[0].plot(ts,(thetamid-np.pi/2)[:,iofr(2)],'--',label=r'$\theta_{\rm 2}$') ##### continue here
        plotlist[0].plot(ts,(thetamid-np.pi/2)[:,iofr(4)],'--',label=r'$\theta_{\rm 4}$')
        plotlist[0].plot(ts,(thetamid-np.pi/2)[:,iofr(8)],'--',label=r'$\theta_{\rm 8}$')
        #plotlist[0].plot(ts,(thetamid-np.pi/2)[:,iofr(10)],'--',label=r'$\theta_{\rm 10}$')
        #plotlist[0].plot(ts,(thetamid-np.pi/2)[:,iofr(12)],'--',label=r'$\theta_{\rm 12}$')
        #plotlist[0].plot(ts,(thetamid-np.pi/2)[:,iofr(15)],'--',label=r'$\theta_{\rm 15}$')
        #plotlist[0].plot(ts,fs,'r+') #, label=r'$\Phi_{\rm h}/0.5\Phi_{\rm i}$: Data Points')
        #legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plotlist[0].legend(loc='upper right',ncol=4)
        #plt.xlabel(r'$t\;(r_g/c)$')
        plotlist[0].set_ylabel(r'$h/r$',fontsize=16)
        plt.setp( plotlist[0].get_xticklabels(), visible=False)
        plotlist[0].grid(True)
        #
        #plotlist[1].subplot(212,sharex=True)
        plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,ihor],label=r'$-u^r_{\rm h}$')
        plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,iofr(2)],label=r'$-u^r_{\rm 2}$') ##### continue here
        plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,iofr(4)],label=r'$-u^r_{\rm 4}$')
        plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,iofr(8)],label=r'$-u^r_{\rm 8}$')
        #plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,iofr(10)],label=r'$-u^r_{\rm 10}$')
        #plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,iofr(12)],label=r'$-u^r_{\rm 12}$')
        #plotlist[1].plot(ts,(-vus1hor*dxdxp[1][1][:,0,0])[:,iofr(15)],label=r'$-u^r_{\rm 15}$')
        plotlist[1].legend(loc='upper right')
        #plotlist[1].set_xlabel(r'$t\;(r_g/c)$')
        plotlist[1].set_ylabel(r'$u^r$',fontsize=16)
        plt.setp( plotlist[1].get_xticklabels(), visible=False)

        plotlist[2].plot(ts,rhoshor[:,ihor],label=r'$\rho_{\rm h}$')
        plotlist[2].plot(ts,rhoshor[:,iofr(2)],label=r'$\rho_{\rm 2}$') ##### continue here
        plotlist[2].plot(ts,rhoshor[:,iofr(4)],label=r'$\rho_{\rm 4}$')
        plotlist[2].plot(ts,rhoshor[:,iofr(8)],label=r'$\rho_{\rm 8}$')
        #plotlist[2].plot(ts,rhoshor[:,iofr(10)],label=r'$\rho_{\rm 10}$')
        #plotlist[2].plot(ts,rhoshor[:,iofr(12)],label=r'$\rho_{\rm 12}$')
        #plotlist[2].plot(ts,rhoshor[:,iofr(15)],label=r'$\rho_{\rm 15}$')
        plotlist[2].legend(loc='upper left')
        #plotlist[2].set_xlabel(r'$t\;(r_g/c)$')
        plotlist[2].set_ylabel(r'$\rho$',fontsize=16)

        plotlist[3].plot(ts,(ugshor/rhoshor)[:,ihor],label=r'$u^r_{\rm h}$')
        plotlist[3].plot(ts,(ugshor/rhoshor)[:,iofr(2)],label=r'$u^r_{\rm 2}$') ##### continue here
        plotlist[3].plot(ts,(ugshor/rhoshor)[:,iofr(4)],label=r'$u^r_{\rm 4}$')
        plotlist[3].plot(ts,(ugshor/rhoshor)[:,iofr(8)],label=r'$u^r_{\rm 8}$')
        #plotlist[3].plot(ts,(ugshor/rhoshor)[:,iofr(10)],label=r'$u^r_{\rm 10}$')
        #plotlist[3].plot(ts,(ugshor/rhoshor)[:,iofr(12)],label=r'$u^r_{\rm 12}$')
        #plotlist[3].plot(ts,(ugshor/rhoshor)[:,iofr(15)],label=r'$u^r_{\rm 15}$')
        plotlist[3].legend(loc='upper left')
        plotlist[3].set_xlabel(r'$t\;(r_g/c)$')
        plotlist[3].set_ylabel(r'$u_g/\rho$',fontsize=16)

        #title("\TeX\ is Number $\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!", 
        #      fontsize=16, color='r')
        plotlist[0].grid(True)
        plotlist[1].grid(True)
        plotlist[2].grid(True)
        plotlist[3].grid(True)
        fig.savefig('pjet2_%s.pdf' % os.path.basename(os.getcwd()) )
    
        plt.figure(3)
        plt.clf()
        plt.plot(r[:,0,0],mdotfinavgvsr,label=r'$\dot M_{\rm tot}$')
        plt.plot(r[:,0,0],mdotfinavgvsr5,label=r'$\dot M_{b^2/\rho<5}$')
        plt.plot(r[:,0,0],mdotfinavgvsr10,label=r'$\dot M_{b^2/\rho<10}$')
        plt.plot(r[:,0,0],mdotfinavgvsr20,label=r'$\dot M_{b^2/\rho<20}$')
        plt.plot(r[:,0,0],mdotfinavgvsr30,label=r'$\dot M_{b^2/\rho<30}$')
        plt.plot(r[:,0,0],mdotfinavgvsr40,label=r'$\dot M_{b^2/\rho<40}$')
        plt.xlim(1+(1-a**2)**0.5,20)
        plt.ylim(0,np.max(mdotfinavgvsr[r[:,0,0]<20]))
        plt.legend(loc='lower right')
        plt.grid()
        plt.savefig('pjet3_%s.pdf' % os.path.basename(os.getcwd()) )

        plt.figure(4)
        plt.clf()
        rmax=50
        plt.plot(r[:,0,0],pjemfinavgvsr,'b',label=r'$\dot Pem_{\rm tot}$')
        plt.plot(r[:,0,0],pjemfinavgvsr5,'g',label=r'$\dot Pem_{b^2/\rho>5}$')
        #plt.plot(r[:,0,0],pjemfinavgvsr10,'r',label=r'$\dot Pem_{b^2/\rho>10}$')
        #plt.plot(r[:,0,0],pjemfinavgvsr20,'c',label=r'$\dot Pem_{b^2/\rho>20}$')
        #plt.plot(r[:,0,0],pjemfinavgvsr30,'m',label=r'$\dot Pem_{b^2/\rho>30}$')
        #plt.plot(r[:,0,0],pjemfinavgvsr40,'y',label=r'$\dot Pem_{b^2/\rho>40}$')
        plt.plot(r[:,0,0],pjtotfinavgvsr,'b--',label=r'$\dot P_{\rm tot}$')
        plt.plot(r[:,0,0],pjtotfinavgvsr5,'g--',label=r'$\dot P_{b^2/\rho>5}$')
        #plt.plot(r[:,0,0],pjtotfinavgvsr10,'r--',label=r'$\dot P_{b^2/\rho>10}$')
        #plt.plot(r[:,0,0],pjtotfinavgvsr20,'c--',label=r'$\dot P_{b^2/\rho>20}$')
        #plt.plot(r[:,0,0],pjtotfinavgvsr30,'m--',label=r'$\dot P_{b^2/\rho>30}$')
        #plt.plot(r[:,0,0],pjtotfinavgvsr40,'y--',label=r'$\dot P_{b^2/\rho>40}$')
        plt.xlim(1+(1-a**2)**0.5,rmax)
        plt.ylim(0,np.max(pjemfinavgvsr[r[:,0,0]<rmax]))
        plt.legend(loc='lower right',ncol=2)
        plt.grid()
        plt.savefig('pjet4_%s.pdf' % os.path.basename(os.getcwd()) )

        plt.figure(5)
        plt.clf()
        rmax=200
        plt.plot(r[:,0,0],phiabsj_mu1vsr,'b',label=r'$\Phi_{\rm j}$')
        plt.xlim(1+(1-a**2)**0.5,rmax)
        plt.ylim(0,np.max(phiabsj_mu1vsr[r[:,0,0]<rmax]))
        plt.legend(loc='lower right',ncol=2)
        plt.grid()
        plt.savefig('phi1_%s.pdf' % os.path.basename(os.getcwd()) )
    #
    #
    print("done with residual" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #######################################
    # Begin full results output
    #######################################
    if fullresultsoutput==0:
        # GODMARK: maybe split calculation and prints/writes, so the below isn't a duplicate calculation
        # used by some whichplot=None cases
        hoverr_jet_vsr=np.zeros(nx,dtype=r.dtype)
        for ii in np.arange(0,nx):
            hoverr_jet_vsr[ii]=timeavg(hoverr_jet[:,ii],ts,fti,ftf)
        return(hoverr_jet_vsr)
    #
    #
    #######################################
    #
    #
    #
    ######################################
    # BEGIN data vs r and \theta and space-time plots
    ######################################
    #
    dodatavsrh=1
    dodatavst=1
    dopowervsmplots=makepowervsmplots
    dospacetimeplots=makespacetimeplots
    dofftplot=makefftplot
    dospecplot=makespecplot
    doinitfinalplot=makeinitfinalplot
    dothradfinalplot=makethradfinalplot
    #
    if 1==0:
        # for easy conversion of existing data to quasi-orthonormal basis
        # ok, not so easy -- easier to just redo full calculation with correction
        sigmaks=r**2+(a*np.cos(h))**2
        deltaks=r**2-2*r+a**2
        Aks=(r**2+a**2)**2-a**2*deltaks*(np.sin(h))**2
        #
        gvks00=-(1.0-2.0*r/sigmaks)
        gvks11=(1.0+2.0*r/sigmaks)
        gvks22=sigma
        gvks33=(np.sin(h))**2*(sigmaks + a**2*(1.0 + 2.0*r/sigmaks)*(np.sin(h))**2)
        #
        sqrtgv311_vsr=np.zeros(nx,dtype=r.dtype)
        sqrtgv311_vsr=np.sqrt(gvks11[:,ny/2,0])
        sqrtgv322_vsr=np.zeros(nx,dtype=r.dtype)
        sqrtgv322_vsr=np.sqrt(gvks22[:,ny/2,0])
        sqrtgv333_vsr=np.zeros(nx,dtype=r.dtype)
        gv333_vsr=np.sqrt(gvks33[:,ny/2,0])
    #
    #
    if dodatavsrh==1:
        print("dodatavsrh==1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        #
        #
        #
        favg1 = open('datavsrhead.txt', 'w')
        favg1.write("%d %g %s %g\n" % (iin1,rfitin1,iout1,rfitout1))
        favg1.write("%d %g %s %g\n" % (iin2,rfitin2,iout2,rfitout2))
        favg1.write("%d %g %s %g\n" % (iin3,rfitin3,iout3,rfitout3))
        favg1.write("%d %g %s %g\n" % (iin4,rfitin4,iout4,rfitout4))
        favg1.write("%d %g %s %g\n" % (iin5,rfitin5,iout5,rfitout5))
        favg1.write("%d %g %s %g\n" % (iin6,rfitin6,iout6,rfitout6))
        favg1.close()
        #
        #
        #
        ###################
        # r1 (rho,u over non-jet, v,B over whole flow)
        ###################
        #
        rhosrhosq_vsr=np.zeros(nx,dtype=r.dtype)
        ugsrhosq_vsr=np.zeros(nx,dtype=r.dtype)
        uu0rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        vus1rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        vuas1rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        vus3rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        vuas3rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        Bs1rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        Bas1rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        Bs2rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        Bas2rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        Bs3rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        Bas3rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bs1rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bas1rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bs2rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bas2rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bs3rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bas3rhosq_vsr=np.zeros(nx,dtype=r.dtype)
        bsqrhosq_vsr=np.zeros(nx,dtype=r.dtype)
        #
        #
        favg1 = open('datavsr1.txt', 'w')
        favg1.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","rhosrhosq_vsr","ugsrhosq_vsr","uu0rhosq_vsr","vus1rhosq_vsr","vuas1rhosq_vsr","vus3rhosq_vsr","vuas3rhosq_vsr","Bs1rhosq_vsr","Bas1rhosq_vsr","Bs2rhosq_vsr","Bas2rhosq_vsr","Bs3rhosq_vsr","Bas3rhosq_vsr","bs1rhosq_vsr","bas1rhosq_vsr","bs2rhosq_vsr","bas2rhosq_vsr","bs3rhosq_vsr","bas3rhosq_vsr","bsqrhosq_vsr" ) )
        for ii in np.arange(0,nx):
            #
            # Q vs r
            # 2+20
            rhosrhosq_vsr[ii]=timeavg(rhosrhosq[:,ii],ts,fti,ftf)
            ugsrhosq_vsr[ii]=timeavg(ugsrhosq[:,ii],ts,fti,ftf)
            uu0rhosq_vsr[ii]=timeavg(uu0rhosq[:,ii],ts,fti,ftf)
            vus1rhosq_vsr[ii]=timeavg(vus1rhosq[:,ii],ts,fti,ftf)
            vuas1rhosq_vsr[ii]=timeavg(vuas1rhosq[:,ii],ts,fti,ftf)
            vus3rhosq_vsr[ii]=timeavg(vus3rhosq[:,ii],ts,fti,ftf)
            vuas3rhosq_vsr[ii]=timeavg(vuas3rhosq[:,ii],ts,fti,ftf)
            Bs1rhosq_vsr[ii]=timeavg(Bs1rhosq[:,ii],ts,fti,ftf)
            Bas1rhosq_vsr[ii]=timeavg(Bas1rhosq[:,ii],ts,fti,ftf)
            Bs2rhosq_vsr[ii]=timeavg(Bs2rhosq[:,ii],ts,fti,ftf)
            Bas2rhosq_vsr[ii]=timeavg(Bas2rhosq[:,ii],ts,fti,ftf)
            Bs3rhosq_vsr[ii]=timeavg(Bs3rhosq[:,ii],ts,fti,ftf)
            Bas3rhosq_vsr[ii]=timeavg(Bas3rhosq[:,ii],ts,fti,ftf)
            bs1rhosq_vsr[ii]=timeavg(bs1rhosq[:,ii],ts,fti,ftf)
            bas1rhosq_vsr[ii]=timeavg(bas1rhosq[:,ii],ts,fti,ftf)
            bs2rhosq_vsr[ii]=timeavg(bs2rhosq[:,ii],ts,fti,ftf)
            bas2rhosq_vsr[ii]=timeavg(bas2rhosq[:,ii],ts,fti,ftf)
            bs3rhosq_vsr[ii]=timeavg(bs3rhosq[:,ii],ts,fti,ftf)
            bas3rhosq_vsr[ii]=timeavg(bas3rhosq[:,ii],ts,fti,ftf)
            bsqrhosq_vsr[ii]=timeavg(bsqrhosq[:,ii],ts,fti,ftf)
            #
            favg1.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],rhosrhosq_vsr[ii],ugsrhosq_vsr[ii],uu0rhosq_vsr[ii],vus1rhosq_vsr[ii],vuas1rhosq_vsr[ii],vus3rhosq_vsr[ii],vuas3rhosq_vsr[ii],Bs1rhosq_vsr[ii],Bas1rhosq_vsr[ii],Bs2rhosq_vsr[ii],Bas2rhosq_vsr[ii],Bs3rhosq_vsr[ii],Bas3rhosq_vsr[ii],bs1rhosq_vsr[ii],bas1rhosq_vsr[ii],bs2rhosq_vsr[ii],bas2rhosq_vsr[ii],bs3rhosq_vsr[ii],bas3rhosq_vsr[ii],bsqrhosq_vsr[ii] ) )
            #
        favg1.close()
        #
        # 
        #
        #" *\(.*vsr\).*" -> "        \1_fit=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(\1[iin2:iout2])),1,dologx=1,dology=1,doabs=1)"
        #
        # then for goodness stuff do:
        # Query replace regexp (default \( *\)\(.*_fit\)\( *=.*\) -> \1(\2,\2sigma,\2goodness)\3):
        #
        # get fit
        print("rhosrhosq numfit=%d" % (numfit)) ; sys.stdout.flush()
        (rhosrhosq_vsr_fit,rhosrhosq_vsr_fitsigma,rhosrhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(rhosrhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (ugsrhosq_vsr_fit,ugsrhosq_vsr_fitsigma,ugsrhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(ugsrhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (uu0rhosq_vsr_fit,uu0rhosq_vsr_fitsigma,uu0rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(uu0rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus1rhosq_vsr_fit,vus1rhosq_vsr_fitsigma,vus1rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus1rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas1rhosq_vsr_fit,vuas1rhosq_vsr_fitsigma,vuas1rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas1rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus3rhosq_vsr_fit,vus3rhosq_vsr_fitsigma,vus3rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus3rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas3rhosq_vsr_fit,vuas3rhosq_vsr_fitsigma,vuas3rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas3rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs1rhosq_vsr_fit,Bs1rhosq_vsr_fitsigma,Bs1rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs1rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas1rhosq_vsr_fit,Bas1rhosq_vsr_fitsigma,Bas1rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas1rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs2rhosq_vsr_fit,Bs2rhosq_vsr_fitsigma,Bs2rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs2rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas2rhosq_vsr_fit,Bas2rhosq_vsr_fitsigma,Bas2rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas2rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs3rhosq_vsr_fit,Bs3rhosq_vsr_fitsigma,Bs3rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs3rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas3rhosq_vsr_fit,Bas3rhosq_vsr_fitsigma,Bas3rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas3rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs1rhosq_vsr_fit,bs1rhosq_vsr_fitsigma,bs1rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs1rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas1rhosq_vsr_fit,bas1rhosq_vsr_fitsigma,bas1rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas1rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs2rhosq_vsr_fit,bs2rhosq_vsr_fitsigma,bs2rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs2rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas2rhosq_vsr_fit,bas2rhosq_vsr_fitsigma,bas2rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas2rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs3rhosq_vsr_fit,bs3rhosq_vsr_fitsigma,bs3rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs3rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas3rhosq_vsr_fit,bas3rhosq_vsr_fitsigma,bas3rhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas3rhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqrhosq_vsr_fit,bsqrhosq_vsr_fitsigma,bsqrhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqrhosq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (brhosq_vsr_fit,brhosq_vsr_fitsigma,brhosq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.sqrt(np.fabs(bsqrhosq_vsr[iin2:iout2]))),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        #
        ###################
        # r1b (all over non-jet in strict sense of bsq/rho<1 only)
        ###################
        #
        rhosrhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        ugsrhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        uu0rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        vus1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        vus3rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bs1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bas1rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bs2rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bas2rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bs3rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bas3rhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        bsqrhosqdc_vsr=np.zeros(nx,dtype=r.dtype)
        #
        favg1b = open('datavsr1b.txt', 'w')
        favg1b.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","rhosrhosqdc_vsr","ugsrhosqdc_vsr","uu0rhosqdc_vsr","vus1rhosqdc_vsr","vuas1rhosqdc_vsr","vus3rhosqdc_vsr","vuas3rhosqdc_vsr","Bs1rhosqdc_vsr","Bas1rhosqdc_vsr","Bs2rhosqdc_vsr","Bas2rhosqdc_vsr","Bs3rhosqdc_vsr","Bas3rhosqdc_vsr","bs1rhosqdc_vsr","bas1rhosqdc_vsr","bs2rhosqdc_vsr","bas2rhosqdc_vsr","bs3rhosqdc_vsr","bas3rhosqdc_vsr","bsqrhosqdc_vsr" ) )
        for ii in np.arange(0,nx):
            #
            # Q vs r
            # 2+20
            rhosrhosqdc_vsr[ii]=timeavg(rhosrhosqdc[:,ii],ts,fti,ftf)
            ugsrhosqdc_vsr[ii]=timeavg(ugsrhosqdc[:,ii],ts,fti,ftf)
            uu0rhosqdc_vsr[ii]=timeavg(uu0rhosqdc[:,ii],ts,fti,ftf)
            vus1rhosqdc_vsr[ii]=timeavg(vus1rhosqdc[:,ii],ts,fti,ftf)
            vuas1rhosqdc_vsr[ii]=timeavg(vuas1rhosqdc[:,ii],ts,fti,ftf)
            vus3rhosqdc_vsr[ii]=timeavg(vus3rhosqdc[:,ii],ts,fti,ftf)
            vuas3rhosqdc_vsr[ii]=timeavg(vuas3rhosqdc[:,ii],ts,fti,ftf)
            Bs1rhosqdc_vsr[ii]=timeavg(Bs1rhosqdc[:,ii],ts,fti,ftf)
            Bas1rhosqdc_vsr[ii]=timeavg(Bas1rhosqdc[:,ii],ts,fti,ftf)
            Bs2rhosqdc_vsr[ii]=timeavg(Bs2rhosqdc[:,ii],ts,fti,ftf)
            Bas2rhosqdc_vsr[ii]=timeavg(Bas2rhosqdc[:,ii],ts,fti,ftf)
            Bs3rhosqdc_vsr[ii]=timeavg(Bs3rhosqdc[:,ii],ts,fti,ftf)
            Bas3rhosqdc_vsr[ii]=timeavg(Bas3rhosqdc[:,ii],ts,fti,ftf)
            bs1rhosqdc_vsr[ii]=timeavg(bs1rhosqdc[:,ii],ts,fti,ftf)
            bas1rhosqdc_vsr[ii]=timeavg(bas1rhosqdc[:,ii],ts,fti,ftf)
            bs2rhosqdc_vsr[ii]=timeavg(bs2rhosqdc[:,ii],ts,fti,ftf)
            bas2rhosqdc_vsr[ii]=timeavg(bas2rhosqdc[:,ii],ts,fti,ftf)
            bs3rhosqdc_vsr[ii]=timeavg(bs3rhosqdc[:,ii],ts,fti,ftf)
            bas3rhosqdc_vsr[ii]=timeavg(bas3rhosqdc[:,ii],ts,fti,ftf)
            bsqrhosqdc_vsr[ii]=timeavg(bsqrhosqdc[:,ii],ts,fti,ftf)
            #
            favg1b.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],rhosrhosqdc_vsr[ii],ugsrhosqdc_vsr[ii],uu0rhosqdc_vsr[ii],vus1rhosqdc_vsr[ii],vuas1rhosqdc_vsr[ii],vus3rhosqdc_vsr[ii],vuas3rhosqdc_vsr[ii],Bs1rhosqdc_vsr[ii],Bas1rhosqdc_vsr[ii],Bs2rhosqdc_vsr[ii],Bas2rhosqdc_vsr[ii],Bs3rhosqdc_vsr[ii],Bas3rhosqdc_vsr[ii],bs1rhosqdc_vsr[ii],bas1rhosqdc_vsr[ii],bs2rhosqdc_vsr[ii],bas2rhosqdc_vsr[ii],bs3rhosqdc_vsr[ii],bas3rhosqdc_vsr[ii],bsqrhosqdc_vsr[ii] ) )
            #
        favg1b.close()
        #
        #
        #" *\(.*vsr\).*" -> "        \1_fit=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(\1[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1"
        #
        # get fit
        print("rhosrhosqdc numfit=%d" % (numfit)) ; sys.stdout.flush()
        (rhosrhosqdc_vsr_fit,rhosrhosqdc_vsr_fitsigma,rhosrhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(rhosrhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (ugsrhosqdc_vsr_fit,ugsrhosqdc_vsr_fitsigma,ugsrhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(ugsrhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (uu0rhosqdc_vsr_fit,uu0rhosqdc_vsr_fitsigma,uu0rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(uu0rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus1rhosqdc_vsr_fit,vus1rhosqdc_vsr_fitsigma,vus1rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus1rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas1rhosqdc_vsr_fit,vuas1rhosqdc_vsr_fitsigma,vuas1rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas1rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus3rhosqdc_vsr_fit,vus3rhosqdc_vsr_fitsigma,vus3rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus3rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas3rhosqdc_vsr_fit,vuas3rhosqdc_vsr_fitsigma,vuas3rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas3rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs1rhosqdc_vsr_fit,Bs1rhosqdc_vsr_fitsigma,Bs1rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs1rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas1rhosqdc_vsr_fit,Bas1rhosqdc_vsr_fitsigma,Bas1rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas1rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs2rhosqdc_vsr_fit,Bs2rhosqdc_vsr_fitsigma,Bs2rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs2rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas2rhosqdc_vsr_fit,Bas2rhosqdc_vsr_fitsigma,Bas2rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas2rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs3rhosqdc_vsr_fit,Bs3rhosqdc_vsr_fitsigma,Bs3rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs3rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas3rhosqdc_vsr_fit,Bas3rhosqdc_vsr_fitsigma,Bas3rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas3rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs1rhosqdc_vsr_fit,bs1rhosqdc_vsr_fitsigma,bs1rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs1rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas1rhosqdc_vsr_fit,bas1rhosqdc_vsr_fitsigma,bas1rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas1rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs2rhosqdc_vsr_fit,bs2rhosqdc_vsr_fitsigma,bs2rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs2rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas2rhosqdc_vsr_fit,bas2rhosqdc_vsr_fitsigma,bas2rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas2rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs3rhosqdc_vsr_fit,bs3rhosqdc_vsr_fitsigma,bs3rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs3rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas3rhosqdc_vsr_fit,bas3rhosqdc_vsr_fitsigma,bas3rhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas3rhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqrhosqdc_vsr_fit,bsqrhosqdc_vsr_fitsigma,bsqrhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqrhosqdc_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (brhosqdc_vsr_fit,brhosqdc_vsr_fitsigma,brhosqdc_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.sqrt(np.fabs(bsqrhosqdc_vsr[iin2:iout2]))),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        #
        ###################
        # r1c (density weighted over full non-jet)
        ###################
        #
        #
        rhosrhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        ugsrhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        uu0rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        vus1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        vus3rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bs1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bas1rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bs2rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bas2rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bs3rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bas3rhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        bsqrhosqdcden_vsr=np.zeros(nx,dtype=r.dtype)
        #
        favg1c = open('datavsr1c.txt', 'w')
        favg1c.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","rhosrhosqdcden_vsr","ugsrhosqdcden_vsr","uu0rhosqdcden_vsr","vus1rhosqdcden_vsr","vuas1rhosqdcden_vsr","vus3rhosqdcden_vsr","vuas3rhosqdcden_vsr","Bs1rhosqdcden_vsr","Bas1rhosqdcden_vsr","Bs2rhosqdcden_vsr","Bas2rhosqdcden_vsr","Bs3rhosqdcden_vsr","Bas3rhosqdcden_vsr","bs1rhosqdcden_vsr","bas1rhosqdcden_vsr","bs2rhosqdcden_vsr","bas2rhosqdcden_vsr","bs3rhosqdcden_vsr","bas3rhosqdcden_vsr","bsqrhosqdcden_vsr" ) )
        for ii in np.arange(0,nx):
            #
            # Q vs r
            # 2+20
            rhosrhosqdcden_vsr[ii]=timeavg(rhosrhosqdcden[:,ii],ts,fti,ftf)
            ugsrhosqdcden_vsr[ii]=timeavg(ugsrhosqdcden[:,ii],ts,fti,ftf)
            uu0rhosqdcden_vsr[ii]=timeavg(uu0rhosqdcden[:,ii],ts,fti,ftf)
            vus1rhosqdcden_vsr[ii]=timeavg(vus1rhosqdcden[:,ii],ts,fti,ftf)
            vuas1rhosqdcden_vsr[ii]=timeavg(vuas1rhosqdcden[:,ii],ts,fti,ftf)
            vus3rhosqdcden_vsr[ii]=timeavg(vus3rhosqdcden[:,ii],ts,fti,ftf)
            vuas3rhosqdcden_vsr[ii]=timeavg(vuas3rhosqdcden[:,ii],ts,fti,ftf)
            Bs1rhosqdcden_vsr[ii]=timeavg(Bs1rhosqdcden[:,ii],ts,fti,ftf)
            Bas1rhosqdcden_vsr[ii]=timeavg(Bas1rhosqdcden[:,ii],ts,fti,ftf)
            Bs2rhosqdcden_vsr[ii]=timeavg(Bs2rhosqdcden[:,ii],ts,fti,ftf)
            Bas2rhosqdcden_vsr[ii]=timeavg(Bas2rhosqdcden[:,ii],ts,fti,ftf)
            Bs3rhosqdcden_vsr[ii]=timeavg(Bs3rhosqdcden[:,ii],ts,fti,ftf)
            Bas3rhosqdcden_vsr[ii]=timeavg(Bas3rhosqdcden[:,ii],ts,fti,ftf)
            bs1rhosqdcden_vsr[ii]=timeavg(bs1rhosqdcden[:,ii],ts,fti,ftf)
            bas1rhosqdcden_vsr[ii]=timeavg(bas1rhosqdcden[:,ii],ts,fti,ftf)
            bs2rhosqdcden_vsr[ii]=timeavg(bs2rhosqdcden[:,ii],ts,fti,ftf)
            bas2rhosqdcden_vsr[ii]=timeavg(bas2rhosqdcden[:,ii],ts,fti,ftf)
            bs3rhosqdcden_vsr[ii]=timeavg(bs3rhosqdcden[:,ii],ts,fti,ftf)
            bas3rhosqdcden_vsr[ii]=timeavg(bas3rhosqdcden[:,ii],ts,fti,ftf)
            bsqrhosqdcden_vsr[ii]=timeavg(bsqrhosqdcden[:,ii],ts,fti,ftf)
            #
            favg1c.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],rhosrhosqdcden_vsr[ii],ugsrhosqdcden_vsr[ii],uu0rhosqdcden_vsr[ii],vus1rhosqdcden_vsr[ii],vuas1rhosqdcden_vsr[ii],vus3rhosqdcden_vsr[ii],vuas3rhosqdcden_vsr[ii],Bs1rhosqdcden_vsr[ii],Bas1rhosqdcden_vsr[ii],Bs2rhosqdcden_vsr[ii],Bas2rhosqdcden_vsr[ii],Bs3rhosqdcden_vsr[ii],Bas3rhosqdcden_vsr[ii],bs1rhosqdcden_vsr[ii],bas1rhosqdcden_vsr[ii],bs2rhosqdcden_vsr[ii],bas2rhosqdcden_vsr[ii],bs3rhosqdcden_vsr[ii],bas3rhosqdcden_vsr[ii],bsqrhosqdcden_vsr[ii] ) )
            #
        favg1c.close()
        #
        #
        #" *\(.*vsr\).*" -> "        \1_fit=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(\1[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1"
        #
        # get fit
        print("dcden fits start") ; sys.stdout.flush()
        print("rhosrhosqdcden numfit=%d iin2=%d iout2=%d" % (numfit,iin2,iout2)) ; sys.stdout.flush()
        (rhosrhosqdcden_vsr_fit,rhosrhosqdcden_vsr_fitsigma,rhosrhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(rhosrhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (ugsrhosqdcden_vsr_fit,ugsrhosqdcden_vsr_fitsigma,ugsrhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(ugsrhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (uu0rhosqdcden_vsr_fit,uu0rhosqdcden_vsr_fitsigma,uu0rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(uu0rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus1rhosqdcden_vsr_fit,vus1rhosqdcden_vsr_fitsigma,vus1rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus1rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas1rhosqdcden_vsr_fit,vuas1rhosqdcden_vsr_fitsigma,vuas1rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas1rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus3rhosqdcden_vsr_fit,vus3rhosqdcden_vsr_fitsigma,vus3rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus3rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas3rhosqdcden_vsr_fit,vuas3rhosqdcden_vsr_fitsigma,vuas3rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas3rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs1rhosqdcden_vsr_fit,Bs1rhosqdcden_vsr_fitsigma,Bs1rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs1rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas1rhosqdcden_vsr_fit,Bas1rhosqdcden_vsr_fitsigma,Bas1rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas1rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs2rhosqdcden_vsr_fit,Bs2rhosqdcden_vsr_fitsigma,Bs2rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs2rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas2rhosqdcden_vsr_fit,Bas2rhosqdcden_vsr_fitsigma,Bas2rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas2rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs3rhosqdcden_vsr_fit,Bs3rhosqdcden_vsr_fitsigma,Bs3rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs3rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas3rhosqdcden_vsr_fit,Bas3rhosqdcden_vsr_fitsigma,Bas3rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas3rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs1rhosqdcden_vsr_fit,bs1rhosqdcden_vsr_fitsigma,bs1rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs1rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas1rhosqdcden_vsr_fit,bas1rhosqdcden_vsr_fitsigma,bas1rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas1rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs2rhosqdcden_vsr_fit,bs2rhosqdcden_vsr_fitsigma,bs2rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs2rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas2rhosqdcden_vsr_fit,bas2rhosqdcden_vsr_fitsigma,bas2rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas2rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs3rhosqdcden_vsr_fit,bs3rhosqdcden_vsr_fitsigma,bs3rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs3rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas3rhosqdcden_vsr_fit,bas3rhosqdcden_vsr_fitsigma,bas3rhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas3rhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqrhosqdcden_vsr_fit,bsqrhosqdcden_vsr_fitsigma,bsqrhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqrhosqdcden_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (brhosqdcden_vsr_fit,brhosqdcden_vsr_fitsigma,brhosqdcden_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.sqrt(np.fabs(bsqrhosqdcden_vsr[iin2:iout2]))),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        #
        ###################
        # r2
        ###################
        rhosrhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        ugsrhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        uu0rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        vus1rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        vus3rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bs1rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bas1rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bs2rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bas2rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bs3rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bas3rhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        bsqrhosqeq_vsr=np.zeros(nx,dtype=r.dtype)
        #
        favg2 = open('datavsr2.txt', 'w')
        favg2.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","rhosrhosqeq_vsr","ugsrhosqeq_vsr","uu0rhosqeq_vsr","vus1rhosqeq_vsr","vuas1rhosqeq_vsr","vus3rhosqeq_vsr","vuas3rhosqeq_vsr","Bs1rhosqeq_vsr","Bas1rhosqeq_vsr","Bs2rhosqeq_vsr","Bas2rhosqeq_vsr","Bs3rhosqeq_vsr","Bas3rhosqeq_vsr","bs1rhosqeq_vsr","bas1rhosqeq_vsr","bs2rhosqeq_vsr","bas2rhosqeq_vsr","bs3rhosqeq_vsr","bas3rhosqeq_vsr","bsqrhosqeq_vsr") )
        for ii in np.arange(0,nx):
            # Q vs. r
            # 2+20
            rhosrhosqeq_vsr[ii]=timeavg(rhosrhosqeq[:,ii],ts,fti,ftf)
            ugsrhosqeq_vsr[ii]=timeavg(ugsrhosqeq[:,ii],ts,fti,ftf)
            uu0rhosqeq_vsr[ii]=timeavg(uu0rhosqeq[:,ii],ts,fti,ftf)
            vus1rhosqeq_vsr[ii]=timeavg(vus1rhosqeq[:,ii],ts,fti,ftf)
            vuas1rhosqeq_vsr[ii]=timeavg(vuas1rhosqeq[:,ii],ts,fti,ftf)
            vus3rhosqeq_vsr[ii]=timeavg(vus3rhosqeq[:,ii],ts,fti,ftf)
            vuas3rhosqeq_vsr[ii]=timeavg(vuas3rhosqeq[:,ii],ts,fti,ftf)
            Bs1rhosqeq_vsr[ii]=timeavg(Bs1rhosqeq[:,ii],ts,fti,ftf)
            Bas1rhosqeq_vsr[ii]=timeavg(Bas1rhosqeq[:,ii],ts,fti,ftf)
            Bs2rhosqeq_vsr[ii]=timeavg(Bs2rhosqeq[:,ii],ts,fti,ftf)
            Bas2rhosqeq_vsr[ii]=timeavg(Bas2rhosqeq[:,ii],ts,fti,ftf)
            Bs3rhosqeq_vsr[ii]=timeavg(Bs3rhosqeq[:,ii],ts,fti,ftf)
            Bas3rhosqeq_vsr[ii]=timeavg(Bas3rhosqeq[:,ii],ts,fti,ftf)
            bs1rhosqeq_vsr[ii]=timeavg(bs1rhosqeq[:,ii],ts,fti,ftf)
            bas1rhosqeq_vsr[ii]=timeavg(bas1rhosqeq[:,ii],ts,fti,ftf)
            bs2rhosqeq_vsr[ii]=timeavg(bs2rhosqeq[:,ii],ts,fti,ftf)
            bas2rhosqeq_vsr[ii]=timeavg(bas2rhosqeq[:,ii],ts,fti,ftf)
            bs3rhosqeq_vsr[ii]=timeavg(bs3rhosqeq[:,ii],ts,fti,ftf)
            bas3rhosqeq_vsr[ii]=timeavg(bas3rhosqeq[:,ii],ts,fti,ftf)
            bsqrhosqeq_vsr[ii]=timeavg(bsqrhosqeq[:,ii],ts,fti,ftf)
            #
            favg2.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],rhosrhosqeq_vsr[ii],ugsrhosqeq_vsr[ii],uu0rhosqeq_vsr[ii],vus1rhosqeq_vsr[ii],vuas1rhosqeq_vsr[ii],vus3rhosqeq_vsr[ii],vuas3rhosqeq_vsr[ii],Bs1rhosqeq_vsr[ii],Bas1rhosqeq_vsr[ii],Bs2rhosqeq_vsr[ii],Bas2rhosqeq_vsr[ii],Bs3rhosqeq_vsr[ii],Bas3rhosqeq_vsr[ii],bs1rhosqeq_vsr[ii],bas1rhosqeq_vsr[ii],bs2rhosqeq_vsr[ii],bas2rhosqeq_vsr[ii],bs3rhosqeq_vsr[ii],bas3rhosqeq_vsr[ii],bsqrhosqeq_vsr[ii]) )
            #
        favg2.close()
        #
        # get fit
        print("rhosrhosqeq numfit=%d" % (numfit)) ; sys.stdout.flush()
        (rhosrhosqeq_vsr_fit,rhosrhosqeq_vsr_fitsigma,rhosrhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(rhosrhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (ugsrhosqeq_vsr_fit,ugsrhosqeq_vsr_fitsigma,ugsrhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(ugsrhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (uu0rhosqeq_vsr_fit,uu0rhosqeq_vsr_fitsigma,uu0rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(uu0rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus1rhosqeq_vsr_fit,vus1rhosqeq_vsr_fitsigma,vus1rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus1rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas1rhosqeq_vsr_fit,vuas1rhosqeq_vsr_fitsigma,vuas1rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas1rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus3rhosqeq_vsr_fit,vus3rhosqeq_vsr_fitsigma,vus3rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus3rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas3rhosqeq_vsr_fit,vuas3rhosqeq_vsr_fitsigma,vuas3rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas3rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs1rhosqeq_vsr_fit,Bs1rhosqeq_vsr_fitsigma,Bs1rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs1rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas1rhosqeq_vsr_fit,Bas1rhosqeq_vsr_fitsigma,Bas1rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas1rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs2rhosqeq_vsr_fit,Bs2rhosqeq_vsr_fitsigma,Bs2rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs2rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas2rhosqeq_vsr_fit,Bas2rhosqeq_vsr_fitsigma,Bas2rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas2rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs3rhosqeq_vsr_fit,Bs3rhosqeq_vsr_fitsigma,Bs3rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs3rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas3rhosqeq_vsr_fit,Bas3rhosqeq_vsr_fitsigma,Bas3rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas3rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs1rhosqeq_vsr_fit,bs1rhosqeq_vsr_fitsigma,bs1rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs1rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas1rhosqeq_vsr_fit,bas1rhosqeq_vsr_fitsigma,bas1rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas1rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs2rhosqeq_vsr_fit,bs2rhosqeq_vsr_fitsigma,bs2rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs2rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas2rhosqeq_vsr_fit,bas2rhosqeq_vsr_fitsigma,bas2rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas2rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs3rhosqeq_vsr_fit,bs3rhosqeq_vsr_fitsigma,bs3rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs3rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas3rhosqeq_vsr_fit,bas3rhosqeq_vsr_fitsigma,bas3rhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas3rhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqrhosqeq_vsr_fit,bsqrhosqeq_vsr_fitsigma,bsqrhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqrhosqeq_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (brhosqeq_vsr_fit,brhosqeq_vsr_fitsigma,brhosqeq_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.sqrt(np.fabs(bsqrhosqeq_vsr[iin2:iout2]))),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        #
        ###################
        # r3
        ###################
        #
        rhosrhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        ugsrhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        uu0rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        vus1rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        vus3rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bs1rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bas1rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bs2rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bas2rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bs3rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bas3rhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        bsqrhosqhorpick_vsr=np.zeros(nx,dtype=r.dtype)
        #
        favg3 = open('datavsr3.txt', 'w')
        favg3.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","rhosrhosqhorpick_vsr","ugsrhosqhorpick_vsr","uu0rhosqhorpick_vsr","vus1rhosqhorpick_vsr","vuas1rhosqhorpick_vsr","vus3rhosqhorpick_vsr","vuas3rhosqhorpick_vsr","Bs1rhosqhorpick_vsr","Bas1rhosqhorpick_vsr","Bs2rhosqhorpick_vsr","Bas2rhosqhorpick_vsr","Bs3rhosqhorpick_vsr","Bas3rhosqhorpick_vsr","bs1rhosqhorpick_vsr","bas1rhosqhorpick_vsr","bs2rhosqhorpick_vsr","bas2rhosqhorpick_vsr","bs3rhosqhorpick_vsr","bas3rhosqhorpick_vsr","bsqrhosqhorpick_vsr") )
        for ii in np.arange(0,nx):
            # Q vs. r
            # 2+20
            rhosrhosqhorpick_vsr[ii]=timeavg(rhosrhosqhorpick[:,ii],ts,fti,ftf)
            ugsrhosqhorpick_vsr[ii]=timeavg(ugsrhosqhorpick[:,ii],ts,fti,ftf)
            uu0rhosqhorpick_vsr[ii]=timeavg(uu0rhosqhorpick[:,ii],ts,fti,ftf)
            vus1rhosqhorpick_vsr[ii]=timeavg(vus1rhosqhorpick[:,ii],ts,fti,ftf)
            vuas1rhosqhorpick_vsr[ii]=timeavg(vuas1rhosqhorpick[:,ii],ts,fti,ftf)
            vus3rhosqhorpick_vsr[ii]=timeavg(vus3rhosqhorpick[:,ii],ts,fti,ftf)
            vuas3rhosqhorpick_vsr[ii]=timeavg(vuas3rhosqhorpick[:,ii],ts,fti,ftf)
            Bs1rhosqhorpick_vsr[ii]=timeavg(Bs1rhosqhorpick[:,ii],ts,fti,ftf)
            Bas1rhosqhorpick_vsr[ii]=timeavg(Bas1rhosqhorpick[:,ii],ts,fti,ftf)
            Bs2rhosqhorpick_vsr[ii]=timeavg(Bs2rhosqhorpick[:,ii],ts,fti,ftf)
            Bas2rhosqhorpick_vsr[ii]=timeavg(Bas2rhosqhorpick[:,ii],ts,fti,ftf)
            Bs3rhosqhorpick_vsr[ii]=timeavg(Bs3rhosqhorpick[:,ii],ts,fti,ftf)
            Bas3rhosqhorpick_vsr[ii]=timeavg(Bas3rhosqhorpick[:,ii],ts,fti,ftf)
            bs1rhosqhorpick_vsr[ii]=timeavg(bs1rhosqhorpick[:,ii],ts,fti,ftf)
            bas1rhosqhorpick_vsr[ii]=timeavg(bas1rhosqhorpick[:,ii],ts,fti,ftf)
            bs2rhosqhorpick_vsr[ii]=timeavg(bs2rhosqhorpick[:,ii],ts,fti,ftf)
            bas2rhosqhorpick_vsr[ii]=timeavg(bas2rhosqhorpick[:,ii],ts,fti,ftf)
            bs3rhosqhorpick_vsr[ii]=timeavg(bs3rhosqhorpick[:,ii],ts,fti,ftf)
            bas3rhosqhorpick_vsr[ii]=timeavg(bas3rhosqhorpick[:,ii],ts,fti,ftf)
            bsqrhosqhorpick_vsr[ii]=timeavg(bsqrhosqhorpick[:,ii],ts,fti,ftf)
            #
            favg3.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],rhosrhosqhorpick_vsr[ii],ugsrhosqhorpick_vsr[ii],uu0rhosqhorpick_vsr[ii],vus1rhosqhorpick_vsr[ii],vuas1rhosqhorpick_vsr[ii],vus3rhosqhorpick_vsr[ii],vuas3rhosqhorpick_vsr[ii],Bs1rhosqhorpick_vsr[ii],Bas1rhosqhorpick_vsr[ii],Bs2rhosqhorpick_vsr[ii],Bas2rhosqhorpick_vsr[ii],Bs3rhosqhorpick_vsr[ii],Bas3rhosqhorpick_vsr[ii],bs1rhosqhorpick_vsr[ii],bas1rhosqhorpick_vsr[ii],bs2rhosqhorpick_vsr[ii],bas2rhosqhorpick_vsr[ii],bs3rhosqhorpick_vsr[ii],bas3rhosqhorpick_vsr[ii],bsqrhosqhorpick_vsr[ii]) )
            #
        favg3.close()
        #
        # get fit
        print("rhosrhosqpick numfit=%d" % (numfit)) ; sys.stdout.flush()
        (rhosrhosqhorpick_vsr_fit,rhosrhosqhorpick_vsr_fitsigma,rhosrhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(rhosrhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (ugsrhosqhorpick_vsr_fit,ugsrhosqhorpick_vsr_fitsigma,ugsrhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(ugsrhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (uu0rhosqhorpick_vsr_fit,uu0rhosqhorpick_vsr_fitsigma,uu0rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(uu0rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus1rhosqhorpick_vsr_fit,vus1rhosqhorpick_vsr_fitsigma,vus1rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus1rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas1rhosqhorpick_vsr_fit,vuas1rhosqhorpick_vsr_fitsigma,vuas1rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas1rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus3rhosqhorpick_vsr_fit,vus3rhosqhorpick_vsr_fitsigma,vus3rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus3rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas3rhosqhorpick_vsr_fit,vuas3rhosqhorpick_vsr_fitsigma,vuas3rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas3rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs1rhosqhorpick_vsr_fit,Bs1rhosqhorpick_vsr_fitsigma,Bs1rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs1rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas1rhosqhorpick_vsr_fit,Bas1rhosqhorpick_vsr_fitsigma,Bas1rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas1rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs2rhosqhorpick_vsr_fit,Bs2rhosqhorpick_vsr_fitsigma,Bs2rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs2rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas2rhosqhorpick_vsr_fit,Bas2rhosqhorpick_vsr_fitsigma,Bas2rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas2rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs3rhosqhorpick_vsr_fit,Bs3rhosqhorpick_vsr_fitsigma,Bs3rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs3rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas3rhosqhorpick_vsr_fit,Bas3rhosqhorpick_vsr_fitsigma,Bas3rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas3rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs1rhosqhorpick_vsr_fit,bs1rhosqhorpick_vsr_fitsigma,bs1rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs1rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas1rhosqhorpick_vsr_fit,bas1rhosqhorpick_vsr_fitsigma,bas1rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas1rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs2rhosqhorpick_vsr_fit,bs2rhosqhorpick_vsr_fitsigma,bs2rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs2rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas2rhosqhorpick_vsr_fit,bas2rhosqhorpick_vsr_fitsigma,bas2rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas2rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs3rhosqhorpick_vsr_fit,bs3rhosqhorpick_vsr_fitsigma,bs3rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs3rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas3rhosqhorpick_vsr_fit,bas3rhosqhorpick_vsr_fitsigma,bas3rhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas3rhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqrhosqhorpick_vsr_fit,bsqrhosqhorpick_vsr_fitsigma,bsqrhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqrhosqhorpick_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (brhosqhorpick_vsr_fit,brhosqhorpick_vsr_fitsigma,brhosqhorpick_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.sqrt(np.fabs(bsqrhosqhorpick_vsr[iin2:iout2]))),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        #
        ###################
        # r4
        ###################
        rhoshor_vsr=np.zeros(nx,dtype=r.dtype)
        ugshor_vsr=np.zeros(nx,dtype=r.dtype)
        bsqshor_vsr=np.zeros(nx,dtype=r.dtype)
        bsqorhoshor_vsr=np.zeros(nx,dtype=r.dtype)
        bsqougshor_vsr=np.zeros(nx,dtype=r.dtype)
        uu0hor_vsr=np.zeros(nx,dtype=r.dtype)
        vus1hor_vsr=np.zeros(nx,dtype=r.dtype)
        vuas1hor_vsr=np.zeros(nx,dtype=r.dtype)
        vus3hor_vsr=np.zeros(nx,dtype=r.dtype)
        vuas3hor_vsr=np.zeros(nx,dtype=r.dtype)
        Bs1hor_vsr=np.zeros(nx,dtype=r.dtype)
        Bas1hor_vsr=np.zeros(nx,dtype=r.dtype)
        Bs2hor_vsr=np.zeros(nx,dtype=r.dtype)
        Bas2hor_vsr=np.zeros(nx,dtype=r.dtype)
        Bs3hor_vsr=np.zeros(nx,dtype=r.dtype)
        Bas3hor_vsr=np.zeros(nx,dtype=r.dtype)
        bs1hor_vsr=np.zeros(nx,dtype=r.dtype)
        bas1hor_vsr=np.zeros(nx,dtype=r.dtype)
        bs2hor_vsr=np.zeros(nx,dtype=r.dtype)
        bas2hor_vsr=np.zeros(nx,dtype=r.dtype)
        bs3hor_vsr=np.zeros(nx,dtype=r.dtype)
        bas3hor_vsr=np.zeros(nx,dtype=r.dtype)
        bsqhor_vsr=np.zeros(nx,dtype=r.dtype)
        #
        favg4 = open('datavsr4.txt', 'w')
        favg4.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","rhoshor_vsr","ugshor_vsr","bsqshor_vsr","bsqorhoshor_vsr","bsqougshor_vsr","uu0hor_vsr","vus1hor_vsr","vuas1hor_vsr","vus3hor_vsr","vuas3hor_vsr","Bs1hor_vsr","Bas1hor_vsr","Bs2hor_vsr","Bas2hor_vsr","Bs3hor_vsr","Bas3hor_vsr","bs1hor_vsr","bas1hor_vsr","bs2hor_vsr","bas2hor_vsr","bs3hor_vsr","bas3hor_vsr","bsqhor_vsr") )
        for ii in np.arange(0,nx):
            # Q vs. r
            # 2+23=25
            rhoshor_vsr[ii]=timeavg(rhoshor[:,ii],ts,fti,ftf)
            ugshor_vsr[ii]=timeavg(ugshor[:,ii],ts,fti,ftf)
            bsqshor_vsr[ii]=timeavg(bsqshor[:,ii],ts,fti,ftf)
            bsqorhoshor_vsr[ii]=timeavg(bsqorhoshor[:,ii],ts,fti,ftf)
            bsqougshor_vsr[ii]=timeavg(bsqougshor[:,ii],ts,fti,ftf)
            uu0hor_vsr[ii]=timeavg(uu0hor[:,ii],ts,fti,ftf)
            vus1hor_vsr[ii]=timeavg(vus1hor[:,ii],ts,fti,ftf)
            vuas1hor_vsr[ii]=timeavg(vuas1hor[:,ii],ts,fti,ftf)
            vus3hor_vsr[ii]=timeavg(vus3hor[:,ii],ts,fti,ftf)
            vuas3hor_vsr[ii]=timeavg(vuas3hor[:,ii],ts,fti,ftf)
            Bs1hor_vsr[ii]=timeavg(Bs1hor[:,ii],ts,fti,ftf)
            Bas1hor_vsr[ii]=timeavg(Bas1hor[:,ii],ts,fti,ftf)
            Bs2hor_vsr[ii]=timeavg(Bs2hor[:,ii],ts,fti,ftf)
            Bas2hor_vsr[ii]=timeavg(Bas2hor[:,ii],ts,fti,ftf)
            Bs3hor_vsr[ii]=timeavg(Bs3hor[:,ii],ts,fti,ftf)
            Bas3hor_vsr[ii]=timeavg(Bas3hor[:,ii],ts,fti,ftf)
            bs1hor_vsr[ii]=timeavg(bs1hor[:,ii],ts,fti,ftf)
            bas1hor_vsr[ii]=timeavg(bas1hor[:,ii],ts,fti,ftf)
            bs2hor_vsr[ii]=timeavg(bs2hor[:,ii],ts,fti,ftf)
            bas2hor_vsr[ii]=timeavg(bas2hor[:,ii],ts,fti,ftf)
            bs3hor_vsr[ii]=timeavg(bs3hor[:,ii],ts,fti,ftf)
            bas3hor_vsr[ii]=timeavg(bas3hor[:,ii],ts,fti,ftf)
            bsqhor_vsr[ii]=timeavg(bsqhor[:,ii],ts,fti,ftf)
            #
            favg4.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],rhoshor_vsr[ii],ugshor_vsr[ii],bsqshor_vsr[ii],bsqorhoshor_vsr[ii],bsqougshor_vsr[ii],uu0hor_vsr[ii],vus1hor_vsr[ii],vuas1hor_vsr[ii],vus3hor_vsr[ii],vuas3hor_vsr[ii],Bs1hor_vsr[ii],Bas1hor_vsr[ii],Bs2hor_vsr[ii],Bas2hor_vsr[ii],Bs3hor_vsr[ii],Bas3hor_vsr[ii],bs1hor_vsr[ii],bas1hor_vsr[ii],bs2hor_vsr[ii],bas2hor_vsr[ii],bs3hor_vsr[ii],bas3hor_vsr[ii],bsqhor_vsr[ii]) )
            #
        favg4.close()
        #
        # get fit
        print("rhoshor numfit=%d" % (numfit)) ; sys.stdout.flush()
        (rhoshor_vsr_fit,rhoshor_vsr_fitsigma,rhoshor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(rhoshor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (ugshor_vsr_fit,ugshor_vsr_fitsigma,ugshor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(ugshor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqshor_vsr_fit,bsqshor_vsr_fitsigma,bsqshor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqshor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqorhoshor_vsr_fit,bsqorhoshor_vsr_fitsigma,bsqorhoshor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqorhoshor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqougshor_vsr_fit,bsqougshor_vsr_fitsigma,bsqougshor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqougshor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (uu0hor_vsr_fit,uu0hor_vsr_fitsigma,uu0hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(uu0hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus1hor_vsr_fit,vus1hor_vsr_fitsigma,vus1hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus1hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas1hor_vsr_fit,vuas1hor_vsr_fitsigma,vuas1hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas1hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vus3hor_vsr_fit,vus3hor_vsr_fitsigma,vus3hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vus3hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (vuas3hor_vsr_fit,vuas3hor_vsr_fitsigma,vuas3hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(vuas3hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs1hor_vsr_fit,Bs1hor_vsr_fitsigma,Bs1hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs1hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas1hor_vsr_fit,Bas1hor_vsr_fitsigma,Bas1hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas1hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs2hor_vsr_fit,Bs2hor_vsr_fitsigma,Bs2hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs2hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas2hor_vsr_fit,Bas2hor_vsr_fitsigma,Bas2hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas2hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bs3hor_vsr_fit,Bs3hor_vsr_fitsigma,Bs3hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bs3hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (Bas3hor_vsr_fit,Bas3hor_vsr_fitsigma,Bas3hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(Bas3hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs1hor_vsr_fit,bs1hor_vsr_fitsigma,bs1hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs1hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas1hor_vsr_fit,bas1hor_vsr_fitsigma,bas1hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas1hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs2hor_vsr_fit,bs2hor_vsr_fitsigma,bs2hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs2hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas2hor_vsr_fit,bas2hor_vsr_fitsigma,bas2hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas2hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bs3hor_vsr_fit,bs3hor_vsr_fitsigma,bs3hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bs3hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bas3hor_vsr_fit,bas3hor_vsr_fitsigma,bas3hor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bas3hor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bsqhor_vsr_fit,bsqhor_vsr_fitsigma,bsqhor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(bsqhor_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        (bhor_vsr_fit,bhor_vsr_fitsigma,bhor_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.sqrt(np.fabs(bsqhor_vsr[iin2:iout2]))),1,dologx=1,dology=1,doabs=1,badfit=globalbadfit,num=numfit) ; numfit+=1
        #
        ###################
        # r5
        ###################
        favg5 = open('datavsr5.txt', 'w')
        favg5.write("#%s %s   %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s  %s %s %s %s  %s %s %s  %s %s %s %s %s %s  %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","r","mdotfinavgvsr","mdotfinavgvsr5","mdotfinavgvsr10","mdotfinavgvsr30","edemvsr","edmavsr","edmvsr","ldemvsr","ldmavsr","ldmvsr","phiabsj_mu1vsr","pjemfinavgvsr","pjmakefinavgvsr","pjkefinavgvsr","ljemfinavgvsr","ljmakefinavgvsr","ljkefinavgvsr","mdin_vsr","mdjet_vsr","mdmwind_vsr","mdwind_vsr","alphamag1_vsr","alphamag2_vsr","alphamag3_vsr","fstot_vsr","fsin_vsr","feqtot_vsr","fsmaxtot_vsr","fsuphalf_vsr","upsilon_vsr","etajEM_vsr","etajMAKE_vsr","etamwEM_vsr","etamwMAKE_vsr","etawEM_vsr","etawMAKE_vsr","letajEM_vsr","letajMAKE_vsr","letamwEM_vsr","letamwMAKE_vsr","letawEM_vsr","letawMAKE_vsr" ) )
        #
        #
        for ii in np.arange(0,nx):
            # Q vs. r
            #
            #
            # 2+17+4+3+6+12=43
            favg5.write("%d %g  %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,r[ii,0,0],mdotfinavgvsr[ii],mdotfinavgvsr5[ii],mdotfinavgvsr10[ii],mdotfinavgvsr30[ii],edemvsr[ii],edmavsr[ii],edmvsr[ii],ldemvsr[ii],ldmavsr[ii],ldmvsr[ii],phiabsj_mu1vsr[ii],pjemfinavgvsr[ii],pjmakefinavgvsr[ii],pjkefinavgvsr[ii],ljemfinavgvsr[ii],ljmakefinavgvsr[ii],ljkefinavgvsr[ii],mdin_vsr[ii],mdjet_vsr[ii],mdmwind_vsr[ii],mdwind_vsr[ii],alphamag1_vsr[ii],alphamag2_vsr[ii],alphamag3_vsr[ii],fstot_vsr[ii],fsin_vsr[ii],feqtot_vsr[ii],fsmaxtot_vsr[ii],fsuphalf_vsr[ii],upsilon_vsr[ii],etajEM_vsr[ii],etajMAKE_vsr[ii],etamwEM_vsr[ii],etamwMAKE_vsr[ii],etawEM_vsr[ii],etawMAKE_vsr[ii],letajEM_vsr[ii],letajMAKE_vsr[ii],letamwEM_vsr[ii],letamwMAKE_vsr[ii],letawEM_vsr[ii],letawMAKE_vsr[ii]) )
        #
        favg5.close()
        #
        # get fit
        print("mdotfinavgvsr numfit=%d" % (numfit)) ; sys.stdout.flush()
        (mdotfinavgvsr_fit,mdotfinavgvsr_fitsigma,mdotfinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(mdotfinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (mdotfinavgvsr5_fit,mdotfinavgvsr5_fitsigma,mdotfinavgvsr5_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(mdotfinavgvsr5[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1 # odd ball name
        (mdotfinavgvsr10_fit,mdotfinavgvsr10_fitsigma,mdotfinavgvsr10_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(mdotfinavgvsr10[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1 # odd ball name
        (mdotfinavgvsr30_fit,mdotfinavgvsr30_fitsigma,mdotfinavgvsr30_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(mdotfinavgvsr30[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1 # odd ball name
        (edemvsr_fit,edemvsr_fitsigma,edemvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(edemvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (edmavsr_fit,edmavsr_fitsigma,edmavsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(edmavsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (edmvsr_fit,edmvsr_fitsigma,edmvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(edmvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (ldemvsr_fit,ldemvsr_fitsigma,ldemvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(ldemvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (ldmavsr_fit,ldmavsr_fitsigma,ldmavsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(ldmavsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (ldmvsr_fit,ldmvsr_fitsigma,ldmvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(ldmvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (phiabsj_mu1vsr_fit,phiabsj_mu1vsr_fitsigma,phiabsj_mu1vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(phiabsj_mu1vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (pjemfinavgvsr_fit,pjemfinavgvsr_fitsigma,pjemfinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(pjemfinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (pjmakefinavgvsr_fit,pjmakefinavgvsr_fitsigma,pjmakefinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(pjmakefinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (pjkefinavgvsr_fit,pjkefinavgvsr_fitsigma,pjkefinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(pjkefinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (ljemfinavgvsr_fit,ljemfinavgvsr_fitsigma,ljemfinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(ljemfinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (ljmakefinavgvsr_fit,ljmakefinavgvsr_fitsigma,ljmakefinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(ljmakefinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (ljkefinavgvsr_fit,ljkefinavgvsr_fitsigma,ljkefinavgvsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(ljkefinavgvsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        #
        # thickdisk16 (full data) barfs on mdjet or something later, perhaps related to warning about division by zero in log10.  So maybe input is nan and that stalls polyfit.  Maybe set nan's to small number in wrapperto polyfit.
        # fit mdin-mdotbh with log instead of mdin that isn't loggy due to constant mdotbh
        print("mdin_vsr numfit=%d" % (numfit)) ; sys.stdout.flush()
        (mdin_vsr_fit,mdin_vsr_fitsigma,mdin_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin3:iout3,0,0])),(np.fabs(mdin_vsr[iin3:iout3])-np.fabs(mdin_vsr[ihor])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (mdjet_vsr_fit,mdjet_vsr_fitsigma,mdjet_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(mdjet_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (mdmwind_vsr_fit,mdmwind_vsr_fitsigma,mdmwind_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(mdmwind_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (mdwind_vsr_fit,mdwind_vsr_fitsigma,mdwind_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(mdwind_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        # normal fit for alphamag?
        (alphamag1_vsr_fit,alphamag1_vsr_fitsigma,alphamag1_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(alphamag1_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (alphamag2_vsr_fit,alphamag2_vsr_fitsigma,alphamag2_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(alphamag2_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (alphamag3_vsr_fit,alphamag3_vsr_fitsigma,alphamag3_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(alphamag3_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (fstot_vsr_fit,fstot_vsr_fitsigma,fstot_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(fstot_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (fsin_vsr_fit,fsin_vsr_fitsigma,fsin_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(fsin_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (feqtot_vsr_fit,feqtot_vsr_fitsigma,feqtot_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(feqtot_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (fsmaxtot_vsr_fit,fsmaxtot_vsr_fitsigma,fsmaxtot_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(fsmaxtot_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (fsuphalf_vsr_fit,fsuphalf_vsr_fitsigma,fsuphalf_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(fsuphalf_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (upsilon_vsr_fit,upsilon_vsr_fitsigma,upsilon_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin1:iout1,0,0])),(np.fabs(upsilon_vsr[iin1:iout1])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        #
        #" *\(.*vsr\).*" -> "        \1_fit=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(\1[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1"
        print("etajEM_vsr numfit=%d" % (numfit)) ; sys.stdout.flush()
        (etajEM_vsr_fit,etajEM_vsr_fitsigma,etajEM_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(etajEM_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (etajMAKE_vsr_fit,etajMAKE_vsr_fitsigma,etajMAKE_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(etajMAKE_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (etamwEM_vsr_fit,etamwEM_vsr_fitsigma,etamwEM_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(etamwEM_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (etamwMAKE_vsr_fit,etamwMAKE_vsr_fitsigma,etamwMAKE_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(etamwMAKE_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (etawEM_vsr_fit,etawEM_vsr_fitsigma,etawEM_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(etawEM_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (etawMAKE_vsr_fit,etawMAKE_vsr_fitsigma,etawMAKE_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(etawMAKE_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (etaw_vsr_fit,etaw_vsr_fitsigma,etaw_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(etaw_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letajEM_vsr_fit,letajEM_vsr_fitsigma,letajEM_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(letajEM_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letajMAKE_vsr_fit,letajMAKE_vsr_fitsigma,letajMAKE_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(letajMAKE_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letamwEM_vsr_fit,letamwEM_vsr_fitsigma,letamwEM_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(letamwEM_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letamwMAKE_vsr_fit,letamwMAKE_vsr_fitsigma,letamwMAKE_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin4:iout4,0,0])),(np.fabs(letamwMAKE_vsr[iin4:iout4])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letamw_vsr_fit,letamw_vsr_fitsigma,letamw_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(letamw_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letawEM_vsr_fit,letawEM_vsr_fitsigma,letawEM_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(letawEM_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letawMAKE_vsr_fit,letawMAKE_vsr_fitsigma,letawMAKE_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(letawMAKE_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (letaw_vsr_fit,letaw_vsr_fitsigma,letaw_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin5:iout5,0,0])),(np.fabs(letaw_vsr[iin5:iout5])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        #
        ###################
        # r6
        ###################
        hoverr_vsr=np.zeros(nx,dtype=r.dtype)
        hoverrcorona_vsr=np.zeros(nx,dtype=r.dtype)
        hoverr_jet_vsr=np.zeros(nx,dtype=r.dtype)
        qmridisk_vsr=np.zeros(nx,dtype=r.dtype)
        iq2mridisk_vsr=np.zeros(nx,dtype=r.dtype)
        qmridiskweak_vsr=np.zeros(nx,dtype=r.dtype)
        iq2mridiskweak_vsr=np.zeros(nx,dtype=r.dtype)
        #
        favg6 = open('datavsr6.txt', 'w')
        favg6.write("#%s %s %s %s %s %s %s   %s %s %s   %s   %s %s %s %s\n" % ("ii","rnyO2","dtheta","dphi","drvsr","dHvsr","dPvsr","hoverr_vsr","hoverrcorona_vsr","hoverr_jet_vsr","thetaalongfield","qmridisk_vsr","iq2mridisk_vsr","qmridiskweak_vsr","iq2mridiskweak_vsr" ) )
        #
        #
        for ii in np.arange(0,nx):
            # Q vs r
            # 2+12=15
            #
            # 5 other things that are static in time so no timeavg() needed
            hoverr_vsr[ii]=timeavg(hoverr[:,ii],ts,fti,ftf)
            hoverrcorona_vsr[ii]=timeavg(hoverrcorona[:,ii],ts,fti,ftf)
            hoverr_jet_vsr[ii]=timeavg(hoverr_jet[:,ii],ts,fti,ftf)
            qmridisk_vsr[ii]=timeavg(qmridisk[:,ii],ts,fti,ftf)
            iq2mridisk_vsr[ii]=timeavg(iq2mridisk[:,ii],ts,fti,ftf)
            qmridiskweak_vsr[ii]=timeavg(qmridiskweak[:,ii],ts,fti,ftf)
            iq2mridiskweak_vsr[ii]=timeavg(iq2mridiskweak[:,ii],ts,fti,ftf)
            #
            dthetaeq_vsr=dxdxp[2][2][:,ny/2,0]*_dx2
            dphieq_vsr=dxdxp[3][3][:,ny/2,0]*_dx3
            #
        print("SECOND=%g %g" % (hoverr_vsr[0],iq2mridisk_vsr[0]))
        # get thetaalongfield
        aphijetbase,thetaalongfield=compute_thetaalongfield(picki=ihor,thetaalongjet=hoverr_jet_vsr)
        #
        # cat datavsr6.txt | awk '{print $1" "$2" "$3" "$8" "$8/$3}' | column -t | less -S
        for ii in np.arange(0,nx):
            favg6.write("%d %g %g %g %g %g %g  %g %g %g  %g   %g %g %g %g\n" % (ii,r[ii,ny/2,0],dthetaeq_vsr[ii],dphieq_vsr[ii],drvsr[ii],dHvsr[ii],dPvsr[ii],hoverr_vsr[ii],hoverrcorona_vsr[ii],hoverr_jet_vsr[ii],thetaalongfield[ii],qmridisk_vsr[ii],iq2mridisk_vsr[ii],qmridiskweak_vsr[ii],iq2mridiskweak_vsr[ii]) )
            #
        favg6.close()
        # get fit
        ijetout=iofr(rjetout)
        print("hoverr_vsr numfit=%d" % (numfit)) ; sys.stdout.flush()
        (hoverr_vsr_fit,hoverr_vsr_fitsigma,hoverr_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(hoverr_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (hoverrcorona_vsr_fit,hoverrcorona_vsr_fitsigma,hoverrcorona_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(hoverrcorona_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        (hoverr_jet_vsr_fit,hoverr_jet_vsr_fitsigma,hoverr_jet_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin:ijetout,0,0])),(np.fabs(hoverr_jet_vsr[iin:ijetout])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        # below stalls python for some reason
        #thetaalongfield_fit,#thetaalongfield_fitsigma,#thetaalongfield_fitgoodness)=jonpolyfit((np.fabs(r[iin:ijetout,0,0])),(np.fabs(thetaalongfield[iin:ijetout])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        print("wtf1") ; sys.stdout.flush()
        (qmridisk_vsr_fit,qmridisk_vsr_fitsigma,qmridisk_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(qmridisk_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        print("wtf2") ; sys.stdout.flush()
        (iq2mridisk_vsr_fit,iq2mridisk_vsr_fitsigma,iq2mridisk_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(iq2mridisk_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        print("wtf3") ; sys.stdout.flush()
        (qmridiskweak_vsr_fit,qmridiskweak_vsr_fitsigma,qmridiskweak_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(qmridiskweak_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        print("wtf4") ; sys.stdout.flush()
        (iq2mridiskweak_vsr_fit,iq2mridiskweak_vsr_fitsigma,iq2mridiskweak_vsr_fitgoodness)=jonpolyfit((np.fabs(r[iin2:iout2,0,0])),(np.fabs(iq2mridiskweak_vsr[iin2:iout2])),1,dologx=1,dology=1,doabs=1,num=numfit) ; numfit+=1
        #
        print("hoverr_jet_vsr_fit=%g" % (hoverr_jet_vsr_fit[0]))
        #
        # report rfitin1 and rfitout1 used for wind-parts
        #
        # output fit power-law index for various quantities
        #
        #roundto2fit(powerlaw,goodness)
        # http://www.gnu.org/s/emacs/manual/html_node/elisp/Regexp-Special.html
        #roundto2(\([][A-Z_a-z0-9]*\))
        #roundto2(\([A-Z_a-z0-9]*\)\([][0-9]*\))
        #Query replace regexp: roundto2(\([A-Z_a-z0-9]*\)\([][0-9]*\)) -> roundto2fit(\1[0],\1goodness[0])
        #Query replace regexp: roundto2fit(\([A-Z_a-z0-9]*\)\([][0-9]*\), -> roundto2fit(\1[0],\1sigma[0],
        #
        # montage only those we actually fit
        # files=`ls -rt fitplot46.png fitplot47.png fitplot46.png fitplot50.png fitplot52.png fitplot60.png fitplot66.png    fitplot150.png fitplot152.png fitplot153.png   fitplot164.png fitplot165.png fitplot168.png fitplot173.png fitplot176.png` ; montage -geometry 300x300 $files montage_fitplotpaper.png ; display montage_fitplotpaper.png
        #
        if 1==0:
            print( "HLatex12: ModelName & $r^{\\rm{}dc}_{\\rm{}i}$ & $r^{\\rm{}dc}_{\\rm{}o}$ & $r^{\\rm{}dc}_{\\rm{}s}$ & $\\rho$ & $p_g$ & $|v_r|$ & $|v_\phi|$ & $|b_r|$ & $|b_\\theta|$ & $|b_\\phi|$ & $|b|$    \\\\" )
            print( "VLatex12: %s        & %g                       & %g                       & %g                       & %s      & %s    & %s      & %s         & %s      & %s            & %s          & %s       \\\\ %% %s" % (truemodelname, roundto2(rfitin2),roundto2(rfitout2),roundto2(rstagreport),roundto2fit(rhosrhosqdcden_vsr_fit[0],rhosrhosqdcden_vsr_fitsigma[0],rhosrhosqdcden_vsr_fitgoodness[0]),roundto2fit(ugsrhosqdcden_vsr_fit[0],ugsrhosqdcden_vsr_fitsigma[0],ugsrhosqdcden_vsr_fitgoodness[0]),roundto2fit(vuas1rhosqdcden_vsr_fit[0],vuas1rhosqdcden_vsr_fitsigma[0],vuas1rhosqdcden_vsr_fitgoodness[0]),roundto2fit(vuas3rhosqdcden_vsr_fit[0],vuas3rhosqdcden_vsr_fitsigma[0],vuas3rhosqdcden_vsr_fitgoodness[0]),roundto2fit(bas1rhosqdcden_vsr_fit[0],bas1rhosqdcden_vsr_fitsigma[0],bas1rhosqdcden_vsr_fitgoodness[0]),roundto2fit(bas2rhosqdcden_vsr_fit[0],bas2rhosqdcden_vsr_fitsigma[0],bas2rhosqdcden_vsr_fitgoodness[0]),roundto2fit(bas3rhosqdcden_vsr_fit[0],bas3rhosqdcden_vsr_fitsigma[0],bas3rhosqdcden_vsr_fitgoodness[0]),roundto2fit(brhosqdcden_vsr_fit[0],brhosqdcden_vsr_fitsigma[0],brhosqdcden_vsr_fitgoodness[0]) , modelname ) )
        else:
            # b_\theta varies too much and need to cut something.
            # also b_r\sim b_\phi or |b| good enough for b_\phi
            print( "HLatex12: ModelName & $r^{\\rm{}dc}_{\\rm{}i}$ & $r^{\\rm{}dc}_{\\rm{}o}$ & $r^{\\rm{}dc}_{\\rm{}f}$ & $r^{\\rm{}dc}_{\\rm{}s}$ & $\\rho$ & $p_g$ & $|v_r|$ & $|v_\phi|$ & $|b_r|$ & $|b|$    \\\\" )
            print( "VLatex12: %s        & %g                       & %g                       & %g                       & %s                       & %s      & %s    & %s      & %s         & %s      & %s       \\\\ %% %s" % (truemodelname, roundto2(rfitin2),roundto2(rfitout2),roundto2(rfitout6),roundto2(rstagreport),roundto2fit(rhosrhosqdcden_vsr_fit[0],rhosrhosqdcden_vsr_fitsigma[0],rhosrhosqdcden_vsr_fitgoodness[0]),roundto2fit(ugsrhosqdcden_vsr_fit[0],ugsrhosqdcden_vsr_fitsigma[0],ugsrhosqdcden_vsr_fitgoodness[0]),roundto2fit(vuas1rhosqdcden_vsr_fit[0],vuas1rhosqdcden_vsr_fitsigma[0],vuas1rhosqdcden_vsr_fitgoodness[0]),roundto2fit(vuas3rhosqdcden_vsr_fit[0],vuas3rhosqdcden_vsr_fitsigma[0],vuas3rhosqdcden_vsr_fitgoodness[0]),roundto2fit(bas1rhosqdcden_vsr_fit[0],bas1rhosqdcden_vsr_fitsigma[0],bas1rhosqdcden_vsr_fitgoodness[0]),roundto2fit(brhosqdcden_vsr_fit[0],brhosqdcden_vsr_fitsigma[0],brhosqdcden_vsr_fitgoodness[0]) , modelname ) )
        #
        #
        # 13 things
        if 1==0:
            print( "HLatex13: ModelName & $r^{\\rm{}w}_{\\rm{}i}$ & $r^{\\rm{}w}_{\\rm{}o}$ & $\\dot{M}_{\\rm{}in}-\\dot{M}_{\\rm{}H}$ & $\\dot{M}_{\\rm{}mw}$ & $\\dot{M}_{\\rm{}w}$ & $\\eta^{\\rm{}EM}_{\\rm{}mw}$ & $\\eta^{\\rm{}EM}_{\\rm{}w}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}mw}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}w}$ & $l^{\\rm{}EM}_{\\rm{}mw}$ & $l^{\\rm{}EM}_{\\rm{}w}$ & $l^{\\rm{}MAKE}_{\\rm{}mw}$ & $l^{\\rm{}MAKE}_{\\rm{}w}$   \\\\" )
            print( "VLatex13: %s        & %g                      & %g                      & %s                                        & %s                    & %s                   & %s                            & %s                           & %s                              & %s                             & %s                        & %s                       & %s                          & %s                              \\\\ %% %s" % (truemodelname, roundto2(rfitin3),roundto2(rfitout3),roundto2fit(mdin_vsr_fit[0],mdin_vsr_fitsigma[0],mdin_vsr_fitgoodness[0]),roundto2fit(mdmwind_vsr_fit[0],mdmwind_vsr_fitsigma[0],mdmwind_vsr_fitgoodness[0]),roundto2fit(mdwind_vsr_fit[0],mdwind_vsr_fitsigma[0],mdwind_vsr_fitgoodness[0]),roundto2fit(etamwEM_vsr_fit[0],etamwEM_vsr_fitsigma[0],etamwEM_vsr_fitgoodness[0]),roundto2fit(etawEM_vsr_fit[0],etawEM_vsr_fitsigma[0],etawEM_vsr_fitgoodness[0]),roundto2fit(etamwMAKE_vsr_fit[0],etamwMAKE_vsr_fitsigma[0],etamwMAKE_vsr_fitgoodness[0]),roundto2fit(etawMAKE_vsr_fit[0],etawMAKE_vsr_fitsigma[0],etawMAKE_vsr_fitgoodness[0]), roundto2fit(letamwEM_vsr_fit[0],letamwEM_vsr_fitsigma[0],letamwEM_vsr_fitgoodness[0]),roundto2fit(letawEM_vsr_fit[0],letawEM_vsr_fitsigma[0],letawEM_vsr_fitgoodness[0]),roundto2fit(letamwMAKE_vsr_fit[0],letamwMAKE_vsr_fitsigma[0],letamwMAKE_vsr_fitgoodness[0]),roundto2fit(letawMAKE_vsr_fit[0],letawMAKE_vsr_fitsigma[0],letawMAKE_vsr_fitgoodness[0]) , modelname ) )
        else:
            print( "HLatex13: ModelName & $r^{\\rm{}w}_{\\rm{}i}$ & $r^{\\rm{}w}_{\\rm{}o}$ & $\\dot{M}_{\\rm{}in}-\\dot{M}_{\\rm{}H}$ & $\\dot{M}_{\\rm{}mw}$ & $\\dot{M}_{\\rm{}w}$ & $\\eta^{\\rm{}EM}_{\\rm{}mw}$ & $\\eta^{\\rm{}MAKE}_{\\rm{}mw}$ & $\\eta_{\\rm{}w}$ & $l_{\\rm{}mw}$  & $l_{\\rm{}w}$   \\\\" )
            print( "VLatex13: %s        & %g                      & %g                      & %s                                        & %s                    & %s                   & %s                            & %s                              & %s                & %s              & %s              \\\\ %% %s" % (truemodelname, roundto2(rfitin3),roundto2(rfitout3),roundto2fit(mdin_vsr_fit[0],mdin_vsr_fitsigma[0],mdin_vsr_fitgoodness[0]),roundto2fit(mdmwind_vsr_fit[0],mdmwind_vsr_fitsigma[0],mdmwind_vsr_fitgoodness[0]),roundto2fit(mdwind_vsr_fit[0],mdwind_vsr_fitsigma[0],mdwind_vsr_fitgoodness[0]),roundto2fit(etamwEM_vsr_fit[0],etamwEM_vsr_fitsigma[0],etamwEM_vsr_fitgoodness[0]),roundto2fit(etamwMAKE_vsr_fit[0],etamwMAKE_vsr_fitsigma[0],etamwMAKE_vsr_fitgoodness[0]),roundto2fit(etaw_vsr_fit[0],etaw_vsr_fitsigma[0],etaw_vsr_fitgoodness[0]), roundto2fit(letamw_vsr_fit[0],letamw_vsr_fitsigma[0],letamw_vsr_fitgoodness[0]),roundto2fit(letaw_vsr_fit[0],letaw_vsr_fitsigma[0],letaw_vsr_fitgoodness[0]) , modelname ) )
        #
        ##################
        # 14 is reduced version of original 12+13
        # avoid fits for 2D models and MB09D model that have poor fits
        if nz>1 and modelname!="runlocaldipole3dfiducial":
            print( "HLatex14: ModelName & $r^{\\rm{}dc}_{\\rm{}i}$ & $r^{\\rm{}dc}_{\\rm{}o}$ & $r^{\\rm{}dc}_{\\rm{}f}$ & $r^{\\rm{}dc}_{\\rm{}s}$ & $\\rho$ & $p_g$ & $|b|$ & $r^{\\rm{}w}_{\\rm{}i}$ & $r^{\\rm{}w}_{\\rm{}o}$ & $\\dot{M}_{\\rm{}in}-\\dot{M}_{\\rm{}H}$ & $\\dot{M}_{\\rm{}mw}$ & $\\dot{M}_{\\rm{}w}$  \\\\" )
            print( "VLatex14: %s        & %g                       & %g                       & %g                       & %s                       & %s      & %s    & %s      & %g                    & %g                      & %s                      & %s                    & %s                    \\\\ %% %s" % (truemodelname, roundto2(rfitin2),roundto2(rfitout2),roundto2(rfitout6),roundto2(rstagreport),roundto2fit(rhosrhosqdcden_vsr_fit[0],rhosrhosqdcden_vsr_fitsigma[0],rhosrhosqdcden_vsr_fitgoodness[0]),roundto2fit(ugsrhosqdcden_vsr_fit[0],ugsrhosqdcden_vsr_fitsigma[0],ugsrhosqdcden_vsr_fitgoodness[0]),roundto2fit(brhosqdcden_vsr_fit[0],brhosqdcden_vsr_fitsigma[0],brhosqdcden_vsr_fitgoodness[0]),roundto2(rfitin3),roundto2(rfitout3),roundto2fit(mdin_vsr_fit[0],mdin_vsr_fitsigma[0],mdin_vsr_fitgoodness[0]),roundto2fit(mdmwind_vsr_fit[0],mdmwind_vsr_fitsigma[0],mdmwind_vsr_fitgoodness[0]),roundto2fit(mdwind_vsr_fit[0],mdwind_vsr_fitsigma[0],mdwind_vsr_fitgoodness[0]) , modelname ) )
        #
        #
        #
        print( "HLatex93: ModelName & $\\rho^{\\rm{}dc}$ & $p_g^{\\rm{}dc}$ & $v_r^{\\rm{}dc}$ & $v_\\phi^{\\rm{}dc}$ & $b_r^{\\rm{}dc}$ & $b_\\theta^{\\rm{}dc}$ & $b_\\phi^{\\rm{}dc}$ & $|b|^{\\rm{}dc}$ & $\\rho^{\\rm{}hor}$ & $p^{\\rm{}hor}_g$ & $v^{\\rm{}hor}_r$ & $v^{\\rm{}hor}_\\phi$ & $b^{\\rm{}hor}_r$ & $b^{\\rm{}hor}_\\theta$ & $b^{\\rm{}hor}_\\phi$ & $|b|^{\\rm{}hor}$ & $\\dot{M}_{\\rm{}in}-\\dot{M}_{\\rm{}H}$ & $\\dot{M}_{\\rm{}mw}$ & $\\dot{M}_{\\rm{}w}$   \\\\" )
        print( "VLatex93: %s         & %g     & %g    & %g    & %g        & %g    & %g          & %g        & %g    & %g        & %g      & %g      & %g          & %g      & %g            & %g          & %g      & %g                    & %g                    & %g                     \\\\ %% %s" % (truemodelname, roundto2(rhosrhosqdc_vsr_fit[0]),roundto2(ugsrhosqdc_vsr_fit[0]),roundto2(vuas1rhosqdc_vsr_fit[0]),roundto2(vuas3rhosqdc_vsr_fit[0]),roundto2(bas1rhosqdc_vsr_fit[0]),roundto2(bas2rhosqdc_vsr_fit[0]),roundto2(bas3rhosqdc_vsr_fit[0]),roundto2(brhosqdc_vsr_fit[0]),roundto2(rhoshor_vsr_fit[0]),roundto2(ugshor_vsr_fit[0]),roundto2(vuas1hor_vsr_fit[0]),roundto2(vuas3hor_vsr_fit[0]),roundto2(bas1hor_vsr_fit[0]),roundto2(bas2hor_vsr_fit[0]),roundto2(bas3hor_vsr_fit[0]),roundto2(bhor_vsr_fit[0]),roundto2(mdin_vsr_fit[0]),roundto2(mdmwind_vsr_fit[0]),roundto2(mdwind_vsr_fit[0]) , modelname ) )
        print( "HLatex94: ModelName & $\\rho^{\\rm{}dc}$ & $p_g^{\\rm{}dc}$ & $v_r^{\\rm{}dc}$ & $v_\\phi^{\\rm{}dc}$ & $b_r^{\\rm{}dc}$ & $b_\\theta^{\\rm{}dc}$ & $b_\\phi^{\\rm{}dc}$ & $|b|^{\\rm{}dc}$ & $\\rho^{\\rm{}eq}$ & $p^{\\rm{}eq}_g$ & $v^{\\rm{}eq}_r$ & $v^{\\rm{}eq}_\\phi$ & $b^{\\rm{}eq}_r$ & $b^{\\rm{}eq}_\\theta$ & $b^{\\rm{}eq}_\\phi$ & $|b|^{\\rm{}eq}$ & $\\dot{M}_{\\rm{}in}-\\dot{M}_{\\rm{}H}$ & $\\dot{M}_{\\rm{}mw}$ & $\\dot{M}_{\\rm{}w}$   \\\\" )
        print( "VLatex94: %s         & %g     & %g    & %g    & %g        & %g    & %g          & %g        & %g    & %g        & %g      & %g      & %g          & %g      & %g            & %g          & %g      & %g                    & %g                    & %g                     \\\\ %% %s" % (truemodelname, roundto2(rhosrhosq_vsr_fit[0]),roundto2(ugsrhosqdc_vsr_fit[0]),roundto2(vuas1rhosqdc_vsr_fit[0]),roundto2(vuas3rhosqdc_vsr_fit[0]),roundto2(bas1rhosqdc_vsr_fit[0]),roundto2(bas2rhosqdc_vsr_fit[0]),roundto2(bas3rhosqdc_vsr_fit[0]),roundto2(brhosqdc_vsr_fit[0]),roundto2(rhosrhosqeq_vsr_fit[0]),roundto2(ugsrhosqeq_vsr_fit[0]),roundto2(vuas1rhosqeq_vsr_fit[0]),roundto2(vuas3rhosqeq_vsr_fit[0]),roundto2(bas1rhosqeq_vsr_fit[0]),roundto2(bas2rhosqeq_vsr_fit[0]),roundto2(bas3rhosqeq_vsr_fit[0]),roundto2(brhosqeq_vsr_fit[0]),roundto2(mdin_vsr_fit[0]),roundto2(mdmwind_vsr_fit[0]),roundto2(mdwind_vsr_fit[0]) , modelname ) )
        #
        sys.stdout.flush()
        #
        #
    #
    if dodatavsrh==1 or dofftplot==1 or dospecplot==1:
    #
        print("wtfa1") ; sys.stdout.flush()
        ###################
        # h1
        ###################
        rhosrhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        ugsrhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        uu0rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        vus1rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        vus3rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bs1rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bas1rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bs2rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bas2rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bs3rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bas3rhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        bsqrhosqrad4_vsh=np.zeros(nx,dtype=r.dtype)
        #
        # now interpolate from size ny to size nx
        # get \theta at r=4 in size of nx rather than ny
        xold=tj[0,0,0]+(tj[0,:,0]-tj[0,0,0])/(tj[0,-1,0]-tj[0,0,0])
        xnew=ti[0,0,0]+(ti[:,0,0]-ti[0,0,0])/(ti[-1,0,0]-ti[0,0,0])
        hinnx4=np.interp(xnew,xold,h[iofr(4),:,0])
        #
        favgrad4 = open('datavsh1.txt', 'w')
        favgrad4.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","hinnx4","rhosrhosqrad4_vsh","ugsrhosqrad4_vsh","uu0rhosqrad4_vsh","vus1rhosqrad4_vsh","vuas1rhosqrad4_vsh","vus3rhosqrad4_vsh","vuas3rhosqrad4_vsh","Bs1rhosqrad4_vsh","Bas1rhosqrad4_vsh","Bs2rhosqrad4_vsh","Bas2rhosqrad4_vsh","Bs3rhosqrad4_vsh","Bas3rhosqrad4_vsh","bs1rhosqrad4_vsh","bas1rhosqrad4_vsh","bs2rhosqrad4_vsh","bas2rhosqrad4_vsh","bs3rhosqrad4_vsh","bas3rhosqrad4_vsh","bsqrhosqrad4_vsh" ) )
        for ii in np.arange(0,nx):
            # Q vs h
            # 2+20
            rhosrhosqrad4_vsh[ii]=timeavg(rhosrhosqrad4[:,ii],ts,fti,ftf)
            ugsrhosqrad4_vsh[ii]=timeavg(ugsrhosqrad4[:,ii],ts,fti,ftf)
            uu0rhosqrad4_vsh[ii]=timeavg(uu0rhosqrad4[:,ii],ts,fti,ftf)
            vus1rhosqrad4_vsh[ii]=timeavg(vus1rhosqrad4[:,ii],ts,fti,ftf)
            vuas1rhosqrad4_vsh[ii]=timeavg(vuas1rhosqrad4[:,ii],ts,fti,ftf)
            vus3rhosqrad4_vsh[ii]=timeavg(vus3rhosqrad4[:,ii],ts,fti,ftf)
            vuas3rhosqrad4_vsh[ii]=timeavg(vuas3rhosqrad4[:,ii],ts,fti,ftf)
            Bs1rhosqrad4_vsh[ii]=timeavg(Bs1rhosqrad4[:,ii],ts,fti,ftf)
            Bas1rhosqrad4_vsh[ii]=timeavg(Bas1rhosqrad4[:,ii],ts,fti,ftf)
            Bs2rhosqrad4_vsh[ii]=timeavg(Bs2rhosqrad4[:,ii],ts,fti,ftf)
            Bas2rhosqrad4_vsh[ii]=timeavg(Bas2rhosqrad4[:,ii],ts,fti,ftf)
            Bs3rhosqrad4_vsh[ii]=timeavg(Bs3rhosqrad4[:,ii],ts,fti,ftf)
            Bas3rhosqrad4_vsh[ii]=timeavg(Bas3rhosqrad4[:,ii],ts,fti,ftf)
            bs1rhosqrad4_vsh[ii]=timeavg(bs1rhosqrad4[:,ii],ts,fti,ftf)
            bas1rhosqrad4_vsh[ii]=timeavg(bas1rhosqrad4[:,ii],ts,fti,ftf)
            bs2rhosqrad4_vsh[ii]=timeavg(bs2rhosqrad4[:,ii],ts,fti,ftf)
            bas2rhosqrad4_vsh[ii]=timeavg(bas2rhosqrad4[:,ii],ts,fti,ftf)
            bs3rhosqrad4_vsh[ii]=timeavg(bs3rhosqrad4[:,ii],ts,fti,ftf)
            bas3rhosqrad4_vsh[ii]=timeavg(bas3rhosqrad4[:,ii],ts,fti,ftf)
            bsqrhosqrad4_vsh[ii]=timeavg(bsqrhosqrad4[:,ii],ts,fti,ftf)
            #
            favgrad4.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,hinnx4[ii],rhosrhosqrad4_vsh[ii],ugsrhosqrad4_vsh[ii],uu0rhosqrad4_vsh[ii],vus1rhosqrad4_vsh[ii],vuas1rhosqrad4_vsh[ii],vus3rhosqrad4_vsh[ii],vuas3rhosqrad4_vsh[ii],Bs1rhosqrad4_vsh[ii],Bas1rhosqrad4_vsh[ii],Bs2rhosqrad4_vsh[ii],Bas2rhosqrad4_vsh[ii],Bs3rhosqrad4_vsh[ii],Bas3rhosqrad4_vsh[ii],bs1rhosqrad4_vsh[ii],bas1rhosqrad4_vsh[ii],bs2rhosqrad4_vsh[ii],bas2rhosqrad4_vsh[ii],bs3rhosqrad4_vsh[ii],bas3rhosqrad4_vsh[ii],bsqrhosqrad4_vsh[ii]) )
            #
        favgrad4.close()
        ###################
        # h2
        ###################
        print("wtfa2") ; sys.stdout.flush()
        # now interpolate from size ny to size nx
        # get \theta at r=8 in size of nx rather than ny
        xold=tj[0,0,0]+(tj[0,:,0]-tj[0,0,0])/(tj[0,-1,0]-tj[0,0,0])
        xnew=ti[0,0,0]+(ti[:,0,0]-ti[0,0,0])/(ti[-1,0,0]-ti[0,0,0])
        hinnx8=np.interp(xnew,xold,h[iofr(8),:,0])
        #
        rhosrhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        ugsrhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        uu0rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        vus1rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        vus3rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bs1rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bas1rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bs2rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bas2rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bs3rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bas3rhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        bsqrhosqrad8_vsh=np.zeros(nx,dtype=r.dtype)
        #
        favgrad8 = open('datavsh2.txt', 'w')
        favgrad8.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","hinnx8","rhosrhosqrad8_vsh","ugsrhosqrad8_vsh","uu0rhosqrad8_vsh","vus1rhosqrad8_vsh","vuas1rhosqrad8_vsh","vus3rhosqrad8_vsh","vuas3rhosqrad8_vsh","Bs1rhosqrad8_vsh","Bas1rhosqrad8_vsh","Bs2rhosqrad8_vsh","Bas2rhosqrad8_vsh","Bs3rhosqrad8_vsh","Bas3rhosqrad8_vsh","bs1rhosqrad8_vsh","bas1rhosqrad8_vsh","bs2rhosqrad8_vsh","bas2rhosqrad8_vsh","bs3rhosqrad8_vsh","bas3rhosqrad8_vsh","bsqrhosqrad8_vsh" ) )
        for ii in np.arange(0,nx):
            # Q vs h
            # 2+20
            rhosrhosqrad8_vsh[ii]=timeavg(rhosrhosqrad8[:,ii],ts,fti,ftf)
            ugsrhosqrad8_vsh[ii]=timeavg(ugsrhosqrad8[:,ii],ts,fti,ftf)
            uu0rhosqrad8_vsh[ii]=timeavg(uu0rhosqrad8[:,ii],ts,fti,ftf)
            vus1rhosqrad8_vsh[ii]=timeavg(vus1rhosqrad8[:,ii],ts,fti,ftf)
            vuas1rhosqrad8_vsh[ii]=timeavg(vuas1rhosqrad8[:,ii],ts,fti,ftf)
            vus3rhosqrad8_vsh[ii]=timeavg(vus3rhosqrad8[:,ii],ts,fti,ftf)
            vuas3rhosqrad8_vsh[ii]=timeavg(vuas3rhosqrad8[:,ii],ts,fti,ftf)
            Bs1rhosqrad8_vsh[ii]=timeavg(Bs1rhosqrad8[:,ii],ts,fti,ftf)
            Bas1rhosqrad8_vsh[ii]=timeavg(Bas1rhosqrad8[:,ii],ts,fti,ftf)
            Bs2rhosqrad8_vsh[ii]=timeavg(Bs2rhosqrad8[:,ii],ts,fti,ftf)
            Bas2rhosqrad8_vsh[ii]=timeavg(Bas2rhosqrad8[:,ii],ts,fti,ftf)
            Bs3rhosqrad8_vsh[ii]=timeavg(Bs3rhosqrad8[:,ii],ts,fti,ftf)
            Bas3rhosqrad8_vsh[ii]=timeavg(Bas3rhosqrad8[:,ii],ts,fti,ftf)
            bs1rhosqrad8_vsh[ii]=timeavg(bs1rhosqrad8[:,ii],ts,fti,ftf)
            bas1rhosqrad8_vsh[ii]=timeavg(bas1rhosqrad8[:,ii],ts,fti,ftf)
            bs2rhosqrad8_vsh[ii]=timeavg(bs2rhosqrad8[:,ii],ts,fti,ftf)
            bas2rhosqrad8_vsh[ii]=timeavg(bas2rhosqrad8[:,ii],ts,fti,ftf)
            bs3rhosqrad8_vsh[ii]=timeavg(bs3rhosqrad8[:,ii],ts,fti,ftf)
            bas3rhosqrad8_vsh[ii]=timeavg(bas3rhosqrad8[:,ii],ts,fti,ftf)
            bsqrhosqrad8_vsh[ii]=timeavg(bsqrhosqrad8[:,ii],ts,fti,ftf)
            #
            favgrad8.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,hinnx8[ii],rhosrhosqrad8_vsh[ii],ugsrhosqrad8_vsh[ii],uu0rhosqrad8_vsh[ii],vus1rhosqrad8_vsh[ii],vuas1rhosqrad8_vsh[ii],vus3rhosqrad8_vsh[ii],vuas3rhosqrad8_vsh[ii],Bs1rhosqrad8_vsh[ii],Bas1rhosqrad8_vsh[ii],Bs2rhosqrad8_vsh[ii],Bas2rhosqrad8_vsh[ii],Bs3rhosqrad8_vsh[ii],Bas3rhosqrad8_vsh[ii],bs1rhosqrad8_vsh[ii],bas1rhosqrad8_vsh[ii],bs2rhosqrad8_vsh[ii],bas2rhosqrad8_vsh[ii],bs3rhosqrad8_vsh[ii],bas3rhosqrad8_vsh[ii],bsqrhosqrad8_vsh[ii]) )
            #
        favgrad8.close()
        ###################
        # h3
        ###################
        # now interpolate from size ny to size nx
        # get \theta at r=8 in size of nx rather than ny
        xold=tj[0,0,0]+(tj[0,:,0]-tj[0,0,0])/(tj[0,-1,0]-tj[0,0,0])
        xnew=ti[0,0,0]+(ti[:,0,0]-ti[0,0,0])/(ti[-1,0,0]-ti[0,0,0])
        hinnx30=np.interp(xnew,xold,h[iofr(30),:,0])
        #
        rhosrhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        ugsrhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        uu0rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        vus1rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        vuas1rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        vus3rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        vuas3rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        Bs1rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        Bas1rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        Bs2rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        Bas2rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        Bs3rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        Bas3rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bs1rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bas1rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bs2rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bas2rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bs3rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bas3rhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        bsqrhosqrad30_vsh=np.zeros(nx,dtype=r.dtype)
        #
        favgrad30 = open('datavsh3.txt', 'w')
        favgrad30.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("ii","hinnx30","rhosrhosqrad30_vsh","ugsrhosqrad30_vsh","uu0rhosqrad30_vsh","vus1rhosqrad30_vsh","vuas1rhosqrad30_vsh","vus3rhosqrad30_vsh","vuas3rhosqrad30_vsh","Bs1rhosqrad30_vsh","Bas1rhosqrad30_vsh","Bs2rhosqrad30_vsh","Bas2rhosqrad30_vsh","Bs3rhosqrad30_vsh","Bas3rhosqrad30_vsh","bs1rhosqrad30_vsh","bas1rhosqrad30_vsh","bs2rhosqrad30_vsh","bas2rhosqrad30_vsh","bs3rhosqrad30_vsh","bas3rhosqrad30_vsh","bsqrhosqrad30_vsh" ) )
        for ii in np.arange(0,nx):
            # Q vs h
            # 2+20
            rhosrhosqrad30_vsh[ii]=timeavg(rhosrhosqrad30[:,ii],ts,fti,ftf)
            ugsrhosqrad30_vsh[ii]=timeavg(ugsrhosqrad30[:,ii],ts,fti,ftf)
            uu0rhosqrad30_vsh[ii]=timeavg(uu0rhosqrad30[:,ii],ts,fti,ftf)
            vus1rhosqrad30_vsh[ii]=timeavg(vus1rhosqrad30[:,ii],ts,fti,ftf)
            vuas1rhosqrad30_vsh[ii]=timeavg(vuas1rhosqrad30[:,ii],ts,fti,ftf)
            vus3rhosqrad30_vsh[ii]=timeavg(vus3rhosqrad30[:,ii],ts,fti,ftf)
            vuas3rhosqrad30_vsh[ii]=timeavg(vuas3rhosqrad30[:,ii],ts,fti,ftf)
            Bs1rhosqrad30_vsh[ii]=timeavg(Bs1rhosqrad30[:,ii],ts,fti,ftf)
            Bas1rhosqrad30_vsh[ii]=timeavg(Bas1rhosqrad30[:,ii],ts,fti,ftf)
            Bs2rhosqrad30_vsh[ii]=timeavg(Bs2rhosqrad30[:,ii],ts,fti,ftf)
            Bas2rhosqrad30_vsh[ii]=timeavg(Bas2rhosqrad30[:,ii],ts,fti,ftf)
            Bs3rhosqrad30_vsh[ii]=timeavg(Bs3rhosqrad30[:,ii],ts,fti,ftf)
            Bas3rhosqrad30_vsh[ii]=timeavg(Bas3rhosqrad30[:,ii],ts,fti,ftf)
            bs1rhosqrad30_vsh[ii]=timeavg(bs1rhosqrad30[:,ii],ts,fti,ftf)
            bas1rhosqrad30_vsh[ii]=timeavg(bas1rhosqrad30[:,ii],ts,fti,ftf)
            bs2rhosqrad30_vsh[ii]=timeavg(bs2rhosqrad30[:,ii],ts,fti,ftf)
            bas2rhosqrad30_vsh[ii]=timeavg(bas2rhosqrad30[:,ii],ts,fti,ftf)
            bs3rhosqrad30_vsh[ii]=timeavg(bs3rhosqrad30[:,ii],ts,fti,ftf)
            bas3rhosqrad30_vsh[ii]=timeavg(bas3rhosqrad30[:,ii],ts,fti,ftf)
            bsqrhosqrad30_vsh[ii]=timeavg(bsqrhosqrad30[:,ii],ts,fti,ftf)
            #
            favgrad30.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (ii,hinnx30[ii],rhosrhosqrad30_vsh[ii],ugsrhosqrad30_vsh[ii],uu0rhosqrad30_vsh[ii],vus1rhosqrad30_vsh[ii],vuas1rhosqrad30_vsh[ii],vus3rhosqrad30_vsh[ii],vuas3rhosqrad30_vsh[ii],Bs1rhosqrad30_vsh[ii],Bas1rhosqrad30_vsh[ii],Bs2rhosqrad30_vsh[ii],Bas2rhosqrad30_vsh[ii],Bs3rhosqrad30_vsh[ii],Bas3rhosqrad30_vsh[ii],bs1rhosqrad30_vsh[ii],bas1rhosqrad30_vsh[ii],bs2rhosqrad30_vsh[ii],bas2rhosqrad30_vsh[ii],bs3rhosqrad30_vsh[ii],bas3rhosqrad30_vsh[ii],bsqrhosqrad30_vsh[ii]) )
            #
            #
        favgrad30.close()
        #
    #
    #
    #
    #
    #
    ####################################################
    # Q vs. time
    ####################################################
    #
    #
    if dodatavst==1:
    #
        print("dodatavst==1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        sizet=len(ts)
        #
        favg1 = open('datavst1.txt', 'w')
        favg1.write("#%s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts","mdtotihor","md10ihor","md30ihor","mdinrdiskin","mdinrdiskout","mdjetrjetout","mdmwindrjetin","mdmwindrjetout","mdwindrdiskin","mdwindrdiskout" ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg1.write("%d %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], mdtot[tici,ihor],md10[tici,ihor],md30[tici,ihor],mdin[tici,iofr(rdiskin)],mdin[tici,iofr(rdiskout)],mdjet[tici,iofr(rjetout)],mdmwind[tici,iofr(rjetin)],mdmwind[tici,iofr(rjetout)],mdwind[tici,iofr(rdiskin)],mdwind[tici,iofr(rdiskout)]  ) )
            #
        favg1.close()
        #
        favg2 = open('datavst2.txt', 'w')
        favg2.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts"," etabhEM","etabhMAKE","etabh","etajEM","etajMAKE","etaj","etamwinEM","etamwinMAKE","etamwin","etamwoutEM","etamwoutMAKE","etamwout","etawinEM","etawinMAKE","etawin","etawoutEM","etawoutMAKE","etawout"  ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg2.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], etabhEM[tici],etabhMAKE[tici],etabh[tici],etajEM[tici],etajMAKE[tici],etaj[tici],etamwinEM[tici],etamwinMAKE[tici],etamwin[tici],etamwoutEM[tici],etamwoutMAKE[tici],etamwout[tici],etawinEM[tici],etawinMAKE[tici],etawin[tici],etawoutEM[tici],etawoutMAKE[tici],etawout[tici]  ) )
            #
        favg2.close()
        #
        favg3 = open('datavst3.txt', 'w')
        favg3.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts"," letabhEM","letabhMAKE","letabh","letajEM","letajMAKE","letaj","letamwinEM","letamwinMAKE","letamwin","letamwoutEM","letamwoutMAKE","letamwout","letawinEM","letawinMAKE","letawin","letawoutEM","letawoutMAKE","letawout"  ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg3.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], letabhEM[tici],letabhMAKE[tici],letabh[tici],letajEM[tici],letajMAKE[tici],letaj[tici],letamwinEM[tici],letamwinMAKE[tici],letamwin[tici],letamwoutEM[tici],letamwoutMAKE[tici],letamwout[tici],letawinEM[tici],letawinMAKE[tici],letawin[tici],letawoutEM[tici],letawoutMAKE[tici],letawout[tici]  ) )
            #
        favg3.close()
        #
        favg4 = open('datavst4.txt', 'w')
        favg4.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts"," hoverrhor","hoverr2","hoverr5","hoverr10","hoverr20","hoverr100","hoverrcoronahor","hoverrcorona2","hoverrcorona5","hoverrcorona10","hoverrcorona20","hoverrcorona100","hoverr_jethor","hoverr_jet2","hoverr_jet5","hoverr_jet10","hoverr_jet20","hoverr_jet100"  ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg4.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], hoverrhor[tici],hoverr2[tici],hoverr5[tici],hoverr10[tici],hoverr20[tici],hoverr100[tici],hoverrcoronahor[tici],hoverrcorona2[tici],hoverrcorona5[tici],hoverrcorona10[tici],hoverrcorona20[tici],hoverrcorona100[tici],hoverr_jethor[tici],hoverr_jet2[tici],hoverr_jet5[tici],hoverr_jet10[tici],hoverr_jet20[tici],hoverr_jet100[tici]  ) )
            #
        favg4.close()
        #
        # actually luminosities:    betamin[findex,1:12]=luminosities()
        #
        favg5 = open('datavst5.txt', 'w')
        # 
        favg5.write("#%s %s %s %s %s %s  %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts"," betamin0","betaavg0","betaratofavg0","betaratofmax0","alphamag1_10","alphamag2_10","alphamag3_10","lum1","lum2","lum3","lum4","lum5","lum6","lum7","lum8","lum9","lum10","lum11","lum12","lumsynchth","lumsynchnon1","lumsynchnon2","lumsynchnon3"  ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg5.write("%d %g %g %g %g %g %g  %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], betamin[tici,0],betaavg[tici,0],betaratofavg[tici,0],betaratofmax[tici,0],alphamag1[tici,iofr(10.0)],alphamag2[tici,iofr(10.0)],alphamag3[tici,iofr(10.0)],betamin[tici,1],betamin[tici,2],betamin[tici,3],betamin[tici,4],betamin[tici,5],betamin[tici,6],betamin[tici,7],betamin[tici,8],betamin[tici,9],betamin[tici,10],betamin[tici,11],betamin[tici,12],betamin[tici,13],betamin[tici,14],betamin[tici,15],betamin[tici,16]  ) )
            #
        favg5.close()
        #
        favg6 = open('datavst6.txt', 'w')
        favg6.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts"," qmridiskrfitin2","qmridiskrfitout2","qmridiskrfitout6","iq2mridiskrfitin2","iq2mridiskrfitout2","iq2mridiskrfitout6","qmridiskweakrfitin2","qmridiskweakrfitout2","qmridiskweakrfitout6","iq2mridiskweakrfitin2","iq2mridiskweakrfitout2","iq2mridiskweakrfitout6"   ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg6.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], qmridiskrfitin2[tici],qmridiskrfitout2[tici],qmridiskrfitout6[tici],iq2mridiskrfitin2[tici],iq2mridiskrfitout2[tici],iq2mridiskrfitout6[tici],qmridiskweakrfitin2[tici],qmridiskweakrfitout2[tici],qmridiskweakrfitout6[tici],iq2mridiskweakrfitin2[tici],iq2mridiskweakrfitout2[tici],iq2mridiskweakrfitout6[tici]   ) )
            #
        favg6.close()
        #
        favg7 = open('datavst7.txt', 'w')
        favg7.write("#%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % ("tici","ts"," phibh","phirdiskin","phirdiskout","phij","phimwin","phimwout","phiwin","phiwout","phijn","phijs","fstotihor","fsmaxtotihor","fsuphalfihor","fmaxvst","rifmaxvst","reqstagvst","feqstag","feqstagnearfin","fstotnormA0","fstotnormA1","fstotnormA2","fstotnormC","fstotnormC2","fstotnormBwhichfirstlimited","fstotnormD","fstotnormE","fstotnormE2","fstotnormF" ) )
        for tic in ts:
            tici=np.where(ts==tic)[0]
            #
            favg7.write("%d %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n" % (tici,ts[tici], phibh[tici],phirdiskin[tici],phirdiskout[tici],phij[tici],phimwin[tici],phimwout[tici],phiwin[tici],phiwout[tici],phijn[tici],phijs[tici],fstot[tici,ihor],fsmaxtot[tici,ihor],fsuphalf[tici,ihor],fmaxvst[tici],r[ifmaxvst[tici],0,0],reqstagvst[tici],feqstag[tici],feqstagnearfin[tici],fstotnormA[0][tici],fstotnormA[1][tici],fstotnormA[2][tici],fstotnormC[tici],fstotnormC2[tici],fstotnormB[whichfirstlimited][tici],fstotnormD[tici],fstotnormE[tici],fstotnormE2[tici],fstotnormF[tici]   ) )
            #
        favg7.close()
        #
    #
    #
    #
    #
    #
    ################ Power vs. m plots
    #
    if dopowervsmplots==1:
        print("dopowervsmplots==1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        nfft=nz/2+1
        numm=min(nx,nfft)
        #
        #print("rhosrhosq_diskcorona_phipow_rad4") ; sys.stdout.flush()
        #print(rhosrhosq_diskcorona_phipow_rad4) ; sys.stdout.flush()
        #print("rhosrhosq_jet_phipow_rad4") ; sys.stdout.flush()
        #print(rhosrhosq_jet_phipow_rad4) ; sys.stdout.flush()
        ################################
        # Power vs. m for disk+corona
        ################################
        print("diskcorona" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        ####################################
        rhosrhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_diskcorona_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(rhosrhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            ugsrhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(ugsrhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            uu0rhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(uu0rhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            vuas3rhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(vuas3rhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            bas1rhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(bas1rhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            bas2rhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(bas2rhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            bas3rhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(bas3rhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            bsqrhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(bsqrhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            FMrhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(FMrhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            FEMArhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(FEMArhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
            FEEMrhosq_diskcorona_phipow_radhor_vsm[ii]=timeavg_sqrt(FEEMrhosq_diskcorona_phipow_radhor[:,ii],ts,fti,ftf)
        #
        #  skip: uu0rhosq_diskcorona_phipow_radhor_vsm,vuas3rhosq_diskcorona_phipow_radhor_vsm,
        arrayvsmz=[rhosrhosq_diskcorona_phipow_radhor_vsm,ugsrhosq_diskcorona_phipow_radhor_vsm,bas1rhosq_diskcorona_phipow_radhor_vsm,bas2rhosq_diskcorona_phipow_radhor_vsm,bas3rhosq_diskcorona_phipow_radhor_vsm,bsqrhosq_diskcorona_phipow_radhor_vsm,FMrhosq_diskcorona_phipow_radhor_vsm,FEMArhosq_diskcorona_phipow_radhor_vsm,FEEMrhosq_diskcorona_phipow_radhor_vsm]
        bsqorhohvsmz=bsqrhosq_diskcorona_phipow_radhor_vsm/rhosrhosq_diskcorona_phipow_radhor_vsm
        bsqouhvsmz=bsqrhosq_diskcorona_phipow_radhor_vsm/ugsrhosq_diskcorona_phipow_radhor_vsm
        arrayvsmzname=['rhosrhosq_diskcorona_phipow_radhor_vsm','ugsrhosq_diskcorona_phipow_radhor_vsm','bas1rhosq_diskcorona_phipow_radhor_vsm','bas2rhosq_diskcorona_phipow_radhor_vsm','bas3rhosq_diskcorona_phipow_radhor_vsm','bsqrhosq_diskcorona_phipow_radhor_vsm','FMrhosq_diskcorona_phipow_radhor_vsm','FEMArhosq_diskcorona_phipow_radhor_vsm','FEEMrhosq_diskcorona_phipow_radhor_vsm']
        logvaluearrayvsmz=[0,0,0,0,0,0,0,0,0,0]
        #
        iter=1
        for fil in arrayvsmz:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmzname[iter-1],filenum=iter,fileletter="vsmz",logvalue=logvaluearrayvsmz[iter-1],radius=rhor,bsqorho=bsqorhohvsmz,bsqou=bsqouhvsmz)
            iter=iter+1
        ####################################
        rhosrhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_diskcorona_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(rhosrhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            ugsrhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(ugsrhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            uu0rhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(uu0rhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            vuas3rhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(vuas3rhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            bas1rhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(bas1rhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            bas2rhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(bas2rhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            bas3rhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(bas3rhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            bsqrhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(bsqrhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            FMrhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(FMrhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            FEMArhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(FEMArhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
            FEEMrhosq_diskcorona_phipow_rad4_vsm[ii]=timeavg_sqrt(FEEMrhosq_diskcorona_phipow_rad4[:,ii],ts,fti,ftf)
        #
        arrayvsma=[rhosrhosq_diskcorona_phipow_rad4_vsm,ugsrhosq_diskcorona_phipow_rad4_vsm,uu0rhosq_diskcorona_phipow_rad4_vsm,vuas3rhosq_diskcorona_phipow_rad4_vsm,bas1rhosq_diskcorona_phipow_rad4_vsm,bas2rhosq_diskcorona_phipow_rad4_vsm,bas3rhosq_diskcorona_phipow_rad4_vsm,bsqrhosq_diskcorona_phipow_rad4_vsm,FMrhosq_diskcorona_phipow_rad4_vsm,FEMArhosq_diskcorona_phipow_rad4_vsm,FEEMrhosq_diskcorona_phipow_rad4_vsm]
        bsqorhohvsma=bsqrhosq_diskcorona_phipow_rad4_vsm/rhosrhosq_diskcorona_phipow_rad4_vsm
        bsqouhvsma=bsqrhosq_diskcorona_phipow_rad4_vsm/ugsrhosq_diskcorona_phipow_rad4_vsm
        arrayvsmaname=['rhosrhosq_diskcorona_phipow_rad4_vsm','ugsrhosq_diskcorona_phipow_rad4_vsm','uu0rhosq_diskcorona_phipow_rad4_vsm','vuas3rhosq_diskcorona_phipow_rad4_vsm','bas1rhosq_diskcorona_phipow_rad4_vsm','bas2rhosq_diskcorona_phipow_rad4_vsm','bas3rhosq_diskcorona_phipow_rad4_vsm','bsqrhosq_diskcorona_phipow_rad4_vsm','FMrhosq_diskcorona_phipow_rad4_vsm','FEMArhosq_diskcorona_phipow_rad4_vsm','FEEMrhosq_diskcorona_phipow_rad4_vsm']
        logvaluearrayvsma=[0,0,0,0,0,0,0,0,0,0,0,0]
        #
        iter=1
        for fil in arrayvsma:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmaname[iter-1],filenum=iter,fileletter="vsma",logvalue=logvaluearrayvsma[iter-1],radius=4,bsqorho=bsqorhohvsma,bsqou=bsqouhvsma)
            iter=iter+1
        ####################################
        rhosrhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_diskcorona_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(rhosrhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            ugsrhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(ugsrhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            uu0rhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(uu0rhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            vuas3rhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(vuas3rhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            bas1rhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(bas1rhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            bas2rhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(bas2rhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            bas3rhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(bas3rhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            bsqrhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(bsqrhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            FMrhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(FMrhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            FEMArhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(FEMArhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
            FEEMrhosq_diskcorona_phipow_rad8_vsm[ii]=timeavg_sqrt(FEEMrhosq_diskcorona_phipow_rad8[:,ii],ts,fti,ftf)
        #
        arrayvsmb=[rhosrhosq_diskcorona_phipow_rad8_vsm,ugsrhosq_diskcorona_phipow_rad8_vsm,uu0rhosq_diskcorona_phipow_rad8_vsm,vuas3rhosq_diskcorona_phipow_rad8_vsm,bas1rhosq_diskcorona_phipow_rad8_vsm,bas2rhosq_diskcorona_phipow_rad8_vsm,bas3rhosq_diskcorona_phipow_rad8_vsm,bsqrhosq_diskcorona_phipow_rad8_vsm,FMrhosq_diskcorona_phipow_rad8_vsm,FEMArhosq_diskcorona_phipow_rad8_vsm,FEEMrhosq_diskcorona_phipow_rad8_vsm]
        bsqorhohvsmb=bsqrhosq_diskcorona_phipow_rad8_vsm/rhosrhosq_diskcorona_phipow_rad8_vsm
        bsqouhvsmb=bsqrhosq_diskcorona_phipow_rad8_vsm/ugsrhosq_diskcorona_phipow_rad8_vsm
        arrayvsmbname=['rhosrhosq_diskcorona_phipow_rad8_vsm','ugsrhosq_diskcorona_phipow_rad8_vsm','uu0rhosq_diskcorona_phipow_rad8_vsm','vuas3rhosq_diskcorona_phipow_rad8_vsm','bas1rhosq_diskcorona_phipow_rad8_vsm','bas2rhosq_diskcorona_phipow_rad8_vsm','bas3rhosq_diskcorona_phipow_rad8_vsm','bsqrhosq_diskcorona_phipow_rad8_vsm','FMrhosq_diskcorona_phipow_rad8_vsm','FEMArhosq_diskcorona_phipow_rad8_vsm','FEEMrhosq_diskcorona_phipow_rad8_vsm']
        logvaluearrayvsmb=[0,0,0,0,0,0,0,0,0,0,0,0]
        #
        #
        iter=1
        for fil in arrayvsmb:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmbname[iter-1],filenum=iter,fileletter="vsmb",logvalue=logvaluearrayvsmb[iter-1],radius=8,bsqorho=bsqorhohvsmb,bsqou=bsqouhvsmb)
            iter=iter+1
        ####################################
        rhosrhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_diskcorona_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(rhosrhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            ugsrhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(ugsrhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            uu0rhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(uu0rhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            vuas3rhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(vuas3rhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            bas1rhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(bas1rhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            bas2rhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(bas2rhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            bas3rhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(bas3rhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            bsqrhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(bsqrhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            FMrhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(FMrhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            FEMArhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(FEMArhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
            FEEMrhosq_diskcorona_phipow_rad30_vsm[ii]=timeavg_sqrt(FEEMrhosq_diskcorona_phipow_rad30[:,ii],ts,fti,ftf)
        #
        arrayvsmc=[rhosrhosq_diskcorona_phipow_rad30_vsm,ugsrhosq_diskcorona_phipow_rad30_vsm,uu0rhosq_diskcorona_phipow_rad30_vsm,vuas3rhosq_diskcorona_phipow_rad30_vsm,bas1rhosq_diskcorona_phipow_rad30_vsm,bas2rhosq_diskcorona_phipow_rad30_vsm,bas3rhosq_diskcorona_phipow_rad30_vsm,bsqrhosq_diskcorona_phipow_rad30_vsm,FMrhosq_diskcorona_phipow_rad30_vsm,FEMArhosq_diskcorona_phipow_rad30_vsm,FEEMrhosq_diskcorona_phipow_rad30_vsm]
        bsqorhohvsmc=bsqrhosq_diskcorona_phipow_rad30_vsm/rhosrhosq_diskcorona_phipow_rad30_vsm
        bsqouhvsmc=bsqrhosq_diskcorona_phipow_rad30_vsm/ugsrhosq_diskcorona_phipow_rad30_vsm
        arrayvsmcname=['rhosrhosq_diskcorona_phipow_rad30_vsm','ugsrhosq_diskcorona_phipow_rad30_vsm','uu0rhosq_diskcorona_phipow_rad30_vsm','vuas3rhosq_diskcorona_phipow_rad30_vsm','bas1rhosq_diskcorona_phipow_rad30_vsm','bas2rhosq_diskcorona_phipow_rad30_vsm','bas3rhosq_diskcorona_phipow_rad30_vsm','bsqrhosq_diskcorona_phipow_rad30_vsm','FMrhosq_diskcorona_phipow_rad30_vsm','FEMArhosq_diskcorona_phipow_rad30_vsm','FEEMrhosq_diskcorona_phipow_rad30_vsm']
        logvaluearrayvsmc=[0,0,0,0,0,0,0,0,0,0,0,0]
        #
        iter=1
        for fil in arrayvsmc:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmcname[iter-1],filenum=iter,fileletter="vsmc",logvalue=logvaluearrayvsmc[iter-1],radius=30,bsqorho=bsqorhohvsmc,bsqou=bsqouhvsmc)
            iter=iter+1
        ####################################
        #
        #
        ################################
        # Power vs. m for jet
        ################################
        print("jet" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        ####################################
        ####################################
        rhosrhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_jet_phipow_radhor_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(rhosrhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            ugsrhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(ugsrhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            uu0rhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(uu0rhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            vuas3rhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(vuas3rhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            bas1rhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(bas1rhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            bas2rhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(bas2rhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            bas3rhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(bas3rhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            bsqrhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(bsqrhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            FMrhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(FMrhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            FEMArhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(FEMArhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
            FEEMrhosq_jet_phipow_radhor_vsm[ii]=timeavg_sqrt(FEEMrhosq_jet_phipow_radhor[:,ii],ts,fti,ftf)
        #
        #  skip: uu0rhosq_jet_phipow_radhor_vsm,vuas3rhosq_jet_phipow_radhor_vsm,
        arrayvsmz=[rhosrhosq_jet_phipow_radhor_vsm,ugsrhosq_jet_phipow_radhor_vsm,bas1rhosq_jet_phipow_radhor_vsm,bas2rhosq_jet_phipow_radhor_vsm,bas3rhosq_jet_phipow_radhor_vsm,bsqrhosq_jet_phipow_radhor_vsm,FMrhosq_jet_phipow_radhor_vsm,FEMArhosq_jet_phipow_radhor_vsm,FEEMrhosq_jet_phipow_radhor_vsm]
        bsqorhohvsmz=bsqrhosq_jet_phipow_radhor_vsm/rhosrhosq_jet_phipow_radhor_vsm
        bsqouhvsmz=bsqrhosq_jet_phipow_radhor_vsm/ugsrhosq_jet_phipow_radhor_vsm
        arrayvsmzname=['rhosrhosq_jet_phipow_radhor_vsm','ugsrhosq_jet_phipow_radhor_vsm','bas1rhosq_jet_phipow_radhor_vsm','bas2rhosq_jet_phipow_radhor_vsm','bas3rhosq_jet_phipow_radhor_vsm','bsqrhosq_jet_phipow_radhor_vsm','FMrhosq_jet_phipow_radhor_vsm','FEMArhosq_jet_phipow_radhor_vsm','FEEMrhosq_jet_phipow_radhor_vsm']
        logvaluearrayvsmz=[0,0,0,0,0,0,0,0,0,0]
        #
        iter=1
        for fil in arrayvsmz:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmzname[iter-1],filenum=iter,fileletter="vsmz",logvalue=logvaluearrayvsmz[iter-1],radius=rhor,bsqorho=bsqorhohvsmz,bsqou=bsqouhvsmz)
            iter=iter+1
        ####################################
        rhosrhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_jet_phipow_rad4_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(rhosrhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            ugsrhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(ugsrhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            uu0rhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(uu0rhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            vuas3rhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(vuas3rhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            bas1rhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(bas1rhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            bas2rhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(bas2rhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            bas3rhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(bas3rhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            bsqrhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(bsqrhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            FMrhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(FMrhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            FEMArhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(FEMArhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
            FEEMrhosq_jet_phipow_rad4_vsm[ii]=timeavg_sqrt(FEEMrhosq_jet_phipow_rad4[:,ii],ts,fti,ftf)
        #
        arrayvsma=[rhosrhosq_jet_phipow_rad4_vsm,ugsrhosq_jet_phipow_rad4_vsm,uu0rhosq_jet_phipow_rad4_vsm,vuas3rhosq_jet_phipow_rad4_vsm,bas1rhosq_jet_phipow_rad4_vsm,bas2rhosq_jet_phipow_rad4_vsm,bas3rhosq_jet_phipow_rad4_vsm,bsqrhosq_jet_phipow_rad4_vsm,FMrhosq_jet_phipow_rad4_vsm,FEMArhosq_jet_phipow_rad4_vsm,FEEMrhosq_jet_phipow_rad4_vsm]
        bsqorhohvsma=bsqrhosq_jet_phipow_rad4_vsm/rhosrhosq_jet_phipow_rad4_vsm
        bsqouhvsma=bsqrhosq_jet_phipow_rad4_vsm/ugsrhosq_jet_phipow_rad4_vsm
        arrayvsmaname=['rhosrhosq_jet_phipow_rad4_vsm','ugsrhosq_jet_phipow_rad4_vsm','uu0rhosq_jet_phipow_rad4_vsm','vuas3rhosq_jet_phipow_rad4_vsm','bas1rhosq_jet_phipow_rad4_vsm','bas2rhosq_jet_phipow_rad4_vsm','bas3rhosq_jet_phipow_rad4_vsm','bsqrhosq_jet_phipow_rad4_vsm','FMrhosq_jet_phipow_rad4_vsm','FEMArhosq_jet_phipow_rad4_vsm','FEEMrhosq_jet_phipow_rad4_vsm']
        logvaluearrayvsma=[0,0,0,0,0,0,0,0,0,0,0,0]
        #
        iter=1
        for fil in arrayvsma:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmaname[iter-1],filenum=iter,fileletter="vsma",logvalue=logvaluearrayvsma[iter-1],radius=4,bsqorho=bsqorhohvsma,bsqou=bsqouhvsma)
            iter=iter+1
        ####################################
        rhosrhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_jet_phipow_rad8_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(rhosrhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            ugsrhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(ugsrhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            uu0rhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(uu0rhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            vuas3rhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(vuas3rhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            bas1rhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(bas1rhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            bas2rhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(bas2rhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            bas3rhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(bas3rhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            bsqrhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(bsqrhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            FMrhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(FMrhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            FEMArhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(FEMArhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
            FEEMrhosq_jet_phipow_rad8_vsm[ii]=timeavg_sqrt(FEEMrhosq_jet_phipow_rad8[:,ii],ts,fti,ftf)
        #
        arrayvsmb=[rhosrhosq_jet_phipow_rad8_vsm,ugsrhosq_jet_phipow_rad8_vsm,uu0rhosq_jet_phipow_rad8_vsm,vuas3rhosq_jet_phipow_rad8_vsm,bas1rhosq_jet_phipow_rad8_vsm,bas2rhosq_jet_phipow_rad8_vsm,bas3rhosq_jet_phipow_rad8_vsm,bsqrhosq_jet_phipow_rad8_vsm,FMrhosq_jet_phipow_rad8_vsm,FEMArhosq_jet_phipow_rad8_vsm,FEEMrhosq_jet_phipow_rad8_vsm]
        bsqorhohvsmb=bsqrhosq_jet_phipow_rad8_vsm/rhosrhosq_jet_phipow_rad8_vsm
        bsqouhvsmb=bsqrhosq_jet_phipow_rad8_vsm/ugsrhosq_jet_phipow_rad8_vsm
        arrayvsmbname=['rhosrhosq_jet_phipow_rad8_vsm','ugsrhosq_jet_phipow_rad8_vsm','uu0rhosq_jet_phipow_rad8_vsm','vuas3rhosq_jet_phipow_rad8_vsm','bas1rhosq_jet_phipow_rad8_vsm','bas2rhosq_jet_phipow_rad8_vsm','bas3rhosq_jet_phipow_rad8_vsm','bsqrhosq_jet_phipow_rad8_vsm','FMrhosq_jet_phipow_rad8_vsm','FEMArhosq_jet_phipow_rad8_vsm','FEEMrhosq_jet_phipow_rad8_vsm']
        logvaluearrayvsmb=[0,0,0,0,0,0,0,0,0,0,0,0]
        #
        #
        iter=1
        for fil in arrayvsmb:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmbname[iter-1],filenum=iter,fileletter="vsmb",logvalue=logvaluearrayvsmb[iter-1],radius=8,bsqorho=bsqorhohvsmb,bsqou=bsqouhvsmb)
            iter=iter+1
        ####################################
        rhosrhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        ugsrhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        uu0rhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        vuas3rhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bas1rhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bas2rhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bas3rhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        bsqrhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        FMrhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        FEMArhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        FEEMrhosq_jet_phipow_rad30_vsm=np.zeros(numm,dtype=r.dtype)
        for ii in np.arange(0,numm):
            rhosrhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(rhosrhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            ugsrhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(ugsrhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            uu0rhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(uu0rhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            vuas3rhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(vuas3rhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            bas1rhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(bas1rhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            bas2rhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(bas2rhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            bas3rhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(bas3rhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            bsqrhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(bsqrhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            FMrhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(FMrhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            FEMArhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(FEMArhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
            FEEMrhosq_jet_phipow_rad30_vsm[ii]=timeavg_sqrt(FEEMrhosq_jet_phipow_rad30[:,ii],ts,fti,ftf)
        #
        arrayvsmc=[rhosrhosq_jet_phipow_rad30_vsm,ugsrhosq_jet_phipow_rad30_vsm,uu0rhosq_jet_phipow_rad30_vsm,vuas3rhosq_jet_phipow_rad30_vsm,bas1rhosq_jet_phipow_rad30_vsm,bas2rhosq_jet_phipow_rad30_vsm,bas3rhosq_jet_phipow_rad30_vsm,bsqrhosq_jet_phipow_rad30_vsm,FMrhosq_jet_phipow_rad30_vsm,FEMArhosq_jet_phipow_rad30_vsm,FEEMrhosq_jet_phipow_rad30_vsm]
        bsqorhohvsmc=bsqrhosq_jet_phipow_rad30_vsm/rhosrhosq_jet_phipow_rad30_vsm
        bsqouhvsmc=bsqrhosq_jet_phipow_rad30_vsm/ugsrhosq_jet_phipow_rad30_vsm
        arrayvsmcname=['rhosrhosq_jet_phipow_rad30_vsm','ugsrhosq_jet_phipow_rad30_vsm','uu0rhosq_jet_phipow_rad30_vsm','vuas3rhosq_jet_phipow_rad30_vsm','bas1rhosq_jet_phipow_rad30_vsm','bas2rhosq_jet_phipow_rad30_vsm','bas3rhosq_jet_phipow_rad30_vsm','bsqrhosq_jet_phipow_rad30_vsm','FMrhosq_jet_phipow_rad30_vsm','FEMArhosq_jet_phipow_rad30_vsm','FEEMrhosq_jet_phipow_rad30_vsm']
        logvaluearrayvsmc=[0,0,0,0,0,0,0,0,0,0,0,0]
        #
        iter=1
        for fil in arrayvsmc:
            mkpowervsm(loadq=0,qty=fil,pllabel=arrayvsmcname[iter-1],filenum=iter,fileletter="vsmc",logvalue=logvaluearrayvsmc[iter-1],radius=30,bsqorho=bsqorhohvsmc,bsqou=bsqouhvsmc)
            iter=iter+1
        ####################################
    #
    #########################################################################################
    #
    #
    # to see big norms do:
    # grep normpowersumnotm0 python.plot.full.out | sed 's/=/ /' | sort -g -k7
    #
    #
    ############################
    #
    # some space-time plots
    #
    ###########################
    #
    if dospacetimeplots==0:
        print("****************************")
        print("WARNING: dospacetimeplots==0")
        print("****************************")
    #
    #
    #
    #
    if dospacetimeplots==1:
        print("dospacetimeplots==1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
        #
        #
        dospacetimetest=0
        #
        if dospacetimetest==1:
            #
            #mktr(loadq=0,qty=uu0rhosq,filenum=1,fileletter="q",logvalue=0)
            #print("asdf")
            #print(uu0rhosq)
            #
            #mktr(loadq=0,qty=rhosrhosqhorpick,filenum=1,fileletter="x",logvalue=0)
            #print("asdf")
            #print(rhosrhosqhorpick)
            #
            mktr(loadq=0,qty=vus1rhosq,filenum=1,fileletter="x",logvalue=0)
            print("asdf")
            print(vus1rhosq)
            #
            #mkthrad(loadq=0,qty=uu0rhosqrad4,filenum=1,fileletter="q",logvalue=0,radius=4)
            #print("asdf2")
            #print(uu0rhosqrad4)
        #
        #
        dospacetime=1
        #
        if dospacetime==1:
            ################################
            # t vs. r
            #
            ####################################
            arrayvsra=[rhosrhosq,ugsrhosq,uu0rhosq,vus1rhosq,vuas1rhosq,vus3rhosq,vuas3rhosq,Bs1rhosq,Bas1rhosq,Bs2rhosq,Bas2rhosq,Bs3rhosq,Bas3rhosq,bs1rhosq,bas1rhosq,bs2rhosq,bas2rhosq,bs3rhosq,bas3rhosq,bsqrhosq]
            bsqorhora=bsqrhosq/rhosrhosq
            bsqoura=bsqrhosq/ugsrhosq
            arrayvsraname=['rhosrhosq','ugsrhosq','uu0rhosq','vus1rhosq','vuas1rhosq','vus3rhosq','vuas3rhosq','Bs1rhosq','Bas1rhosq','Bs2rhosq','Bas2rhosq','Bs3rhosq','Bas3rhosq','bs1rhosq','bas1rhosq','bs2rhosq','bas2rhosq','bs3rhosq','bas3rhosq','bsqrhosq']
            logvaluearrayvsra=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvsra:
                mktr(loadq=0,qty=fil,pllabel=arrayvsraname[iter-1],filenum=iter,fileletter="a",logvalue=logvaluearrayvsra[iter-1],bsqorho=bsqorhora,bsqou=bsqoura,maxbsqorho=1E15,maxbsqou=1E15)
                iter=iter+1
            #
            ################################
            arrayvsra=[rhosrhosqdc,ugsrhosqdc,uu0rhosqdc,vus1rhosqdc,vuas1rhosqdc,vus3rhosqdc,vuas3rhosqdc,Bs1rhosqdc,Bas1rhosqdc,Bs2rhosqdc,Bas2rhosqdc,Bs3rhosqdc,Bas3rhosqdc,bs1rhosqdc,bas1rhosqdc,bs2rhosqdc,bas2rhosqdc,bs3rhosqdc,bas3rhosqdc,bsqrhosqdc]
            bsqorhora=bsqrhosqdc/rhosrhosqdc
            bsqoura=bsqrhosqdc/ugsrhosqdc
            arrayvsraname=['rhosrhosqdc','ugsrhosqdc','uu0rhosqdc','vus1rhosqdc','vuas1rhosqdc','vus3rhosqdc','vuas3rhosqdc','Bs1rhosqdc','Bas1rhosqdc','Bs2rhosqdc','Bas2rhosqdc','Bs3rhosqdc','Bas3rhosqdc','bs1rhosqdc','bas1rhosqdc','bs2rhosqdc','bas2rhosqdc','bs3rhosqdc','bas3rhosqdc','bsqrhosqdc']
            logvaluearrayvsra=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvsra:
                mktr(loadq=0,qty=fil,pllabel=arrayvsraname[iter-1],filenum=iter,fileletter="ab",logvalue=logvaluearrayvsra[iter-1],bsqorho=bsqorhora,bsqou=bsqoura,maxbsqorho=1E15,maxbsqou=1E15)
                iter=iter+1
            #
            ################################
            arrayvsra=[rhosrhosqdcden,ugsrhosqdcden,uu0rhosqdcden,vus1rhosqdcden,vuas1rhosqdcden,vus3rhosqdcden,vuas3rhosqdcden,Bs1rhosqdcden,Bas1rhosqdcden,Bs2rhosqdcden,Bas2rhosqdcden,Bs3rhosqdcden,Bas3rhosqdcden,bs1rhosqdcden,bas1rhosqdcden,bs2rhosqdcden,bas2rhosqdcden,bs3rhosqdcden,bas3rhosqdcden,bsqrhosqdcden]
            bsqorhora=bsqrhosqdcden/rhosrhosqdcden
            bsqoura=bsqrhosqdcden/ugsrhosqdcden
            arrayvsraname=['rhosrhosqdcden','ugsrhosqdcden','uu0rhosqdcden','vus1rhosqdcden','vuas1rhosqdcden','vus3rhosqdcden','vuas3rhosqdcden','Bs1rhosqdcden','Bas1rhosqdcden','Bs2rhosqdcden','Bas2rhosqdcden','Bs3rhosqdcden','Bas3rhosqdcden','bs1rhosqdcden','bas1rhosqdcden','bs2rhosqdcden','bas2rhosqdcden','bs3rhosqdcden','bas3rhosqdcden','bsqrhosqdcden']
            logvaluearrayvsra=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvsra:
                mktr(loadq=0,qty=fil,pllabel=arrayvsraname[iter-1],filenum=iter,fileletter="ac",logvalue=logvaluearrayvsra[iter-1],bsqorho=bsqorhora,bsqou=bsqoura,maxbsqorho=1E15,maxbsqou=1E15)
                iter=iter+1
            #
            ####################################
            arrayvsrb=[rhosrhosqeq,ugsrhosqeq,uu0rhosqeq,vus1rhosqeq,vuas1rhosqeq,vus3rhosqeq,vuas3rhosqeq,Bs1rhosqeq,Bas1rhosqeq,Bs2rhosqeq,Bas2rhosqeq,Bs3rhosqeq,Bas3rhosqeq,bs1rhosqeq,bas1rhosqeq,bs2rhosqeq,bas2rhosqeq,bs3rhosqeq,bas3rhosqeq,bsqrhosqeq]
            bsqorhorb=bsqrhosqeq/rhosrhosqeq
            bsqourb=bsqrhosqeq/ugsrhosqeq
            arrayvsrbname=['rhosrhosqeq','ugsrhosqeq','uu0rhosqeq','vus1rhosqeq','vuas1rhosqeq','vus3rhosqeq','vuas3rhosqeq','Bs1rhosqeq','Bas1rhosqeq','Bs2rhosqeq','Bas2rhosqeq','Bs3rhosqeq','Bas3rhosqeq','bs1rhosqeq','bas1rhosqeq','bs2rhosqeq','bas2rhosqeq','bs3rhosqeq','bas3rhosqeq','bsqrhosqeq']
            logvaluearrayvsrb=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            iter=1
            for fil in arrayvsrb:
                mktr(loadq=0,qty=fil,pllabel=arrayvsrbname[iter-1],filenum=iter,fileletter="b",logvalue=logvaluearrayvsrb[iter-1],bsqorho=bsqorhorb,bsqou=bsqourb,maxbsqorho=1E15,maxbsqou=1E15)
                iter=iter+1
            #
            ####################################
            arrayvsrc=[rhosrhosqhorpick,ugsrhosqhorpick,uu0rhosqhorpick,vus1rhosqhorpick,vuas1rhosqhorpick,vus3rhosqhorpick,vuas3rhosqhorpick,Bs1rhosqhorpick,Bas1rhosqhorpick,Bs2rhosqhorpick,Bas2rhosqhorpick,Bs3rhosqhorpick,Bas3rhosqhorpick,bs1rhosqhorpick,bas1rhosqhorpick,bs2rhosqhorpick,bas2rhosqhorpick,bs3rhosqhorpick,bas3rhosqhorpick,bsqrhosqhorpick]
            bsqorhorc=bsqrhosqhorpick/rhosrhosqhorpick
            bsqourc=bsqrhosqhorpick/ugsrhosqhorpick
            arrayvsrcname=['rhosrhosqhorpick','ugsrhosqhorpick','uu0rhosqhorpick','vus1rhosqhorpick','vuas1rhosqhorpick','vus3rhosqhorpick','vuas3rhosqhorpick','Bs1rhosqhorpick','Bas1rhosqhorpick','Bs2rhosqhorpick','Bas2rhosqhorpick','Bs3rhosqhorpick','Bas3rhosqhorpick','bs1rhosqhorpick','bas1rhosqhorpick','bs2rhosqhorpick','bas2rhosqhorpick','bs3rhosqhorpick','bas3rhosqhorpick','bsqrhosqhorpick']
            logvaluearrayvsrc=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvsrc:
                mktr(loadq=0,qty=fil,pllabel=arrayvsrcname[iter-1],filenum=iter,fileletter="c",logvalue=logvaluearrayvsrc[iter-1],bsqorho=bsqorhorc,bsqou=bsqourc,maxbsqorho=1E15,maxbsqou=1E15)
                iter=iter+1
            #
            ####################################
            arrayvsrd=[rhoshor,ugshor,bsqshor,bsqorhoshor,bsqougshor,uu0hor,vus1hor,vuas1hor,vus3hor,vuas3hor,Bs1hor,Bas1hor,Bs2hor,Bas2hor,Bs3hor,Bas3hor,bs1hor,bas1hor,bs2hor,bas2hor,bs3hor,bas3hor,bsqhor]
            bsqorhord=bsqhor/rhoshor
            bsqourd=bsqhor/ugshor
            arrayvsrdname=['rhoshor','ugshor','bsqshor','bsqorhoshor','bsqougshor','uu0hor','vus1hor','vuas1hor','vus3hor','vuas3hor','Bs1hor','Bas1hor','Bs2hor','Bas2hor','Bs3hor','Bas3hor','bs1hor','bas1hor','bs2hor','bas2hor','bs3hor','bas3hor','bsqhor']
            logvaluearrayvsrd=[1,1,1,1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvsrd:
                mktr(loadq=0,qty=fil,pllabel=arrayvsrdname[iter-1],filenum=iter,fileletter="d",logvalue=logvaluearrayvsrd[iter-1],bsqorho=bsqorhord,bsqou=bsqourd,maxbsqorho=1E15,maxbsqou=1E15)
                iter=iter+1
            #
            ################################
            # t vs. \theta no restriction
            #
            ####################################
            arrayvsha=[rhosrhosqrad4,ugsrhosqrad4,uu0rhosqrad4,vus1rhosqrad4,vuas1rhosqrad4,vus3rhosqrad4,vuas3rhosqrad4,Bs1rhosqrad4,Bas1rhosqrad4,Bs2rhosqrad4,Bas2rhosqrad4,Bs3rhosqrad4,Bas3rhosqrad4,bs1rhosqrad4,bas1rhosqrad4,bs2rhosqrad4,bas2rhosqrad4,bs3rhosqrad4,bas3rhosqrad4,bsqrhosqrad4]
            bsqorhoha=bsqrhosqrad4/rhosrhosqrad4
            bsqouha=bsqrhosqrad4/ugsrhosqrad4
            arrayvshaname=['rhosrhosqrad4','ugsrhosqrad4','uu0rhosqrad4','vus1rhosqrad4','vuas1rhosqrad4','vus3rhosqrad4','vuas3rhosqrad4','Bs1rhosqrad4','Bas1rhosqrad4','Bs2rhosqrad4','Bas2rhosqrad4','Bs3rhosqrad4','Bas3rhosqrad4','bs1rhosqrad4','bas1rhosqrad4','bs2rhosqrad4','bas2rhosqrad4','bs3rhosqrad4','bas3rhosqrad4','bsqrhosqrad4']
            logvaluearrayvsha=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvsha:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshaname[iter-1],filenum=iter,fileletter="a",logvalue=logvaluearrayvsha[iter-1],radius=4,bsqorho=bsqorhoha,bsqou=bsqouha)
                iter=iter+1
            #
            ####################################
            arrayvshb=[rhosrhosqrad8,ugsrhosqrad8,uu0rhosqrad8,vus1rhosqrad8,vuas1rhosqrad8,vus3rhosqrad8,vuas3rhosqrad8,Bs1rhosqrad8,Bas1rhosqrad8,Bs2rhosqrad8,Bas2rhosqrad8,Bs3rhosqrad8,Bas3rhosqrad8,bs1rhosqrad8,bas1rhosqrad8,bs2rhosqrad8,bas2rhosqrad8,bs3rhosqrad8,bas3rhosqrad8,bsqrhosqrad8]
            bsqorhohb=bsqrhosqrad8/rhosrhosqrad8
            bsqouhb=bsqrhosqrad8/ugsrhosqrad8
            arrayvshbname=['rhosrhosqrad8','ugsrhosqrad8','uu0rhosqrad8','vus1rhosqrad8','vuas1rhosqrad8','vus3rhosqrad8','vuas3rhosqrad8','Bs1rhosqrad8','Bas1rhosqrad8','Bs2rhosqrad8','Bas2rhosqrad8','Bs3rhosqrad8','Bas3rhosqrad8','bs1rhosqrad8','bas1rhosqrad8','bs2rhosqrad8','bas2rhosqrad8','bs3rhosqrad8','bas3rhosqrad8','bsqrhosqrad8']
            logvaluearrayvshb=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvshb:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshbname[iter-1],filenum=iter,fileletter="b",logvalue=logvaluearrayvshb[iter-1],radius=8,bsqorho=bsqorhohb,bsqou=bsqouhb)
                iter=iter+1
            #
            ####################################
            arrayvshc=[rhosrhosqrad30,ugsrhosqrad30,uu0rhosqrad30,vus1rhosqrad30,vuas1rhosqrad30,vus3rhosqrad30,vuas3rhosqrad30,Bs1rhosqrad30,Bas1rhosqrad30,Bs2rhosqrad30,Bas2rhosqrad30,Bs3rhosqrad30,Bas3rhosqrad30,bs1rhosqrad30,bas1rhosqrad30,bs2rhosqrad30,bas2rhosqrad30,bs3rhosqrad30,bas3rhosqrad30,bsqrhosqrad30]
            bsqorhohc=bsqrhosqrad30/rhosrhosqrad30
            bsqouhc=bsqrhosqrad30/ugsrhosqrad30
            arrayvshcname=['rhosrhosqrad30','ugsrhosqrad30','uu0rhosqrad30','vus1rhosqrad30','vuas1rhosqrad30','vus3rhosqrad30','vuas3rhosqrad30','Bs1rhosqrad30','Bas1rhosqrad30','Bs2rhosqrad30','Bas2rhosqrad30','Bs3rhosqrad30','Bas3rhosqrad30','bs1rhosqrad30','bas1rhosqrad30','bs2rhosqrad30','bas2rhosqrad30','bs3rhosqrad30','bas3rhosqrad30','bsqrhosqrad30']
            logvaluearrayvshc=[1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1]
            #
            iter=1
            for fil in arrayvshc:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshcname[iter-1],filenum=iter,fileletter="c",logvalue=logvaluearrayvshc[iter-1],radius=30,bsqorho=bsqorhohc,bsqou=bsqouhc)
                iter=iter+1
            #
            ################################
            # t vs. \theta  Restrict using bsq/rho.
            ################################
            iter=1
            for fil in arrayvsha:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshaname[iter-1],filenum=iter,fileletter="a",logvalue=logvaluearrayvsha[iter-1],radius=4,bsqorho=bsqorhoha,bsqou=bsqouha,maxbsqorho=1)
                iter=iter+1
            #
            ####################################
            iter=1
            for fil in arrayvshb:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshbname[iter-1],filenum=iter,fileletter="b",logvalue=logvaluearrayvshb[iter-1],radius=8,bsqorho=bsqorhohb,bsqou=bsqouhb,maxbsqorho=1)
                iter=iter+1
            #
            ####################################
            iter=1
            for fil in arrayvshc:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshcname[iter-1],filenum=iter,fileletter="c",logvalue=logvaluearrayvshc[iter-1],radius=30,bsqorho=bsqorhohc,bsqou=bsqouhc,maxbsqorho=1)
                iter=iter+1
            #
            ################################
            # t vs. \theta  Restrict using bsq/u.
            ####################################
            iter=1
            for fil in arrayvsha:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshaname[iter-1],filenum=iter,fileletter="a",logvalue=logvaluearrayvsha[iter-1],radius=4,bsqorho=bsqorhoha,bsqou=bsqouha,maxbsqou=1)
                iter=iter+1
            #
            ####################################
            iter=1
            for fil in arrayvshb:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshbname[iter-1],filenum=iter,fileletter="b",logvalue=logvaluearrayvshb[iter-1],radius=8,bsqorho=bsqorhohb,bsqou=bsqouhb,maxbsqou=1)
                iter=iter+1
            #
            ####################################
            iter=1
            for fil in arrayvshc:
                mkthrad(loadq=0,qty=fil,pllabel=arrayvshcname[iter-1],filenum=iter,fileletter="c",logvalue=logvaluearrayvshc[iter-1],radius=30,bsqorho=bsqorhohc,bsqou=bsqouhc,maxbsqou=1)
                iter=iter+1
            #
            ####################################
        #
        #
        #
        # once these are generated, can quickly view all of them at once at lower resolution by doing:
        # http://www.imagemagick.org/discourse-server/viewtopic.php?f=1&t=11113
        #
        # montage plot*.png output1.png ; display output1.png
        #
        # to get put in order outputted by time:
        #
        # files=`ls -rt plot*.png` ; montage $files output2.png ; display output2.png
        #
        # other programs don't seem as friendly:
        # mogrify
        # convert *.png -composite output.png
        # convert *.png -append output.png
    #
    #
    #
    #
    whichnorm=1
    whichxaxis=1
    numplots=3
    #
    ######################################
    # first ensure time sequence is uniform
    tsnew,bsqrhosqrad4new=maketsuniform(toplot=bsqrhosqrad4)
    tsnew,bs3rhosqrad4new=maketsuniform(toplot=bs3rhosqrad4)
    # 
    # 
    #
    for whichfftplot in np.arange(0,numplots):
    #
    #
        if dofftplot==1 or dospecplot==1: # needed by dospecplot==1
            print("dofftplot==1 whichfftplot==%d" % (whichfftplot) + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
            #
            ####################
            # PLOT:
            fig1 = plt.figure(1)
            if whichfftplot==0:
                fig1.clf()
                #plt.cla()
            #plt.figure(1, figsize=(6,5.8),dpi=200)
            #fig = plt.figure(1)
            #ax1 = fig1.gca()
            #fig1.clf()
            #gs = GridSpec(3, 3)
            #gs.update(left=0.12, right=0.94, top=0.95, bottom=0.1, wspace=0.01, hspace=0.04)
            #ax = fig1.subplot(gs[0,:])
            #
            #
            if numplots==3:
                topf=0.97
                bottomf=0.04
                dropf=(topf-bottomf)/numplots
                if whichfftplot==0:
                    #ax=plt.subplot(311)
                    gs1 = GridSpec(1, 1)
                    gs1.update(left=0.12, right=0.98, top=topf, bottom=topf-dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs1[:,-1])
                    ax.set_xticklabels([])
                elif whichfftplot==1:
                    #ax=plt.subplot(312)
                    gs2 = GridSpec(1, 1)
                    gs2.update(left=0.12, right=0.98, top=topf-dropf, bottom=topf-2*dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs2[:,-1])
                    ax.set_xticklabels([])
                elif whichfftplot==2:
                    #ax=plt.subplot(313)
                    gs3 = GridSpec(1, 1)
                    gs3.update(left=0.12, right=0.98, top=topf-2*dropf, bottom=topf-3*dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs3[:,-1])
            elif numplots==2:
                topf=0.96
                bottomf=0.06
                dropf=(topf-bottomf)/numplots
                if whichfftplot==0:
                    #ax=plt.subplot(311)
                    gs1 = GridSpec(1, 1)
                    gs1.update(left=0.12, right=0.98, top=topf, bottom=topf-dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs1[:,-1])
                    ax.set_xticklabels([])
                elif whichfftplot==1:
                    #ax=plt.subplot(312)
                    gs2 = GridSpec(1, 1)
                    gs2.update(left=0.12, right=0.98, top=topf-dropf, bottom=topf-2*dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs2[:,-1])
                    ax.set_xticklabels([])
            #
            #params = {'xtick.labelsize': 10,'ytick.labelsize': 12}
            #plt.rcParams.update(params)
            #########################################################################################
            # Consider particular slices of the tvsr or tvsh plots for Fourier analysis to see if QPOs clearly present as apparant by eye.
            # http://linuxgazette.net/115/andreasen.html
            #
            # condition for using data is that is within averaging time range
            if modelname=="thickdisk7":
                condt = (tsnew<=ftf)*(tsnew>=fti)
                condt = condt*(tsnew!=tsnew[-1])
                condt = condt*(tsnew>12000.0)
            else:
                condt = (tsnew<=ftf)*(tsnew>=fti)
                # often include final data dump even if not part of periodically chosen set, so avoid for this Fourier measure to avoid contamination
                condt = condt*(tsnew!=tsnew[-1])
            #
            condtfull = (tsnew>=0.0)
            #
            #
            ####################
            xvalue=tsnew[condt]
            xvaluefull=tsnew[condtfull]
            #
            #####################
            # PICK:
            pickradius=4.0 # must be consistent with where yvalue was picked
            iradius=iofr(pickradius)
            if whichfftplot==0:
                picktheta=np.pi*0.5 + 0.0*hoverr_vsr[iradius]
            elif whichfftplot==1:
                picktheta=np.pi*0.5 + 1.0*hoverr_vsr[iradius] # most robust
            elif whichfftplot==2:
                picktheta=np.pi*0.5 + 10.0*hoverr_vsr[iradius] # most robust
            #
            if picktheta>0.95*np.pi:
                picktheta=0.95*np.pi
            if picktheta<0.01:
                picktheta=0.01
            # pick original j value
            pickj=jofh(picktheta,iradius)
            #
            # get nx-sized original h
            xold=(tj[0,:,0]-tj[0,0,0])/(tj[0,-1,0]-tj[0,0,0])
            xnew=(ti[:,0,0]-ti[0,0,0])/(ti[-1,0,0]-ti[0,0,0])
            hnx=np.interp(xnew,xold,h[iradius,:,0])
            jnxofhnx=interp1d(hnx[:],ti[:,0,0],kind='linear')
            pickjnx=jnxofhnx(picktheta)
            pickjnx=np.floor(pickjnx+0.5)
            #
            #
            ############
            # TEST or not:
            testfft=0
            if testfft==0:
                if whichfftplot==0:
                    yvalue=bsqrhosqrad4new[condt,pickjnx] # kinda visible at 8
                    yvaluefull=bsqrhosqrad4new[condtfull,pickjnx] # kinda visible at 8
                    yvaluefull0=yvaluefull
                    plt.title(r"Power in $b^2$ at $r=4r_g$ in Disk Plane",fontsize=16)
                elif whichfftplot==1:
                    yvalue=bsqrhosqrad4new[condt,pickjnx] # kinda visible at 8
                    yvaluefull=bsqrhosqrad4new[condtfull,pickjnx] # kinda visible at 8
                    yvaluefull1=yvaluefull
                    plt.title(r"Power in $b^2$ at $r=4r_g$ at $|h/r|$",fontsize=16)
                elif whichfftplot==2:
                    yvalue=bsqrhosqrad4new[condt,pickjnx] # kinda visible at 8
                    yvaluefull=bsqrhosqrad4new[condtfull,pickjnx] # kinda visible at 8
                    yvaluefull2=yvaluefull
                    plt.title(r"Power in $b^2$ at $r=4r_g$ in Jet",fontsize=16)
                elif whichfftplot==3:
                    yvalue=bsqrhosqrad4new[condt,pickjnx] # kinda visible at 8
                    yvaluefull=bsqrhosqrad4new[condtfull,pickjnx] # kinda visible at 8
                    yvaluefull1=yvaluefull
                    plt.title(r"Power in $b^2$ at $r=4r_g$ in Jet",fontsize=16)
                elif whichfftplot==4:
                    yvalue=bs3rhosqrad4new[condt,pickjnx] # 10 very visible (most robust)
                    print("test yvalue")
                    print(yvalue)
                    yvaluefull=bs3rhosqrad4new[condtfull,pickjnx] # 10 very visible (most robust)
                    yvaluefull2=yvaluefull
                    plt.title(r"Power in $b_\phi^2$ at $r=4r_g$ in Jet",fontsize=16)
                #
            else:
                taupick=65.0
                yvalue=np.sin(2.0*np.pi*(xvalue/taupick))
                yvaluefull0=np.sin(2.0*np.pi*(xvaluefull/taupick))
                yvaluefull1=yvaluefull0
                yvaluefull2=yvaluefull0
            #
            print("picktheta=%g pickj=%d pickjnx=%d" % (picktheta,pickj,pickjnx)); sys.stdout.flush()
            #
            #
            #Yfft=sp.fftpack.fft(yvalue)
            # http://docs.scipy.org/doc/numpy/reference/routines.fft.html
            # http://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.rfft.html#numpy.fft.rfft
            Yfft=np.fft.rfft(yvalue)
            nfft=len(Yfft)
            print("nfft(ninput/2+1)=%d" % (nfft)); sys.stdout.flush()
            #
            Yfftfull=np.fft.rfft(yvaluefull)
            nfftfull=len(Yfftfull)
            print("nfftfull(ninput/2+1)=%d" % (nfftfull)); sys.stdout.flush()
            #
            ####################
            # X:
            #print("normpowerfft")
            #print(normpowerfft)
            DTavg=tsnew[condt][-1]-tsnew[condt][0]
            dtavg=tsnew[condt][-1]-tsnew[condt][-2]
            DTavgfull=tsnew[condtfull][-1]-tsnew[condtfull][0]
            dtavgfull=tsnew[condtfull][-1]-tsnew[condtfull][-2]
            nyquistfft=1.0/(2.0*dtavg)
            nyquistfftfull=1.0/(2.0*dtavgfull)
            print("DTavg=%g dtavg=%g nyquistfft=%g" % (DTavg,dtavg,nyquistfft))
            print("DTavgfull=%g dtavgfull=%g nyquistfftfull=%g" % (DTavgfull,dtavgfull,nyquistfftfull))
            freqfft=np.arange(nfft)/(1.0*nfft)*nyquistfft
            freqfftfull=np.arange(nfftfull)/(1.0*nfftfull)*nyquistfftfull
            periodfft=1./freqfft
            periodfftfull=1./freqfftfull
            normperiodfft=periodfft[1:len(periodfft)]
            normperiodfftfull=periodfftfull[1:len(periodfftfull)]
            #
            if whichxaxis==0:
                xtoplot=normperiodfft
                xtoplotfull=normperiodfftfull
                plt.xscale('log')
                plt.set_xticklabels([])
                if whichfftplot==numplots-1:
                    plt.xlabel(r"Period [$\tau$]",ha='center',labelpad=6)
            else:
                xtoplot=freqfft[1:len(freqfft)]
                xtoplotfull=freqfftfull[1:len(freqfftfull)]
                plt.xscale('log')
                if whichfftplot==numplots-1:
                    plt.xlabel(r"Frequency [$f$, $c/r_g$]",ha='center',labelpad=6)
                #
            #
            #
            ####################
            # Y:
            if whichnorm==0:
                # normalized by total power including period=infinity mode (i.e. average)
                normpowerfft = np.absolute(Yfft[1:nfft])/np.sum(np.absolute(Yfft[0:nfft]))
                #normpowerfftfull = np.absolute(Yfftfull[1:nfftfull])/np.sum(np.absolute(Yfftfull[0:nfftfull]))
                plt.ylabel(r"Power Density",ha='center',labelpad=10,fontsize=16)
            else:
                yaverage=np.mean(yvalue)
                yaveragefull=np.mean(yvaluefull)
                yrms=np.std(yvalue)
                yrmsfull=np.std(yvaluefull)
                fftfactor=(yrms/yaverage)**2
                fftfactorfull=(yrmsfull/yaveragefull)**2
                # van der Klis 1997 and Leahy et al. (1983)
                normpowerfft = 2.0*np.absolute(Yfft[1:nfft])**2/np.absolute(Yfft[0])**2*DTavg
                normpowerfftfull = 2.0*np.absolute(Yfftfull[1:nfftfull])**2/np.absolute(Yfftfull[0])**2*DTavgfull
                # so that \int normpowerfft d\nu = (rms/mean)^2 @ j for d\nu = j/T
                #
                # check this point
                dnu=freqfft[1]-freqfft[0]
                totalrmssq=np.sum(normpowerfft*dnu)
                print("average=%g rms=%g rmsoaveragesq=%g result=%g" % (yaverage,yrms,(yrms/yaverage)**2,totalrmssq)) ; sys.stdout.flush()
                #
                dnufull=freqfftfull[1]-freqfftfull[0]
                totalrmssqfull=np.sum(normpowerfftfull*dnufull)
                print("averagefull=%g rmsfull=%g rmsoaveragesqfull=%g resultfull=%g" % (yaveragefull,yrmsfull,(yrmsfull/yaveragefull)**2,totalrmssqfull)) ; sys.stdout.flush()
                #
                plt.ylabel(r"Power Density [$({\rm rms}/{\rm mean})^2$ $F^{-1}$]",ha='center',labelpad=10,fontsize=16)
            #
            ytoplot=normpowerfft
            #
            if whichfftplot==0:
                yvalue0=np.copy(yvalue)
                ytoplot0=np.copy(ytoplot)
            elif whichfftplot==1:
                yvalue1=np.copy(yvalue)
                ytoplot1=np.copy(ytoplot)
            elif whichfftplot==2:
                yvalue2=np.copy(yvalue)
                ytoplot2=np.copy(ytoplot)
            #
            #
            # FOR PLOT:
            #plt.xlim(0,d/2.); plt.ylim(-d,d)
            #plt.plot(periodfft[1:len(periodfft)],normpowerfft,'o',label=r'label',mfc='r')
            #xtoplot=np.log10(periodfft[1:len(periodfft)])
            #ytoplot=np.log10(normpowerfft)
            #
            plt.yscale('log')
            #
            plt.plot(xtoplot,ytoplot,color='k')
            #
            ################
            # show smothed version too
            window_len=min(10,len(ytoplot))
            sytoplot=smooth(ytoplot,window_len=window_len,window='hanning')
            plt.plot(xtoplot,sytoplot,color='r')
            #
            #
            plt.axis('tight')
            #plt.xlim(np.log10(xtoplot[0]),np.log10(xtoplot[-1]))
            #plt.ylim(np.log10(ytoplot[0]),np.log10(ytoplot[-1]))
            #
            #
            # only save after both plots are done
            if whichfftplot==numplots-1:
                ####################
                # need resolution to show all time resolution -- space is resolved normally
                # total size in inches
                xinches=6.0
                yinches=6.0*numplots
                # non-plotting part that takes up space
                xnonplot=0.75
                ynonplot=0.75
                DPIx=len(xtoplot)/(xinches-xnonplot)
                DPIy=len(ytoplot*numplots)/(yinches-ynonplot*numplots)
                maxresx=10000
                maxresy=10000
                maxDPIx=maxresx/xinches
                maxDPIy=maxresy/yinches
                DPIx=min(DPIx,maxDPIx)
                DPIy=min(DPIy,maxDPIy)
                DPI=max(DPIx,DPIy)
                resx=DPI*xinches
                resy=DPI*yinches
                minres=600
                if resx<minres:
                    DPI=minres/xinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                if resy<minres:
                    DPI=minres/yinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                F = pylab.gcf()
                F.set_size_inches( (xinches, yinches) )
                print("fft Resolution should be %i x %i pixels from DPI=%d (DPIxy=%d %d)" % (resx,resy,DPI,DPIx,DPIy))
                #
                ####################
                plt.savefig("fft1.pdf",dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
                plt.savefig("fft1.eps",dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
                plt.savefig("fft1.png",dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
                #
                # FILE:
                if numplots==3:
                    ffft1 = open('dataprefft1.txt', 'w')
                    for ii in np.arange(0,len(xvalue)):
                        ffft1.write("%d %g   %g %g %g\n" % (ii,xvalue[ii],yvalue0[ii],yvalue1[ii],yvalue2[ii]))
                    ffft1.close()
                    ffft1 = open('dataprefullfft1.txt', 'w')
                    for ii in np.arange(0,len(xvaluefull)):
                        ffft1.write("%d %g   %g %g %g\n" % (ii,xvaluefull[ii],yvaluefull0[ii],yvaluefull1[ii],yvaluefull2[ii]))
                    ffft1.close()
                    ffft1 = open('datafft1.txt', 'w')
                    for ii in np.arange(0,len(xtoplot)):
                        ffft1.write("%d %g   %g %g %g\n" % (ii,xtoplot[ii],ytoplot0[ii],ytoplot1[ii],ytoplot2[ii]))
                    ffft1.close()
                elif numplots==2:
                    ffft1 = open('dataprefft1.txt', 'w')
                    for ii in np.arange(0,len(xvalue)):
                        ffft1.write("%d %g   %g %g\n" % (ii,xvalue[ii],yvalue0[ii],yvalue1[ii]))
                    ffft1.close()
                    ffft1 = open('dataprefullfft1.txt', 'w')
                    for ii in np.arange(0,len(xvaluefull)):
                        ffft1.write("%d %g   %g %g\n" % (ii,xvaluefull[ii],yvaluefull0[ii],yvaluefull1[ii]))
                    ffft1.close()
                    ffft1 = open('datafft1.txt', 'w')
                    for ii in np.arange(0,len(xtoplot)):
                        ffft1.write("%d %g   %g %g\n" % (ii,xtoplot[ii],ytoplot0[ii],ytoplot1[ii]))
                    ffft1.close()
                #
                    
            #
        #
        #########################################################################################
    #
    ######################################
    # SPECTROGRAM
    for whichfftplot in np.arange(0,numplots):
        #
        #########################################################################################
        # fft needed for specplot
        if dospecplot==1 and dofftplot==1:
            print("dospecplot==1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
            # Create a spectogram using matplotlib.mlab.specgram()
            # http://matplotlib.sourceforge.net/api/mlab_api.html#matplotlib.mlab.specgram
            #http://stackoverflow.com/questions/3716528/multi-panel-time-series-of-lines-and-filled-contours-using-matplotlib
            #
            from scipy import fftpack
            #
            if whichfftplot==0:
                yvaluespec=yvaluefull0
            elif whichfftplot==1:
                yvaluespec=yvaluefull1
            elif whichfftplot==2:
                yvaluespec=yvaluefull2
            #
            fig2 = plt.figure(2)
            plt.clf()
            #plt.cla()
            #ax2 = plt.subplot(111)
            params = {'xtick.labelsize': 10,'ytick.labelsize': 12}
            plt.rcParams.update(params)
            gs1 = GridSpec(1, 1)
            gs1.update(left=0.12, right=0.85, top=0.95, bottom=0.10, wspace=0.01, hspace=0.05)
            ax2 = plt.subplot(gs1[:, -1])
            #
            #gs1 = GridSpec(1, 1)
            #gs1.update(left=0.05, right=0.95, top=0.30, bottom=0.03, wspace=0.01, hspace=0.04)
            # get equal resolution in frequency and time for this specgram
            #myNFFT=np.int_(np.rint(np.floor(np.sqrt(len(xvaluefull)))/2)*2)
            myNFFT=np.int_(np.rint(np.floor(np.sqrt(len(xvaluefull)))/2)*2)*2
            #myNFFT=len(tsnew)/16
            noverlap=0
            if myNFFT<noverlap-1:
                noverlap=myNFFT-1
            print("myNFFT=%d noverlap=%d" % (myNFFT,noverlap) ); sys.stdout.flush()
            spec_img,freq,_ = matplotlib.mlab.specgram(yvaluespec,NFFT=myNFFT,noverlap=noverlap,Fs=2.0*nyquistfft)
            #
            if whichnorm==0:
                #plt.title("Normalized Power Density",fontsize=8)
                spec_img=spec_img/np.sum(spec_img)
            else:
                #plt.title(r"Power Density [$({\rm rms}/{\rm mean})^2$ $F^{-1}$]",fontsize=8)
                for iter in np.arange(0,len(spec_img[:,0])):
                    spec_img[iter,:]=2.0*(spec_img[iter,:]**2/spec_img[0,:]**2)*(DTavgfull/len(spec_img[0,:]))
                    #
                #
            #
            period=1/freq
            #print("freq")
            #print(freq)
            #print("period"); sys.stdout.flush()
            #print(period)
            #print("spec_img"); sys.stdout.flush()
            #print(spec_img)
            tspec = np.linspace(xvaluefull.min(), xvaluefull.max(), spec_img.shape[1])
            #
            dologz=1
            if dologz==1:
                spec_img = np.log10(spec_img)
            #
            # avoid period=inf or freq=0
            skipit=2
            periodtoplot=period[skipit:len(period)]
            freqtoplot=freq[skipit:len(freq)]
            # note that even though pcolormesh takes t,period,spec, args of spec are period,tspec !!
            spectoplot=spec_img[skipit:-1,:]
            if dologz==1:
                # dynamic range of 8 allowed
                spectoplot=np.ma.masked_array(spectoplot,mask=spectoplot<np.max(spectoplot)-8)
            else:
                spectoplot=np.ma.masked_array(spectoplot,mask=spectoplot<np.max(spectoplot)/1E8)
            #
            ttoplot=tspec[:]
            #
            if len(periodtoplot>2) and len(spectoplot)>2:
                #
                #
                if whichxaxis==0:
                    im = plt.pcolormesh(ttoplot, periodtoplot, spectoplot)
                    #im = plt.pcolormesh(t, period, spec_img)
                    # periodtoplot is backwards
                    ax2.set_ylim([periodtoplot[-1], periodtoplot[0]])
                    plt.xlabel(r"$t$ [$t_g$]",ha='center',labelpad=6)
                    plt.ylabel(r"$\tau$ [$t_g$]",ha='center',labelpad=6)
                else:
                    im = plt.pcolormesh(ttoplot, freqtoplot, spectoplot)
                    ax2.set_ylim([freqtoplot[0], freqtoplot[-1]])
                    plt.xlabel(r"$t$ [$r_g/c$]",ha='center',labelpad=6,fontsize=16)
                    plt.ylabel(r"Frequency [$f$ , $c/r_g$]",ha='center',labelpad=6,fontsize=16)
                #
                cax = make_legend_axes(ax2)
                if dologz==1:
                    #cbar = plt.colorbar(im, cax=cax, format=r'$10^{%0.1f}$')
                    cbar = plt.colorbar(im, cax=cax, format=r'$10^{%d}$')
                else:
                    cbar = plt.colorbar(im, cax=cax, )
                #
                if whichnorm==0:
                    cbar.set_label('Normalized Power Density', rotation=-90)
                elif whichnorm==1:
                    cbar.set_label(r"Power Density [$({\rm rms}/{\rm mean})^2$ $F^{-1}$]", rotation=-90)                    
                #
                ax2.set_yscale('log')
                #
                #ax2.set_ylim([freq[1], freq.max()])
                # Hide x-axis tick labels
                #plt.setp(plt.get_xticklabels(), visible=False)
                #print("spec")
                #print(spec)
                #extent=(-spec[,len,-len,len)
                #
                #palette=cm.jet
                #palette.set_bad('k', 1.0)
                #
                #CS = plt.imshow(toplot, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=mintoplot,vmax=maxtoplot)
                #CS = plt.imshow(spec[0], cmap = palette)
                #plt.axis('tight')
                #plt.xscale('log')
                #plt.xlim([extent[0],extent[1]])
                #plt.ylim([extent[2],extent[3]])
                #
                #
                #
                #
                #ax1.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
                #plt.ticklabel_format(style='sci', scilimits=(0,0), axis='y')      
                #
                #plt.xlabel(r"$r [r_g]$",ha='center',labelpad=0,fontsize=14)
                #plt.ylabel(r"$t [r_g]$",ha='left',labelpad=20,fontsize=14)
                #
                #gs2 = GridSpec(1, 1)
                #gs2.update(left=0.5, right=1, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
                #ax2 = plt.subplot(gs2[:, -1])
                #
                #if cb==1:
                #    plt.colorbar(CS) # draw colorbar
                #
                #plt.subptitle(pllabel,fontsize=8)
                #plt.title(pllabel,fontsize=8)
                #print("pllabel=%s" % (pllabel))
                #
                #F = pylab.gcf()
                #
                #
                #
                # need resolution to show all time resolution -- space is resolved normally
                #
                xtoplot=tspec
                ytoplot=periodtoplot
                #
                # total size in inches
                xinches=6.0
                yinches=6.0
                # non-plotting part that takes up space
                xnonplot=0.75
                ynonplot=0.75
                DPIy=len(ytoplot)/(yinches-ynonplot)
                DPIx=len(xtoplot)/(xinches-xnonplot)
                maxresx=10000
                maxresy=10000
                maxDPIx=maxresx/xinches
                maxDPIy=maxresy/yinches
                DPIx=min(DPIx,maxDPIx)
                DPIy=min(DPIy,maxDPIy)
                DPI=max(DPIx,DPIy)
                resx=DPI*xinches
                resy=DPI*yinches
                minres=600
                if resx<minres:
                    DPI=minres/xinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                if resy<minres:
                    DPI=minres/yinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                #
                F = pylab.gcf()
                F.set_size_inches( (xinches, yinches) )
                print("fft Resolution should be %i x %i pixels from DPI=%d (DPIxy=%d %d)" % (resx,resy,DPI,DPIx,DPIy))
                #
                if whichfftplot==0:
                    plt.savefig( "spec0.png" ,dpi=DPI)
                    plt.savefig( "spec0.eps" ,dpi=DPI)
                elif whichfftplot==1:
                    plt.savefig( "spec1.png" ,dpi=DPI)
                    plt.savefig( "spec1.eps" ,dpi=DPI)
                elif whichfftplot==2:
                    plt.savefig( "spec2.png" ,dpi=DPI)
                    plt.savefig( "spec2.eps" ,dpi=DPI)
                #
                #sys.stdout.flush()
            else:
                print("Cannot do specplot")
                #
        # end doing specplot
    # end over whichfftplot
    #
    # LUMINOSITIES
    # uses       betamin[findex,1:17]=luminosities()
    numplots=3 # thermal, non-thermal-ug, non-thermal-bsq
    #
    # GODMARK: Need to resample luminosities
    #
    for whichfftplot in np.arange(0,numplots):
    #
    #
        if dofftplot==1 or dospecplot==1: # needed by dospecplot==1
            print("dofftplot==1 whichfftplot==%d" % (whichfftplot) + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
            #
            ####################
            # PLOT:
            fig1 = plt.figure(1)
            if whichfftplot==0:
                fig1.clf()
                #plt.cla()
            #plt.figure(1, figsize=(6,5.8),dpi=200)
            #fig = plt.figure(1)
            #ax1 = fig1.gca()
            #fig1.clf()
            #gs = GridSpec(3, 3)
            #gs.update(left=0.12, right=0.94, top=0.95, bottom=0.1, wspace=0.01, hspace=0.04)
            #ax = fig1.subplot(gs[0,:])
            #
            #
            if numplots==3:
                topf=0.97
                bottomf=0.04
                dropf=(topf-bottomf)/numplots
                if whichfftplot==0:
                    #ax=plt.subplot(311)
                    gs1 = GridSpec(1, 1)
                    gs1.update(left=0.12, right=0.98, top=topf, bottom=topf-dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs1[:,-1])
                    ax.set_xticklabels([])
                elif whichfftplot==1:
                    #ax=plt.subplot(312)
                    gs2 = GridSpec(1, 1)
                    gs2.update(left=0.12, right=0.98, top=topf-dropf, bottom=topf-2*dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs2[:,-1])
                    ax.set_xticklabels([])
                elif whichfftplot==2:
                    #ax=plt.subplot(313)
                    gs3 = GridSpec(1, 1)
                    gs3.update(left=0.12, right=0.98, top=topf-2*dropf, bottom=topf-3*dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs3[:,-1])
            elif numplots==2:
                topf=0.96
                bottomf=0.06
                dropf=(topf-bottomf)/numplots
                if whichfftplot==0:
                    #ax=plt.subplot(311)
                    gs1 = GridSpec(1, 1)
                    gs1.update(left=0.12, right=0.98, top=topf, bottom=topf-dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs1[:,-1])
                    ax.set_xticklabels([])
                elif whichfftplot==1:
                    #ax=plt.subplot(312)
                    gs2 = GridSpec(1, 1)
                    gs2.update(left=0.12, right=0.98, top=topf-dropf, bottom=topf-2*dropf, wspace=0.01, hspace=0.04)
                    ax = plt.subplot(gs2[:,-1])
                    ax.set_xticklabels([])
            #
            #params = {'xtick.labelsize': 10,'ytick.labelsize': 12}
            #plt.rcParams.update(params)
            #########################################################################################
            # Consider particular slices of the tvsr or tvsh plots for Fourier analysis to see if QPOs clearly present as apparant by eye.
            # http://linuxgazette.net/115/andreasen.html
            #
            # condition for using data is that is within averaging time range
            if modelname=="thickdisk7":
                condt = (ts<=ftf)*(ts>=fti)
                condt = condt*(ts!=ts[-1])
                condt = condt*(ts>12000.0)
            else:
                condt = (ts<=ftf)*(ts>=fti)
                # often include final data dump even if not part of periodically chosen set, so avoid for this Fourier measure to avoid contamination
                condt = condt*(ts!=ts[-1])
            #
            condtfull = (ts>=0.0)
            #
            #
            ####################
            xvalue=ts[condt]
            xvaluefull=ts[condtfull]
            #
            #####################
            #
            #lum1=13 ; lum2=14 ; lum3=15
            #lum1=1 ; lum2=2 ; lum3=3
            #lum1=4 ; lum2=5 ; lum3=6
            #lum1=7 ; lum2=8 ; lum3=9
            #lum1=10 ; lum2=11 ; lum3=12
            if modelname=="thickdisk3" or modelname=="thickdiskhr3":
                # no jet, so values=0 and kills fft
                lum1=12 ; lum2=13 ; lum3=14
            else:
                lum1=13 ; lum2=15 ; lum3=16
            #
            ############
            if whichfftplot==0:
                yvalue=betamin[condt,lum1]
                yvaluefull=betamin[condtfull,lum1]
                yvaluefull0=yvaluefull
                plt.title(r"Power in Thermal Synchrotron",fontsize=10)
            elif whichfftplot==1:
                yvalue=betamin[condt,lum2]
                yvaluefull=betamin[condtfull,lum2]
                yvaluefull1=yvaluefull
                plt.title(r"Power in Non-Thermal ($n_{e,\rm non-th}\propto u_g$) Synchrotron",fontsize=10)
            elif whichfftplot==2:
                yvalue=betamin[condt,lum3]
                yvaluefull=betamin[condtfull,lum3]
                yvaluefull2=yvaluefull
                plt.title(r"Power in Non-Thermal ($n_{e,\rm non-th}\propto b^2$) Synchrotron",fontsize=10)
            #
            #
            Yfft=np.fft.rfft(yvalue)
            nfft=len(Yfft)
            print("nfft(ninput/2+1)=%d" % (nfft)); sys.stdout.flush()
            #
            Yfftfull=np.fft.rfft(yvaluefull)
            nfftfull=len(Yfftfull)
            print("nfftfull(ninput/2+1)=%d" % (nfftfull)); sys.stdout.flush()
            #
            ####################
            # X:
            #print("normpowerfft")
            #print(normpowerfft)
            DTavg=ts[condt][-1]-ts[condt][0]
            dtavg=ts[condt][-1]-ts[condt][-2]
            DTavgfull=ts[condtfull][-1]-ts[condtfull][0]
            dtavgfull=ts[condtfull][-1]-ts[condtfull][-2]
            nyquistfft=1.0/(2.0*dtavg)
            nyquistfftfull=1.0/(2.0*dtavgfull)
            print("DTavg=%g dtavg=%g nyquistfft=%g" % (DTavg,dtavg,nyquistfft))
            print("DTavgfull=%g dtavgfull=%g nyquistfftfull=%g" % (DTavgfull,dtavgfull,nyquistfftfull))
            freqfft=np.arange(nfft)/(1.0*nfft)*nyquistfft
            freqfftfull=np.arange(nfftfull)/(1.0*nfftfull)*nyquistfftfull
            periodfft=1./freqfft
            periodfftfull=1./freqfftfull
            normperiodfft=periodfft[1:len(periodfft)]
            normperiodfftfull=periodfftfull[1:len(periodfftfull)]
            #
            if whichxaxis==0:
                xtoplot=normperiodfft
                xtoplotfull=normperiodfftfull
                plt.xscale('log')
                plt.set_xticklabels([])
                if whichfftplot==numplots-1:
                    plt.xlabel(r"Period [$\tau$]",ha='center',labelpad=6)
            else:
                xtoplot=freqfft[1:len(freqfft)]
                xtoplotfull=freqfftfull[1:len(freqfftfull)]
                plt.xscale('log')
                if whichfftplot==numplots-1:
                    plt.xlabel(r"Frequency [$f$, $c/r_g$]",ha='center',labelpad=6)
                #
            #
            #
            ####################
            # Y:
            if whichnorm==0:
                # normalized by total power including period=infinity mode (i.e. average)
                normpowerfft = np.absolute(Yfft[1:nfft])/np.sum(np.absolute(Yfft[0:nfft]))
                #normpowerfftfull = np.absolute(Yfftfull[1:nfftfull])/np.sum(np.absolute(Yfftfull[0:nfftfull]))
                plt.ylabel(r"Power Density",ha='center',labelpad=10)
            else:
                yaverage=np.mean(yvalue)
                yaveragefull=np.mean(yvaluefull)
                yrms=np.std(yvalue)
                yrmsfull=np.std(yvaluefull)
                fftfactor=(yrms/yaverage)**2
                fftfactorfull=(yrmsfull/yaveragefull)**2
                # van der Klis 1997 and Leahy et al. (1983)
                normpowerfft = 2.0*np.absolute(Yfft[1:nfft])**2/np.absolute(Yfft[0])**2*DTavg
                normpowerfftfull = 2.0*np.absolute(Yfftfull[1:nfftfull])**2/np.absolute(Yfftfull[0])**2*DTavgfull
                # so that \int normpowerfft d\nu = (rms/mean)^2 @ j for d\nu = j/T
                #
                # check this point
                dnu=freqfft[1]-freqfft[0]
                totalrmssq=np.sum(normpowerfft*dnu)
                print("average=%g rms=%g rmsoaveragesq=%g result=%g" % (yaverage,yrms,(yrms/yaverage)**2,totalrmssq)) ; sys.stdout.flush()
                #
                dnufull=freqfftfull[1]-freqfftfull[0]
                totalrmssqfull=np.sum(normpowerfftfull*dnufull)
                print("averagefull=%g rmsfull=%g rmsoaveragesqfull=%g resultfull=%g" % (yaveragefull,yrmsfull,(yrmsfull/yaveragefull)**2,totalrmssqfull)) ; sys.stdout.flush()
                #
                plt.ylabel(r"Power Density [$({\rm rms}/{\rm mean})^2$ $F^{-1}$]",ha='center',labelpad=10)
            #
            ytoplot=normpowerfft
            #
            if whichfftplot==0:
                yvalue0=np.copy(yvalue)
                ytoplot0=np.copy(ytoplot)
            elif whichfftplot==1:
                yvalue1=np.copy(yvalue)
                ytoplot1=np.copy(ytoplot)
            elif whichfftplot==2:
                yvalue2=np.copy(yvalue)
                ytoplot2=np.copy(ytoplot)
            #
            #
            # FOR PLOT:
            #plt.xlim(0,d/2.); plt.ylim(-d,d)
            #plt.plot(periodfft[1:len(periodfft)],normpowerfft,'o',label=r'label',mfc='r')
            #xtoplot=np.log10(periodfft[1:len(periodfft)])
            #ytoplot=np.log10(normpowerfft)
            #
            plt.yscale('log')
            #
            plt.plot(xtoplot,ytoplot,color='k')
            #
            ################
            # show smothed version too
            window_len=min(10,len(ytoplot))
            sytoplot=smooth(ytoplot,window_len=window_len,window='hanning')
            plt.plot(xtoplot,sytoplot,color='r')
            #
            #
            plt.axis('tight')
            #plt.xlim(np.log10(xtoplot[0]),np.log10(xtoplot[-1]))
            #plt.ylim(np.log10(ytoplot[0]),np.log10(ytoplot[-1]))
            #
            #
            # only save after both plots are done
            if whichfftplot==numplots-1:
                ####################
                # need resolution to show all time resolution -- space is resolved normally
                # total size in inches
                xinches=6.0
                yinches=6.0*numplots
                # non-plotting part that takes up space
                xnonplot=0.75
                ynonplot=0.75
                DPIx=len(xtoplot)/(xinches-xnonplot)
                DPIy=len(ytoplot*numplots)/(yinches-ynonplot*numplots)
                maxresx=10000
                maxresy=10000
                maxDPIx=maxresx/xinches
                maxDPIy=maxresy/yinches
                DPIx=min(DPIx,maxDPIx)
                DPIy=min(DPIy,maxDPIy)
                DPI=max(DPIx,DPIy)
                resx=DPI*xinches
                resy=DPI*yinches
                minres=600
                if resx<minres:
                    DPI=minres/xinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                if resy<minres:
                    DPI=minres/yinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                F = pylab.gcf()
                F.set_size_inches( (xinches, yinches) )
                print("fft Resolution should be %i x %i pixels from DPI=%d (DPIxy=%d %d)" % (resx,resy,DPI,DPIx,DPIy))
                #
                ####################
                plt.savefig("fftsyn.pdf",dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
                plt.savefig("fftsyn.eps",dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
                plt.savefig("fftsyn.png",dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
                #
                # FILE:
                if numplots==3:
                    ffft1 = open('dataprefftsyn.txt', 'w')
                    for ii in np.arange(0,len(xvalue)):
                        ffft1.write("%d %g   %g %g %g\n" % (ii,xvalue[ii],yvalue0[ii],yvalue1[ii],yvalue2[ii]))
                    ffft1.close()
                    ffft1 = open('dataprefullfftsyn.txt', 'w')
                    for ii in np.arange(0,len(xvaluefull)):
                        ffft1.write("%d %g   %g %g %g\n" % (ii,xvaluefull[ii],yvaluefull0[ii],yvaluefull1[ii],yvaluefull2[ii]))
                    ffft1.close()
                    ffft1 = open('datafftsyn.txt', 'w')
                    for ii in np.arange(0,len(xtoplot)):
                        ffft1.write("%d %g   %g %g %g\n" % (ii,xtoplot[ii],ytoplot0[ii],ytoplot1[ii],ytoplot2[ii]))
                    ffft1.close()
                elif numplots==2:
                    ffft1 = open('dataprefftsyn.txt', 'w')
                    for ii in np.arange(0,len(xvalue)):
                        ffft1.write("%d %g   %g %g\n" % (ii,xvalue[ii],yvalue0[ii],yvalue1[ii]))
                    ffft1.close()
                    ffft1 = open('dataprefullfftsyn.txt', 'w')
                    for ii in np.arange(0,len(xvaluefull)):
                        ffft1.write("%d %g   %g %g\n" % (ii,xvaluefull[ii],yvaluefull0[ii],yvaluefull1[ii]))
                    ffft1.close()
                    ffft1 = open('datafftsyn.txt', 'w')
                    for ii in np.arange(0,len(xtoplot)):
                        ffft1.write("%d %g   %g %g\n" % (ii,xtoplot[ii],ytoplot0[ii],ytoplot1[ii]))
                    ffft1.close()
                #
                    
            #
        #
        #########################################################################################
        #
        #
    ######################################
    # SPECTROGRAM
    for whichfftplot in np.arange(0,numplots):
        #
        #########################################################################################
        # fft needed for specplot
        if dospecplot==1 and dofftplot==1:
            print("dospecplot==1" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
            # Create a spectogram using matplotlib.mlab.specgram()
            # http://matplotlib.sourceforge.net/api/mlab_api.html#matplotlib.mlab.specgram
            #http://stackoverflow.com/questions/3716528/multi-panel-time-series-of-lines-and-filled-contours-using-matplotlib
            #
            from scipy import fftpack
            #
            if whichfftplot==0:
                yvaluespec=yvaluefull0
            elif whichfftplot==1:
                yvaluespec=yvaluefull1
            elif whichfftplot==2:
                yvaluespec=yvaluefull2
            #
            fig2 = plt.figure(2)
            plt.clf()
            #plt.cla()
            #ax2 = plt.subplot(111)
            params = {'xtick.labelsize': 10,'ytick.labelsize': 12}
            plt.rcParams.update(params)
            gs1 = GridSpec(1, 1)
            gs1.update(left=0.12, right=0.85, top=0.95, bottom=0.10, wspace=0.01, hspace=0.05)
            ax2 = plt.subplot(gs1[:, -1])
            #
            #gs1 = GridSpec(1, 1)
            #gs1.update(left=0.05, right=0.95, top=0.30, bottom=0.03, wspace=0.01, hspace=0.04)
            # get equal resolution in frequency and time for this specgram
            #myNFFT=np.int_(np.rint(np.floor(np.sqrt(len(xvaluefull)))/2)*2)
            myNFFT=np.int_(np.rint(np.floor(np.sqrt(len(xvaluefull)))/2)*2)*2
            #myNFFT=len(ts)/16
            noverlap=0
            if myNFFT<noverlap-1:
                noverlap=myNFFT-1
            print("myNFFT=%d noverlap=%d" % (myNFFT,noverlap) ); sys.stdout.flush()
            spec_img,freq,_ = matplotlib.mlab.specgram(yvaluespec,NFFT=myNFFT,noverlap=noverlap,Fs=2.0*nyquistfft)
            #
            if whichnorm==0:
                #plt.title("Normalized Power Density",fontsize=8)
                spec_img=spec_img/np.sum(spec_img)
            else:
                #plt.title(r"Power Density [$({\rm rms}/{\rm mean})^2$ $F^{-1}$]",fontsize=8)
                for iter in np.arange(0,len(spec_img[:,0])):
                    spec_img[iter,:]=2.0*(spec_img[iter,:]**2/spec_img[0,:]**2)*(DTavgfull/len(spec_img[0,:]))
                    #
                #
            #
            period=1/freq
            #print("freq")
            #print(freq)
            #print("period"); sys.stdout.flush()
            #print(period)
            #print("spec_img"); sys.stdout.flush()
            #print(spec_img)
            tspec = np.linspace(xvaluefull.min(), xvaluefull.max(), spec_img.shape[1])
            #
            dologz=1
            if dologz==1:
                spec_img = np.log10(spec_img)
            #
            # avoid period=inf or freq=0
            skipit=2
            periodtoplot=period[skipit:len(period)]
            freqtoplot=freq[skipit:len(freq)]
            # note that even though pcolormesh takes t,period,spec, args of spec are period,tspec !!
            spectoplot=spec_img[skipit:-1,:]
            if dologz==1:
                # dynamic range of 8 allowed
                spectoplot=np.ma.masked_array(spectoplot,mask=spectoplot<np.max(spectoplot)-8)
            else:
                spectoplot=np.ma.masked_array(spectoplot,mask=spectoplot<np.max(spectoplot)/1E8)
            #
            ttoplot=tspec[:]
            #
            if len(periodtoplot>2) and len(spectoplot)>2:
                #
                #
                if whichxaxis==0:
                    im = plt.pcolormesh(ttoplot, periodtoplot, spectoplot)
                    #im = plt.pcolormesh(t, period, spec_img)
                    # periodtoplot is backwards
                    ax2.set_ylim([periodtoplot[-1], periodtoplot[0]])
                    plt.xlabel(r"$t$ [$t_g$]",ha='center',labelpad=6)
                    plt.ylabel(r"$\tau$ [$t_g$]",ha='center',labelpad=6)
                else:
                    im = plt.pcolormesh(ttoplot, freqtoplot, spectoplot)
                    ax2.set_ylim([freqtoplot[0], freqtoplot[-1]])
                    plt.xlabel(r"$t$ [$r_g/c$]",ha='center',labelpad=6)
                    plt.ylabel(r"Frequency [$f$ , $c/r_g$]",ha='center',labelpad=6)
                #
                cax = make_legend_axes(ax2)
                if dologz==1:
                    #cbar = plt.colorbar(im, cax=cax, format=r'$10^{%0.1f}$')
                    cbar = plt.colorbar(im, cax=cax, format=r'$10^{%d}$')
                else:
                    cbar = plt.colorbar(im, cax=cax, )
                #
                if whichnorm==0:
                    cbar.set_label('Normalized Power Density', rotation=-90)
                elif whichnorm==1:
                    cbar.set_label(r"Power Density [$({\rm rms}/{\rm mean})^2$ $F^{-1}$]", rotation=-90)                    
                #
                ax2.set_yscale('log')
                #
                #ax2.set_ylim([freq[1], freq.max()])
                # Hide x-axis tick labels
                #plt.setp(plt.get_xticklabels(), visible=False)
                #print("spec")
                #print(spec)
                #extent=(-spec[,len,-len,len)
                #
                #palette=cm.jet
                #palette.set_bad('k', 1.0)
                #
                #CS = plt.imshow(toplot, extent=extent, cmap = palette, norm = colors.Normalize(clip = False),origin='lower',vmin=mintoplot,vmax=maxtoplot)
                #CS = plt.imshow(spec[0], cmap = palette)
                #plt.axis('tight')
                #plt.xscale('log')
                #plt.xlim([extent[0],extent[1]])
                #plt.ylim([extent[2],extent[3]])
                #
                #
                #
                #
                #ax1.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
                #plt.ticklabel_format(style='sci', scilimits=(0,0), axis='y')      
                #
                #plt.xlabel(r"$r [r_g]$",ha='center',labelpad=0,fontsize=14)
                #plt.ylabel(r"$t [r_g]$",ha='left',labelpad=20,fontsize=14)
                #
                #gs2 = GridSpec(1, 1)
                #gs2.update(left=0.5, right=1, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
                #ax2 = plt.subplot(gs2[:, -1])
                #
                #if cb==1:
                #    plt.colorbar(CS) # draw colorbar
                #
                #plt.subptitle(pllabel,fontsize=8)
                #plt.title(pllabel,fontsize=8)
                #print("pllabel=%s" % (pllabel))
                #
                #F = pylab.gcf()
                #
                #
                #
                # need resolution to show all time resolution -- space is resolved normally
                #
                xtoplot=tspec
                ytoplot=periodtoplot
                #
                # total size in inches
                xinches=6.0
                yinches=6.0
                # non-plotting part that takes up space
                xnonplot=0.75
                ynonplot=0.75
                DPIy=len(ytoplot)/(yinches-ynonplot)
                DPIx=len(xtoplot)/(xinches-xnonplot)
                maxresx=10000
                maxresy=10000
                maxDPIx=maxresx/xinches
                maxDPIy=maxresy/yinches
                DPIx=min(DPIx,maxDPIx)
                DPIy=min(DPIy,maxDPIy)
                DPI=max(DPIx,DPIy)
                resx=DPI*xinches
                resy=DPI*yinches
                minres=600
                if resx<minres:
                    DPI=minres/xinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                if resy<minres:
                    DPI=minres/yinches
                    resx=DPI*xinches
                    resy=DPI*yinches
                #
                F = pylab.gcf()
                F.set_size_inches( (xinches, yinches) )
                print("fft Resolution should be %i x %i pixels from DPI=%d (DPIxy=%d %d)" % (resx,resy,DPI,DPIx,DPIy))
                #
                if whichfftplot==0:
                    plt.savefig( "specsyn0.png" ,dpi=DPI)
                    plt.savefig( "specsyn0.eps" ,dpi=DPI)
                elif whichfftplot==1:
                    plt.savefig( "specsyn1.png" ,dpi=DPI)
                    plt.savefig( "specsyn1.eps" ,dpi=DPI)
                elif whichfftplot==2:
                    plt.savefig( "specsyn2.png" ,dpi=DPI)
                    plt.savefig( "specsyn2.eps" ,dpi=DPI)
                #
                #sys.stdout.flush()
            else:
                print("Cannot do specplot")
                #
        # end doing specplot
    # end over whichfftplot
    #
    #########################################
    #
    dofinalplots=1
    #
    # FINALPLOTS:
    #
    if dofinalplots==1 and dothradfinalplot==1:
        # b_\phi vs. \theta and time (have to account for fact that fieldline files have dump period different at early times.)
        # the below changes defaults to rcparams, so leave for last
        bsqorhoha=bsqrhosqrad4/rhosrhosqrad4
        bsqouha=bsqrhosqrad4/ugsrhosqrad4
        toplot=bs3rhosqrad4
        mkthrad(loadq=0,qty=toplot,pllabel='',filenum=0,fileletter="q",logvalue=0,radius=4,bsqorho=bsqorhoha,bsqou=bsqouha)
    #
    #
    #########################
    # INIT PLOT
    #
    if dofinalplots==1 and doinitfinalplot==1:
        mkinitfinalplot()
        print("mkinitfinalplot" + " time elapsed: %d" % (datetime.now()-start_time).seconds ) ; sys.stdout.flush()
    #
    #
    #
    #
    #
    #
    #################################################                    
    # output density vs. \phi on r_{\\rm{}H}, 4M, 8M, 30M so can see mode structure in \phi
    rhor=1+(1-a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    i4 = np.floor(iofr(4)+0.5)
    i8 = np.floor(iofr(8)+0.5)
    i30 = np.floor(iofr(30)+0.5)
    #
    #
    if modelname=="thickdisk7":
        # choose frame where there is interesting \phi structure
        if len(ts)>1000:
            rfd("fieldline3215.bin")
        else:
            rfd("../fieldline3215.bin")
    else:
        rfdlastfile()
    #
    denfactor=1.0 + rho*0
    diskcondition=condmaxbsqorho # full non-jet
    keywordsrhosqdcfull1={'which': diskcondition}
    tiny=np.finfo(rho.dtype).tiny
    rhosqdcfull1int=intangle(gdet*denfactor,doavgn3=0,**keywordsrhosqdcfull1)+tiny # gdet is 2d by default
    rhosrhosqdcfull1=intangle(gdet*denfactor*rho,doavgn3=0,**keywordsrhosqdcfull1)/rhosqdcfull1int
    #
    datavsphi = open('datavsphi1.txt', 'w')
    for ii in np.arange(0,nz):
        datavsphi.write("%g %d %g  %g %g %g %g  %g %g %g %g  %g %g %g %g\n" % (t,ii,ph[0,ny/2,ii],rhosrhosqdcfull1[ihor,ii],rhosrhosqdcfull1[i4,ii],rhosrhosqdcfull1[i8,ii],rhosrhosqdcfull1[i30,ii],rhoclean[ihor,ny/2,ii],rhoclean[i4,ny/2,ii],rhoclean[i8,ny/2,ii],rhoclean[i30,ny/2,ii],rhounclean[ihor,ny/2,ii],rhounclean[i4,ny/2,ii],rhounclean[i8,ny/2,ii],rhounclean[i30,ny/2,ii]))
    datavsphi.close()
    #
    # output density vs. \phi on r_{\\rm{}H}, 4M, 8M, 30M so can see mode structure in \phi
    if modelname=="thickdisk7":
        # choose frame where there is interesting \phi structure
        rfd("fieldline4190.bin")
    else:
        rfdlastfile()
    #
    denfactor=1.0 + rho*0
    diskcondition=condmaxbsqorho # full non-jet
    keywordsrhosqdcfull2={'which': diskcondition}
    tiny=np.finfo(rho.dtype).tiny
    rhosqdcfull2int=intangle(gdet*denfactor,doavgn3=0,**keywordsrhosqdcfull2)+tiny # gdet is 2d by default
    rhosrhosqdcfull2=intangle(gdet*denfactor*rho,doavgn3=0,**keywordsrhosqdcfull2)/rhosqdcfull2int
    #
    datavsphi = open('datavsphi2.txt', 'w')
    for ii in np.arange(0,nz):
        datavsphi.write("%g %d %g  %g %g %g %g  %g %g %g %g  %g %g %g %g\n" % (t,ii,ph[0,ny/2,ii],rhosrhosqdcfull2[ihor,ii],rhosrhosqdcfull2[i4,ii],rhosrhosqdcfull2[i8,ii],rhosrhosqdcfull2[i30,ii],rhoclean[ihor,ny/2,ii],rhoclean[i4,ny/2,ii],rhoclean[i8,ny/2,ii],rhoclean[i30,ny/2,ii],rhounclean[ihor,ny/2,ii],rhounclean[i4,ny/2,ii],rhounclean[i8,ny/2,ii],rhounclean[i30,ny/2,ii]))
    datavsphi.close()
    #
    # output density vs. \phi on r_{\\rm{}H}, 4M, 8M, 30M so can see mode structure in \phi
    if modelname=="thickdisk7":
        if len(ts)>1000:
            # choose frame where there is interesting \phi structure
            rfd("fieldline4300.bin")
        else:
            rfd("../fieldline4300.bin")
    else:
        rfdlastfile()
    #
    denfactor=1.0 + rho*0
    diskcondition=condmaxbsqorho # full non-jet
    keywordsrhosqdcfull3={'which': diskcondition}
    tiny=np.finfo(rho.dtype).tiny
    rhosqdcfull3int=intangle(gdet*denfactor,doavgn3=0,**keywordsrhosqdcfull3)+tiny # gdet is 2d by default
    rhosrhosqdcfull3=intangle(gdet*denfactor*rho,doavgn3=0,**keywordsrhosqdcfull3)/rhosqdcfull3int
    #
    datavsphi = open('datavsphi3.txt', 'w')
    for ii in np.arange(0,nz):
        datavsphi.write("%g %d %g  %g %g %g %g  %g %g %g %g  %g %g %g %g\n" % (t,ii,ph[0,ny/2,ii],rhosrhosqdcfull3[ihor,ii],rhosrhosqdcfull3[i4,ii],rhosrhosqdcfull3[i8,ii],rhosrhosqdcfull3[i30,ii],rhoclean[ihor,ny/2,ii],rhoclean[i4,ny/2,ii],rhoclean[i8,ny/2,ii],rhoclean[i30,ny/2,ii],rhounclean[ihor,ny/2,ii],rhounclean[i4,ny/2,ii],rhounclean[i8,ny/2,ii],rhounclean[i30,ny/2,ii]))
    datavsphi.close()
    #
    #
    #
    #
    # FINALPLOT:
    # ssh jmckinne@orange.slac.stanford.edu
    # cd /lustre/ki/orange/jmckinne/thickdisk7/movie8new2
    #
    # scp fft1.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/fft1_thickdisk7.eps ;scp spec1.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/spec1_thickdisk7.eps ;scp spec2.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/spec2_thickdisk7.eps ; scp plot0qvsth_.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/plottvsr_bphi.eps ; scp plot0qvsth_.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/plottvsth_bphi.eps

    # scp lrhosmall3215_Rzxym1.eps lrhosmall4190_Rzxym1.eps lrhosmall4300_Rzxym1.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/ ; scp init1.eps middle1.eps final1.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/

    # convert final1_stream.png final1_stream.eps ; scp final1_stream.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/figfinalflowfield.eps ; convert middle1_stream.png middle1_stream.eps ; scp middle1_stream.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/figmiddleflowfield.eps


    #
    # copy over data vs. radius , data vs. time, data vs. angle for SM plots:
    # whichrun="thickdisk7" ; scp datavs*.txt jmckinne@ki-jmck:/data2/jmckinne/$whichrun/fromorange_movie8new2/


#/data2/jmckinne/thickdisk7/fromorange_movie8new2







# get levels for aphi plot part of init/final plots
def mkinitfinalplotpre2(whichlevs=0):
    #
    if whichlevs==0:
        aphijetoutermax=np.max(aphi[:,:,:])
        aphijetoutermin=np.min(aphi[:,:,:])
        aphijetouter=np.max(np.fabs(aphijetoutermax),np.fabs(aphijetoutermin))
    else:
        # now get field line that attaches to H
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        aphijetoutermax=np.max(aphi[ihor,:,:])
        aphijetoutermin=np.min(aphi[ihor,:,:])
        if np.fabs(aphijetoutermax)>np.fabs(aphijetoutermin):
            aphijetouter=aphijetoutermax
        else:
            aphijetouter=aphijetoutermin
        #
    print("whichlevs=%d aphijetouter=%g" % (whichlevs,aphijetouter))
    #
    return(aphijetouter)
    #

# compute things for init/final plots
def mkinitfinalplotpre1():
    print("init/final plot: cvel()") ; sys.stdout.flush()
    cvel()
    #
    #aphi = fieldcalc() # cvel() does that now
    #aphi = np.sqrt(aphi**2)
    #
    print("init/final plot: done aphi()") ; sys.stdout.flush()
    # below not needed for initfinal and makes things very slow
    if 1==0:
        print("init/final plot: Tcalcud()") ; sys.stdout.flush()
        Tcalcud(maxbsqorho=maxbsqorhonear,which=condmaxbsqorho)
        print("init/final plot: faraday()") ; sys.stdout.flush()
        faraday()
        print("init/final plot: done faraday()") ; sys.stdout.flush()
    #print("finalplots firstlast=%d t=%g" % (firstlast,t) )
    #cvel()
    #Tcalcud()
    #faraday()
    #






#true init/final plot
def mkinitfinalplot():
    #########################
    # INIT/FINAL type PLOT
    #
    #
    aphipow=1.0
    #
    for firstlast in np.arange(2,-1,-1):
        #
        if firstlast==0:
            rfdfirstfile()
            inputlevs=returnlevsinitfinal
        elif firstlast==1:
            if modelname=="thickdisk7":
                rfd("fieldline3000.bin")
            else:
                rfdlastfile()
            inputlevs=None
            #inputlevs=returnlevsinitfinal
        elif firstlast==2:
            if modelname=="thickdisk7":
                # thickdisk7 ran long enough so last dump is not typical, it's where jet is being destroyed
                #rfdlastfile()
                # so instead choose typical frame
                rfd("fieldline4373.bin")
            else:
                rfdlastfile()
            #
            #
            inputlevs=None
        #
        # default
        numcontours=60
        #
        if firstlast==0:
            print("Outputting init1"); sys.stdout.flush()
            fname="init1"
        elif firstlast==1:
            print("Outputting middle1"); sys.stdout.flush()
            fname="middle1"
        else:
            print("Outputting final1"); sys.stdout.flush()
            fname="final1"
        #
        if firstlast==0:
            fnamestream="init1_stream"
        elif firstlast==1:
            fnamestream="middle1_stream"
        else:
            fnamestream="final1_stream"
        #      
        # compute
        mkinitfinalplotpre1()
        #
        # get information to setup levels if required
        if inputlevs==None:
            aphijetouter=mkinitfinalplotpre2(whichlevs=1)
        #
        returnlevsinitfinal=mkinitfinalplotpost(fname=fname,plottype=firstlast,aphijetouter=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
        #
        #
        if firstlast==1 or firstlast==2:
            # Only doing non-initstremaline.  init streamline dies with memory issue if density=8
            # inputlevs=None so independent contours from initplot
            # default
            showuu1eq0=True
            if firstlast==1:
                numcontours=30 # less contours for field lines
                showuu1eq0=False
            #
            returnlevsstream=mkstreamplotprepost(fname=fnamestream,inputlevs=None,numcontours=numcontours,aphipow=aphipow,showuu1eq0=showuu1eq0)
    # end over firstlast loop



# do single initfinal type plot
# fname: filename
# plottype: 1=always same  0=different (used for true init plot that has different range for z-values (e.g. beta))
def mkinitfinalplotpost(fname=None,plottype=0,aphijetouter=None,inputlevs=None,numcontours=30,aphipow=1.0):
    #
    maxnumpanels=5 # up to 5, but 5 too many for final figure and not necessary
    #myplots=[0,1,2] # choose quantities
    myplots=[1] # reduced paper to save space and eliminate redundancy
    numpanels=len(myplots)
    #
    #
    whichpanel=-1
    for whichplot in np.arange(0,maxnumpanels):
        # whichplot: indicates which plot number to use and so *quantity* to plot (picks myplot number)
        # whichpanel : iterates across desired plots and so *panel* to use (picks panel to plot in)
        #
        if whichplot not in myplots:
            continue
        #
        whichpanel=whichpanel+1
        #
        #
        ####################
        # PLOT:
        if whichpanel==0:
            fig1 = plt.figure(999)
            fig1.clf()
            figprops = dict(figsize=(8., 8. / 1.618), dpi=128)
            if numpanels==5:
                adjustprops = dict(left=0.1, bottom=0.02, right=0.97, top=0.99, wspace=0.0, hspace=0.0)
            elif numpanels==3:
                adjustprops = dict(left=0.1, bottom=0.03, right=0.97, top=0.99, wspace=0.0, hspace=0.0)
            else:
                adjustprops = dict(left=0.1, bottom=0.03, right=0.97, top=0.99, wspace=0.0, hspace=0.0)
            #plt.cla()
            #fig = pylab.figure(**figprops)
            fig1.subplots_adjust(**adjustprops)
            #gs1 = GridSpec(numplots, 1)
            #gs1.update(left=0.12, right=0.98, top=0.97, bottom=0.04, wspace=0.01, hspace=0.04)
            #gs2=gs1
            #gs3=gs1
            #gs4=gs1
            #gs5=gs1
            #
        #topf=0.97
        #bottomf=0.04
        #dropf=(topf-bottomf)/numpanels
        #http://matplotlib.sourceforge.net/gallery.html
        # http://www.scipy.org/Cookbook/Matplotlib/Multiple_Subplots_with_One_Axis_Label
        # http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.subplot
        # http://comments.gmane.org/gmane.comp.python.matplotlib.general/27961
        if whichpanel==0:
            #gs1.update(left=0.12, right=0.98, top=topf, bottom=topf-dropf, wspace=0.01, hspace=0.04)
            #gs1 = GridSpec(numpanels, 1)
            #ax1 = plt.subplot(gs1[0,:])
            #ax1.set_xticklabels([])
            ax1 = fig1.add_subplot(numpanels,1,whichpanel+1)
            cax=ax1
            if whichpanel!=numpanels-1:
                plt.setp(ax1.get_xticklabels(), visible=False)
            #plt.cla()
        if whichpanel==1:
            #gs2 = GridSpec(1, 1)
            #gs2.update(left=0.12, right=0.98, top=topf-1*dropf, bottom=topf-2*dropf, wspace=0.01, hspace=0.04)
            #ax2 = plt.subplot(gs2[1,:])
            #ax2 = fig1.add_subplot(gs2[1,:],sharex=ax1)
            #ax2.set_xticklabels([])
            ax2 = fig1.add_subplot(numpanels,1,whichpanel+1,sharex=ax1,sharey=ax1)
            cax=ax2
            if whichpanel!=numpanels-1:
                plt.setp(ax2.get_xticklabels(), visible=False)
            #plt.cla()
        if whichpanel==2:
            #gs3 = GridSpec(1, 1)
            #gs3.update(left=0.12, right=0.98, top=topf-2*dropf, bottom=topf-3*dropf, wspace=0.01, hspace=0.04)
            #ax3 = plt.subplot(gs3[2,:])
            #ax3 = fig1.add_subplot(gs3[2,:],sharex=ax1)
            #ax3.set_xticklabels([])
            ax3 = fig1.add_subplot(numpanels,1,whichpanel+1,sharex=ax1,sharey=ax1)
            cax=ax3
            if whichpanel!=numpanels-1:
                plt.setp(ax3.get_xticklabels(), visible=False)
            #plt.cla()
        if whichpanel==3:
            #gs4 = GridSpec(1, 1)
            #gs4.update(left=0.12, right=0.98, top=topf-3*dropf, bottom=topf-4*dropf, wspace=0.01, hspace=0.04)
            #ax4 = plt.subplot(gs4[3,:])
            #ax4 = fig1.add_subplot(gs4[3,:],sharex=ax1)
            #ax4.set_xticklabels([])
            ax4 = fig1.add_subplot(numpanels,1,whichpanel+1,sharex=ax1,sharey=ax1)
            cax=ax4
            if whichpanel!=numpanels-1:
                plt.setp(ax4.get_xticklabels(), visible=False)
            #plt.cla()
        if whichpanel==4:
            #gs5 = GridSpec(1, 1)
            #gs5.update(left=0.12, right=0.98, top=topf-3*dropf, bottom=topf-5*dropf, wspace=0.01, hspace=0.04)
            #ax5 = plt.subplot(gs5[3,:])
            #ax5 = fig1.add_subplot(gs5[3,:],sharex=ax1)
            #ax5.set_xticklabels([])
            ax5 = fig1.add_subplot(numpanels,1,whichpanel+1,sharex=ax1,sharey=ax1)
            cax=ax5
            if whichpanel!=numpanels-1:
                plt.setp(ax5.get_xticklabels(), visible=False)
            #plt.cla()
        #
        #plt.title(r"Power in $b_\phi^2$ at $r=4r_g$ in Jet",fontsize=10)
        #plt.xscale('log')
        #plt.set_xticklabels([])
        #
        if 1==1:
            findex=0
            framesize=150
            plotsize=framesize
            plotsizex=framesize*90.0/150.0
            plotsizey=framesize
            #
            #
#            if whichplot==0:
#                if plottype==0 or plottype==1:
#                    vmaxforframe=np.max(np.log10(rho[0:iofr(framesize),:,:]))
#                    vminforframe=vmaxforframe-4
#                elif plottype==2:
#                    (vminforframe,vmaxforframe)=vminmax_rho(qty=rho)
#                #
#                returnlevs=mkframe("inittype%04d_Rz%g" % (findex,plotsize),vmin=vminforframe,vmax=vmaxforframe,lenx=plotsizex,leny=plotsizey,ax=cax,cb=True,tight=True,pt=False,dorho=True,doaphi=True,dostreamlines=False,shrink=0.8,doaphicont=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
            if whichplot==0:
                if plottype==0 or plottype==1:
                    #vmaxforframe=np.max(np.log10(entropy[0:iofr(framesize),:,:]))
                    vmaxforframe=-0.8
                    vminforframe=-1.25
                elif plottype==2:
                    (vminforframe,vmaxforframe)=vminmax_entropy(qty=entropy)
                #
                returnlevs=mkframe("inittype%04d_Rz%g" % (findex,plotsize),vmin=vminforframe,vmax=vmaxforframe,lenx=plotsizex,leny=plotsizey,ax=cax,cb=True,tight=True,pt=False,dorho=False,doentropy=True,doaphi=True,dostreamlines=False,shrink=0.8,doaphicont=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
            elif whichplot==1:
                if plottype==0 or plottype==1:
                    vmaxforframe=np.max(np.log10(bsq[0:iofr(framesize),:,:]))
                    vminforframe=vmaxforframe-7
                else:
                    (vminforframe,vmaxforframe)=vminmax_bsq(qty=bsq)
                #
                returnlevs=mkframe("inittype%04d_Rz%g" % (findex,plotsize),vmin=vminforframe,vmax=vmaxforframe,lenx=plotsizex,leny=plotsizey,ax=cax,cb=True,tight=True,pt=False,dorho=False,dobsq=True,doaphi=True,dostreamlines=False,shrink=0.8,doaphicont=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
            elif whichplot==2:
                if plottype==0 or plottype==1:
                    vminforframe=np.log10(1.0/np.max(1.0/beta[0:iofr(framesize),:,:]))
                    vmaxforframe=np.log10(min(500.0,np.max(beta[0:iofr(framesize),:,:])))
                else:
                    #vminforframe=1.0/np.max(1.0/beta[0:iofr(framesize),:,:])
                    #vmaxforframe=min(50.0,np.max(beta[0:iofr(framesize),:,:]))
                    vminforframe=-3.0
                    vmaxforframe=3.0
                returnlevs=mkframe("inittype%04d_Rz%g" % (findex,plotsize),vmin=vminforframe,vmax=vmaxforframe,lenx=plotsizex,leny=plotsizey,ax=cax,cb=True,tight=True,pt=False,dorho=False,dobeta=True,doaphi=True,dostreamlines=False,shrink=0.8,doaphicont=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
            elif whichplot==3:
                vminforframe=0
                vmaxforframe=np.max(Q1[0:iofr(framesize),:,:])
                #
                returnlevs=mkframe("inittype%04d_Rz%g" % (findex,plotsize),vmin=vminforframe,vmax=vmaxforframe,lenx=plotsizex,leny=plotsizey,ax=cax,cb=True,tight=True,pt=False,dorho=False,doQ1=True,doaphi=True,dostreamlines=False,shrink=0.8,doaphicont=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
            elif whichplot==4:
                vminforframe=np.min(Q2[0:iofr(framesize),:,:])
                vmaxforframe=min(10.0,np.max(Q2[0:iofr(framesize),:,:]))
                #
                returnlevs=mkframe("inittype%04d_Rz%g" % (findex,plotsize),vmin=vminforframe,vmax=vmaxforframe,lenx=plotsizex,leny=plotsizey,ax=cax,cb=True,tight=True,pt=False,dorho=False,doQ2=True,doaphi=True,dostreamlines=False,shrink=0.8,doaphicont=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
            #
        if 1==1:
            plt.ylabel(r"$z\ [r_g]$",ha='left',labelpad=10,fontsize=16)
            if whichpanel==numpanels-1:
                plt.xlabel(r"$x\ [r_g]$",fontsize=16,ha='center')
        #
        ####################
        # need resolution to show all time resolution -- space is resolved normally
        # total size in inches
        xinches=6.0
        yinches=6.0*numpanels
        # non-plotting part that takes up space
        xnonplot=0.75+2 # 2 more inches for colorbar
        ynonplot=0.75
        DPIx=len(rho[:,0,0])/(xinches-xnonplot)
        DPIy=len(rho[:,0,0]*numpanels)/(yinches-ynonplot*numpanels)
        maxresx=10000
        maxresy=10000
        maxDPIx=maxresx/xinches
        maxDPIy=maxresy/yinches
        DPIx=min(DPIx,maxDPIx)
        DPIy=min(DPIy,maxDPIy)
        DPI=max(DPIx,DPIy)
        resx=DPI*xinches
        resy=DPI*yinches
        minres=600
        if resx<minres:
            DPI=minres/xinches
            resx=DPI*xinches
            resy=DPI*yinches
        if resy<minres:
            DPI=minres/yinches
            resx=DPI*xinches
            resy=DPI*yinches
        F = pylab.gcf()
        F.set_size_inches( (xinches, yinches) )
        print("init Resolution should be %i x %i pixels from DPI=%d (DPIxy=%d %d)" % (resx,resy,DPI,DPIx,DPIy)); sys.stdout.flush()
        print("whichplot=%d whichpanel=%d numpanels=%d" % (whichplot,whichpanel,numpanels)) ; sys.stdout.flush()
        #
        # only save after both plots are done
        ####################
        if whichpanel==numpanels-1:
            print("Outputting %s" % fname); sys.stdout.flush()
            plt.savefig("%s.pdf" % fname ,dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
            plt.savefig("%s.eps" % fname ,dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
            plt.savefig("%s.png" % fname ,dpi=DPI)#,bbox_inches='tight',pad_inches=0.1)
        #
        #
        #
        # end if whichpanel==numpanels-1
    # end over mywhichplot loop
    return(returnlevs)




def vminmax_rho(qty=None):
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-4.0
        vmaxforframe=0.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-4.0
        vmaxforframe=0.5
    else:
        # for Jon's thickdisk models
        vminforframe=-2.4
        vmaxforframe=1.5625
    #
    return(vminforframe,vmaxforframe)


def vminmax_ug(qty=None):
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-5.0
        vmaxforframe=1.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-5.0
        vmaxforframe=1.5
    else:
        # for Jon's thickdisk models
        vminforframe=-3.4
        vmaxforframe=3.0
    #
    return(vminforframe,vmaxforframe)

def vminmax_bsq(qty=None):
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-7.0
        vmaxforframe=1.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-7.0
        vmaxforframe=1.5
    else:
        # for Jon's thickdisk models
        vminforframe=-7.0
        vmaxforframe=3.0
    #
    #
    return(vminforframe,vmaxforframe)

def vminmax_entropy(qty=None):
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-1.0
        vmaxforframe=2.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-1.0
        vmaxforframe=2.5
    else:
        # for Jon's thickdisk models
        vminforframe=-1.0
        vmaxforframe=4.0
    #
    #
    return(vminforframe,vmaxforframe)



def mkstreamplotprepost(fname=None,veldensity=8,inputlevs=None,numcontours=30,aphipow=1.0,showuu1eq0=True):
    # stream plot
    forceeqsym=0
    #mylen = 30
    #mylen = 200
    fntsize=24
    arrowsize=4
    #veldensity=8 # test, use 8 for real
    signaphi=1.0
    #
    if 1==0:
        #finallenx=140
        #finalleny=200
        # don't know why, but stream starts at lowest value even if not square.
        finallenx=110
        finalleny=110
        mylenshowx=100
        mylenshowy=100
    else:
        finallenx=51
        finalleny=51
        mylenshowx=50
        mylenshowy=50
    #
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-4.0
        vmaxforframe=0.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-4.0
        vmaxforframe=0.5
    else:
        # for Jon's thickdisk models
        vminforframe=-2.4
        vmaxforframe=1.5625
    #
    # for dojonwindplot
    global B,uutrue
    Btrue=np.copy(B)
    uutrue=uu
    #      
    returnlevs=mkstreamplot1(Btrue=Btrue,gdetB=gdetB,bsq=bsq,rho=rho,uu=uu,lenx=finallenx,leny=finalleny,mylenshowx=mylenshowx,mylenshowy=mylenshowy,fntsize=fntsize,arrowsize=arrowsize,vminforframe=vminforframe,vmaxforframe=vmaxforframe,forceeqsym=forceeqsym,fname=fname,veldensity=veldensity,signaphi=signaphi,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow,dojonwindplot=1,showuu1eq0=showuu1eq0)
    #
    # since could have modified B, fix back
    B=np.copy(Btrue)
    #
    return(returnlevs)







# cat datavsr6.txt | awk '{print $1" "$2" "$10" "$11}' | column -t | less -S
# cat datavsr6.txt | awk '{print $1" "$2" "1.57-$10" "$11}' | column -t > datavsrshare.txt
def compute_thetaalongfield(aphi=None,picki=None,thetaalongjet=None,whichpole=0):
    # need to compute this again
    rhor=1+(1-a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    #
    if aphi is None:
        # compute final-time aphi for now
        rfdlastfile()
        aphi = fieldcalcface()
        #maxaphibh=np.max(aphi[ihor,:,0])
        #
        plt.figure(6)
        myfun=aphi[0:iofr(30.0),:,0]
        myxcoord=r[0:iofr(30.0),:,0]*np.sin(h[0:iofr(30.0),:,0])
        myycoord=r[0:iofr(30.0),:,0]*np.cos(h[0:iofr(30.0),:,0])
        plco(myfun,xcoord=myxcoord,ycoord=myycoord,colors='k',nc=30)
        #plco(aphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),colors='k',nc=30)
        #plc(daphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='r')
        #d=500
        #plt.xlim(0,d/2.); plt.ylim(-d,d)
        #plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.savefig("aphi.pdf")
        plt.savefig("aphi.eps")
        plt.savefig("aphi.png")
        #
        #
        print("aphi.shape()"); sys.stdout.flush()
        print(aphi.shape); sys.stdout.flush()
        # aphi is now 2D (r,\theta) averaged in \phi-direction
        #aphi = fieldcalc()
        #iaphi = reinterp(aphi,extent,ncell,domask=0)
        #aphi = fieldcalc()
        #iaphi = reinterp(aphi,extent,ncell,domask=0)
    #
    ###############
    # find out aphi value where thetaalongjet[picki]
    print("thetaalongjet[picki]=%g" % (thetaalongjet[picki]))
    if whichpole==0:
        signpole=-1
    else:
        signpole=+1
    #
    pickh=np.pi*0.5+signpole*thetaalongjet[picki]
    #
    print("pickh=%g" % (pickh))
    pickj=jofh(pickh,picki)
    # too close to jet and field bends back around potentially.  Also aphi can be very slightly non-monotonic and interp1d then can barf
    # GODMARK: numjoffset has to be tuned for a given setup/model/etc.
    # 10 works for runlocaldipole last snapshot, but not for averages (field bleeds into the wind and loops around)
    # GODMARK: need modelname=="" here?
    numjoffset=16*(ny/128)
    pickj=pickj+signpole*numjoffset
    aphijetbase=aphi[picki,pickj,0]
    print("aphijetbase"); sys.stdout.flush()
    print(aphijetbase); sys.stdout.flush()
    #
    cs = plt.contour(r[:,:,0],h[:,:,0],aphi[:,:,0], [aphijetbase])
    p = cs.collections[0].get_paths()[0]
    v = p.vertices
    x = v[:,0]
    y = v[:,1]
    #
    # find parts that cross horizon since otherwise ambiguous
    lastx=x[0]
    maxnumcrosses=1000
    whichiv=0
    ivihorlist=np.zeros(maxnumcrosses,dtype=np.float32)
    dirihorlist=np.zeros(maxnumcrosses,dtype=np.float32)
    for iv in np.arange(1,len(x)):
        if (x[iv-1]<rhor and x[iv]>rhor):
            ivihorlist[whichiv]=iv
            dirihorlist[whichiv]=+1
            whichiv=whichiv+1
        if (x[iv-1]>rhor and x[iv]<rhor):
            ivihorlist[whichiv]=iv
            dirihorlist[whichiv]=-1
            whichiv=whichiv+1
        #
    #
    print("original number of vertices=%d" % (len(x)))
    print("number of crosses of horizon: %d" % (whichiv)); sys.stdout.flush()
    print("ivihorlist"); sys.stdout.flush()
    print(ivihorlist[0:whichiv+1]); sys.stdout.flush()
    print("dirihorlist"); sys.stdout.flush()
    print(dirihorlist[0:whichiv+1]); sys.stdout.flush()
    #
    #
    #
    # only use portion that is monotonically increasing in radius
    if whichpole==0:
        lastx=x[0]
        lastiv=len(x)
        for iv in np.arange(1,len(x)):
            if x[iv]<lastx:
                lastiv=iv
                break
            else:
                lastx=x[iv]
            #
        print("lastiv=%d" % (lastiv))
        xnew=x[0:lastiv] # avoids final decrease in x
        ynew=y[0:lastiv] # avoids final decrease in x
    #
    # only use portion that is monotonically increasing in radius
    if whichpole==1:
        lastx=x[len(x)-1]
        lastiv=0
        for iv in np.arange(len(x)-2,-1,-1):
            if x[iv]<lastx:
                lastiv=iv
                break
            else:
                lastx=x[iv]
            #
        print("lastiv=%d" % (lastiv))
        xnew=x[len(x)-1:lastiv:-1] # avoids final decrease in x
        ynew=y[len(x)-1:lastiv:-1] # avoids final decrease in x
    #
    #
    #print("xnew")
    #print(xnew)
    #print("ynew")
    #print(ynew)
    #
    # get x back to r[:,0,0] since r doesn't depend upon \theta most of the time
    # have to fill since radii in xnew (or even x) less sampled than r[:,0,0]
    if len(xnew)>2 and len(ynew)>2:
        if modelname=="runlocaldipole3dfiducial":
            yofx = interp1d(xnew[:], ynew[:], kind='linear',bounds_error=False,fill_value=ynew[-2])
        else:
            yofx = interp1d(xnew[:], ynew[:], kind='linear',bounds_error=False,fill_value=ynew[-1])
        #
        thetaalongfield=yofx(r[:,0,0])
        # the below model has issues with reflection at large radii
        if modelname=="runlocaldipole3dfiducial":
            rchop=900.0
            ichop=iofr(rchop)
            thetaalongfield[ti[:,0,0]>ichop]=thetaalongfield[ichop]
        #
    else:
        thetaalongfield=0*r[:,0,0]
        print("Could not get thetaalongfield")
    #
    return(aphijetbase,thetaalongfield)
    #







# plot power vs. m for a given quantity
def mkpowervsm(loadq=0,qty=None,pllabel="",filenum=0,fileletter="",logvalue=0,radius=None,bsqorho=None,bsqou=None):
    #plt.figure(1, figsize=(6,5.8),dpi=200)
    plt.figure(1)
    plt.clf()
    #plt.cla()
    #plt.clf()
    #gs = GridSpec(3, 3)
    #gs.update(left=0.12, right=0.94, top=0.95, bottom=0.1, wspace=0.01, hspace=0.04)
    #ax1 = plt.subplot(gs[0,:])
    #plt.xlim(0,d/2.); plt.ylim(-d,d)
    #plt.plot(periodfft[1:len(periodfft)],powerfft,'o',label=r'label',mfc='r')
    #xtoplot=np.log10(periodfft[1:len(periodfft)])
    #ytoplot=np.log10(powerfft)
    #
    # Set xtoplot as m
    #
    #translate to nx size
    nfft=nz/2+1
    numm=min(nx,nfft)
    xtoplot=np.zeros(numm,dtype=np.float32)
    for mm in np.arange(0,numm):
        xtoplot[mm]=mm
    #
    # see if can to plot at all
    if qty[0]!=0.0:
        #
        #
        # set ytoplot as Normalized power (normalized to total power!)
        # power was originally saved as |a_j|^2, but want to see |a_j| since if (e.g.) a_1=a_0, then sin(\phi) generates deviations as large as average, such that if a_0=1, then a_1=1  means F_M goes up to 2 and down to 0 across in \phi, which is maximum possible deviation.  So normalize to a_0, not sum.
        #ytoplot=qty/np.sum(qty)
        ytoplot=np.fabs(qty/qty[0])
        #
        normpowersumnotm0a=np.sum(qty[1:len(qty)]**2)/np.sum(qty**2)
        normpowersumnotm0b=np.sum(np.fabs(qty[1:len(qty)]))/np.fabs(qty[0])
        print("mkpowervsm: %d %s %s : normpowersumnotm0a=%g normpowersumnotm0b=%g" % (filenum,fileletter,pllabel,normpowersumnotm0a,normpowersumnotm0b) )
    else:
        ytoplot=np.fabs(qty)
        normpowersumnotm0a=np.sum(qty[1:len(qty)]**2)
        normpowersumnotm0b=np.sum(np.fabs(qty[1:len(qty)]))
    #
    #
    if np.sum(qty)==0.0:
        print("Can't do log plot since all values are just zero")
        dologplot=0
    else:
        dologplot=1
    #
    #
    #
    print("mkpowervsm: len(xtoplot)=%d len(ytoplot)=%d" % (len(xtoplot),len(ytoplot))) ; sys.stdout.flush()
    #
    #print("mkpowervsm: xtoplot") ; sys.stdout.flush()
    #print(xtoplot) ; sys.stdout.flush()
    #
    #print("mkpowervsm: ytoplot") ; sys.stdout.flush()
    #print(ytoplot) ; sys.stdout.flush()
    #
    plt.title("%s %g" % (pllabel,normpowersumnotm0b) , fontsize=8)
    print("pllabel=%s npnotm=%g" % (pllabel,normpowersumnotm0b))
    #
    plt.plot(xtoplot[1:numm],ytoplot[1:numm])
    #plt.axis('tight')
    if dologplot==1:
        plt.xscale('log')
        plt.yscale('log')
        #plt.xlim(np.log10(xtoplot[0]),np.log10(xtoplot[-1]))
        #plt.ylim(np.log10(ytoplot[0]),np.log10(ytoplot[-1]))
    #
    plt.xlabel(r"$m$ mode",ha='center',labelpad=6)
    plt.ylabel(r"Normalized Power Density",ha='center',labelpad=6)
    plt.savefig("powervsm%d%s_%s.pdf" % (filenum,fileletter,pllabel) )#,bbox_inches='tight',pad_inches=0.1)
    plt.savefig("powervsm%d%s_%s.eps" % (filenum,fileletter,pllabel))#,bbox_inches='tight',pad_inches=0.1)
    plt.savefig("powervsm%d%s_%s.png" % (filenum,fileletter,pllabel))#,bbox_inches='tight',pad_inches=0.1)
    #
    # FILE:
    file1 = open("powervsm%d%s_%s.txt" % (filenum,fileletter,pllabel) , 'w')
    file1.write("#%g %g %g\n" % (_dx1,_dx2,_dx3))
    file1.write("#%s %s   %s\n" % ("ii","xtoplot","ytoplot"))
    # For fluxes (i.e. FM) last entry gives (e.g. Mdot) but will be off by 30% or so from true accretion rate because of how form spatial angular wedge where the average value of bsqorho>maxbsqorho so that mode decomposition makes sense.
    file1.write("#%g %g   %g   %g\n" % (normpowersumnotm0a,normpowersumnotm0b,np.fabs(qty[0]),(1.0/_dx1)*np.fabs(qty[0])))
    for ii in np.arange(0,len(xtoplot)):
        file1.write("%d %g   %g\n" % (ii,xtoplot[ii],ytoplot[ii]))
    file1.close()
    #
    # FINALPLOTS:
    #
    # whichrun="thickdisk7" ; scp powervsm*.txt jmckinne@ki-jmck:/data2/jmckinne/$whichrun/fromorange_movie8new2/
    #









def timeavg_vstvsr( qty, ts, fti, ftf, step = 1 ):
    cond = (ts<=ftf)*(ts>=fti)
    #use masked array to remove any stray NaN's
    qtycond = np.ma.masked_array(qty[cond,:],np.isnan(qty[cond,:]))
    qtycond = qtycond[::step,:]
    qtyavg = qtycond.mean(axis=0,dtype=np.float64)
    return( qtyavg )


def timeavg( qty, ts, fti, ftf, step = 1 ):
    cond = (ts<=ftf)*(ts>=fti)
    #use masked array to remove any stray NaN's
    qtycond = np.ma.masked_array(qty[cond],np.isnan(qty[cond]))
    qtycond = qtycond[::step]
    qtyavg = qtycond.mean(axis=0,dtype=np.float64)
    return( qtyavg )

def timeavg_sqrt( qty0, ts, fti, ftf, step = 1 ):
    qty=np.sqrt(qty0)
    cond = (ts<=ftf)*(ts>=fti)
    #use masked array to remove any stray NaN's
    qtycond = np.ma.masked_array(qty[cond],np.isnan(qty[cond]))
    qtycond = qtycond[::step]
    qtyavg = qtycond.mean(axis=0,dtype=np.float64)
    return( qtyavg )

def getstagparams2(bsqorho=None,uu=None,var=None,rmax=20,doplot=1,doreadgrid=1):
    if uu is None:
        avgmem = get2davg(usedefault=1)
        assignavg2dvars(avgmem)
    #
    #a large enough distance that floors are not applied, yet close enough that reaches inflow equilibrium
    rnoflooradded=rmax
    #radial index and radius of stagnation surface
    sol = uu[1]*(r-rmax)
    bsqorhorstag = findroot2d( sol, bsqorho, axis = 1, isleft=True, fallback = 1, fallbackval = rnoflooradded )
    bsqorhohstag = findroot2d( sol, bsqorho, axis = 1, isleft=True, fallback = 1, fallbackval = np.pi/2.)
    return bsqorhorstag,bsqorhohstag


def getstagparams(bsqorho=None,uu=None,var=None,rmax=20,doplot=1,doreadgrid=1):
    if uu is None:
        if doreadgrid:
            grid3d("gdump.bin",use2d=True)
        avgmem = get2davg(usedefault=1)
        assignavg2dvars(avgmem)
    #
    #a large enough distance that floors are not applied, yet close enough that reaches inflow equilibrium
    rnoflooradded=rmax
    #radial index and radius of stagnation surface
    #sol = uu[1]*(r-rmax)
    # no artificial restriction -- bsqorho restriction takes care of non-jet part already
    sol = uu[1]
    istag = np.floor( findroot2d(sol, ti, axis = 1, isleft=True, fallback = 1, fallbackval = iofr(rnoflooradded)) + 0.5 )
    jstag = np.floor( findroot2d(sol, tj, axis = 1, isleft=True, fallback = 1, fallbackval = iofr(rnoflooradded)) + 0.5 )
    rstag = findroot2d( sol, r, axis = 1, isleft=True, fallback = 1, fallbackval = rnoflooradded )
    hstag = findroot2d( sol, h, axis = 1, isleft=True, fallback = 1, fallbackval = np.pi/2.)
    # kill unphysical zigzag one cell away from pole
    if 0==1:
        for j in np.array([1,-2]):
            rstag[j]=0.5*(rstag[j-1]+rstag[j+1])
            istag[j]=iofr(rstag[j])
            hstag[j]=h[istag[j],j,0]
    #
    if doplot:
        plt.figure(1)
        plt.clf()
        plt.plot(hstag,rstag)
        plt.figure(2)
        plco(uu[1],levels=(0,),colors='k',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.plot(rstag*np.sin(hstag),rstag*np.cos(hstag))
        plt.xlim(0,10)
        plt.ylim(-5,5)
    #cond=(ti==istag[None,:,None])*(tj==jstag[None,:,None])
    #print( zip(r[cond],rstag) )
    if var is not None:
        varstag = findroot2d( uu[1], var, axis = 1, isleft=True, fallback = 0)
        return varstag
    else:
        return istag, jstag, hstag, rstag

def get_dUfloor( floordumpno, maxrinflowequilibrium = 20 ):
    """ maxrsteady should be chosen to be on the outside of the inflow equilibrium region """
    RR=0
    TH=1
    PH=2
    rfloor( "failfloordudump%04d.bin" % floordumpno )
    #add back in rest-mass energy to conserved energy
    dUfloor[1] -= dUfloor[0]
    condin = (avg_uu[1]<0)*(r[:,:,0:1]<maxrinflowequilibrium)
    #uncomment this if don't want to use stagnation surface
    #condin = (r[:,:,0:1]<maxrinflowequilibrium)
    condout = 1 - condin
    UfloorAout = (dUfloor*condout[None,:,:,:]).sum(1+PH).sum(1+TH).cumsum(1+RR)
    UfloorAin = (dUfloor*condin[None,:,:,:]).sum(1+PH).sum(1+TH).cumsum(1+RR)
    UfloorA = (UfloorAin-UfloorAin[:,nx-1:nx]) + UfloorAout
    UfloorAsum = UfloorA*scaletofullwedge(1.)
    return( UfloorAsum )

def plotfluxes(doreload=1):
    global DU,DU1,DU2,qtymem,qtymem1,qtymem2
    bbox_props = dict(boxstyle="round,pad=0.1", fc="w", ec="w", alpha=0.9)
    plt.figure(4)
    gs = GridSpec(2, 2)
    gs.update(left=0.09, right=0.94, top=0.95, bottom=0.1, wspace=0.01, hspace=0.04)
    ax1 = plt.subplot(gs[-2,-1])
    os.chdir("/home/atchekho/run/rtf2_15r34_2pi_a0.99gg500rbr1e3_0_0_0") 
    if not doreload:
        DU=DU1
        qtymem=qtymem1
    takeoutfloors(fti=7000,ftf=1e6,
        ax=ax1,dolegend=False,doreload=doreload,plotldtot=False,lw=2)
    if doreload:
        DU1=DU
        qtymem1=qtymem
    plt.text(ax1.get_xlim()[0]+(ax1.get_xlim()[1]-ax1.get_xlim()[0])/10., 
             0.85*ax1.get_ylim()[1], r"$(\mathrm{b})$", size=20, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    # plt.text(ax1.get_xlim()[0]+(ax1.get_xlim()[1]-ax1.get_xlim()[0])/2., 
    #          0.85*ax1.get_ylim()[1], r"$a=%g$" % a, size=20, rotation=0.,
    #          ha="center", va="center",
    #          color='k',weight='regular',bbox=bbox_props
    #          )
    plt.text(ax1.get_xlim()[0]+(ax1.get_xlim()[1]-ax1.get_xlim()[0])/2., 
             -7, r"$\langle F_E\rangle<0$", size=20, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular'#,bbox=bbox_props
             )
    plt.text(ax1.get_xlim()[0]+(ax1.get_xlim()[1]-ax1.get_xlim()[0])/2., 
             12, r"$\langle F_M\!\rangle$", size=20, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular'#,bbox=bbox_props
             )
    # ax1r = ax1.twinx()
    # ax1r.set_ylim(ax1.get_ylim())
    # ax1r.set_yticks((ymax/2,ymax))
    for label in ax1.get_xticklabels() + ax1.get_yticklabels():
        label.set_fontsize(16)
    plt.setp( ax1.get_yticklabels(), visible=False )
    ax1.set_ylim((-19,19))
    ax2 = plt.subplot(gs[-2,-2])
    os.chdir("/home/atchekho/run/rtf2_15r34.475_a0.5_0_0_0") 
    if not doreload:
        DU=DU2
        qtymem=qtymem2
    takeoutfloors(fti=10300,ftf=1e6,ax=ax2,dolegend=False,doreload=doreload,plotldtot=False,lw=2)
    if doreload:
        DU2=DU
        qtymem2=qtymem
    plt.text(ax2.get_xlim()[0]+(ax2.get_xlim()[1]-ax2.get_xlim()[0])/10., 
             0.85*ax2.get_ylim()[1], r"$(\mathrm{a})$", size=20, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    # plt.text(ax2.get_xlim()[0]+(ax2.get_xlim()[1]-ax2.get_xlim()[0])/2., 
    #          0.85*ax2.get_ylim()[1], r"$a=%g$" % a, size=20, rotation=0.,
    #          ha="center", va="center",
    #          color='k',weight='regular',bbox=bbox_props
    #          )
    plt.text(ax2.get_xlim()[0]+(ax2.get_xlim()[1]-ax2.get_xlim()[0])/2., 
             5.8, r"$\langle F_E\rangle>0$", size=20, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular'#,bbox=bbox_props
             )
    plt.text(ax2.get_xlim()[0]+(ax2.get_xlim()[1]-ax2.get_xlim()[0])/2., 
             15, r"$\langle F_M\!\rangle$", size=20, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular'#,bbox=bbox_props
             )
    ax2.set_ylim((-19,19))
    ax2.set_ylabel("Fluxes",fontsize=20,ha="left",labelpad=10)
    #ax2r = ax2.twinx()
    #ax2r.set_ylim(ax2.get_ylim())
    for label in ax2.get_xticklabels() + ax2.get_yticklabels(): #+ ax2r.get_yticklabels():
        label.set_fontsize(16)
    plt.savefig("fig4.eps",bbox_inches='tight',pad_inches=0.02)

def takeoutfloors(ax=None,doreload=1,dotakeoutfloors=1,dofeavg=0,fti=None,ftf=None,isinteractive=1,returndf=0,dolegend=True,plotldtot=True,lw=1):
    global dUfloor, qtymem, DUfloorori, etad0, DU
    #Mdot, E, L
    grid3d("gdump.bin",use2d=True)
    istag, jstag, hstag, rstag = getstagparams(rmax=20,doplot=0,doreadgrid=0)
    if np.abs(a - 0.99)<1e-4 and scaletofullwedge(1.0) < 1.5:
        #hi-res 0.99 settings
        print( "Using hires a = 0.99 settings")
        #DTd = 22800-22231.9647756934 + 22200-22167.669585504507268 #22119.452438349220756
        dt = 100.
        # Dt = np.array([dt,-dt])
        # Dno = np.array([224.,223.])
        # fti = 14700.
        # ftf = 25000.
        Dt = np.array([28200-28097.4708711805,
                       28000-27406.4732593203,
                       27400-26763.9946654502,
                       26700-26330.0889135128,
                       26300-25799.8775611997,
                       25700-25124.6341346588,
                       25100-24594.4658011928,
                       24500-23951.5226133435,
                       23900-23292.5857662206,
                       23200-22890.8671337456,
                       22800-22231.9647756934,
                       22200-22167.6695855045])
        Dno = np.array([282,
                        280,
                        274,
                        267,
                        263,
                        257,
                        251,
                        245,
                        239,
                        232,
                        228,
                        222])
        lfti = 22167.6695855045
        lftf = 28200.
    elif np.abs(a - 0.99)<1e-4 and scaletofullwedge(1.0) > 1.5:
        #lo-res 0.99 settings
        print( "Using lores a = 0.99 settings")
        dt = 100.
        # Dt = np.array([13700-11887.3058391312,
        #                11800.-11547.5107224568,
        #                11500-9727.2561911212,
        #                9700-8435.61370926043,
        #                8400-8000,-(8400-8000)])
        # Dno = np.array([137,
        #                 118,
        #                 115,
        #                 97,
        #                 84,80])
        Dt = np.array([13700-11887.3058391312])
        Dno = np.array([137])
        lfti = 11887.3058391312
        lftf = 13700.
    elif np.abs(a - 0.5)<1e-4:
        print( "Using a = 0.5 settings")
        dt1 = 13000.-10279.
        dt2 = 10200.-10000.
        Dt = np.array([dt1,dt2,-dt2])
        Dno = np.array([130,102,100])
        lfti = 10000.
        lftf = 13095.
    elif np.abs(a - 0.2)<1e-4:
        print( "Using a = 0.2 settings")
        Dt = np.array([13300.-10366.5933313178])
        Dno = np.array([133])
        lfti = 10366.5933313178
        lftf = 13300.
    else:
        print( "Unknown case: a = %g, aborting..." % a )
        return
    if fti is None or ftf is None:
        fti = lfti
        ftf = lftf
    #dotakeoutfloors=1
    RR=0
    TH=1
    PH=2
    if doreload:
        etad0 = -1/(-gn3[0,0])**0.5
        #!!!rhor = 1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        qtymem=getqtyvstime(ihor,0.2)
        #initialize with zeros
        DT = 0
        if dotakeoutfloors:
            for (i,iDT) in enumerate(Dt):
                gc.collect() #try to clean up memory if not used
                iDU = get_dUfloor( Dno[i] )
                if iDT > 0:
                    DT += iDT
                if i==0:
                    DU = iDU
                else:
                    DU += iDU * np.sign(iDT)
            #average in time
            DU /= DT
        else:
            DU = np.zeros((8,nx),dtype=np.float64)
    DUfloor0 = DU[0]
    DUfloor1 = DU[1]
    DUfloor4 = DU[4]
    #at this time we have the floor information, now get averages:
    mdtotvsr, edtotvsr, edmavsr, ldtotvsr = plotqtyvstime( qtymem, fullresultsoutput=0,whichplot = -2, fti=fti, ftf=ftf )
    if dofeavg:
        FE=np.load("fe.npy")
    #edtotvsr-=FE
    #avgmem = get2davg(usedefault=1)
    #assignavg2dvars(avgmem)
    #edtotvsr = -(gdet[:,1:ny-1,0:1]*avg_Tud[1][0][:,1:ny-1,0:1]*_dx2*_dx3*nz).sum(-1).sum(-1)
    #!!!rhor = 1+(1-a**2)**0.5
    rh=rhor
    ihor = np.floor(iofr(rhor)+0.5)
    #FIGURE: mass
    if isinteractive:
        if ax is None:
            plt.figure(1)
            plt.clf()
        if ax is None:
            plt.plot(r[:,0,0],mdtotvsr,'b--',label=r"$F_M$ (raw)",lw=2)
    if dotakeoutfloors:
        Fm=(mdtotvsr+DUfloor0)
        if isinteractive:
            plt.plot(r[:,0,0],Fm,'b',label=r"$F_M$",lw=2)
    if isinteractive and ax is None:
        plt.plot(r[:,0,0],-edtotvsr,'r--',label=r"$F_E$ (raw)",lw=2)
    if dofeavg and isinteractive and ax is None:
        plt.plot(r[:,0,0],FE,'k--',label=r"$F_E$",lw=2)
    if dotakeoutfloors:
        Fe=-(edtotvsr+DUfloor1)
        if isinteractive:
            plt.plot(r[:,0,0],Fe,'r',label=r"$F_E$",lw=2)
        if dofeavg and isinteractive: 
            plt.plot(r[:,0,0],FE-DUfloor1,'k',label=r"$F_E$",lw=2)
        if isinteractive and ax is None:
            plt.plot(r[:,0,0],(DUfloor1),'r:',lw=2)
    if ldtotvsr is not None and plotldtot:
        Fl=-(ldtotvsr+DUfloor4)
        if isinteractive and ax is None:
            plt.plot(r[:,0,0],-ldtotvsr/dxdxp[3][3][:,0,0]/10.,'g--',label=r"$F_L/10$ (raw)",lw=2)
        if dotakeoutfloors and isinteractive:
            plt.plot(r[:,0,0],Fl/dxdxp[3][3][:,0,0]/10.,'g',label=r"$F_L/10$",lw=2)
    eta = ((Fm-Fe)/Fm)
    etap = (Fm-Fe)/Fe
    if isinteractive:
        print("Eff = %g, Eff' = %g" % ( eta[iofr(5)], etap[iofr(5)] ) )
        #plt.plot(r[:,0,0],DUfloor0,label=r"$dU^t$")
        #plt.plot(r[:,0,0],DUfloor*1e4,label=r"$dU^t\times10^4$")
        if dolegend:
            plt.legend(loc='lower right',bbox_to_anchor=(0.97,0.22),
                       #borderpad = 1,
                       borderaxespad=0,frameon=True,labelspacing=0,
                       ncol=1)
        plt.xlim(rhor,19.99)
        plt.ylim(-10,18)
        plt.grid()
        plt.xlabel(r"$r\ [r_g]$",fontsize=20)
        if ax is None:
            plt.ylabel("Fluxes",fontsize=20,ha='center')
            plt.savefig("fig4.pdf",bbox_inches='tight',pad_inches=0.02)
            plt.savefig("fig4.eps",bbox_inches='tight',pad_inches=0.02)
            plt.savefig("fig4.png",bbox_inches='tight',pad_inches=0.02)
        #FIGURE: energy
        #plt.figure(2)
        #plt.plot(r[:,0,0],edtotvsr+DUfloor1,label=r"$\dot E+dU^1$")
        #plt.plot(r[:,0,0],DUfloor1,label=r"$dU^1$")
        #plt.legend()
        #plt.xlim(rhor,12)
        #plt.ylim(-3,20)
        #plt.grid()
    #
    if False:
        avgmem = get2davg(usedefault=1)
        assignavg2dvars(avgmem)
        edtot2davg = (gdet[:,:,0:1]*avg_Tud[1][0][:,:,0:1]*_dx2*_dx3*nz).sum(-1).sum(-1)
        rhouuudtot2davg = (gdet[:,:,0:1]*avg_rhouuud[1][0][:,:,0:1]*_dx2*_dx3*nz).sum(-1).sum(-1)
        uguuudtot2davg = (gdet[:,:,0:1]*avg_uguuud[1][0][:,:,0:1]*_dx2*_dx3*nz).sum(-1).sum(-1)
        avg_tudmass = (gdet[:,:,0:1]*(avg_rhouu[1])*(avg_ud[0])*_dx2*_dx3*nz).sum(-1).sum(-1)
        avg_tudug = (gdet[:,:,0:1]*(avg_uguu[1])*(avg_ud[0])*_dx2*_dx3*nz).sum(-1).sum(-1)
        avg_tudmassug = (gdet[:,:,0:1]*(avg_rhouu[1]+avg_uguu[1])*(avg_ud[0])*_dx2*_dx3*nz).sum(-1).sum(-1)
        gc.collect()
    #return efficiency at r = 5:
    if returndf:
        Fmraw = mdtotvsr[ihor]
        Feraw = -edtotvsr[ihor]
        Fmval = Fm[iofr(5)]
        Feval = Fe[iofr(5)]
        epsFm = Fmval/Fmraw
        epsFke = (Fmval-Feval)/(Fmraw-Feraw)
        return( (epsFm,epsFke) )
    return( (eta[iofr(5)], Fm[iofr(5)], Fe[iofr(5)]) )
    #
    # plt.figure(2)
    # plt.plot(r[:,0,0],edtotvsr,label="tot")
    # plt.plot(r[:,0,0],-edtot2davg,label="tot2davg")
    # #plt.plot(r[:,0,0],-rhouuudtot2davg,label="rhouuud")
    # #plt.plot(r[:,0,0],-gam*uguuudtot2davg,label="gamuguuud")
    # myma=-(rhouuudtot2davg+gam*uguuudtot2davg)
    # plt.plot(r[:,0,0],-avg_tudmass,label="mymass")
    # plt.plot(r[:,0,0],-avg_tudmassug,label="mymassug")
    # plt.plot(r[:,0,0],-avg_tudug,label="myug")
    # plt.plot(r[:,0,0],edmavsr,label="ma")
    # plt.plot(r[:,0,0],edtotvsr-edmvsr,label="tot-m")
    # #plt.plot(r[:,0,0],DUfloor[1])
    # plt.xlim(rh,20); plt.ylim(-20,20)
    # plt.legend()
    # if ldtotvsr is not None:
    #     plt.plot(r[:,0,0],ldtotvsr+DUfloor4,label=r"$Lwoutfloor$")
    #plt.xlim(rhor,12)
    #plt.ylim(-3,20)
    #xx
    # plt.grid()
    # #
    # plt.figure(3)
    # plt.plot(r[:,0,0],-edtot2davg,label="tot2davg")
    # gc.collect()

def computeeta(start_t=8000,end_t=1e6,numintervals=8,doreload=1):
    #
    defaultfti,defaultftf=getdefaulttimes()
    #
    start_t=defaultfti
    end_t=defaultftf
    #
    #getqtyvstime(ihor,horval=0.2,fmtver=2,dobob=0,whichi=None,whichn=None):
    grid3d("gdump.bin", use2d = True)
    qtymem = getqtyvstime( iofr(rhor) )
    start_of_sim_t = qtymem[0,0,0]
    end_t1 = qtymem[0,-1,0]
    if end_t>end_t1:
        end_t = end_t1
    a_t,t_step = np.linspace(start_t,end_t,numintervals,retstep=True,endpoint=False)
    print( "start_t = %g, end_t = %g, step_t = %g" % (start_t,end_t,t_step) )
    a_eta = np.zeros_like(a_t)
    a_Fm = np.zeros_like(a_t)
    a_Fe = np.zeros_like(a_t)
    for (i,t_i) in enumerate(a_t):
        if i == 0: 
            doreload_local = doreload
        else: 
            doreload_local = 0
        a_eta[i],a_Fm[i],a_Fe[i] = takeoutfloors(doreload=doreload_local,fti=t_i,ftf=t_i+t_step,isinteractive=0)
    print("Efficiencies:")    
    print zip(a_eta,a_Fm,a_Fe)
    print( "Average efficiency = %g" % a_eta.mean() ) 
    print( "Stdev eta: %g" % a_eta.std() )
    

def plotj(ts,fs,md,jem,jtot):
    #rc('font', family='serif')
    #plt.figure( figsize=(12,9) )
    plt.clf()
    fig,plotlist=plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(12,12))
    plottitle = "a = %g: %s" % ( a, os.path.basename(os.getcwd()) )
    plt.suptitle( plottitle )
    plt.subplots_adjust(hspace=0.1) #increase vertical spacing to avoid crowding
    plotlist[0].plot(ts,fs,label=r'$\Phi_{\rm h}/\Phi_{\rm i}$')
    #plotlist[0].plot(ts,fs,'r+') #, label=r'$\Phi_{\rm h}/0.5\Phi_{\rm i}$: Data Points')
    plotlist[0].legend(loc='lower right')
    #plt.xlabel(r'$t\;(r_g/c)$')
    plotlist[0].set_ylabel(r'$\Phi_{\rm h}$',fontsize=16)
    plt.setp( plotlist[0].get_xticklabels(), visible=False)
    plotlist[0].grid(True)
    #
    #plotlist[1].subplot(212,sharex=True)
    plotlist[1].plot(ts,md,label=r'$\dot M_{\rm h}$')
    #plotlist[1].plot(ts,md,'r+') #, label=r'$\dot M_{\rm h}$: Data Points')
    plotlist[1].legend(loc='lower right')
    #plotlist[1].set_xlabel(r'$t\;(r_g/c)$')
    plotlist[1].set_ylabel(r'$\dot M_{\rm h}$',fontsize=16)
    plt.setp( plotlist[1].get_xticklabels(), visible=False)
    
    #plotlist[2].subplot(212,sharex=True)
    plotlist[2].plot(ts,jem/md,label=r'$P_{\rm j,em}/\dot M$')
    #plotlist[2].plot(ts,jem/md,'r+') #, label=r'$\dot M_{\rm h}$: Data Points')
    plotlist[2].plot(ts,jtot/md,label=r'$P_{\rm j,tot}/\dot M$')
    #plotlist[2].plot(ts,jtot/md,'r+') #, label=r'$\dot M_{\rm h}$: Data Points')
    plotlist[2].legend(loc='lower right')
    plotlist[2].set_xlabel(r'$t\;(r_g/c)$')
    plotlist[2].set_ylabel(r'$P_{\rm j}/\dot M_{\rm h}$',fontsize=16)

    #title("\TeX\ is Number $\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!", 
    #      fontsize=16, color='r')
    plotlist[0].grid(True)
    plotlist[1].grid(True)
    plotlist[2].grid(True)
    fig.savefig('pjetf_%s.pdf' % os.path.basename(os.getcwd()) )


def test():
    t=np.arange(10)
    f=np.arange(10)**2
    plt.plot(t,f,label='$\Phi$')
    plt.title(r"This is a title")
    plt.legend(loc='upper right')
    plt.xlabel(r'$t (r_g/c)$')
    plt.ylabel(r'$\Phi_{\rm h}$',fontsize=16)
    #plt.legend()

def gen_vpot(whichloop=None,phase=0.0,whichfield=None,fieldhor=0.194,rin=10):
    #whichfield = 0 -- single loop follows density contours
    #whichfield = None -- alternating loops
    global rho_av, rho_max, var, uq, uqc, uqcomax, aB, B, res,ud,etad, etau, gamma, vu, vd, bu, bd, bsq, phi
    #res=np.abs(bu[2]/np.sqrt(rho)/((uu[3]+1e-15)/uu[0])/_dx2)
    #plco(res,cb=True)
    #plt.plot(ti[:,ny/2,0],res[:,ny/2,0])
    #Old settings (now incorporated as defaults in this function call):
    #fieldhor = 0.194
    #rin = 10
    startfield = 1.1 * rin
    rho_av = np.copy(rho[:,:,0:1])
    #average to corners
    rho_av[1:nx,1:ny,0:1] = 0.25*(rho[0:nx-1,0:ny-1,0:1]+rho[1:nx,0:ny-1,0:1]+rho[0:nx-1,1:ny,0:1]+rho[1:nx,1:ny,0:1])
    rho_max=np.max(rho_av)
    #define aphi
    if( whichfield == None ):
        var = (r[:,:,0:1]**2*rho_av/rho_max) #**gam #*r[:,:,0:1]**1
        varc = (r[:,:,0:1]**2*rho/rho_max) #**gam #*r[:,:,0:1]**1
    else:
        var = (rho_av/rho_max) #**gam #*r[:,:,0:1]**1
        varc = (rho/rho_max) #**gam #*r[:,:,0:1]**1
    #note r should be shifted, too (not done yet):
    maxvar=np.max(var)
    maxvarc=np.max(varc)
    uq = (var-0.0*maxvar) #*r[:,:,0:1]**0.75 #/(0.1**2+(h-np.pi/2)**2)
    uqc = (varc-0.0*maxvarc) #*r[:,:,0:1]**0.75 #/(0.1**2+(h-np.pi/2)**2)
    uqcomax = varc/maxvarc #rho/rho_max #varc/maxvarc
    phi = np.log(r[:,:,0:1]/startfield)/fieldhor
    arg = phi-phase*np.pi
    #aaphi = uq**2 * (r-startfield)**1.1
    if( whichfield == None ):
        aaphi = uq**2 #* np.sin( arg )**1
    elif( whichfield == 0 ):
        aaphi = uq**2
    #aaphi = uq**2 * (1+0.2*np.sin( arg )**1)
    aaphi[uq<0] = 0
    if whichloop != None:
        notuse1 = arg > np.pi*(whichloop+1)
        notuse2 = arg < np.pi*whichloop
        aaphi[notuse1] = 0.0
        aaphi[notuse2] = 0.0
    #aaphi = uq**2 #* np.log(r[:,:,0:1]/startfield)
    #aaphi = uq**(2)
    aphi2B(aaphi)
    #reset field components outside torus to zero
    #B[1,uqc<0] = 0
    #B[2,uqc<0] = 0
    return(aaphi)

def aphi2B(aaphi):
    #aB -- face-centered
    #B -- cell-centered
    global B, aB, gdetB
    aB = np.zeros_like(B)
    gdetB = np.zeros_like(B)
    gdetB[1,1:nx,0:ny-1] = (aaphi[1:nx,1:ny]-aaphi[1:nx,0:ny-1])/_dx2
    gdetB[2,0:nx-1,1:ny] = (aaphi[1:nx,1:ny]-aaphi[0:nx-1,1:ny])/_dx1
    aB[1,1:nx,0:ny-1] = gdetB[1,1:nx,0:ny-1] / (0.5*(gdet[0:nx-1,0:ny-1]+gdet[1:nx,0:ny-1]))
    aB[2,0:nx-1,1:ny] = gdetB[2,0:nx-1,1:ny] / (0.5*(gdet[0:nx-1,0:ny-1]+gdet[0:nx-1,1:ny]))
    #ab[3] is zeroes
    #
    B=np.zeros_like(aB)
    #properly center the field
    B[1,0:nx-1,0:ny,:] = (aB[1,0:nx-1,0:ny,:] + aB[1,1:nx,0:ny,:])/2
    B[2,0:nx,0:ny-1,:] = (aB[2,0:nx,1:ny,:] + aB[2,0:nx,0:ny-1,:])/2

def pl(x,y,j=None):
    global ny
    if j == None: j = ny/2
    plt.plot(x[:,j,0],y[:,j,0])

def fac(ph):
    return(1+0.5*((ph/np.pi-1.5)/0.5)**2)

def avg2ctof(q):
    qavg2 = np.empty_like(q)
    qavg2[0:nx,1:ny,:] = (q[0:nx,1:ny,:] + q[0:nx,0:ny-1,:])/2
    return(qavg2)

def avg1ctof(q):
    qavg1 = np.empty_like(q)
    qavg1[1:nx,0:ny,:] = (q[0:nx-1,0:ny,:] + q[1:nx,0:ny,:])/2
    return(qavg1)

def avg0ctof(q):
    resavg0 = np.empty_like(q)
    resavg0[1:nx,1:ny,:] = 0.25*(q[0:nx-1,0:ny-1,:]+q[1:nx,0:ny-1,:]+q[0:nx-1,1:ny,:]+q[1:nx,1:ny,:])
    return(resavg0)

def normalize_field(targbsqoug):
    global B, gdetB, bsq, ug
    maxbsqoug = np.max(bsq/(ug+1e-5))
    rat = np.sqrt(targbsqoug/maxbsqoug)
    #rescale all field components
    B *= rat
    gdetB *= rat
    #recompute derived quantities
    cvel()
def plotbs(dy=0):
    plt.clf();
    plot(ti[:,ny/2,0],B[1,:,ny/2+dy,0])
    plot(ti[:,ny/2,0],B[2,:,ny/2+dy,0])
    plot(ti[:,ny/2,0],(bsq/ug)[:,ny/2+dy,0]/100)
    plot(ti[:,ny/2,0],(gdetB[1]/gdet)[:,ny/2+dy,0])
def plotaphi(dy=0):
    aphi=fieldcalc()
    plot(r[:,ny/2,0],aphi[:,ny/2,0])
    xlim(xmin=10,xmax=100)

def face2centdonor():
    global bcent
    bcent=np.zeros_like(B)
    bcent[1][0:nx-1,:,:]=0.5*(gdetB[1][0:nx-1,:,:]+gdetB[2][1:nx,:,:])/gdet[0:nx-1,:,:]
    bcent[2][:,0:ny-1,:]=0.5*(gdetB[2][:,0:ny-1,:]+gdetB[2][:,1:ny,:])/gdet[:,0:ny-1,:]
    bcent[3][:,:,0:nz-1]=0.5*(gdetB[2][:,:,0:nz-1]+gdetB[2][:,:,1:nz])/gdet[:,:,0:nz-1]

def pf(dir=2):
    global bcent
    grid3d("gdump.bin")
    #rfd("fieldline0000.bin")
    #reresrdump("rdump--0000.bin")
    rd("dump0000.bin")
    face2centdonor(); 
    plt.clf(); 
    myi = 20
    myk = 0
    plt.plot(tj[myi,:,myk],bcent[dir,myi,:,myk]);
    plt.plot(tj[myi,:,myk],B[dir,myi,:,myk]);
    plt.plot(tj[myi,0:ny-1,myk]+0.5,gdetB[dir,myi,1:ny,myk]/(0.5*(gdet[myi,0:ny-1,myk]+gdet[myi,1:ny,myk])))


def chophi(var,maxvar):
    newvar = np.copy(var)
    newvar[var>maxvar]=0*var[var>maxvar]+maxvar
    return(newvar)

def choplo(var,minvar):
    newvar = np.copy(var)
    newvar[var<minvar]=0*var[var<minvar]+minvar
    return(newvar)

def Risco(a):
    Z1 = 1 + (1. - a**2)**(1./3.) * ((1. + a)**(1./3.) + (1. - a)**(1./3.))
    Z2 = (3*a**2 + Z1**2)**(1./2.)
    risco = 3 + Z2 - np.sign(a)* ( (3 - Z1)*(3 + Z1 + 2*Z2) )**0.5
    return(risco)


def elinfcalc(a):
    # assume disk rotation sense is always positive, but a can be + or -
    risco=Risco(a)
    risco2=Risco(-a)
    #
    #print( "risco=%g" % (risco) )
    #
    if a<0.9999999:
        einf=(1.0-2.0/risco+a/(risco)**(3.0/2.0))/(1.0-3.0/risco+2.0*a/(risco)**(3.0/2.0))**(1.0/2.0)
        #print( "einf=%g" % (einf) )
        linf=(np.sqrt(risco)*(risco**2.0-2.0*a*np.sqrt(risco)+a**2))/(risco*(risco**2.0-3.0*risco+2.0*a*np.sqrt(risco))**(1.0/2.0))
        #print( "linf=%g" % (linf) )
    else:
        if risco<2.0:
            # einf
            einf=0.57735
            # linf
            linf=0.0
        else:
            # einf
            einf=0.946729
            # linf
            linf=4.2339
        #
    #
    return einf,linf

def plotpowers(fname,hor=0,format=1):
    if format == 0: #old format
        gd1 = np.loadtxt( fname, unpack = True, usecols = [1,2,3,4,5,6,7,8,9,10,11,12,13,14] )
        #gd=gd1.view().reshape((-1,nx,ny,nz), order='F')
        alist = gd1[0]
        rhorlist = 1+(1-alist**2)**0.5
        omhlist = alist / 2 / rhorlist
        mdotlist = gd1[1]
        #etalist = gd1[3]
        powlist=gd1[12] #pow(2*rstag)
        psitotsqlist = gd1[5]
        psi30sqlist = gd1[7]
    elif format == 1: #new avg2d format
        gd1 = np.loadtxt( fname, unpack = True, usecols = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] )
        #gd=gd1.view().reshape((-1,nx,ny,nz), order='F')
        alist = gd1[0]
        rhorlist = 1+(1-alist**2)**0.5
        omhlist = alist / 2 / rhorlist
        mdotlist = gd1[5]
        ftotlist=gd1[6]
        fsqtotlist=gd1[7]
        f30list=gd1[8]
        f30sqlist=gd1[9]
        pjetemtotlist=gd1[10]
        eoutEMtotlist=gd1[11]
        #etalist = gd1[3]
        i = 12
        #1
        powEMKElist=gd1[i]; i+=1
        powwindEMKElist=gd1[i]; i+=1
        powlist=gd1[i]; i+=1
        powwindlist=gd1[i]; i+=1
        rlist=gd1[i]; i+=1
        #2
        powEMKElist2=gd1[i]; i+=1
        powwindlEMKEist2=gd1[i]; i+=1
        powlist2=gd1[i]; i+=1
        powwindlist2=gd1[i]; i+=1
        rlist2=gd1[i]; i+=1
        #3
        powEMKElist3=gd1[i]; i+=1
        powwindEMKElist3=gd1[i]; i+=1
        powlist3=gd1[i]; i+=1
        powwindlist3=gd1[i]; i+=1
        rlist3=gd1[i]; i+=1
    etalist = powEMKElist/mdotlist
    etaEMlist = eoutEMtotlist/mdotlist
    etawindlist = powwindEMKElist/mdotlist
    gin = open( fname, "rt" )
    emptyline = gin.readline()
    for i in np.arange(alist.shape[0]):
        simname = gin.readline().split()[0]
        print '%.2g & %.3g & %.3g & %.3g & %.3g & %% %s' % (alist[i], 100*etaEMlist[i], 100*etalist[i], 100*(etawindlist[i]-etalist[i]), 100*etawindlist[i], simname)
    gin.close()
    mya=np.arange(-1,1,0.001)
    rhor = 1+(1-mya**2)**0.5
    myomh = mya / 2/ rhor
    #fitting function
    f0 = 2.9
    f1 = -0.6
    f1n = 1.4
    f2 = 0.
    f = f0 * (1 + (f1*(1+np.sign(myomh))/2. + f1n*(1-np.sign(myomh))/2.) * myomh + f2 * myomh**2)
    #gammie way -- too large amplitude
    #gammieparamopi = (8./3.*(3.-mya**2+3.*(1-mya**2)**0.5))**0.5
    #f = f0 * 0.25 * gammieparamopi
    #mypwr = 5*myomh**2
    psi = 1.0
    mypwr = 2.0000 * 1.*1.0472*myomh**2 * 1.5*(psi**2-psi**3/3) #prefactor = 2pi/3, consistent with (A7) from TMN10a
    horx=0.09333
    #myr = Risco(mya) #does not work at all: a < 0 power is much greater than a > 0
    myeta = mypwr * (mya**2+3*rhor**2)/3 / (2*np.pi*horx)
    #plt.plot( mya, myeta )
    rhor6 = 1+(1-mspina6[mhor6==hor]**2)**0.5
    #Tried to equate pressures -- works but mistake in calculaton -- wrong power
    #plt.plot(mspina6[mhor6==hor],mpow6[mhor6==hor]* ((mspina6[mhor6==hor]**2+3*rhor6**2)/3/(2*np.pi*horx)) )
    #Simple multiplication by rhor -- works!  \Phi^2/Mdot * rhor ~ const
    fac = 0.838783 #0.044/(1./(6*np.pi))
    #plt.plot(mya,mya**2)
    #plt.plot(alist,etawindlist,'go',label=r'$\eta_{\rm j}+\eta_{\rm w}$')
    # plt.plot(mspina6[mhor6==hor],fac*6.94*mpow6[mhor6==hor],'r--',label=r'$P_{\rm BZ,6}$')
    # plt.plot(mspina6[mhor6==hor],fac*3.75*mpow6[mhor6==hor]*rhor6,'r',label=r'$P_{\rm BZ,6}\times\, r_h$' )
    if False:
        myomh6=np.concatenate((-momh6[mhor6==hor][::-1],momh6[mhor6==hor]))
        myspina6=np.concatenate((-mspina6[mhor6==hor][::-1],mspina6[mhor6==hor]))
        mypow6 = np.concatenate((mpow6[mhor6==hor][::-1],mpow6[mhor6==hor]))
    else:
        myomh6=momh6[mhor6==hor]
        myspina6=mspina6[mhor6==hor]
        mypow6 = mpow6[mhor6==hor]
    mypsiosqrtmdot = f0*(1.+(f1*(1+np.sign(myomh6))/2. + f1n*(1-np.sign(myomh6))/2.)*myomh6)
    myeta6 = (mypsiosqrtmdot)**2*mypow6
    # plt.figure(5)
    # plt.clf()
    # plt.plot(mspina6[mhor6==hor],mpow6[mhor6==hor] )
    # plt.plot(mspina2[mhor2==hor],mpow2a[mhor2==hor] )
    # mpow2ahere = 2.0000 * 1.*1.0472*momh2**2 * 1.5*(psi**2-psi**3/3)
    # plt.plot(mspina2[mhor2==hor], mpow2ahere[mhor2==hor])
    #plt.plot(mya,mya**2)
    #plt.plot(mya,mypwr)
    #
    if format==0:
        plt.figure(2)
        plt.clf()
        #plt.plot( mya, myeta )
        #plt.plot(mya,mya**2)
        #y = (psi30sqlist)**2/(2*mdotlist)
        y = (psi30sqlist)**2/(2*mdotlist)
        plt.plot(alist,y,'bo')
        plt.plot(mya,(250+0*mya)*rhor) 
        plt.plot(mya,250./((3./(mya**2 + 3*rhor**2))**2*2*rhor**2)) 
        #plt.plot(mya,((mya**2+3*rhor**2)/3)**2/(2/rhor)) 
        plt.ylim(ymin=0)
        #plt.plot(alist,2*mdotlist/(psitotsqlist)**2,'o')
        #plt.plot(mspina6[mhor6==hor],5*mpow6[mhor6==hor])
        #plt.plot(mspina2[mhor2==hor],5*mpow2a[mhor2==hor])
        # plt.figure(4)
        # plt.clf()
        # y = (psi30sqlist)**2/(2*mdotlist*rhorlist**2)
        # plt.plot(alist,1/(y/np.max(y)),'o')
        # plt.plot(mya,Risco(mya)**(1./2.)*0.9) 
        # plt.ylim(ymin=0)
    else:
        plt.figure(2)
        plt.clf()
        #plt.plot( mya, myeta )
        #plt.plot(mya,mya**2)
        #y = (psi30sqlist)**2/(2*mdotlist)
        y = (f30sqlist/2./(2*np.pi))/(mdotlist)**0.5
        y1= (fsqtotlist/2./(2*np.pi))/(mdotlist)**0.5
        #plt.plot(alist,y,'bo')
        plt.plot(alist,y1,'ro')
        plt.plot(mya,f,'g')
        # plt.plot(mya,(250+0*mya)*rhor) 
        # plt.plot(mya,250./((3./(mya**2 + 3*rhor**2))**2*2*rhor**2)) 
        #plt.plot(mya,((mya**2+3*rhor**2)/3)**2/(2/rhor)) 
        plt.ylim(ymin=0)
        #plt.plot(alist,2*mdotlist/(psitotsqlist)**2,'o')
        #plt.plot(mspina6[mhor6==hor],5*mpow6[mhor6==hor])
        #plt.plot(mspina2[mhor2==hor],5*mpow2a[mhor2==hor])
        # plt.figure(4)
        # plt.clf()
        # y = (psi30sqlist)**2/(2*mdotlist*rhorlist**2)
        # plt.plot(alist,1/(y/np.max(y)),'o')
        # plt.plot(mya,Risco(mya)**(1./2.)*0.9) 
        # plt.ylim(ymin=0)
    #
    plt.figure(1, figsize=(6,5.8),dpi=200)
    plt.clf()
    gs = GridSpec(3, 3)
    gs.update(left=0.12, right=0.94, top=0.95, bottom=0.1, wspace=0.01, hspace=0.04)
    #mdot
    ax1 = plt.subplot(gs[0,:])
    plt.plot(alist,y1,'o',label=r'$\langle\phi_{\rm H}^2\rangle^{1/2}$',mfc='r')
    plt.plot(mya[mya>0],f[mya>0],'k-',label=r'$\phi_{\rm fit}=2.9(1-0.6 \Omega_{\rm H})$')
    # plt.plot(mya,(250+0*mya)*rhor) 
    # plt.plot(mya,250./((3./(mya**2 + 3*rhor**2))**2*2*rhor**2)) 
    #plt.plot(mya,((mya**2+3*rhor**2)/3)**2/(2/rhor)) 
    plt.ylim(ymin=0.0001)
    plt.ylabel(r"$\phi_{\rm H}$",fontsize='x-large',ha='center',labelpad=16)
    plt.grid()
    plt.setp( ax1.get_xticklabels(), visible=False )
    plt.legend(ncol=1,loc='lower center')
    bbox_props = dict(boxstyle="round,pad=0.1", fc="w", ec="w", alpha=0.9)
    plt.text(-0.9, 2.5, r"$(\mathrm{a})$", size=16, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    #second y-axis
    ax1r = ax1.twinx()
    ax1r.set_xlim(-1,1)
    ax1r.set_ylim(ax1.get_ylim())
    #
    ax2 = plt.subplot(gs[1,:])
    plt.plot(alist,100*etaEMlist,'o',label=r'$\eta_{\rm H}$',mfc='r')
    #plt.plot(alist,100*(etawindlist-etalist),'gv',label=r'$\eta_{\rm w}$')
    #plt.plot(myspina6,0.9*100*fac*myeta6,'k',label=r'$0.9\eta_{\rm BZ6}(\phi_{\rm fit})$' )
    plt.plot(myspina6,100*fac*myeta6,'k-',label=r'$\eta_{\rm BZ6}(\phi_{\rm fit})$' )
    plt.ylim(0.0001,150)
    plt.grid()
    plt.setp( ax2.get_xticklabels(), visible=False )
    plt.ylabel(r"$\eta_{\rm H}\  [\%]$",fontsize='x-large',ha='center',labelpad=12)
    plt.text(-0.9, 125, r"$(\mathrm{b})$", size=16, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    plt.legend(ncol=2,loc='upper center')
    #second y-axis
    ax2r = ax2.twinx()
    ax2r.set_xlim(-1,1)
    ax2r.set_ylim(0.0001,150)
    #
    ax3 = plt.subplot(gs[-1,:])
    newy1 = 100*fac*myeta6
    newy2 = 0.8*100*fac*myeta6
    ax3.fill_between(myspina6,newy1,newy2,where=newy1>newy2,facecolor=(0.8,1,0.8,1),edgecolor=(0.8,1,0.8,1))
    #plt.plot(myspina6,myeta6,'r:',label=r'$\eta_{\rm BZ,6}$')
    plt.plot(alist,100*etalist,'gs',label=r'$\eta_{\rm j}$')
    #plt.plot(alist,100*etaEMlist,'rx',label=r'$\eta_{\rm j}$')
    plt.plot(alist,100*(etawindlist-etalist),'bv',label=r'$\eta_{\rm w,o}$')
    plt.plot(myspina6,100*fac*myeta6,'k-',label=r'$\eta_{\rm BZ6}(\phi_{\rm fit})$' )
    plt.plot(myspina6,0.9*100*fac*myeta6,'k--',label=r'$0.9\eta_{\rm BZ6}(\phi_{\rm fit})$' )
    plt.ylim(0.0001,150)
    plt.grid()
    plt.legend(ncol=2,loc='upper center')
    plt.xlabel(r"$a$",fontsize='x-large')
    plt.ylabel(r"$\eta_{\rm j},\ \eta_{\rm w,o}\  [\%]$",fontsize='x-large',ha='center',labelpad=12)
    plt.text(-0.9, 125, r"$(\mathrm{c})$", size=16, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    #second y-axis
    ax3r = ax3.twinx()
    ax3r.set_xlim(-1,1)
    ax3r.set_ylim(ax3.get_ylim())
    #
    #plt.savefig("jetwindeta.pdf",bbox_inches='tight',pad_inches=0)
    #plt.savefig("jetwindeta.eps",bbox_inches='tight',pad_inches=0)
    plt.savefig("jetwindeta.pdf",bbox_inches='tight',pad_inches=0.02)
    plt.savefig("jetwindeta.eps",bbox_inches='tight',pad_inches=0.02)
    plt.savefig("jetwindeta.png",bbox_inches='tight',pad_inches=0.02)
    #plt.plot(mspina2[mhor2==hor],5*mpow2a[mhor2==hor])
    #
    #
    plt.figure(3)
    plt.clf()
    #plt.plot( mya, myeta )
    #plt.plot(mya,mya**2)
    psi=1.0
    pow6func = interp1d(momh6[mhor6==hor], mpow6[mhor6==hor])
    #divide flux by 2 (converts flux to single hemisphere) and by dxdxp33 (accounts for A_3 -> A_\phi):
    # pwrlist = (psi30sqlist/2/(2*np.pi))**2*2.0000 * 1.*1.0472*omhlist**2 * 1.5*(psi**2-psi**3/3)
    # plt.plot(alist,pwrlist6/mdotlist,'o')
    if format == 0:
        pwrlist6 = (psi30sqlist/2/(2*np.pi))**2*pow6func(np.abs(omhlist))
        plt.plot(alist,pwrlist6/mdotlist,'o')
    plt.ylim(ymin=0,ymax=3)
    #plt.plot(alist,2*mdotlist/(psitotsqlist)**2,'o')
    plt.plot( mya, myeta )
    plt.plot(mspina6[mhor6==hor],5*mpow6[mhor6==hor])
    plt.plot(mspina2[mhor2==hor],5*mpow2a[mhor2==hor])
    # psi = 1
    # mp = 2.0000 * 1.*1.0472*myomh**2 * 1.5*(psi**2-psi**3/3)
    # plt.plot(mya,1.5*mp)
    # plt.figure(2)
    # plt.clf()
    # plt.plot(mya,myomh)
    # plt.plot(mspina2[mhor2==hor],momh2[mhor2==hor])
    

def readmytests1():
    global momh2, mhor2, mpsi2, mpow2, mBr2, mtheta2, mspina2, mpow2a
    global momh4, mhor4, mpsi4, mpow4, mBr4, mtheta4, mspina4
    global momh6, mhor6, mpsi6, mpow6, mBr6, mtheta6, mspina6
    #
    gd2 = np.loadtxt( "mytest2", unpack = True )
    momh2, mhor2, mpsi2, mpow2, mBr2 = gd2[0:5]
    mtheta2 = np.pi/2-mhor2
    mspina2 = 4*momh2/(1+4*momh2**2)
    psi = (1-np.cos(np.pi/2-mhor2))
    mpow2a = 2.0000 * 1.*1.0472*momh2**2 * 1.5*(psi**2-psi**3/3)  #for two jets? 1.0472=pi/3
    #
    gd4 = np.loadtxt( "mytest4", unpack = True )
    momh4, mhor4, mpsi4, mpow4, mBr4 = gd4[0:5]
    mtheta4 = np.pi/2-mhor4
    mspina4 = 4*momh4/(1+4*momh4**2)
    #
    gd6 = np.loadtxt( "mytest6", unpack = True )
    momh6, mhor6, mpsi6, mpow6, mBr6 = gd6[0:5]
    mtheta6 = np.pi/2-mhor6
    mspina6 = 4*momh6/(1+4*momh6**2)

def plotomegaf2hor():
    #plot omegaf2/omegah on the horizon
    plt.clf(); 
    rhor = 1 + (1-a**2)**0.5
    omh = a / (2*rhor)
    ihor = np.floor(iofr(rhor)+0.5)
    rhoavg=(rho[ihor].sum(1)/nz)
    bsqorhoavg=(bsq/rho)[ihor].sum(1)/nz
    TudEM10avg = (-gdet*TudEM[1,0])[ihor].sum(1)/nz
    Etot = (-gdet*TudEM[1,0])[ihor].sum()*_dx2*_dx3*2
    plt.plot(tj[ihor,:,0],omegaf2[ihor].sum(1)/nz*dxdxp[3][3][0,0,0]/omh); 
    plt.plot(tj[ihor,:,0],0.5*rhoavg/np.max(rhoavg)); 
    plt.plot(tj[ihor,:,0],bsqorhoavg/100); 
    plt.plot(tj[ihor,:,0],0.5*TudEM10avg/np.max(TudEM10avg)); 
    print( "Etot = %g" % Etot )
    plt.ylim(0,0.5)

def plotakshay():
    #grid3d("gdump.bin")
    #rfd("fieldline4670.bin")
    #cvel()
    #rhor = 1+(1-a**2)**0.5
    # ihor = np.floor(iofr(rhor)+0.5)
    iref = 0
    rref = r[iref,0,0]
    #far view
    plt.figure(1)
    plt.clf()
    #Density
    plt.suptitle(r"Angular density profile ($a = %g$ at $i = %d$, $r = %g$, $t = %g$)" % (a, iref, rref,t))
    plt.plot(h[iref,:,0],rho[iref,:,0])
    plt.plot(h[iref,:,0],rho[iref,:,0],'o')
    plt.xlim(0,3.5)
    plt.xlabel(r"$\theta-\pi/2$")
    plt.ylabel(r"$\rho$")
    plt.savefig("rho-i0.pdf")
    #close view
    plt.figure(2)
    plt.clf()
    #Density
    plt.suptitle(r"[blowup] Angular density profile ($a = %g$ at $i = %d$, $r = %g$, $t = %g)$" % (a, iref, rref,t))
    plt.plot(h[iref,:,0]-np.pi/2,rho[iref,:,0])
    plt.plot(h[iref,:,0]-np.pi/2,rho[iref,:,0],'o')
    plt.xlim(-0.2,0.2)
    plt.xlabel(r"$\theta-\pi/2$")
    plt.ylabel(r"$\rho$")
    plt.savefig("rho-i0_blowup.pdf")
    #Time step
    #dt2 = _dx2 / amax(np.abs(v2m),np.abs(v2p)) 
    #plt.plot(h[iref,:,0]-np.pi/2,dt2*1000)
 
def plotrfisco():
    plco(v1p,levels=(0,),xcoord=r*np.sin(h),ycoord=r*np.cos(h),colors='c'); plt.xlim(0,10); plt.ylim(-5,5)
    plc(np.log10(rho),xcoord=r*np.sin(h),ycoord=r*np.cos(h),cb=True)
    rh=1+(1-a**2)**0.5
    plc(r-rh,levels=(0,),colors='k',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
    risco = Risco(a)
    print( "Risco(a=%g) = %g" % (a, risco) )
    plc(r*np.sin(h)-risco,levels=(0,),colors='g',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
    plt.grid()

def plotaphivsr():
    plt.clf();plt.semilogx(r[:,0,0],aphi[:,ny/2,0]/10,label=r'$\Phi/10$')
    plt.semilogx(r[:,0,0],15+lrho[:,ny/2,0],label=r'$\log_{10}\rho+15$')
    plt.semilogx(r[:,0,0],20+np.log10(ug[:,ny/2,0]),label=r'$\log_{10}u_g\!+20$')
    plt.semilogx(r[:,0,0],(r[:,0,0]-34)**(2./3.)/2.1,label=r'$\propto (r-r_{\rm max})^{2/3}\!$')
    plt.grid()
    plt.legend()
    plt.xlabel(r'$r$')
    plt.ylim(0,20)

def div( vec ):
    res = np.zeros_like(vec[1])
    res[0:-1]  = (vec[1][1:]-vec[1][:-1])
    return( res )

def plotdiv():    
    global madded, eadded
    rh = 1+(1-a**2)**0.5
    omegah=a/2/rh
    etad = np.zeros_like(uu)
    mdotden = (gdet[:,:,0:1]*avg_rhouu)[1]
    mdotval = scaletofullwedge(nz*(mdotden*_dx2*_dx3).sum(axis=-1).sum(-1))
    edotval = -scaletofullwedge(nz*(gdet*avg_Tud[1,0]*_dx2*_dx3).sum(axis=-1).sum(-1))
    ldotval = scaletofullwedge(nz*(gdet*avg_Tud[1,3]/dxdxp[3][3][:,:,0:1]*_dx2*_dx3).sum(axis=-1).sum(-1))
    etad[0] = -1/(-gn3[0,0])**0.5
    gdetdivrhouu=div(gdet[:,:,0:1]*avg_rhouu)
    etot = scaletofullwedge(nz*(-gdet*avg_Tud[1,0]*_dx2*_dx3).sum(axis=-1).sum(-1))
    madded = scaletofullwedge(nz*(gdetdivrhouu*_dx2*_dx3).sum(axis=-1)).sum(-1).cumsum(0)
    madded -= madded[iofr(10)]
    eadded = scaletofullwedge(nz*(etad[0]*gdetdivrhouu*_dx2*_dx3).sum(axis=-1)).sum(-1).cumsum(0)
    eadded -= eadded[iofr(10)]
    eadded/=nz
    plt.figure(10)
    #xxx
    #plt.plot(r[:,0,0], mdotval-mdotval[iofr(10)],label="mdotval")
    #$plt.plot(r[:,0,0], madded,label="madded")
    #plt.plot(r[:,0,0], eadded,label="eadded")
    plt.plot(r[:,0,0], edotval,label="Etot")
    plt.plot(r[:,0,0], ldotval/10.,label="Ltot/10")
    #plt.plot(r[:,0,0], ldotval*omegah,label="Omegah * Ltot")
    plt.plot(r[:,0,0], -mdotval,label="Mtot")
    plt.ylim(0,10)
    plt.legend(loc='lower right')
    rh = 1+(1-a**2)**0.5
    plt.xlim(rh,30)
    #plt.ylim(-20,20)
    #res[:,1:-1] += (vec[2][:,2:]-vec[2][:,:-2])  

def ploteta():
    #FIGURE 1 LOTSOPANELS
    #Figure 1
    #To make plot, run 
    #run ~/py/mread/__init__.py 1 1
    #To re-make plot without reloading the fiels, run
    #run ~/py/mread/__init__.py 1 -1
    bbox_props = dict(boxstyle="round,pad=0.1", fc="w", ec="w", alpha=0.9)
    #AT: plt.legend( loc = 'upper left', bbox_to_anchor = (0.5, 0.5) ) #0.5, 0.5 = center of plot
    #To generate movies for all sub-folders of a folder:
    #cd ~/Research/runart; for f in *; do cd ~/Research/runart/$f; (python  ~/py/mread/__init__.py &> python.out &); done
    grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]), use2d=True )
    #rd( "dump0000.bin" )
    #rfd("fieldline0000.bin")  #to definea
    #grid3dlight("gdump")
    qtymem=None #clear to free mem
    rhor=1+(1+a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    qtymem=getqtyvstime(ihor,0.2)
    fig=plt.figure(0, figsize=(12,6), dpi=100)
    plt.clf()
    #
    # eta = pjet/<mdot>
    #
    ax34 = plt.gca()
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax34,whichplot=4,prefactor=1)
    ymax=ax34.get_ylim()[1]
    #if 1 < ymax and ymax < 2: 
    #    #ymax = 2
    #    tck=(1,)
    #    ax34.set_yticks(tck)
    #    #ax34.set_yticklabels(('','1','2'))
    #elif ymax < 1: 
    #    #ymax = 1
    #    tck=np.arange(ymax/10,ymax)
    #    ax34.set_yticks(tck)
    #    #ax34.set_yticklabels(('','1'))
    if ymax >= 1:
        ymax=np.floor(ymax)+1
        tck=np.arange(1,ymax,(ymax-1.0)/2.0)
        ax34.set_yticks(tck)
    else:
        #ymax=np.floor(ymax)+1
        ymax=2*(np.floor(np.floor(ymax+1.5)/2))
        tck=np.arange(0,ymax,ymax/2.0)
        ax34.set_yticks(tck)
    #
    #reset lower limit to 0
    #ax34.set_ylim((0,ax34.get_ylim()[1]))
    ax34.set_ylim((0,ymax))
    ax34.grid(True)
    ax34.set_ylabel(r"$\eta$")
    # plt.text(ax34.get_xlim()[1]/40., 0.8*ax34.get_ylim()[1], r"$(\mathrm{g})$", size=16, rotation=0.,
    #          ha="center", va="center",
    #          color='k',weight='regular',bbox=bbox_props
    #          )
    ax34r = ax34.twinx()
    ax34r.set_ylim(ax34.get_ylim())
    ax34r.set_yticks(tck)
    gc.collect()

def mkmovie(framesize=50, domakeavi=False):
    # use to avoid making plots in ploqty...() while creating plots
    global avoidplotsglobal
    avoidplotsglobal=1
    #
    #Rz and xy planes side by side
    plotlenf=10
    plotleni=framesize
    plotlenti=1e6 #so high that never gets used
    plotlentf=2e6
    #To generate movies for all sub-folders of a folder:
    #cd ~/Research/runart; for f in *; do cd ~/Research/runart/$f; (python  ~/py/mread/__init__.py &> python.out &); done
    global modelname
    if len(sys.argv[1:])>0:
        modelname = sys.argv[1]
    else:
        modelname = "Unknown Model"
    #
    print("ModelName = %s" % (modelname) )
    #
    if len(sys.argv[1:])==3 and sys.argv[2].isdigit() and (sys.argv[3].isdigit() or sys.argv[3][0]=="-") :
        whichi = int(sys.argv[2])
        whichn = int(sys.argv[3])
        print( "Doing every %d slice of total %d slices" % (whichi, whichn) ) ;sys.stdout.flush()
    else:
        whichi = None
        whichn = None
    if whichn < 0 and whichn is not None:
        whichn = -whichn
        dontloadfiles = True
    else:
        dontloadfiles = False
        print("Loading grid3d") ;sys.stdout.flush()
        grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]), use2d=True )
        #grid3dlight("gdump")
        #rd( "dump0000.bin" )
        #flist = np.sort(glob.glob( os.path.join("dumps/", "fieldline*.bin") ) )
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
        firstfieldlinefile=flist[0]
        #rfd("fieldline0000.bin")  #to definea
        print("Loading header of first file") ;sys.stdout.flush()
        rfdheaderonly(firstfieldlinefile)
        #
        ########################
        rfdfirstfile()
        global maxrho
        maxrho=np.max(rho)
        print("maxrho=%g" % (maxrho))
        #
        global qtymem
        qtymem=None #clear to free mem
        rhor=1+(1+a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        print("Loading qty file") ;sys.stdout.flush()
        qtymem=getqtyvstime(ihor,0.2)
        numtimeslices = qtymem.shape[1]
    #
    #
    #
    #
    #
    ########################
    ################################################
    # get levels for all frames showing aphi so aphi values constant.
    numcontours=100
    aphipow=1.0
    #
    # for thickdisk7 use fieldline2500 (if available) to set levels.  Otherwise use final available file.
    if modelname=="thickdisk7" and os.path.isfile("dumps/fieldline2500.bin"):
        rfd("fieldline2500.bin")
    else:
        lenflist=len(flist)
        choseindex=lenflist/2
        levelfieldlinefile=flist[choseindex]
        levelfieldlinefile=re.sub("dumps/","",levelfieldlinefile)
        rfd(levelfieldlinefile)
    #
    # DEBUG: Avoid initfinal and stream unless specifically wanted
    skip1gen=0
    skip2gen=1
    skip3gen=1
    #
    if skip2gen==0: 
        #########
        inputlevs=None
        # compute
        mkinitfinalplotpre1()
        #
        # get information to setup levels if required
        if inputlevs==None:
            aphijetouter=mkinitfinalplotpre2(whichlevs=1)
        #
        # outputs file, but just name fake file because just using it to get contours -- will repeat in loop below
        # plottype as firstlast=1 meaning no funny redefinitin of z-range for any plots
        returnlevsinitfinal=mkinitfinalplotpost(fname="fake_%d_%d" % (whichi,whichn) ,plottype=2,aphijetouter=aphijetouter,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
        #
        # now have levels as inputlevs and aphijetouter for that contour line
        inputlevsinitfinal=returnlevsinitfinal
        #
        #
        veldensity=2 # only applies to fakestream below -- so quick since don't care about the stream result.
        returnlevsstream=mkstreamplotprepost(fname="fakestream_%d_%d" % (whichi,whichn),veldensity=veldensity,inputlevs=inputlevs,numcontours=numcontours,aphipow=aphipow)
        inputlevsstream=returnlevsstream
    #
    #
    lenflist=len(flist)
    #
    #
    ################################################
    #
    #
    ################################################
    # LOOP over frames
    for findex, fname in enumerate(flist):
        #
        # check if skip based upon if this core should be doing this findex
        if findex % whichn != whichi:
            continue
        #
        # extract number of actual file independent of findex
        filenum=re.sub("dumps/fieldline","",fname)
        filenum=re.sub(".bin","",filenum)
        filenum=int(filenum)
        print("fname=%s filenum=%d" % (fname,filenum)) ; sys.stdout.flush()
        #
        # control where ticker is located in mkmovieframe plots
        if 1==1:
            # use this if qty2.npy uses same fieldline file list as movie frames in here
            qtyfindex=findex
            # offset non-zero for thickdiskhr3 since number of field line dumps doesn't match number of time slices in qty2.npy that's merged from thickdisk3 qty2.npy
            offset = numtimeslices - len(flist)
            print("offset=%d" % (offset)) ; sys.stdout.flush()
            qtyfindex=qtyfindex+offset
        else:
            # use this if using full qty2.npy but only partial fieldline files for movie frames
            qtyfindex=filenum
        #
        # check if can fully skip (avoids read of fieldline file if not needed):
        skip1=(dontloadfiles == False and os.path.isfile("lrho%04d_Rzxym1.png" % (filenum)) and os.path.isfile("lrhosmall%04d_Rzxym1.png" % (filenum)))
        skip2=(dontloadfiles == False and os.path.isfile("initfinal%04d.png" % (filenum)))
        skip3=(dontloadfiles == False and os.path.isfile("stream%04d.png" % (filenum)))
        #
        # Avoid initfinal and stream unless specifically wanted
        if skip1gen==1:
            skip1=skip1gen
        if skip2gen==1:
            skip2=skip2gen
        if skip3gen==1:
            skip3=skip3gen
        #
        #
        #
        if skip1 and skip2 and skip3:
            print("Fully skipped: %s",fname)
            continue
        #
        #
        ############
        # load fieldline file
        mkmovieframepre1(fname=fname)
        print("Doing: %s",fname)
        #
        cvelalready=0 # currently all these need is cvel(), so can do this check on all frame types below
        #
        #
        if skip1==1:
            print( "lrho and lrhosmall: Skipping " + fname + " as lrho%04d_Rzxym1.png exists" % (filenum) + " and lrhosmall%04d_Rzxym1.png exists" % (filenum) )  ; sys.stdout.flush()
        else:
            print( "lrho and lrhosmall: Processing " + fname + " ..." ) ;  sys.stdout.flush()
            #
            #
            ####################################
            # normal movie frame
            if cvelalready==0:
                mkmovieframepre2()
                cvelalready=1
            #
            mkmovieframe(findex=qtyfindex,filenum=filenum,framesize=framesize)
            #
        if skip2==1:
            print( "initfinal: Skipping " + fname + " as initfinal%04d.png exists" % (filenum) ) ; sys.stdout.flush()
        else:
            print( "initfinal: Processing " + fname + " ..." ) ; sys.stdout.flush()
            ####################################
            # get init/final type frames
            #
            if cvelalready==0:
                mkinitfinalplotpre1()
                cvelalready=1
            #
            #
            # use inputlevs and aphijetouter from defined frame before frame loop
            returnlevsinitfinalnew=mkinitfinalplotpost(fname="initfinal"+"%04d" % filenum,plottype=2,aphijetouter=aphijetouter,inputlevs=inputlevsinitfinal,numcontours=numcontours,aphipow=aphipow)
            #
            ####################################
        if skip3==1:
            print( "stream: Skipping " + fname + " as stream%04d.png exists" % (filenum) ) ; sys.stdout.flush()
        else:
            print( "stream: Processing " + fname + " ..." ) ; sys.stdout.flush()
            # get stream frame
            if cvelalready==0:
                cvel()
                cvelalready=1
            #
            veldensity=8
            #
            if modelname=="thickdisk7":
                if lenflist>1000:
                    switchnum=500
                else:
                    switchnum=50
                if filenum<switchnum:
                    veldensity=2
            else:
                if lenflist>1000:
                    switchnum=500
                else:
                    switchnum=50
                if filenum<switchnum:
                    veldensity=2
            #
            print("veldensity=%d" % veldensity) ; sys.stdout.flush()
            print(B.shape) ; sys.stdout.flush()
            returnlevsstreamnew=mkstreamplotprepost(fname="stream%04d" % filenum,veldensity=veldensity,inputlevs=inputlevsstream,numcontours=numcontours,aphipow=aphipow)
            ####################################
            #
            #
    print( "Done mkmovie!" ) ; sys.stdout.flush()
    #
    # some oldish information on how to produce movies
    if domakeavi:
        #print( "Now you can make a movie by running:" )
        #print( "ffmpeg -fflags +genpts -r 10 -i lrho%04d.png -vcodec mpeg4 -qmax 5 mov.avi" )
        os.system("mv mov_%s_Rzxym1.avi mov_%s_Rzxym1.bak.avi" % ( os.path.basename(os.getcwd()), os.path.basename(os.getcwd())) )
        #os.system("ffmpeg -fflags +genpts -r 20 -i lrho%%04d_Rzxym1.png -vcodec mpeg4 -qmax 5 mov_%s_Rzxym1.avi" % (os.path.basename(os.getcwd())) )
        os.system("ffmpeg -fflags +genpts -r 20 -i lrho%%04d_Rzxym1.png -vcodec mpeg4 -qmax 5 -b 10000k -pass 1 mov_%s_Rzxym1p1.avi" % (os.path.basename(os.getcwd())) )
        os.system("ffmpeg -fflags +genpts -r 20 -i lrho%%04d_Rzxym1.png -vcodec mpeg4 -qmax 5 -b 10000k -pass 2 mov_%s_Rzxym1.avi" % (os.path.basename(os.getcwd())) )
        #os.system("scp mov.avi 128.112.70.76:Research/movies/mov_`basename \`pwd\``.avi")


def mkmovieframepre1(fname=None):
    rfd("../"+fname)
    # if oldnz < nz:
    #     #resolution changed on the fly, get correct-size arrays for r, h, ph
    #     rd("dump0147.bin")
    #     #reread the fieldline dump
    #     rfd("../"+fname)

def mkmovieframepre2():
    # oldnz=nz
    cvel() #for calculating bsq


def mkmovieframe(findex=None,filenum=None,framesize=None):
    #
    print("mkmovieframe: findex=%d filenum=%d framesize=%d" % (findex,filenum,framesize)) ; sys.stdout.flush()
    # could do time-dependent frame size
    #plotlen = plotleni+(plotlenf-plotleni)*(t-plotlenti)/(plotlentf-plotlenti)
    #plotlen = min(plotlen,plotleni)
    #plotlen = max(plotlen,plotlenf)
    plotlen = framesize
    #
    plt.figure(0, figsize=(12,9), dpi=100)
    plt.clf()
    #SWITCH OFF SUPTITLE
    #plt.suptitle(r'$\log_{10}\rho$ at t = %4.0f' % t)
    ##########
    #
    #mdot,pjet,pjet/mdot plots
    gs3 = GridSpec(3, 3)
    #gs3.update(left=0.055, right=0.97, top=0.42, bottom=0.06, wspace=0.01, hspace=0.04)
    gs3.update(left=0.055, right=0.97, top=0.41, bottom=0.06, wspace=0.01, hspace=0.04)
    #gs3.update(left=0.055, right=0.95, top=0.42, bottom=0.03, wspace=0.01, hspace=0.04)
    #
    ##############
    #mdot
    ax31 = plt.subplot(gs3[-3,:])
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax31,whichplot=1,findex=findex)
    ymax=ax31.get_ylim()[1]
    #ymax=2*(np.floor(np.floor(ymax+1.5)/2))
    ax31.set_yticks((ymax/2.0,ymax,ymax/2.0))
    ax31.grid(True)
    #ax31.set_ylim((0,ymax))
    #pjet
    # ax32 = plt.subplot(gs3[-2,:])
    # plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax32,whichplot=2)
    # ymax=ax32.get_ylim()[1]
    # ax32.set_yticks((ymax/2.0,ymax))
    # ax32.grid(True)
    #pjet/mdot
    # ax33 = plt.subplot(gs3[-1,:])
    # plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax33,whichplot=3)
    # ymax=ax33.get_ylim()[1]
    # ax33.set_yticks((ymax/2.0,ymax))
    # ax33.grid(True)
    #
    ##############
    #\phi
    #
    ax35 = plt.subplot(gs3[-2,:])
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax35,whichplot=5,findex=findex)
    ymax=ax35.get_ylim()[1]
    #if 1 < ymax and ymax < 2: 
    #    #ymax = 2
    #    tck=(1,)
    #    ax35.set_yticks(tck)
    #    #ax35.set_yticklabels(('','1','2'))
    #elif ymax < 1: 
    #    #ymax = 1
    #    tck=(ymax/10,ymax)
    #    ax35.set_yticks(tck)
    #    ax35.set_yticklabels(('','1'))
    if ymax >=1:
        ymax=np.floor(ymax*0.9999)+1
        tck=np.arange(1,ymax,(ymax-1.0)/2.0)
        ax35.set_yticks(tck)
    elif ymax <1 and ymax > 0.1:
        ymax=1
        ax35.set_ylim((0,ymax))
        tck=np.arange(ymax/2.0,(3.0/2.0)*ymax,ymax/2.0)
        ax35.set_yticks(tck)
    else:
        ax35.set_yticks((ymax/2.0,ymax))
        #ax35.set_ylim((0,ymax))
    #
    ax35.grid(True)
    #
    #####################
    # eta=pjet/<mdot>
    #
    ax34 = plt.subplot(gs3[-1,:])
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax34,whichplot=4,findex=findex)
    ymax=ax34.get_ylim()[1]
    #if 100 < ymax and ymax < 200: 
    #    #ymax = 2
    #    tck=(100,)
    #    ax34.set_yticks(tck)
    #    #ax34.set_yticklabels(('','100','200'))
    #elif ymax < 100: 
    #    #ymax = 100
    #    tck=(ymax/10,ymax)
    #    ax34.set_yticks(tck)
    #    ax34.set_yticklabels(('','100'))
    if ymax>=100:
        ymax=np.floor(ymax/100.*0.9999)+1
        ymax*=100
        tck=np.arange(1,ymax/100.,(ymax/100.0-1.0)/2.0)*100
        ax34.set_yticks(tck)
    elif ymax>=10:
        ymax=np.floor(ymax/10.*0.9999)+1
        ymax*=10
        tck=np.arange(1,ymax/10.,(ymax/10.0-1.0)/2.0)*10
        ax34.set_yticks(tck)
    else:
        ax34.set_yticks((ymax/2.0,ymax))
    #
    ax34.grid(True)
    #reset lower limit to 0
    #Rz xy
    #
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-4.0
        vmaxforframe=0.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-4.0
        vmaxforframe=0.5
    else:
        # for Jon's thickdisk models
        vminforframe=-2.4
        vmaxforframe=1.5625
    #
    #
    ###########################
    # BIG BOX
    ###########################
    plotsize=framesize
    #
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.05, right=0.45, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
    ax1 = plt.subplot(gs1[:, -1])
    mkframe("lrho%04d_Rz%g" % (filenum,plotsize),vmin=vminforframe,vmax=vmaxforframe,len=plotsize,ax=ax1,cb=False,pt=False)
    #
    plt.xlabel(r"$x\ [r_g]$",fontsize=16,ha='center')
    plt.ylabel(r"$z\ [r_g]$",ha='left',labelpad=10,fontsize=16)
    #
    gs2 = GridSpec(1, 1)
    gs2.update(left=0.5, right=1, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
    ax2 = plt.subplot(gs2[:, -1])
    #
    if nz==1:
        mkframe("lrho%04d_xy%g" % (filenum,plotsize),vmin=vminforframe,vmax=vmaxforframe,len=plotsize,ax=ax2,cb=True,dostreamlines=True)
    else:
        # If using 2D data, then for now, have to replace below with mkframe version above and replace ax1->ax2.  Some kind of qhull error.
        mkframexy("lrho%04d_xy%g" % (filenum,plotsize),vmin=vminforframe,vmax=vmaxforframe,len=plotsize,ax=ax2,cb=True,pt=False,dostreamlines=True)
    #
    #
    plt.xlabel(r"$x\ [r_g]$",fontsize=16,ha='center')
    plt.ylabel(r"$y\ [r_g]$",ha='left',labelpad=10,fontsize=16)
    #
    #
    #print xxx
    plt.savefig( "lrho%04d_Rzxym1.png" % (filenum)  )
    plt.savefig( "lrho%04d_Rzxym1.eps" % (filenum)  )
    #
    ###########################
    # SMALL BOX
    ###########################
    plotsize=framesize/5
    #
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.05, right=0.45, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
    ax1 = plt.subplot(gs1[:, -1])
    mkframe("lrhosmall%04d_Rz%g" % (filenum,plotsize),vmin=vminforframe,vmax=vmaxforframe,len=plotsize,ax=ax1,cb=False,pt=False)
    #
    plt.xlabel(r"$x\ [r_g]$",fontsize=16,ha='center')
    plt.ylabel(r"$z\ [r_g]$",ha='left',labelpad=10,fontsize=16)
    #
    gs2 = GridSpec(1, 1)
    gs2.update(left=0.5, right=1, top=0.99, bottom=0.48, wspace=0.01, hspace=0.05)
    ax2 = plt.subplot(gs2[:, -1])
    #
    if nz==1:
        mkframe("lrhosmall%04d_xy%g" % (filenum,plotsize),vmin=vminforframe,vmax=vmaxforframe,len=plotsize,ax=ax2,cb=True,dostreamlines=True)
    else:
        # If using 2D data, then for now, have to replace below with mkframe version above and replace ax1->ax2.  Some kind of qhull error.
        mkframexy("lrhosmall%04d_xy%g" % (filenum,plotsize),vmin=vminforframe,vmax=vmaxforframe,len=plotsize,ax=ax2,cb=True,pt=False,dostreamlines=True)
    #
    #
    plt.xlabel(r"$x\ [r_g]$",fontsize=16,ha='center')
    plt.ylabel(r"$y\ [r_g]$",ha='left',labelpad=10,fontsize=16)
    #
    #
    #print xxx
    plt.savefig( "lrhosmall%04d_Rzxym1.png" % (filenum)  )
    plt.savefig( "lrhosmall%04d_Rzxym1.eps" % (filenum)  )
    #print xxx




def mk2davg():
    #
    global modelname
    if len(sys.argv[1:])>0:
        modelname = sys.argv[1]
    else:
        modelname = "Unknown Model"
    #
    print("ModelName = %s" % (modelname) ) ; sys.stdout.flush()
    ####################################
    global avoidplotsglobal
    avoidplotsglobal=1
    #
    if len(sys.argv[1:])>1:
        grid3d("gdump.bin",use2d=True)
        #rd("dump0000.bin")
        #rfd("fieldline0000.bin")
        #rfdheaderfirstfile()
    # gets structure of uu and other things
    rfdfirstfile()
    global maxrho
    maxrho=np.max(rho)
    print("maxrho=%g" % (maxrho))
    #
    #
    flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
    numfiles=len(flist)
    ####################################
    #itemspergroup = 20
    if len(sys.argv[1:])==4 and sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit():
        whichgroups = int(sys.argv[2])
        step = int(sys.argv[3])
        itemspergroup = int(sys.argv[4])
        whichgroupe=int(np.ceil(1.0*numfiles/itemspergroup))
        print("NONMERGE: whichgroups=%d step=%d whichgroupe=%d itemspergroup=%d" % (whichgroups,step,whichgroupe,itemspergroup)) ; sys.stdout.flush()
        for whichgroup in np.arange(whichgroups,whichgroupe,step):
            avgmem = get2davg(whichgroup=whichgroup,itemspergroup=itemspergroup)
        #plot2davg(avgmem)
    elif len(sys.argv[1:])==5 and sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit() and sys.argv[5].isdigit():
        whichgroups = int(sys.argv[2])
        whichgroupe = int(sys.argv[3])
        step = int(sys.argv[4])
        itemspergroup = int(sys.argv[5])
        print("MERGE: whichgroups=%d step=%d whichgroupe=%d itemspergroup=%d" % (whichgroups,step,whichgroupe,itemspergroup)) ; sys.stdout.flush()
        if step == 0:
            avgmem = get2davg(usedefault=1)
        elif step == 1:
            avgmem = get2davg(whichgroups=whichgroups,whichgroupe=whichgroupe,itemspergroup=itemspergroup)
        else:
            for whichgroup in np.arange(whichgroups,whichgroupe,step):
                avgmem = get2davg(whichgroup=whichgroup,itemspergroup=itemspergroup)
        print( "Assigning averages..." ) ; sys.stdout.flush()
        assignavg2dvars(avgmem)
    #
    # below is unnecessary and expensive (because repeats qty2.npy creation) if only doing avg with stream lines
    if 1==0:
        plot2davg(whichplot=1)
    #
    gc.collect()




def mkstreamplot1(Btrue=None,gdetB=None,bsq=None,rho=None,uu=None,len=30,lenx=None,leny=None,mylenshowx=None,mylenshowy=None,fntsize=24,arrowsize=4,vminforframe=-4,vmaxforframe=0.5,forceeqsym=0,fname=None,veldensity=8,signaphi=1,numcontours=30,inputlevs=None,aphipow=1.0,dojonwindplot=0,showuu1eq0=True):
    #
    returnlevs=None
    global B # need to tell this function that B is global because assignment to B is taken as local otherwise
    #
    bsqorho = bsq/rho
    #
    #
    if mylenshowx is None:
        if lenx is not None:
            mylenshowx=lenx
        else:
            mylenshowx=len
    #
    if mylenshowy is None:
        if leny is not None:
            mylenshowy=leny
        else:
            mylenshowy=len
    #
    if lenx is None:
        lenx=len
    if leny is None:
        leny=len
    #
    print("mkstreamplot1b: %g %g %g %g" % (lenx,leny,mylenshowx,mylenshowy)) ; sys.stdout.flush()
    #
    #
    fig=plt.figure(176,figsize=(12,9),dpi=300)
    fig.clf()
    #plt.cla()
    axnew = fig.add_subplot(111, aspect='equal')
    #
    if True:
    #if False:
        #velocity
        print("Doing velocity mkstreamplot1") ; sys.stdout.flush()
        B=np.copy(Btrue)
        B[1:] = np.copy(uu[1:])
        # density=24 is highest quality but 10X-30X slower than density=8
        # 8 looks fine.
        # 2 good for testing.
        #veldensity=8
        #
        mkframe("myframe",dovel=True,len=len,lenx=lenx,leny=leny,ax=axnew,density=veldensity,downsample=1,cb=False,pt=False,dorho=False,dovarylw=False,vmin=vminforframe,vmax=vmaxforframe,dobhfield=False,dodiskfield=False,minlenbhfield=0.2,minlendiskfield=0.5,dsval=0.005,color='k',doarrows=False,dorandomcolor=True,lw=1,skipblankint=True,detectLoops=False,ncell=800,minindent=5,minlengthdefault=0.2,startatmidplane=False,forceeqsym=forceeqsym,inputlevs=inputlevs)
        #
        # fix back
        B=np.copy(Btrue)
    #
    if showuu1eq0==True:
    #if False:
        print("Doing stagnation surface mkstreamplot1") ; sys.stdout.flush()
        istag, jstag, hstag, rstag = getstagparams(bsqorho=bsqorho,uu=uu,doplot=0)
        if 1==0:
            myRmax=4
            #z>0
            rs=rstag[(rstag*np.sin(hstag)<myRmax)*np.cos(hstag)>0]
            hs=hstag[(rstag*np.sin(hstag)<myRmax)*np.cos(hstag)>0]
            axnew.plot(rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
            axnew.plot(-rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
            #z<0
            rs=rstag[(rstag*np.sin(hstag)<myRmax)*np.cos(hstag)<0]
            hs=hstag[(rstag*np.sin(hstag)<myRmax)*np.cos(hstag)<0]
            axnew.plot(rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
            axnew.plot(-rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
        if 1==1:
            bsqorhorstag,bsqorhohstag=getstagparams2(bsqorho=bsqorho,uu=uu,doplot=0)
            #bsq = avg_bsq
            #rho = avg_rho
            #bsqorho = bsq/rho
            #z>0
            #print("%d %d %d" % (len(rstag),len(hstag),len(bsqorho))) ; sys.stdout.flush()
            truemaxbsqorhorstag=np.max(bsqorhorstag)
            print("truemaxbsqorhorstag=%g" % (truemaxbsqorhorstag) ) ; sys.stdout.flush()
            # modelname=blandford3d_new has no region with bsqorho>2
            #maxbsqorhorstag=0.95*truemaxbsqorhorstag
            if modelname=="blandford3d_new":
                setnothing=1
            else:
                #if truemaxbsqorhorstag>2.0:
                #maxbsqorhorstag=2.0
                #maxbsqorhorstag=40.0
                maxbsqorhorstag=10.0
                #
                cond=(bsqorhorstag>maxbsqorhorstag)*np.cos(hstag)>0
                rs=rstag[cond]
                hs=hstag[cond]
                print("shapesstag1") ; sys.stdout.flush()
                print(rs.shape) ; sys.stdout.flush()
                print(hs.shape) ; sys.stdout.flush()
                axnew.plot(rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
                axnew.plot(-rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
                #z<0
                cond=((bsqorhorstag>maxbsqorhorstag)*np.cos(hstag)<0)
                rs=rstag[cond]
                hs=hstag[cond]
                print("shapesstag2") ; sys.stdout.flush()
                print(rs.shape) ; sys.stdout.flush()
                print(hs.shape) ; sys.stdout.flush()
                axnew.plot(rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
                axnew.plot(-rs*np.sin(hs),rs*np.cos(hs),'g',lw=3)
            #
        #
    #
    if True:
        #field
        print("Doing field mkstreamplot1") ; sys.stdout.flush()
        # use true B
        B=np.copy(Btrue)
        #
        #plt.figure(1)
        # Sasha says this may help avoid field edge effects
        #finallen=25./30.*mylen
        finallen=len
        finallenx=lenx
        finalleny=leny
        #finallen=2.0*mylen
        # useblank=True causes field lines to stop tracing when they get closer together at slightly larger distances.  
        returnlevs=mkframe("myframe",doaphiavg=False,doaphi=True,dostreamlines=False,useblank=False,len=finallen,lenx=finallenx,leny=finalleny,ax=axnew,density=1,downsample=4,cb=False,pt=False,dorho=False,dovarylw=False,vmin=vminforframe,vmax=vmaxforframe,dobhfield=8,dodiskfield=True,minlenbhfield=0.2,minlendiskfield=0.01,dsval=0.01,color='r',lw=2,startatmidplane=True,domidfield=False,showjet=False,arrowsize=arrowsize,forceeqsym=forceeqsym,signaphi=signaphi,numcontours=numcontours,inputlevs=inputlevs,aphipow=aphipow,dojonwindplot=dojonwindplot,showuu1eq0=showuu1eq0)
        #
        # fix back
        B=np.copy(Btrue)
    #
#    if False:
#        x = (r*np.sin(h))[:,:,0]
#        z = (r*np.cos(h))[:,:,0]
#        x = np.concatenate(-x,x)
#        z = np.concatenate(y,y)
#        mu = np.concatenate(mu[:,:,0],mu[:,:,0])
#        plt.contourf( x, z, mu )
    #
    print("Writing File: %s" % fname) ; sys.stdout.flush()
    #
    ##########################
    # finish setup of plot
    axnew.set_aspect('equal')   
    rhor=1+(1-a**2)**0.5
    el = Ellipse((0,0), 2*rhor, 2*rhor, facecolor='k', alpha=1)
    art=axnew.add_artist(el)
    art.set_zorder(20)
    plt.xlim(-mylenshowx,mylenshowx)
    plt.ylim(-mylenshowy,mylenshowy)
    plt.xlabel(r"$x\ [r_g]$",fontsize=fntsize,ha='center')
    plt.ylabel(r"$z\ [r_g]$",ha='left',labelpad=15,fontsize=fntsize)
    for label in axnew.get_xticklabels() + axnew.get_yticklabels():
        label.set_fontsize(fntsize)
    #
    #plt.savefig("%s.pdf" % fname,bbox_inches='tight',pad_inches=0.02,dpi=300)
    #plt.savefig("%s.eps" % fname,bbox_inches='tight',pad_inches=0.02,dpi=300)
    # just convert png to eps or pdf after since otherwise too large
    plt.savefig("%s.png" % fname,bbox_inches='tight',pad_inches=0.02,dpi=300)
    print("Done Writing File: %s" % fname) ; sys.stdout.flush()
    #
    return(returnlevs)


def mkavgfigs():
    ###########################################
    global modelname
    if len(sys.argv[1:])>0:
        modelname = sys.argv[1]
    else:
        modelname = "Unknown Model"
    #
    print("ModelName = %s" % (modelname) )
    #
    ###########################################
    grid3d("gdump.bin",use2d=True)
    #
    rfdfirstfile()
    global maxrho
    maxrho=np.max(rho)
    print("maxrho=%g" % (maxrho))
    #
    avgmem = get2davg(usedefault=1)
    assignavg2dvars(avgmem)
    #
    #
    #
    #
    mkstreampart1=1
    mkstreampart2=1 # NOTEMARK: set to zero if don't want to read-in qty.npy stuff
    mkstreampart3=1
    mkstreampart4=1
    #
    #
    #
    forceeqsym=0 # forceeqsym=1 makes the streaming take alot longer for some reason.  Also, messes up field geometry so it's not obvious that field threads the disk.
    mylen = 30.0
    mylenshowx=(25.0/30.0)*mylen
    mylenshowy=(25.0/30.0)*mylen
    fntsize=24
    arrowsize=4
    numcontours=30  # 60 was too many for jet region
    aphipow=1.0
    # keep sign information in general for aphi, but for specific plots force aphi sign to be constant
    if modelname=="thickdisk7":
        signaphi=-1.0
    else:
        signaphi=1.0
    #
    if modelname=="runlocaldipole3dfiducial" or modelname=="blandford3d_new":
        # for MB09 dipolar fiducial model
        vminforframe=-4.0
        vmaxforframe=0.5
    elif modelname=="sasham9" or modelname=="sasham9full2pi" or modelname=="sasham5" or modelname=="sasha0" or modelname=="sasha1" or modelname=="sasha2" or modelname=="sasha5" or modelname=="sasha9b25" or modelname=="sasha9b50" or modelname=="sasha9b100" or modelname=="sasha9b200" or modelname=="sasha99":
        vminforframe=-4.0
        vmaxforframe=0.5
    else:
        # for Jon's thickdisk models
        vminforframe=-2.4
        vmaxforframe=1.5625
    #
    #
    #########################################
    if mkstreampart1==1:
        #
        # for dojonwindplot
        global rho,ug,B,gdetB,bsq,mu,ud,uu,beta,uutrue
        rho=avg_rho
        ug=avg_ug
        # use t-phi-averaged gdet B
        B[1] = avg_B[0]
        B[2] = avg_B[1]
        B[3] = avg_B[2]
        gdetB[1:] = avg_gdetB[0:]
        bsq = avg_bsq
        mu = avg_mu
        uu=avg_uu
        uutrue=uu
        ud=avg_ud
        beta = avg_beta
        #
        # normal field
        Btrue=np.zeros((4,nx,ny,nz),dtype=avg_B.dtype)
        Btrue[1:4] = np.copy(avg_B[0:3])
        B[1:4] = np.copy(avg_B[0:3])
        gdetB[1:4] = np.copy(avg_gdetB[0:3])
        #call
        returnlevs=mkstreamplot1(Btrue=Btrue,gdetB=gdetB,bsq=avg_bsq,rho=avg_rho,uu=avg_uu,len=mylen,mylenshowx=mylenshowx,mylenshowy=mylenshowy,fntsize=fntsize,arrowsize=arrowsize,vminforframe=vminforframe,vmaxforframe=vmaxforframe,forceeqsym=forceeqsym,fname="fig2",veldensity=8,signaphi=signaphi,numcontours=numcontours,aphipow=aphipow,dojonwindplot=1)
        # fix back
        B=np.copy(Btrue)
        #
    #
    #
    #
    ##################################################
    if mkstreampart2==1:
        #
        ######
        # compute aphi's for getting thetaalongfield and contour plots
        myxcoord=r[0:iofr(30.0),:,0]*np.sin(h[0:iofr(30.0),:,0])
        myycoord=r[0:iofr(30.0),:,0]*np.cos(h[0:iofr(30.0),:,0])
        #
        logmyxcoord=np.log10(1.0+np.fabs(r[:,:,0]*np.sin(h[:,:,0])))*np.sign(r[:,:,0]*np.sin(h[:,:,0]))
        logmyycoord=np.log10(1.0+np.fabs(r[:,:,0]*np.cos(h[:,:,0])))*np.sign(r[:,:,0]*np.cos(h[:,:,0]))
        #
        myfun1zoom=np.sqrt(avg_psisq[0:iofr(30.0),:,0])
        myfun1all=np.sqrt(avg_psisq[:,:,0])
        #
        aphifromavgfield=fieldcalc()
        myfun2zoom=np.sqrt(aphifromavgfield[0:iofr(30.0),:,0]**2)
        myfun2all=np.sqrt(aphifromavgfield[:,:,0]**2)
        #
        #
        aphi1=np.sqrt(avg_psisq)
        aphi2=np.sqrt(aphifromavgfield**2)
        # compute final-time aphi for comparison
        rfdlastfile()
        aphisnapshot = fieldcalcface()
        aphi3=aphisnapshot
        #
        #
        ##############################
        # get generate_time_series() type averages and calculations
        hoverr_jet_vsr = getbasicqtystuff()
        #
        #
        # get thetaalongfield
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        #
        #
        print("thetaalongfield1"); sys.stdout.flush()
        aphijetbase1,thetaalongfield1=compute_thetaalongfield(aphi=aphi1,picki=ihor,thetaalongjet=hoverr_jet_vsr,whichpole=1)
        thetaalongfield1=np.pi - thetaalongfield1
        print("thetaalongfield2"); sys.stdout.flush()
        aphijetbase2,thetaalongfield2=compute_thetaalongfield(aphi=aphi2,picki=ihor,thetaalongjet=hoverr_jet_vsr,whichpole=1)
        thetaalongfield2=np.pi - thetaalongfield2
        print("thetaalongfield3"); sys.stdout.flush()
        aphijetbase3,thetaalongfield3=compute_thetaalongfield(aphi=aphi3,picki=ihor,thetaalongjet=hoverr_jet_vsr,whichpole=0)
        #
        favg1 = open('datavsravg1.txt', 'w')
        favg1.write("#%s   %s %s %s  %s   %s %s %s\n" % ("ii","r1","r2","r3","hoverr_jet_vsr","thetaalongfield1","thetaalongfield2","thetaalongfield3" ) )
        #
        for ii in np.arange(0,nx):
            favg1.write("%d   %g %g %g   %g   %g %g %g\n" % (ii,r[ii,thetaalongfield1[ii],0],r[ii,thetaalongfield2[ii],0],r[ii,thetaalongfield3[ii],0],np.pi*0.5-hoverr_jet_vsr[ii],thetaalongfield1[ii],thetaalongfield2[ii],thetaalongfield3[ii]) )
            #
        #
        favg1.close()
        #
        ################
        # for Shep:
        # cat datavsravg1.txt | awk '{print $1"   "$2" "$3" "$4"   "$5"   "$6" "$7" "$8}' | column -t > datavsrsharenew.txt
        #
        # avoid potential from averaged field that causes problems but medium (flips pole) and large radii (zeros out)
        # cat datavsravg1.txt | awk '{print $1"   "$2"   "$5"   "$6" "$8}' | column -t > datavsrsharenew.txt
        # cat datavsrsharenew.txt | column -t | less -S
        #
        ########################
        # show averaged aphi for comparison with field from stream lines
        plt.figure(1)
        plco(myfun1zoom,xcoord=myxcoord,ycoord=myycoord,colors='k',nc=30)
        plc(myfun1zoom,xcoord=myxcoord,ycoord=myycoord,colors='r',levels=(aphijetbase1,))
        #plc(daphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='r')
        #d=500
        #plt.xlim(0,d/2.); plt.ylim(-d,d)
        #plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.savefig("aphizoom_avg.pdf")
        plt.savefig("aphizoom_avg.eps")
        plt.savefig("aphizoom_avg.png")
        #
        ########################
        # show averaged aphi for comparison with field from stream lines
        plt.figure(1)
        plco(myfun1all,xcoord=logmyxcoord,ycoord=logmyycoord,colors='k',nc=30)
        plc(myfun1all,xcoord=logmyxcoord,ycoord=logmyycoord,colors='r',levels=(aphijetbase1,))
        #plc(daphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='r')
        #d=500
        #plt.xlim(0,d/2.); plt.ylim(-d,d)
        #plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.savefig("aphialllog_avg.pdf")
        plt.savefig("aphialllog_avg.eps")
        plt.savefig("aphialllog_avg.png")
        #
        #
        ########################
        # show aphi from averaged fields for comparison with field from stream lines
        plt.figure(1)
        plco(myfun2zoom,xcoord=myxcoord,ycoord=myycoord,colors='k',nc=30)
        plc(myfun2zoom,xcoord=myxcoord,ycoord=myycoord,colors='r',levels=(aphijetbase2,))
        #d=500
        #plt.xlim(0,d/2.); plt.ylim(-d,d)
        #plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.savefig("aphizoom_avgfield.pdf")
        plt.savefig("aphizoom_avgfield.eps")
        plt.savefig("aphizoom_avgfield.png")
        #
        ########################
        # show averaged aphi for comparison with field from stream lines
        plt.figure(1)
        plco(myfun2all,xcoord=logmyxcoord,ycoord=logmyycoord,colors='k',nc=30)
        plc(myfun2all,xcoord=logmyxcoord,ycoord=logmyycoord,colors='r',levels=(aphijetbase2,))
        #plc(daphi,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=(0,),colors='r')
        #d=500
        #plt.xlim(0,d/2.); plt.ylim(-d,d)
        #plc(aphi-maxaphibh,levels=(0,),colors='b',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.savefig("aphialllog_avgfield_avg.pdf")
        plt.savefig("aphialllog_avgfield_avg.eps")
        plt.savefig("aphialllog_avgfield_avg.png")
        #
    #####################################
    # plots of F_EM, F_MAKE, omegaf on horizon from averaged data
    if mkstreampart3==1:
        # 
        # things have access to:
        # avg_ts,avg_te,avg_nitems,avg_rho,avg_ug,avg_bsq,avg_unb,avg_uu,avg_bu,avg_ud,avg_bd,avg_B,avg_gdetB,avg_omegaf2,avg_omegaf2b,avg_omegaf1
        # avg_omegaf1b,avg_rhouu,avg_rhobu,avg_rhoud,avg_rhobd,avg_uguu,avg_ugud,avg_Tud,avg_fdd,avg_rhouuud,avg_uguuud,avg_bsquuud,avg_bubd,avg_uuud
        # avg_TudEM, avg_TudMA, avg_mu, avg_sigma, avg_bsqorho, avg_absB, avg_absgdetB, avg_psisq
        # avg_TudPA, avg_TudIE
        # avg_gamma
        #
        # get horizon cut of everything and print out for SM plotting vs. theta
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        # FILE:
        print("shapes"); sys.stdout.flush()
        print(h.shape); sys.stdout.flush()
        print(avg_rho.shape); sys.stdout.flush()
        print(avg_ug.shape); sys.stdout.flush()
        print(avg_bsq.shape); sys.stdout.flush()
        print(avg_unb.shape); sys.stdout.flush()
        avg1 = open('dataavgvsh0.txt', 'w')
        avg1.write("#%s %s %s   %s %s\n" % ("avg_ts","avg_te","avg_nitems","rhor","ihor"))
        avg1.write("%g %g %d   %g %g %d  %g %g %g  %g  %d %d %d\n" % (avg_ts[0],avg_te[0],avg_nitems[0],a,rhor,ihor,_dx1,_dx2,_dx3,scaletofullwedge(1.0),nx,ny,nz))
        avg1.close()
        avg1 = open('dataavgvsh1.txt', 'w')
        # below doesn't yet show columns for each component of vector or tensors
        avg1.write("#avg_rho avg_ug avg_bsq avg_unb avg_uu avg_bu avg_ud avg_bd avg_B avg_gdetB avg_omegaf2 avg_omegaf2b avg_omegaf1 avg_omegaf1b avg_rhouu avg_rhobu avg_rhoud avg_rhobd avg_uguu avg_ugud avg_Tud avg_fdd avg_rhouuud avg_uguuud avg_bsquuud avg_bubd avg_uuud avg_TudEM  avg_TudMA  avg_TudPA  avg_TudIE  avg_mu  avg_sigma  avg_bsqorho  avg_absB  avg_absgdetB  avg_psisq avg_gamma gdet dxdxp11 dxdxp22dx2 dxdxp12 dxdxp21 dxdxp33 avg_absuu avg_absbu avg_absud avg_absbd avg_absomegaf2 avg_absomegaf2b avg_absomegaf1 avg_absomegaf1b avg_absrhouu avg_absfdd\n")
        avg1.write("#%g %g %d :  %g %d\n" % (avg_ts[0],avg_te[0],avg_nitems[0],rhor,ihor))
        for jj in np.arange(0,len(h[0,:,0])):
            # columns 1-6
            avg1.write("%d %g %g %g %g %g " % (jj, h[ihor,jj,0], avg_rho[ihor,jj,0],avg_ug[ihor,jj,0],avg_bsq[ihor,jj,0],avg_unb[ihor,jj,0]))
            # columns 7-10
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_uu[ll,ihor,jj,0]))
            # columns 11-14
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_bu[ll,ihor,jj,0]))
            # columns 15-18
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_ud[ll,ihor,jj,0]))
            # columns 19-22
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_bd[ll,ihor,jj,0]))
            # columns 23-25
            for ll in np.arange(0,3):
                avg1.write("%g " % (avg_B[ll,ihor,jj,0]))
            # columns 26-28
            for ll in np.arange(0,3):
                avg1.write("%g " % (avg_gdetB[ll,ihor,jj,0]))
            # columns 29-32
            avg1.write("%g %g %g %g " % (avg_omegaf2[ihor,jj,0],avg_omegaf2b[ihor,jj,0],avg_omegaf1[ihor,jj,0],avg_omegaf1b[ihor,jj,0]))
            # columns 33-36
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_rhouu[ll,ihor,jj,0]))
            # columns 37-40
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_rhobu[ll,ihor,jj,0]))
            # columns 41-44
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_rhoud[ll,ihor,jj,0]))
            # columns 45-48
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_rhobd[ll,ihor,jj,0]))
            # columns 49-52
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_uguu[ll,ihor,jj,0]))
            # columns 53-56
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_ugud[ll,ihor,jj,0]))
            # columns 57-72
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_Tud[mm,ll,ihor,jj,0]))
            # columns 73-88
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_fdd[mm,ll,ihor,jj,0]))
            # columns 89-104
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_rhouuud[mm,ll,ihor,jj,0]))
            # columns 105-120
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_uguuud[mm,ll,ihor,jj,0]))
            # columns 121-136
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_bsquuud[mm,ll,ihor,jj,0]))
            # columns 137-152
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_bubd[mm,ll,ihor,jj,0]))
            # columns 153-168
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_uuud[mm,ll,ihor,jj,0]))
            # columns 169-184
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_TudEM[mm,ll,ihor,jj,0]))
            # columns 185-200
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_TudMA[mm,ll,ihor,jj,0]))
            # columns 201-216
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_TudPA[mm,ll,ihor,jj,0]))
            # columns 217-232
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_TudIE[mm,ll,ihor,jj,0]))
            # columns 233-235
            avg1.write("%g %g %g " % (avg_mu[ihor,jj,0], avg_sigma[ihor,jj,0], avg_bsqorho[ihor,jj,0]))
            # columns 236-238
            for ll in np.arange(0,3):
                avg1.write("%g " % (avg_absB[ll,ihor,jj,0]))
            # columns 239-241
            for ll in np.arange(0,3):
                avg1.write("%g " % (avg_absgdetB[ll,ihor,jj,0]))
            # columns 242-243
            avg1.write("%g %g " % (avg_psisq[ihor,jj,0],avg_gamma[ihor,jj,0]))
            # other added stuff
            # columns 244 245 246 247 248 249
            avg1.write("%g %g %g %g %g %g " % (gdet[ihor,jj,0],dxdxp[1,1][ihor,jj,0],dxdxp[2,2][ihor,jj,0]*_dx2,dxdxp[1,2][ihor,jj,0],dxdxp[2,1][ihor,jj,0],dxdxp[3,3][ihor,jj,0]))
            # columns 250-253
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_absuu[ll,ihor,jj,0]))
            # columns 254-257
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_absbu[ll,ihor,jj,0]))
            # columns 258-261
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_absud[ll,ihor,jj,0]))
            # columns 262-265
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_absbd[ll,ihor,jj,0]))
            # columns 266-269
            avg1.write("%g %g %g %g " % (avg_absomegaf2[ihor,jj,0],avg_absomegaf2b[ihor,jj,0],avg_absomegaf1[ihor,jj,0],avg_absomegaf1b[ihor,jj,0]))
            # columns 270-273
            for ll in np.arange(0,4):
                avg1.write("%g " % (avg_absrhouu[ll,ihor,jj,0]))
            # columns 274-289
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avg_absfdd[mm,ll,ihor,jj,0]))
            avg1.write("\n")
        #
        avg1.close()
        #
        #
        #####################
        # average in theta centered on equatorial region, and output everything for Gammie plot in SM
        #
        print("shapes"); sys.stdout.flush()
        print(h.shape); sys.stdout.flush()
        print(gdet.shape); sys.stdout.flush()
        print(avg_rho.shape); sys.stdout.flush()
        print(avg_ug.shape); sys.stdout.flush()
        print(avg_bsq.shape); sys.stdout.flush()
        print(avg_unb.shape); sys.stdout.flush()
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        # FILE:
        avg1 = open('dataavgvsr0.txt', 'w')
        avg1.write("#%s %s %s   %s %s\n" % ("avg_ts","avg_te","avg_nitems","rhor","ihor"))
        avg1.write("%g %g %d   %g %g %d  %g %g %g  %g  %d %d %d\n" % (avg_ts[0],avg_te[0],avg_nitems[0],a,rhor,ihor,_dx1,_dx2,_dx3,scaletofullwedge(1.0),nx,ny,nz))
        avg1.close()
        avg1 = open('dataavgvsr1.txt', 'w')
        # below doesn't yet show columns for each component of vector or tensors
        avg1.write("#avg_rho avg_ug avg_bsq avg_unb avg_uu avg_bu avg_ud avg_bd avg_B avg_gdetB avg_omegaf2 avg_omegaf2b avg_omegaf1 avg_omegaf1b avg_rhouu avg_rhobu avg_rhoud avg_rhobd avg_uguu avg_ugud avg_Tud avg_fdd avg_rhouuud avg_uguuud avg_bsquuud avg_bubd avg_uuud avg_TudEM  avg_TudMA  avg_TudPA  avg_TudIE  avg_mu  avg_sigma  avg_bsqorho  avg_absB  avg_absgdetB  avg_psisq avg_gamma avggdet dxdxp11 dxdxp22dx2 dxdxp12 dxdxp21 dxdxp33 avg_absuu avg_absbu avg_absud avg_absbd avg_absomegaf2 avg_absomegaf2b avg_absomegaf1 avg_absomegaf1b avg_absrhouu avg_absfdd rhosqint rhosqint2\n")
        avg1.write("#%g %g %d :  %g %d\n" % (avg_ts[0],avg_te[0],avg_nitems[0],rhor,ihor))
        #
        bsq=avg_bsq
        rho=avg_rho
        (rhoclean,ugclean,uuclean,maxbsqorhonear,maxbsqorhofar,avgcondmaxbsqorho,avgcondmaxbsqorhorhs,rinterp)=getrhouclean(avg_rho,avg_ug,avg_uu)
        maxbsqorho=np.copy(maxbsqorhonear)
        diskcondition=avgcondmaxbsqorho
        #
        whichhortype=0
        #
        if whichhortype==0:
            # focus on non-jet for Gammie plot purposes
            # just non-jet uses alot of corona, which doesn't follow Gammie. Apparently FLPA very small in simulation compared to Gammie or thin disk.
            diskcondition=(diskcondition)*(1)
        else:
            #choosehor=0.06 # still PA~0, and still have to make upsilon~2*upsilon0, but simpler looking.  Still stratification within ISCO.
            choosehor=0.03 # below disk scale height even at horizon
            diskcondition=(diskcondition)*(np.fabs(h-0.5*np.pi)<choosehor)
        #
        print("diskcondition.shape"); sys.stdout.flush()
        print(diskcondition.shape); sys.stdout.flush()
        denfactor=1.0 + avg_rho*0.0
        #denfactor=avg_rho # 1 weighting -- maybe squared would be better ala Penna, but then should change other weightings when weight by rho
        #no, can't weight like that for integrals
        print("denfactor.shape"); sys.stdout.flush()
        print(denfactor.shape); sys.stdout.flush()
        #
        keywordsrhosq={'which': diskcondition}
        tiny=np.finfo(avg_rho.dtype).tiny
        rhosqint=intangle_foravg2d(gdet*denfactor,**keywordsrhosq)+tiny
        rhosqint2=intangle_foravg2d(denfactor,**keywordsrhosq)+tiny
        #
        #avg_rho,avg_ug,avg_bsq,avg_unb,avg_uu,avg_bu,avg_ud,avg_bd,avg_B,avg_gdetB,avg_omegaf2,avg_omegaf2b,avg_omegaf1
        # avg_omegaf1b,avg_rhouu,avg_rhobu,avg_rhoud,avg_rhobd,avg_uguu,avg_ugud,avg_Tud,avg_fdd,avg_rhouuud,avg_uguuud,avg_bsquuud,avg_bubd,avg_uuud
        # avg_TudEM, avg_TudMA, avg_mu, avg_sigma, avg_bsqorho, avg_absB, avg_absgdetB, avg_psisq
        # avg_TudPA, avg_TudIE
        # avg_gamma
        # get averages (vs radius only in the end)
        avgvsr_rho=intangle_foravg2d(gdet*denfactor*avg_rho,**keywordsrhosq)/rhosqint
        avgvsr_ug=intangle_foravg2d(gdet*denfactor*avg_ug,**keywordsrhosq)/rhosqint
        avgvsr_bsq=intangle_foravg2d(gdet*denfactor*avg_bsq,**keywordsrhosq)/rhosqint
        avgvsr_unb=intangle_foravg2d(gdet*denfactor*avg_unb,**keywordsrhosq)/rhosqint
        avgvsr_uu=np.zeros((4,nx),dtype=np.float32)
        avgvsr_bu=np.zeros_like(avgvsr_uu)
        avgvsr_ud=np.zeros_like(avgvsr_uu)
        avgvsr_bd=np.zeros_like(avgvsr_uu)
        avgvsr_absuu=np.zeros_like(avgvsr_uu)
        avgvsr_absbu=np.zeros_like(avgvsr_uu)
        avgvsr_absud=np.zeros_like(avgvsr_uu)
        avgvsr_absbd=np.zeros_like(avgvsr_uu)
        # doabs=1 so across equator sign-changes in B_\phi u_\theta B_\theta  and B^r are removed to avoid zeroing-out terms.  3-Field (B) also has truly abs-averaged versions below, but not b or u^i or u_i
        for ll in np.arange(0,4):
            avgvsr_uu[ll]=intangle_foravg2d(gdet*denfactor*avg_uu[ll],doabs=0,**keywordsrhosq)/rhosqint
            avgvsr_bu[ll]=intangle_foravg2d(gdet*denfactor*avg_bu[ll],doabs=0,**keywordsrhosq)/rhosqint
            avgvsr_ud[ll]=intangle_foravg2d(gdet*denfactor*avg_ud[ll],doabs=0,**keywordsrhosq)/rhosqint
            avgvsr_bd[ll]=intangle_foravg2d(gdet*denfactor*avg_bd[ll],doabs=0,**keywordsrhosq)/rhosqint
        for ll in np.arange(0,4):
            avgvsr_absuu[ll]=intangle_foravg2d(gdet*denfactor*avg_absuu[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_absbu[ll]=intangle_foravg2d(gdet*denfactor*avg_absbu[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_absud[ll]=intangle_foravg2d(gdet*denfactor*avg_absud[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_absbd[ll]=intangle_foravg2d(gdet*denfactor*avg_absbd[ll],doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_B=np.zeros((3,nx),dtype=np.float32)
        avgvsr_gdetB=np.zeros_like(avgvsr_B)
        for ll in np.arange(0,3):
            avgvsr_B[ll]=intangle_foravg2d(gdet*denfactor*avg_B[ll],doabs=0,**keywordsrhosq)/rhosqint
            avgvsr_gdetB[ll]=intangle_foravg2d(gdet*denfactor*avg_gdetB[ll],doabs=0,**keywordsrhosq)/rhosqint
        avgvsr_omegaf2=intangle_foravg2d(gdet*denfactor*avg_omegaf2,doabs=0,**keywordsrhosq)/rhosqint
        avgvsr_omegaf2b=intangle_foravg2d(gdet*denfactor*avg_omegaf2b,doabs=0,**keywordsrhosq)/rhosqint
        avgvsr_omegaf1=intangle_foravg2d(gdet*denfactor*avg_omegaf1,doabs=0,**keywordsrhosq)/rhosqint
        avgvsr_omegaf1b=intangle_foravg2d(gdet*denfactor*avg_omegaf1b,doabs=0,**keywordsrhosq)/rhosqint
        avgvsr_absomegaf2=intangle_foravg2d(gdet*denfactor*avg_absomegaf2,doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_absomegaf2b=intangle_foravg2d(gdet*denfactor*avg_absomegaf2b,doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_absomegaf1=intangle_foravg2d(gdet*denfactor*avg_absomegaf1,doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_absomegaf1b=intangle_foravg2d(gdet*denfactor*avg_absomegaf1b,doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_rhouu=np.zeros_like(avgvsr_uu)
        avgvsr_rhobu=np.zeros_like(avgvsr_uu)
        avgvsr_rhoud=np.zeros_like(avgvsr_uu)
        avgvsr_rhobd=np.zeros_like(avgvsr_uu)
        avgvsr_absrhouu=np.zeros_like(avgvsr_uu)
        avgvsr_uguu=np.zeros_like(avgvsr_uu)
        avgvsr_ugud=np.zeros_like(avgvsr_uu)
        for ll in np.arange(0,4):
            avgvsr_rhouu[ll]=intangle_foravg2d(gdet*denfactor*avg_rhouu[ll],doabs=0,**keywordsrhosq)/rhosqint
            avgvsr_rhobu[ll]=intangle_foravg2d(gdet*denfactor*avg_rhobu[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_rhoud[ll]=intangle_foravg2d(gdet*denfactor*avg_rhoud[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_rhobd[ll]=intangle_foravg2d(gdet*denfactor*avg_rhobd[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_absrhouu[ll]=intangle_foravg2d(gdet*denfactor*avg_absrhouu[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_uguu[ll]=intangle_foravg2d(gdet*denfactor*avg_uguu[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_ugud[ll]=intangle_foravg2d(gdet*denfactor*avg_ugud[ll],doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_Tud=np.zeros((4,4,nx),dtype=np.float32)
        avgvsr_fdd=np.zeros_like(avgvsr_Tud)
        avgvsr_absfdd=np.zeros_like(avgvsr_Tud)
        avgvsr_rhouuud=np.zeros_like(avgvsr_Tud)
        avgvsr_uguuud=np.zeros_like(avgvsr_Tud)
        avgvsr_bsquuud=np.zeros_like(avgvsr_Tud)
        avgvsr_bubd=np.zeros_like(avgvsr_Tud)
        avgvsr_uuud=np.zeros_like(avgvsr_Tud)
        avgvsr_TudEM=np.zeros_like(avgvsr_Tud)
        avgvsr_TudMA=np.zeros_like(avgvsr_Tud)
        avgvsr_TudPA=np.zeros_like(avgvsr_Tud)
        avgvsr_TudIE=np.zeros_like(avgvsr_Tud)
        # doabs=0 for below since care about sign (e.g. flux in or out) and can't easily recover sign unless know more details
        # except fdd, which oscillates around 0 near equator.  Actually, only fdd has abs during averaging unlike all other doabs==1 quantities, so movement of sign of quantities (e.g. across equator) will cause bad averaging there for these other quantities.
        for ll in np.arange(0,4):
            for mm in np.arange(0,4):
                avgvsr_Tud[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_Tud[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_fdd[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_fdd[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_absfdd[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_absfdd[mm,ll],doabs=1,**keywordsrhosq)/rhosqint
                avgvsr_rhouuud[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_rhouuud[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_uguuud[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_uguuud[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_bsquuud[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_bsquuud[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_bubd[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_bubd[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_uuud[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_uuud[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_TudEM[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_TudEM[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_TudMA[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_TudMA[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_TudPA[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_TudPA[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
                avgvsr_TudIE[mm,ll]=intangle_foravg2d(gdet*denfactor*avg_TudIE[mm,ll],doabs=0,**keywordsrhosq)/rhosqint
        avgvsr_mu=intangle_foravg2d(gdet*denfactor*avg_mu,**keywordsrhosq)/rhosqint
        avgvsr_sigma=intangle_foravg2d(gdet*denfactor*avg_sigma,**keywordsrhosq)/rhosqint
        avgvsr_bsqorho=intangle_foravg2d(gdet*denfactor*avg_bsqorho,**keywordsrhosq)/rhosqint
        avgvsr_absB=np.zeros_like(avgvsr_B)
        avgvsr_absgdetB=np.zeros_like(avgvsr_B)
        for ll in np.arange(0,3):
            avgvsr_absB[ll]=intangle_foravg2d(gdet*denfactor*avg_absB[ll],doabs=1,**keywordsrhosq)/rhosqint
            avgvsr_absgdetB[ll]=intangle_foravg2d(gdet*denfactor*avg_absgdetB[ll],doabs=1,**keywordsrhosq)/rhosqint
        avgvsr_psisq=intangle_foravg2d(gdet*denfactor*avg_psisq,**keywordsrhosq)/rhosqint
        avgvsr_gamma=intangle_foravg2d(gdet*denfactor*avg_gamma,**keywordsrhosq)/rhosqint
        avgvsr_gdet=intangle_foravg2d(gdet*denfactor*gdet,**keywordsrhosq)/rhosqint
        avgvsr_dxdxp11=intangle_foravg2d(gdet*denfactor*dxdxp[1,1],**keywordsrhosq)/rhosqint
        avgvsr_dxdxp22=intangle_foravg2d(gdet*denfactor*dxdxp[2,2],**keywordsrhosq)/rhosqint
        avgvsr_dxdxp12=intangle_foravg2d(gdet*denfactor*dxdxp[1,2],**keywordsrhosq)/rhosqint
        avgvsr_dxdxp21=intangle_foravg2d(gdet*denfactor*dxdxp[2,1],**keywordsrhosq)/rhosqint
        avgvsr_dxdxp33=intangle_foravg2d(gdet*denfactor*dxdxp[3,3],**keywordsrhosq)/rhosqint
        #
        #
        if whichhortype==0:
            avgcondmaxbsqorhol=(avg_bsq/avg_rho > rinterp*25.0 + (1.0-rinterp)*5.0)
            avgcondmaxbsqorhoh=(avg_bsq/avg_rho < rinterp*35.0 + (1.0-rinterp)*15.0)
            diskcondition=avgcondmaxbsqorhol*avgcondmaxbsqorhoh
            # focus on non-jet for Gammie plot purposes
            diskcondition=(diskcondition)*(1)
            keywordsrhosq={'which': diskcondition}
            tiny=np.finfo(avg_rho.dtype).tiny
            denfactor=1.0 + avg_rho*0.0
            #denfactor=avg_rho # 1 weighting -- maybe squared would be better ala Penna, but then should change other weightings when weight by rho
            rhosqint3=intangle_foravg2d(gdet*denfactor,**keywordsrhosq)+tiny
            avgvsr_hor=intangle_foravg2d(gdet*denfactor*np.fabs(h-np.pi*0.5),**keywordsrhosq)/rhosqint3
        else:
            avgvsr_hor=choosehor + avgvsr_rho*0
        #
        # In SM or wherever: To obtain flux rather than average, just multiply by rhosqint
        for ii in np.arange(0,len(r[:,ny/2,0])):
            # columns 1-6
            avg1.write("%d %g   %g %g %g %g " % (ii, r[ii,ny/2,0], avgvsr_rho[ii],avgvsr_ug[ii],avgvsr_bsq[ii],avgvsr_unb[ii]))
            # columns 7-10
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_uu[ll,ii]))
            # columns 11-14
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_bu[ll,ii]))
            # columns 15-18
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_ud[ll,ii]))
            # columns 19-22
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_bd[ll,ii]))
            # columns 23-25
            for ll in np.arange(0,3):
                avg1.write("%g " % (avgvsr_B[ll,ii]))
            # columns 26-28
            for ll in np.arange(0,3):
                avg1.write("%g " % (avgvsr_gdetB[ll,ii]))
            # columns 29-32
            avg1.write("%g %g %g %g " % (avgvsr_omegaf2[ii],avgvsr_omegaf2b[ii],avgvsr_omegaf1[ii],avgvsr_omegaf1b[ii]))
            # columns 33-36
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_rhouu[ll,ii]))
            # columns 37-40
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_rhobu[ll,ii]))
            # columns 41-44
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_rhoud[ll,ii]))
            # columns 45-48
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_rhobd[ll,ii]))
            # columns 49-52
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_uguu[ll,ii]))
            # columns 53-56
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_ugud[ll,ii]))
            # columns 57-72
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_Tud[mm,ll,ii]))
            # columns 73-88
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_fdd[mm,ll,ii]))
            # columns 89-104
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_rhouuud[mm,ll,ii]))
            # columns 105-120
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_uguuud[mm,ll,ii]))
            # columns 121-136
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_bsquuud[mm,ll,ii]))
            # columns 137-152
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_bubd[mm,ll,ii]))
            # columns 153-168
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_uuud[mm,ll,ii]))
            # columns 169-184
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_TudEM[mm,ll,ii]))
            # columns 185-200
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_TudMA[mm,ll,ii]))
            # columns 201-216
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_TudPA[mm,ll,ii]))
            # columns 217-232
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_TudIE[mm,ll,ii]))
            # columns 233-235
            avg1.write("%g %g %g " % (avgvsr_mu[ii], avgvsr_sigma[ii], avgvsr_bsqorho[ii]))
            # columns 236-238
            for ll in np.arange(0,3):
                avg1.write("%g " % (avgvsr_absB[ll,ii]))
            # columns 239-241
            for ll in np.arange(0,3):
                avg1.write("%g " % (avgvsr_absgdetB[ll,ii]))
            # columns 242-243
            avg1.write("%g %g " % (avgvsr_psisq[ii],avgvsr_gamma[ii]))
            # other added stuff
            # columns 244 245 246 247 248 249
            avg1.write("%g %g %g %g %g %g " % (avgvsr_gdet[ii],avgvsr_dxdxp11[ii],avgvsr_dxdxp22[ii],avgvsr_dxdxp12[ii],avgvsr_dxdxp21[ii],avgvsr_dxdxp33[ii]))
            # columns 250-253
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_absuu[ll,ii]))
            # columns 254-257
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_absbu[ll,ii]))
            # columns 258-261
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_absud[ll,ii]))
            # columns 262-265
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_absbd[ll,ii]))
            # columns 266-269
            avg1.write("%g %g %g %g " % (avgvsr_absomegaf2[ii],avgvsr_absomegaf2b[ii],avgvsr_absomegaf1[ii],avgvsr_absomegaf1b[ii]))
            # columns 270-273
            for ll in np.arange(0,4):
                avg1.write("%g " % (avgvsr_absrhouu[ll,ii]))
            # columns 274-289
            for ll in np.arange(0,4):
                for mm in np.arange(0,4):
                    avg1.write("%g " % (avgvsr_absfdd[mm,ll,ii]))
            # columns 290-292
            avg1.write("%g %g %g " % (avgvsr_hor[ii],rhosqint[ii],rhosqint2[ii]))
            avg1.write("\n")
        #
        avg1.close()
        #
        #########################
        # full 2D data (so can plot, e.g., disk-wind-jet stuff in SM to compare with older papers)
        #
        avg1 = open('dataavg0.txt', 'w')
        avg1.write("#%s %s %s   %s %s\n" % ("avg_ts","avg_te","avg_nitems","rhor","ihor"))
        avg1.write("%g %g %d   %g %g %d  %g %g %g  %g  %d %d %d\n" % (avg_ts[0],avg_te[0],avg_nitems[0],a,rhor,ihor,_dx1,_dx2,_dx3,scaletofullwedge(1.0),nx,ny,nz))
        avg1.close()
        avg1 = open('dataavg1.txt', 'w')
        # below doesn't yet show columns for each component of vector or tensors
        avg1.write("#avg_rho avg_ug avg_bsq avg_unb avg_uu avg_bu avg_ud avg_bd avg_B avg_gdetB avg_omegaf2 avg_omegaf2b avg_omegaf1 avg_omegaf1b avg_rhouu avg_rhobu avg_rhoud avg_rhobd avg_uguu avg_ugud avg_Tud avg_fdd avg_rhouuud avg_uguuud avg_bsquuud avg_bubd avg_uuud avg_TudEM  avg_TudMA  avg_TudPA  avg_TudIE  avg_mu  avg_sigma  avg_bsqorho  avg_absB  avg_absgdetB  avg_psisq avg_gamma gdet dxdxp11 dxdxp22 dxdxp12 dxdxp21 dxdxp33 avg_absuu avg_absbu avg_absud avg_absbd avg_absomegaf2 avg_absomegaf2b avg_absomegaf1 avg_absomegaf1b avg_absrhouu avg_absfdd\n")
        avg1.write("#%g %g %d :  %g %d\n" % (avg_ts[0],avg_te[0],avg_nitems[0],rhor,ihor))
        for jj in np.arange(0,len(h[0,:,0])):
            for ii in np.arange(0,len(r[:,0,0])):
                # columns 1-6
                avg1.write("%d %g %g %g %g %g " % (jj, h[ii,jj,0], avg_rho[ii,jj,0],avg_ug[ii,jj,0],avg_bsq[ii,jj,0],avg_unb[ii,jj,0]))
                # columns 7-10
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_uu[ll,ii,jj,0]))
                # columns 11-14
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_bu[ll,ii,jj,0]))
                # columns 15-18
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_ud[ll,ii,jj,0]))
                # columns 19-22
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_bd[ll,ii,jj,0]))
                # columns 23-25
                for ll in np.arange(0,3):
                    avg1.write("%g " % (avg_B[ll,ii,jj,0]))
                # columns 26-28
                for ll in np.arange(0,3):
                    avg1.write("%g " % (avg_gdetB[ll,ii,jj,0]))
                # columns 29-32
                avg1.write("%g %g %g %g " % (avg_omegaf2[ii,jj,0],avg_omegaf2b[ii,jj,0],avg_omegaf1[ii,jj,0],avg_omegaf1b[ii,jj,0]))
                # columns 33-36
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_rhouu[ll,ii,jj,0]))
                # columns 37-40
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_rhobu[ll,ii,jj,0]))
                # columns 41-44
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_rhoud[ll,ii,jj,0]))
                # columns 45-48
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_rhobd[ll,ii,jj,0]))
                # columns 49-52
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_uguu[ll,ii,jj,0]))
                # columns 53-56
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_ugud[ll,ii,jj,0]))
                # columns 57-72
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_Tud[mm,ll,ii,jj,0]))
                # columns 73-88
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_fdd[mm,ll,ii,jj,0]))
                # columns 89-104
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_rhouuud[mm,ll,ii,jj,0]))
                # columns 105-120
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_uguuud[mm,ll,ii,jj,0]))
                # columns 121-136
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_bsquuud[mm,ll,ii,jj,0]))
                # columns 137-152
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_bubd[mm,ll,ii,jj,0]))
                # columns 153-168
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_uuud[mm,ll,ii,jj,0]))
                # columns 169-184
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_TudEM[mm,ll,ii,jj,0]))
                # columns 185-200
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_TudMA[mm,ll,ii,jj,0]))
                # columns 201-216
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_TudPA[mm,ll,ii,jj,0]))
                # columns 217-232
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_TudIE[mm,ll,ii,jj,0]))
                # columns 233-235
                avg1.write("%g %g %g " % (avg_mu[ii,jj,0], avg_sigma[ii,jj,0], avg_bsqorho[ii,jj,0]))
                # columns 236-238
                for ll in np.arange(0,3):
                    avg1.write("%g " % (avg_absB[ll,ii,jj,0]))
                # columns 239-241
                for ll in np.arange(0,3):
                    avg1.write("%g " % (avg_absgdetB[ll,ii,jj,0]))
                # columns 242-243
                avg1.write("%g %g " % (avg_psisq[ii,jj,0],avg_gamma[ii,jj,0]))
                # other added stuff
                # columns 244 245 246 247 248 249
                avg1.write("%g %g %g %g %g %g " % (gdet[ii,jj,0],dxdxp[1,1][ii,jj,0],dxdxp[2,2][ii,jj,0],dxdxp[1,2][ii,jj,0],dxdxp[2,1][ii,jj,0],dxdxp[3,3][ii,jj,0]))
                # columns 250-253
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_absuu[ll,ii,jj,0]))
                # columns 254-257
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_absbu[ll,ii,jj,0]))
                # columns 258-261
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_absud[ll,ii,jj,0]))
                # columns 262-265
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_absbd[ll,ii,jj,0]))
                # columns 266-269
                avg1.write("%g %g %g %g " % (avg_absomegaf2[ii,jj,0],avg_absomegaf2b[ii,jj,0],avg_absomegaf1[ii,jj,0],avg_absomegaf1b[ii,jj,0]))
                # columns 270-273
                for ll in np.arange(0,4):
                    avg1.write("%g " % (avg_absrhouu[ll,ii,jj,0]))
                # columns 274-289
                for ll in np.arange(0,4):
                    for mm in np.arange(0,4):
                        avg1.write("%g " % (avg_absfdd[mm,ll,ii,jj,0]))
                avg1.write("\n")
            # end over ii
        # end over jj
        avg1.close()
        #
    #####################
    #########################################
    if mkstreampart4==1:
        #
        #avg1.write("#avg_rho avg_ug avg_bsq avg_unb avg_uu avg_bu avg_ud avg_bd avg_B avg_gdetB avg_omegaf2 avg_omegaf2b avg_omegaf1 avg_omegaf1b avg_rhouu avg_rhobu avg_rhoud avg_rhobd avg_uguu avg_ugud avg_Tud avg_fdd avg_rhouuud avg_uguuud avg_bsquuud avg_bubd avg_uuud avg_TudEM  avg_TudMA  avg_TudPA  avg_TudIE  avg_mu  avg_sigma  avg_bsqorho  avg_absB  avg_absgdetB  avg_psisq avg_gamma gdet dxdxp11 dxdxp22 dxdxp12 dxdxp21 dxdxp33 avg_absuu avg_absbu avg_absud avg_absbd avg_absomegaf2 avg_absomegaf2b avg_absomegaf1 avg_absomegaf1b avg_absrhouu avg_absfdd")
        print("Doing field mkframe")
        sys.stdout.flush()
        global rho,ug,B,gdetB,bsq,mu,ud,uu,beta
        rho=avg_rho
        ug=avg_ug
        # use t-phi-averaged gdet B
        B[1] = avg_B[0]
        B[2] = avg_B[1]
        B[3] = avg_B[2]
        gdetB[1:] = avg_gdetB[0:]
        bsq = avg_bsq
        mu = avg_mu
        uu=avg_uu
        ud=avg_ud
        beta = avg_beta
        #
        # Sasha says this may help avoid field edge effects
        #finallen=25./30.*mylen
        #finallen=2.0*mylen
        # useblank=True causes field lines to stop tracing when they get closer together at slightly larger distances.  
        forceeqsym=0
        vminforframe=0
        vmaxforframe=0
        fntsize=16
        #
        for figiter in  np.arange(0,2):
            if figiter==0:
                fig=plt.figure(177) #,figsize=(12,9),dpi=300)
                plt.clf()
                ax = fig.add_subplot(111, aspect='equal')
                #
                finallenx=mylen
                finalleny=mylen
                mylenshowx = 25./30.*finallenx
                mylenshowy = 25./30.*finalleny
            else:
                fig=plt.figure(178) #,figsize=(12,9),dpi=300)
                plt.clf()
                ax = fig.add_subplot(111, aspect='equal')
                #
                finallenx=90
                finalleny=150
                mylenshowx = finallenx
                mylenshowy = finalleny
            #
            mkframe("myframe",dojonwindplot=1,doaphiavg=False,doaphi=False,dostreamlines=False,useblank=False,lenx=finallenx,leny=finalleny,ax=ax,density=1,downsample=4,cb=False,pt=False,dorho=False,dovarylw=False,vmin=vminforframe,vmax=vmaxforframe,dobhfield=8,dodiskfield=True,minlenbhfield=0.2,minlendiskfield=0.01,dsval=0.01,color='r',lw=2,startatmidplane=True,domidfield=False,showjet=False,arrowsize=arrowsize,forceeqsym=forceeqsym)
            #
            #
            print("Writing mkstreampart4 File: %d" % (figiter) ) ; sys.stdout.flush()
            #
            ##########################
            # finish setup of plot
            ax.set_aspect('equal')   
            rhor=1+(1-a**2)**0.5
            el = Ellipse((0,0), 2*rhor, 2*rhor, facecolor='k', alpha=1)
            art=ax.add_artist(el)
            art.set_zorder(20)
            plt.xlim(-mylenshowx,mylenshowx)
            plt.ylim(-mylenshowy,mylenshowy)
            plt.xlabel(r"$x\ [r_g]$",fontsize=fntsize,ha='center')
            plt.ylabel(r"$z\ [r_g]$",ha='left',labelpad=15,fontsize=fntsize)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(fntsize)
            #
            plt.savefig("fig4_%d.pdf" % (figiter) ,bbox_inches='tight',pad_inches=0.02,dpi=300)
            plt.savefig("fig4_%d.eps" % (figiter) ,bbox_inches='tight',pad_inches=0.02,dpi=300)
            # just convert png to eps or pdf after since otherwise too large
            plt.savefig("fig4_%d.png" % (figiter) ,bbox_inches='tight',pad_inches=0.02,dpi=300)
            print("Done Writing mkstreampart4 File: %d" % (figiter) ) ; sys.stdout.flush()
        #
    #
    #
    #
    ########################################
    # FINALPLOT:
    # ssh jmckinne@orange.slac.stanford.edu
    # cd /lustre/ki/orange/jmckinne/thickdisk7/movie8new2
    # 
    # convert fig2.png fig2.eps ; scp fig2.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/figavgflowfield.eps ; scp fig4_0.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/outflowzoom.eps; scp fig4_1.eps jon@ki-rh42:/data/jon/thickdisk/harm_thickdisk/outflowlarge.eps
    # whichrun="thickdisk7" ; scp datavsravg1.txt dataavgvsr0.txt dataavgvsh1.txt dataavgvsh0.txt dataavgvsr1.txt dataavg0.txt dataavg1.txt jmckinne@ki-jmck:/data2/jmckinne/$whichrun/fromorange_movie8new2/

def mklotsopanels(epsFm=None,epsFke=None,fti=None,ftf=None,domakeframes=True,prefactor=100):
    global modelname
    if len(sys.argv[1:])>0:
        modelname = sys.argv[1]
    else:
        modelname = "Unknown Model"
    #
    #############################################
    #Figure 1
    #To make plot, run 
    #run ~/py/mread/__init__.py 1 1
    #To re-make plot without reloading the fiels, run
    #run ~/py/mread/__init__.py 1 -1
    doslines=True
    plotlenf=10
    plotleni=25
    plen=plotleni
    plotlenti=40000
    plotlentf=45000
    bbox_props = dict(boxstyle="round,pad=0.1", fc="w", ec="w", alpha=0.9)
    #AT: plt.legend( loc = 'upper left', bbox_to_anchor = (0.5, 0.5) ) #0.5, 0.5 = center of plot
    #To generate movies for all sub-folders of a folder:
    #cd ~/Research/runart; for f in *; do cd ~/Research/runart/$f; (python  ~/py/mread/__init__.py &> python.out &); done
    #############################################
    print("ModelName = %s" % (modelname) )
    if len(sys.argv[1:])==3 and sys.argv[2].isdigit() and (sys.argv[3].isdigit() or sys.argv[3][0]=="-") :
        whichi = int(sys.argv[2])
        whichn = int(sys.argv[3])
        print( "Doing every %d slice of total %d slices" % (whichi, whichn) )
        sys.stdout.flush()
    else:
        whichi = None
        whichn = None
    if whichn < 0 and whichn is not None:
        whichn = -whichn
        dontloadfiles = True
    else:
        dontloadfiles = False
        grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]), use2d=True )
        #rd( "dump0000.bin" )
        rfdheaderfirstfile()
        rfdfirstfile()
        global maxrho
        maxrho=np.max(rho)
        print("maxrho=%g" % (maxrho))
        #
        #grid3dlight("gdump")
        qtymem=None #clear to free mem
        rhor=1+(1+a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        qtymem=getqtyvstime(ihor,0.2)
        #flist = np.sort(glob.glob( os.path.join("dumps/", "fieldline*.bin") ) )
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
    #make accretion rate plot, etc.
    sys.stdout.flush()
    plotlen = plotleni+(plotlenf-plotleni)*(t-plotlenti)/(plotlentf-plotlenti)
    plotlen = min(plotlen,plotleni)
    plotlen = max(plotlen,plotlenf)
    fig=plt.figure(0, figsize=(12,9), dpi=100)
    plt.clf()
    #findexlist=(0,600,1285,1459)
    #findexlist=(0,600,1225,1369)
    findexlist=(0,600,1225,3297)
    #SWITCH OFF SUPTITLE
    #plt.suptitle(r'$\log_{10}\rho$ at t = %4.0f' % t)
    #mdot,pjet,pjet/mdot plots
    findex = 0
    gs3 = GridSpec(3, 3)
    gs3.update(left=0.055, right=0.97, top=0.42, bottom=0.06, wspace=0.01, hspace=0.04)
    #mdot
    ax31 = plt.subplot(gs3[-3,:])
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax31,whichplot=1,findex=findexlist,epsFm=epsFm,epsFke=epsFke,fti=fti,ftf=ftf,prefactor=prefactor) #AT: need to specify index!
    ymax=ax31.get_ylim()[1]
    ymax=2*(np.floor(np.floor(ymax+1.5)/2))
    ax31.set_yticks((0,ymax,ymax/2.0))
    #ax31.set_xlabel(r"$t\ [r_g/c]")
    ax31.grid(True)
    plt.text(ax31.get_xlim()[1]/40., 0.8*ax31.get_ylim()[1], "$(\mathrm{e})$", size=16, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    ax31r = ax31.twinx()
    ax31r.set_ylim(ax31.get_ylim())
    ax31r.set_yticks((0,ymax,ymax/2.0))
    #pjet
    # ax32 = plt.subplot(gs3[-2,:])
    # plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax32,whichplot=2)
    # ymax=ax32.get_ylim()[1]
    # ax32.set_yticks((ymax/2.0,ymax))
    # ax32.grid(True)
    #pjet/mdot
    # ax33 = plt.subplot(gs3[-1,:])
    # plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax33,whichplot=3)
    # ymax=ax33.get_ylim()[1]
    # ax33.set_yticks((ymax/2.0,ymax))
    # ax33.grid(True)
    #
    #\phi
    #

    # plt.text(250, 0.9*ymax, "i", size=10, rotation=0.,
    #          ha="center", va="center",
    #          bbox = dict(boxstyle="square",
    #                      ec=(1., 0.5, 0.5),
    #                      fc=(1., 0.8, 0.8),
    #                      )
    #          )
    ax35 = plt.subplot(gs3[-2,:])
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax35,whichplot=5,findex=findexlist,epsFm=epsFm,epsFke=epsFke,fti=fti,ftf=ftf,prefactor=prefactor)
    ymax=ax35.get_ylim()[1]
    #if 1 < ymax and ymax < 2: 
    #    #ymax = 2
    #    tck=(1,)
    #    ax35.set_yticks(tck)
    #    #ax35.set_yticklabels(('','1','2'))
    #elif ymax < 1: 
    #    #ymax = 1
    #    tck=(ymax/10,ymax)
    #    ax35.set_yticks(tck)
    #    ax35.set_yticklabels(('','1'))
    if ymax >=1:
        ymax=np.floor(ymax*0.9999)+1
        tck=np.arange(1,ymax,(ymax-1.0)/2.0)
        ax35.set_yticks(tck)
    else:
        ax35.set_yticks((ymax/2.0,ymax))
        #ax35.set_ylim((0,ymax))
    #
    ax35.grid(True)
    plt.text(ax35.get_xlim()[1]/40., 0.8*ax35.get_ylim()[1], r"$(\mathrm{f})$", size=16, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    ax35r = ax35.twinx()
    ax35r.set_ylim(ax35.get_ylim())
    ax35r.set_yticks(tck)
    #
    #pjet/<mdot>
    #
    ax34 = plt.subplot(gs3[-1,:])
    plotqtyvstime(qtymem,fullresultsoutput=0,ax=ax34,whichplot=4,findex=findexlist,epsFm=epsFm,epsFke=epsFke,fti=fti,ftf=ftf,prefactor=prefactor)
    ax34.set_ylim((0,3.8))
    ymax=ax34.get_ylim()[1]
# JON next 7 lines
#    if ymax >=100:
#        ymax=np.floor(ymax/100.*0.9999)+1
#        ymax*=100
#        tck=np.arange(1,ymax/100.,(ymax/100.0-1.0)/2.0)*100
#    else:
#        ax34.set_yticks((ymax/2.0,ymax))
#        #ax34.set_ylim((0,ymax))
    #
    if prefactor < ymax and ymax < 2*prefactor: 
        #ymax = 2
        tck=(prefactor,)
        ax34.set_yticks(tck)
        #ax34.set_yticklabels(('','100','200'))
    elif ymax < prefactor: 
        ymax = prefactor
        tck=(0.5*prefactor,prefactor)
        ax34.set_yticks(tck)
        ax34.set_yticklabels(('','%d' % prefactor))
    else:
        ymax=np.floor(ymax/prefactor)+1
        ymax*=prefactor
        tck=np.arange(1,ymax/prefactor)*prefactor
        ax34.set_yticks(tck)
    ax34.set_ylim((0,ax34.get_ylim()[1]))
    ax34.grid(True)
    #reset lower limit to 0
    plt.text(ax34.get_xlim()[1]/40., 0.8*ax34.get_ylim()[1], r"$(\mathrm{g})$", size=16, rotation=0.,
             ha="center", va="center",
             color='k',weight='regular',bbox=bbox_props
             )
    ax34r = ax34.twinx()
    ax34r.set_ylim(ax34.get_ylim())
    ax34r.set_yticks(tck)
    #
    if domakeframes:
        #
        # Make Frames
        #
        dogrid = False
        downsample=4
        density=2
        dodiskfield=True
        minlenbhfield=0.2
        minlendiskfield=0.2
        #
        # PLOT 1
        #
        fname = "fieldline%04d.bin" % findexlist[0]
        rfd(fname)
        cvel() #for calculating bsq
        #xz
        gs1 = GridSpec(4, 4)
        gs1.update(left=0.04, right=0.94, top=0.995, bottom=0.48, wspace=0.05)
        #
        ax1 = plt.subplot(gs1[2:4, 0])
        # plt.text(-0.75*plen, 0.75*plen, r"$(\mathrm{a})$", size=16, rotation=0.,
        #          ha="center", va="center",
        #          color='k',weight='regular',bbox=bbox_props
        #          )
        mkframe("lrho%04d_Rz%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax1,cb=False,pt=False,dostreamlines=doslines,downsample=downsample,density=density,dodiskfield=False)
        ax1.set_ylabel(r'$z\ [r_g]$',fontsize=16,ha='center')
        ax1.set_xlabel(r'$x\ [r_g]$',fontsize=16)
        if dogrid: plt.grid()
        #xy
        ax2 = plt.subplot(gs1[0:2, 0])
        mkframexy("lrho%04d_xy%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax2,cb=False,pt=False,dostreamlines=False,doaphi=True)
        plt.setp( ax2.get_xticklabels(), visible=False)
        plt.text(-0.75*plen, 0.8*plen, r"$(\mathrm{a})$", size=16, rotation=0.,
                 ha="center", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        plt.text(0.9*plen, 0.8*plen, r"$t=%g$" % np.floor(t), size=16, rotation=0.,
                 ha="right", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        ax2.set_ylabel(r'$y\ [r_g]$',fontsize=16,ha='center')
        if dogrid: plt.grid()
        plt.subplots_adjust(hspace=0.03) #increase vertical spacing to avoid crowding
        #
        # PLOT 2
        #
        fname = "fieldline%04d.bin" % findexlist[1]
        rfd(fname)
        cvel() #for calculating bsq
        #Rz
        #gs1 = GridSpec(4, 4)
        #
        ax1 = plt.subplot(gs1[2:4, 1])
        # plt.text(-0.75*plen, 0.75*plen, r"$(\mathrm{c})$", size=16, rotation=0.,
        #          ha="center", va="center",
        #          color='k',weight='regular',bbox=bbox_props
        #          )
        mkframe("lrho%04d_Rz%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,
                ax=ax1,cb=False,pt=False,dostreamlines=doslines,downsample=downsample,
                density=density,dodiskfield=dodiskfield,minlendiskfield=minlendiskfield,minlenbhfield=minlenbhfield)
        ax1.set_xlabel(r'$x\ [r_g]$',fontsize=16)
        if dogrid: plt.grid()
        #xy
        ax2 = plt.subplot(gs1[0:2, 1])
        plt.text(-0.75*plen, 0.8*plen, r"$(\mathrm{b})$", size=16, rotation=0.,
                 ha="center", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        mkframexy("lrho%04d_xy%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax2,cb=False,pt=False,dostreamlines=False,doaphi=True)
        plt.setp( ax2.get_xticklabels(), visible=False)
        plt.text(0.9*plen, 0.8*plen, r"$t=%g$" % np.floor(t), size=16, rotation=0.,
                 ha="right", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        if dogrid: plt.grid()
        plt.subplots_adjust(hspace=0.03) #increase vertical spacing to avoid crowding
        #
        # PLOT 3
        #
        fname = "fieldline%04d.bin" % findexlist[2]
        rfd(fname)
        cvel() #for calculating bsq
        #Rz
        ax1 = plt.subplot(gs1[2:4, 2])
        # plt.text(-0.75*plen, 0.75*plen, r"$(\mathrm{e})$", size=16, rotation=0.,
        #          ha="center", va="center",
        #          color='k',weight='regular',bbox=bbox_props
        #          )
        mkframe("lrho%04d_Rz%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax1,cb=False,pt=False,dostreamlines=doslines,downsample=downsample,density=density,dodiskfield=dodiskfield,minlendiskfield=minlendiskfield,minlenbhfield=minlenbhfield)
        ax1.set_xlabel(r'$x\ [r_g]$',fontsize=16)
        if dogrid: plt.grid()
        #xy
        ax2 = plt.subplot(gs1[0:2, 2])
        plt.text(-0.75*plen, 0.8*plen, r"$(\mathrm{c})$", size=16, rotation=0.,
                 ha="center", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        plt.text(0.9*plen, 0.8*plen, r"$t=%g$" % np.floor(t), size=16, rotation=0.,
                 ha="right", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        mkframexy("lrho%04d_xy%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax2,cb=False,pt=False,dostreamlines=False,doaphi=True)
        plt.setp( ax2.get_xticklabels(), visible=False)
        if dogrid: plt.grid()
        plt.subplots_adjust(hspace=0.03) #increase vertical spacing to avoid crowding
        #
        # PLOT 4
        #
        fname = "fieldline%04d.bin" % findexlist[3]
        rfd(fname)
        cvel() #for calculating bsq
        #Rz
        ax1 = plt.subplot(gs1[2:4, 3])
        # plt.text(-0.75*plen, 0.75*plen, r"$(\mathrm{g})$", size=16, rotation=0.,
        #          ha="center", va="center",
        #          color='k',weight='regular',bbox=bbox_props
        #          )
        mkframe("lrho%04d_Rz%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax1,cb=False,pt=False,dostreamlines=doslines,downsample=downsample,density=density,dodiskfield=dodiskfield,minlendiskfield=minlendiskfield,minlenbhfield=minlenbhfield)
        ax1.set_xlabel(r'$x\ [r_g]$',fontsize=16)
        if dogrid: plt.grid()
        #xy
        ax2 = plt.subplot(gs1[0:2, 3])
        plt.text(-0.75*plen, 0.8*plen, r"$(\mathrm{d})$", size=16, rotation=0.,
                 ha="center", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        plt.text(0.9*plen, 0.8*plen, r"$t=%g$" % np.floor(t), size=16, rotation=0.,
                 ha="right", va="center",
                 color='w',weight='regular' #,bbox=bbox_props
                 )
        mkframexy("lrho%04d_xy%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax2,cb=False,pt=False,dostreamlines=False,doaphi=True)
        plt.setp( ax2.get_xticklabels(), visible=False)
        if dogrid: plt.grid()
        #
        plt.subplots_adjust(hspace=0.03) #increase vertical spacing to avoid crowding
        #
        #(left=0.02, right=0.94, top=0.99, bottom=0.45, wspace=0.05)
        ax1 = fig.add_axes([0.94, 0.48, 0.02, 0.515])
        #
        # Set the colormap and norm to correspond to the data for which
        # the colorbar will be used.
        cmap = mpl.cm.jet
        norm = mpl.colors.Normalize(vmin=-6, vmax=0.5625)
        # ColorbarBase derives from ScalarMappable and puts a colorbar
        # in a specified axes, so it has everything needed for a
        # standalone colorbar.  There are many more kwargs, but the
        # following gives a basic continuous colorbar with ticks
        # and labels.
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                           norm=norm,
                                           orientation='vertical')
        #
        #
        plt.savefig( "fig1.png" )
        plt.savefig( "fig1.eps" )
    #
    print( "Done mklotsopanels!" )
    sys.stdout.flush()

def generate_time_series():
    #
    global modelname
    global makepowervsmplots
    makepowervsmplots=0
    global makespacetimeplots
    makespacetimeplots=0
    global makefftplot
    makefftplot=0
    global makespecplot
    makespecplot=0
    global makeinitfinalplot
    makeinitfinalplot=0
    global makethradfinalplot
    makethradfinalplot=0
    #
    if len(sys.argv[1:])>0:
        modelname = sys.argv[1]
    else:
        modelname = "Unknown Model"
    #
    print("ModelName = %s" % (modelname) ) ; sys.stdout.flush()
    #
    ###################################
    global avoidplotsglobal
    avoidplotsglobal=0
    #cd ~/run; for f in rtf*; do cd ~/run/$f; (nice -n 10 python  ~/py/mread/__init__.py &> python.out); done
    grid3d("gdump.bin",use2d=True)
    #rd("dump0000.bin")
    rfdfirstfile()
    global maxrho
    maxrho=np.max(rho)
    print("maxrho=%g" % (maxrho))
    #
    #
    rhor=1+(1-a**2)**0.5
    ihor = np.floor(iofr(rhor)+0.5)
    #diskflux=diskfluxcalc(ny/2)
    #qtymem=None #clear to free mem
    #
    ###################################
    if len(sys.argv[1:])==3 and sys.argv[2].isdigit() and sys.argv[3].isdigit():
        whichi = int(sys.argv[2])
        whichn = int(sys.argv[3])
        if whichi >= whichn:
            mergeqtyvstime(whichn)
        else:
            qtymem=getqtyvstime(ihor,0.2,whichi=whichi,whichn=whichn)
    else:
        # assume here if "plot" as second argument
        if len(sys.argv[1:])==4+4 and sys.argv[3].isdigit() and sys.argv[4].isdigit() and sys.argv[5].isdigit() and sys.argv[6].isdigit() and sys.argv[7].isdigit() and sys.argv[8].isdigit():
            makepowervsmplots = int(sys.argv[3])
            makespacetimeplots = int(sys.argv[4])
            makefftplot = int(sys.argv[5])
            makespecplot = int(sys.argv[6])
            makeinitfinalplot = int(sys.argv[7])
            makethradfinalplot = int(sys.argv[8])
            print("Got plot args: %d %d %d %d %d %d" % (makepowervsmplots,makespacetimeplots,makefftplot,makespecplot,makeinitfinalplot,makethradfinalplot))
            #
        qtymem=getqtyvstime(ihor,0.2)
        plotqtyvstime(qtymem,fullresultsoutput=1)
        #
    #
    #

def oldstuff():
    if False:
        #cd into the directory that contains the dumps/ directory
        #read in the grid file
        grid3d("gdump.bin")
        #plot log10(radius) vs. grid index, ti
        #plt.plot( ti[:,0,0], np.log10(r[:,0,0]) )
        plt.figure( 1, figsize=(6,12) )
        plt.clf()
        small=1e-5
        #theta grid lines through cell centers
        levs = np.linspace(0,nx-1-small,nx)
        plc(ti,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=levs,colors='#0fffff')
        levs = np.linspace(0,ny-1-small,ny)
        plc(tj,xcoord=r*np.sin(h),ycoord=r*np.cos(h),levels=levs,colors='#0fffff')
        levs = np.linspace(0,nx-small,nx+1)
        plc(tif,xcoord=rf*np.sin(hf),ycoord=rf*np.cos(hf),levels=levs,colors='k')
        #radial grid lines through cell centers
        levs = np.linspace(0,ny-small,ny+1)
        plc(tjf,xcoord=rf*np.sin(hf),ycoord=rf*np.cos(hf),levels=levs,colors='k')
        plt.xlim(0,2)
        plt.ylim(-2,2)
        plt.savefig("grid.png")
        #
        #Read in the dump file and plot it
        #
        #read in the 1000th dump file
        plt.figure( 2, figsize=(6,12) )
        plt.clf()
        rfd("fieldline1000.bin")
        #plot contours of density
        plc(lrho,xcoord=r*np.sin(h),ycoord=r*np.cos(h),cb=True,nc=50)
        plt.xlim(0,2)
        plt.ylim(-2,2)
        plt.savefig("logdensity.png")
    if False:
        grid3d("gdump.bin"); 
        rfdfirstfile()
        aphi = fieldcalcface()
        sig=intangle(gdet*rho)
        plt.clf()
        plt.plot(r[:,0,0],-gdetB[2,:,ny/2,0]/dxdxp[1,1,:,ny/2,0]/dxdxp[3,3,0,0,0]/sig) 
        plt.xlim(0,200)
        plt.ylim(0,2)
    if False:
        #grid3d("gdump")
        #rfd("fieldline0250.bin")
        #cvel()
        #plc(rho)
        grid3d("gdump.bin")
        rfdfirstfile()
        diskflux=diskfluxcalc(ny/2)
        ts,fs,md=fhorvstime(11)
        plotit(ts,fs/(diskflux),md)
    if False:
        #cd ~/run; for f in rtf*; do cd ~/run/$f; (nice -n 10 python  ~/py/mread/__init__.py &> python.out); done
        grid3d("gdump.bin")
        rfdfirstfile()
        diskflux=diskfluxcalc(ny/2)
        ts,fs,md,jem,jtot=mfjhorvstime(11)
        plotj(ts,fs/(diskflux),md,jem,jtot)
    if False:
        rfd("fieldline2344.bin")
        cvel()
        Tcalcud()
        xxx=-Tud[1,0]/(rho*uu[1])
        yyy=choplo(chophi(xxx.sum(2)/nz,50),-50)[:,:,None]
        plco(yyy,cb=True,nc=20)
        aphi=fieldcalcface()
        plc(aphi,nc=30)

    if False:
        #OLD FORMAT
        #Plot qtys vs. time
        #cd ~/run; for f in rtf*; do cd ~/run/$f; (nice -n 10 python  ~/py/mread/__init__.py &> python.out); done
        grid3d("gdump.bin")
        rfdfirstfile()
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        #diskflux=diskfluxcalc(ny/2)
        qtymem=None #clear to free mem, doesn't seem to work
        qtymem=getqtyvstime(ihor,0.2,fmtver=1)
        plotqtyvstime(qtymem,fullresultsoutput=0)
    if False:
        rfd("fieldline0320.bin")
        plt.figure(1)
        aphi=fieldcalc()
        plc(aphi)
        plt.figure(2)
        aphi2=fieldcalc2()
        plc(aphi2)
        test()
    if False:
        grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]) )
        #flist = np.sort(glob.glob( os.path.join("dumps/", "fieldline*.bin") ))
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
        for findex, fname in enumerate(flist):
            print( "Reading " + fname + " ..." )
            rfd("../"+fname)
            plt.clf()
            mkframe("lrho%04d" % findex, vmin=-8,vmax=0.2)
        print( "Done!" )
    if False:
        grid3d("gdump.bin")
        rfdfirstfile()
        rhor=1+(1+a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        hf=horfluxcalc(ivalue=ihor)
        df=diskfluxcalc(ny/2)
        print "Initial (t=%-8g): BHflux = %g, Diskflux = %g" % (t, hf, df)
        rfd("fieldline1308.bin")
        hf=horfluxcalc(ivalue=ihor)
        df=diskfluxcalc(ny/2,rmin=rhor)
        print "Final   (t=%-8g): BHflux = %g, Diskflux = %g" % (t, hf, df)
    if False:
        global modelname
        if len(sys.argv[1:])>0:
            modelname = sys.argv[1]
        else:
            modelname = "UnknownModel"
        #
        print("ModelName = %s" % (modelname) )
        if len(sys.argv[1:])==3 and sys.argv[2].isdigit() and (sys.argv[3].isdigit() or sys.argv[3][0]=="-") :
            whichi = int(sys.argv[2])
            whichn = int(sys.argv[3])
            sys.stdout.flush()
        if whichn < 0 and whichn is not None:
            whichn = -whichn
            dontloadfiles = True
        else:
            dontloadfiles = False
            grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]), use2d=True )
            rd( "dump0000.bin" )
            qtymem=None #clear to free mem
            rhor=1+(1+a**2)**0.5
            ihor = np.floor(iofr(rhor)+0.5)
            qtymem=getqtyvstime(ihor,0.2)
            #flist = np.sort(glob.glob( os.path.join("dumps/", "fieldline*.bin") ) )
            flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
            sort_nicely(flist) 
        fname=flist[whichi]
        print( "Processing " + fname + " ..." )
        sys.stdout.flush()
        rfd("../"+fname)
        cvel() #for calculating bsq
        plt.figure(0, figsize=(12,9), dpi=100)
        plt.clf()
        mkframe("lrho%04d_Rz%g" % (findex,plotlen), vmin=-6.,vmax=0.5625,len=plotlen,ax=ax1,cb=False,pt=False)
    if False:
        len=10
        #To generate movies for all sub-folders of a folder:
        #cd ~/Research/runart; for f in *; do cd ~/Research/runart/$f; (python  ~/py/mread/__init__.py &> python.out &); done
        grid3d( os.path.basename(glob.glob(os.path.join("dumps/", "gdump*"))[0]) )
        #rfd("fieldline0000.bin")  #to define _dx#
        #grid3dlight("gdump")
        #flist = np.sort(glob.glob( os.path.join("dumps/", "fieldline0000.bin") ) )
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
        firstfieldlinefile=flist[0]
        flist=[firstfieldlinefile]
        #
        for findex, fname in enumerate(flist):
            if os.path.isfile("lrho%04d_xy%g.png" % (findex,len)):
                print( "Skipping " + fname + " as lrho%04d_xy%g.png exists" % (findex,len) );
            else:
                print( "Processing " + fname + " ..." )
                rfd("../"+fname)
                plt.clf()
                mkframexy("lrho%04d_xy%g" % (findex,len), vmin=-8,vmax=1.5,len=len)
        print( "Done!" )
        #print( "Now you can make a movie by running:" )
        #print( "ffmpeg -fflags +genpts -r 10 -i lrho%04d.png -vcodec mpeg4 -qmax 5 mov.avi" )
        os.system("mv mov_%s_xy%g.avi mov_%s_xy%g.bak.avi" % ( os.path.basename(os.getcwd()), len, os.path.basename(os.getcwd()), len) )
        os.system("ffmpeg -fflags +genpts -r 10 -i lrho%%04d_xy%g.png -vcodec mpeg4 -qmax 5 mov_%s_xy%g.avi" % (len, os.path.basename(os.getcwd()), len) )
        #os.system("scp mov.avi 128.112.70.76:Research/movies/mov_`basename \`pwd\``.avi")

    #plt.clf(); rfd("fieldline0000.bin"); aphi=fieldcalc(); plc(ug/bsq) 
    #rfd("fieldline0002.bin")
    if False:
        grid3d( "gdump.bin" )
        rfdfirstfile()
        plt.clf();
        mkframe("lrho%04d" % 0, vmin=-8,vmax=0.2)
    if False:
        grid3d("gdump");
        rfdfirstfile()
        reresrdump("rdump--0000");
        plt.clf(); cvel(); plc(bsq,cb=True)
        plt.clf();plt.plot(x1[:,ny/2,0],(bsq/(2*(gam-1)*ug))[:,ny/2,0])
        plt.plot(x1[:,ny/2,0],(bsq/(2*(gam-1)*ug))[:,ny/2,0],'+')
        plt.plot(x1[:,ny/2,0],(0.01*rho)[:,ny/2,0])
    if False:
        plt.clf();plco(lrho,r*np.sin(h),r*np.cos(h),cb=True,levels=np.arange(-12,0,0.5)); plt.xlim(0,40); plt.ylim(-20,20)
    if False:
        rd( os.path.basename(glob.glob(os.path.join("dumps/", "dump0000*"))[0]) )
        #reresrdump("rdump--0000")
        aphi = fieldcalc()
        plt.clf(); plt.plot(x1[:,ny/2,0],aphi[:,ny/2,0])
    if False:
        gen_vpot()
    if False:
        #Generates 6 co-aligned half-loops which combine into one big loop.
        #However, the field is noisy and probably the total flux in the big
        #loop is smaller than max possible given max ibeta.
        npow=4
        ap=np.zeros((6,rho.shape[0],rho.shape[1],rho.shape[2]))
        ap1=np.zeros((6,rho.shape[0],rho.shape[1],rho.shape[2]))
        #gives nearly uniform aphi at maxes
        #c=np.array([10,1.5,1,1,2.7,16])
        #gives uniform bsq/rho**gam at maxes
        c=np.array([3.5,2,1,2,3,10])
        phases=np.array([0,0.5,1,1.5,2,2.5])
        for i,phase in enumerate(phases):
            ap[i]=c[i]*gen_vpot(whichloop=0,phase=phase)
            ap1[i]=gen_vpot(whichloop=0,phase=phase)
        aaphi = np.sum(ap,axis=0)
        aaphi1 = np.sum(ap1,axis=0)
        aaphi2 = aaphi1 * fac(phi)
        plt.clf()
        if True:
            plt.plot(x1[:,ny/2,0],((ap[0]))[:,ny/2,0])
            plt.plot(x1[:,ny/2,0],((ap[1]))[:,ny/2,0])
            plt.plot(x1[:,ny/2,0],((ap[2]))[:,ny/2,0])
            plt.plot(x1[:,ny/2,0],((ap[3]))[:,ny/2,0])
            plt.plot(x1[:,ny/2,0],((ap[4]))[:,ny/2,0])
            plt.plot(x1[:,ny/2,0],((ap[5]))[:,ny/2,0])
            plt.plot(x1[:,ny/2,0],((aaphi))[:,ny/2,0])
        aphi2B(aaphi2)
        cvel()
        res=Qmri()
        #plt.plot(x1[:,ny/2,0],(res)[:,ny/2,0])
        #plt.clf();pl(x1,res)
        #plt.clf();pl(x1,aaphi)
        #plco(bsq/rho**gam,cb=True)
        #plco(res,cb=True)
        #pl(ti,10*fac(phi)); plt.ylim(0,ny-1)
        #pl(x1,res)
        #pl(x1,aaphi2)
        pl(x1,aaphi1)
    if False:
        flist = glob.glob( os.path.join("dumps/", "fieldline*.bin") )
        sort_nicely(flist)
        firstfieldlinefile=flist[0]
        rgfd(firstfieldlinefile)
        if False:
            #generate your favorite vector potential
            aaphi=gen_vpot(whichfield=None)
            #compute the field from that potential
            aphi2B(aaphi)
            B[2] = 1*B[2]
            cvel()
            #generate smoothing function
            profile = ((uqcomax-0.05)/0.1)
            profile[profile>1] = 1
            profile[profile<0] = 0
            #set target beta and desired bsqoug
            beta = 100.
            constbsqoug = 2*(gam-1)/beta
            #smooth bsqoug
            targbsqoug = constbsqoug*profile
            rat = ( targbsqoug*divideavoidinf(bsq/ug) )**0.5
            cvel()
        #rescale the field
        if False:
            B[1] *= rat
            B[2] *= rat
            #cvel()
            aphim=fieldcalcm()
            aphip=fieldcalcp()
            #aphi0 = avg0c2f(aphim)
            aphi2B(aphim)
            cvel()
        if False:
            rat2 = avg2ctof( rat )
            rat1 = avg1ctof( rat )
            gdetB[1] *= rat1
            gdetB[2] *= rat2
        if False:
            rat2 = avg2ctof( rat )
            rat1 = avg1ctof( rat )
            gdetB[1] *= rat1
            gdetB[2] *= rat2
            if False:
            #unsuccessful try to chop off the field spike in the middle of the loop
                minB1 = np.min(gdetB[1]/gdet)/1.5
                maxB1 = np.max(gdetB[1]/gdet)/1.5
                #gdetB1old=np.copy(gdetB[1])
                (gdetB[1])[gdetB[1]<gdet*minB1] = (minB1*gdet)[gdetB[1]<gdet*minB1]
                (gdetB[1])[gdetB[1]>gdet*maxB1] = (maxB1*gdet)[gdetB[1]>gdet*maxB1]
            #gdetB1new=np.copy(gdetB[1])
        if False:
            #at this point divb!=0, i.e. there are monopoles
            #to remove monopoles, compute vector potential
            aphi = fieldcalcface()
            #and compute the field from the potential
            #(this leaves B[1] the same and resets B[2]
            aphi2B(aphi)
        if False:
            cvel()
            normalize_field(constbsqoug)
            cvel()
        print("Disk flux = %g (@r<20: %g)" % (diskfluxcalc(ny/2), diskfluxcalc(ny/2,rmax=20)) )
    if False:
        #pf()
        grid3d("gdump.bin")
        rd("dump0000.bin")
        cvel()
        plco(np.log10(rho))
        plc(bsq/rho**gam)
        print("Disk flux = %g (@r<20: %g)" % (diskfluxcalc(ny/2,rmax=Rout), diskfluxcalc(ny/2,rmax=20)) )
        rh = 1+(1-a**2)**0.5
        print "r[5]/rh = %g\n" % (r[5,0,0]/rh) + "r[10]/rh = %g\n" % (r[10,0,0]/rh)
        res = Qmri()
        res[res>20] = 20+0*res[res>20]
        plc(res,cb=True)
        #plt.plot(x1[:,ny/2,0],(res)[:,ny/2,0])
        #plt.clf();pl(x1,res)
        #plt.clf();pl(x1,aaphi)
        #plco(bsq/rho**gam,cb=True)
        #plco(res,cb=True)
    if False:
        rin=15;
        R=r*np.sin(h);z=r*np.cos(h);
        alpha=1.5;t=0.9;aphi=(R/rin)**2/(1+(np.abs(z)/t/rin/(1+np.log10(1+r/rin)**2))**alpha)**(2/alpha); aphi[aphi>1]=0*aphi[aphi>1]+1; plco(np.log10(rho));plc(aphi)
    if False:
        grid3d("gdump.bin")
        rd("dump0040.bin")
        aphi=fieldcalcface()
        plco(np.log10(rho))
        plc(aphi,nc=50)
    if False:
        grid3d("gdump.bin")
        rfd("fieldline0222.bin")
        cvel()
        Tcalcud()
        jetpowcalc(whichbsqorho=0)[11]
        mdotcalc(11)
    if False:
        cvel()
        #entk=((gam-1)*ug/rho**gam);entk[entk>1]=0*entk[entk>1]+1;
        #plt.clf();
        #plt.figure();
        #pl(r,np.log10(entk));plt.xlim(1,20);plt.ylim(-3,-0.5)
    if False:
        #VRPLOT
        #grid3d("gdump.bin",use2d=True)
        #rd("dump0000.bin")
        #rfd("fieldline0000.bin")
        rhor=1+(1-a**2)**0.5
        ihor = np.floor(iofr(rhor)+0.5)
        #diskflux=diskfluxcalc(ny/2)
        #qtymem=None #clear to free mem
        #qtymem=getqtyvstime(ihor,0.2)
        plt.figure(1)
        plotqtyvstime(qtymem,fullresultsoutput=0,whichplot=-3)
        #plt.figure(2)
        #plotqtyvstime(qtymem,fullresultsoutput=0,whichplot=-4)





if __name__ == "__main__":
    # defaults:
    global avoidplotsglobal
    avoidplotsglobal=1
    #
    #
    if False:
        readmytests1()
        plotpowers('powerlist.txt',format=0) #old format
    if False:
        #Figure 3
        readmytests1()
        plotpowers('powerlist2davg.txt',format=1) #new format; data from 2d average dumps
    if False:
        #2DAVG
        mk2davg()
    if False:
        #NEW FORMAT
        #Plot qtys vs. time
        generate_time_series()
    if False:
        #make a movie
        mkmovie()
    if False:
        #fig2 with grayscalestreamlines and red field lines
        mkavgfigs()
    if False:
        #FIGURE 1 LOTSOPANELS
        fti=7000
        ftf=1e6
        epsFm, epsFke = takeoutfloors(doreload=1,fti=fti,ftf=ftf,returndf=1,isinteractive=0)
        #epsFm = 
        #epsFke = 
        print epsFm, epsFke
        mklotsopanels(epsFm=epsFm,epsFke=epsFke,fti=fti,ftf=ftf,domakeframes=True,prefactor=1)
    if False:
        grid3d( "gdump.bin",use2d=True )
        fno=0
        rfd("fieldline%04d.bin" % fno)
        plt.clf();
        mkframe("lrho%04d" % 0, vmin=-8,vmax=0.2,dostreamlines=False,len=50,doaphi=True)
        plt.savefig("lrho%04d.pdf" % fno)
    if False:
        #Short tutorial. Some of the names will sound familiar :)
        print( "Running a short tutorial: read in grid, 0th dump, plot and compute some things." )
        #1 read in gdump (specifying "use2d=True" reads in just one r-theta slice to save memory)
        grid3d("gdump.bin", use2d = True)
        #2 read in dump0000
        doreaddump = 0
        if doreaddump:
            rd("dump0000.bin")
        #   or, instead of dump, you could read in fieldline0000.bin
        rfdfirstfile()
        #3 compute extra things
        docomputeextrathings = False
        if docomputeextrathings:
            cvel()
            Tcalcud()
            faraday()
        #4 compute vector potential
        aphi = fieldcalc()
        #5 plot density and overplotted vector potential
        plt.figure(1)  #open figure 1
        plco(lrho,cb=True,nc=50) #plco -- erases and plots; cb=True tells it to draw color bar, nc = number of contours
        plc(aphi,colors='k') #plc -- overplots without erasing; colors='k' says plot in blac'k'
        #5a compute same in x-z coordinates
        fig = plt.figure(2)  #open figure 2
        ax = fig.add_subplot(111, aspect='equal')
        plco(lrho,cb=True,nc=50,xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plc(aphi,nc=100,colors='k',xcoord=r*np.sin(h),ycoord=r*np.cos(h))
        plt.xlim(0,50)
        plt.ylim(-25,25)
        ax.set_aspect('equal')   
        #6 compute u^\phi
        uuphi = uu[3] * dxdxp[3,3]
        #7 compute u_\phi
        #  first, lower the index
        ud_computed = mdot(gv3,uu)  #<-- this is already computed as 'ud' inside of cvel() call
        #  then, take 3rd component and convert to phi from x3
        udphi = (ud_computed/dxdxp[3,3])[3]
        #8 phi-average density
        rhophiavg = rho.mean(axis=-1)  #-1 says to average over the last dimension
        #9 clean up some memory
        ud_computed = None
        uuphi = None
        udphi = None
        aphi = None
        gc.collect()










