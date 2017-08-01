"""  This program is free software: you can redistribute it and/or modify
    	it under the terms of the GNU General Public License as published by
    	the Free Software Foundation, either version 3 of the License, or
    	(at your option) any later version.
    	This program is distributed in the hope that it will be useful,
    	but WITHOUT ANY WARRANTY; without even the implied warranty of
    	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    	GNU General Public License for more details.
    	You should have received a copy of the GNU General Public License
    	along with this program.  If not, see <http://www.gnu.org/licenses/>. """

from soundfile import read
from scipy.signal import lfilter
import numpy as np
from apicultor.sonification.Sonification import write_file, normalize
from apicultor.utils.algorithms import mono_stereo, sonify
from apicultor.utils.dj import source_separation #the point is that this works with many speakers
from functools import reduce
import operator
import sys, os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def delay(audio, delay_N): 
    y = np.zeros(audio.size)    
    for i in range(y.size):
        if (i < delay_N):
            y[i] = audio[i]
        elif (i >= delay_N and i < audio.size):
            y[i] = audio[i] + audio[i - delay_N]
        else:
            y[i] = audio[i-delay_N]
    return y

def lagrange_interpolation(prefilter, xyz):
    ps = []
    for j in range(len(xyz[0])):
        p = []
        for m in range(len(xyz[0])):
            if m != j:
                p.append((prefilter - xyz[0][m])/(xyz[0][j] - xyz[0][m]))
        basis = reduce(operator.mul, p)
        ps.append(basis * xyz[1][j])
    return sum(ps)

def renormalize(_tmp):                                                          
    if _tmp == round(float(str(_tmp)), 308): #find out if the number is denormal
        _tmp = 0                                 
    return _tmp                                  
def filterABEqualSize(x,y,a,b,state):            
    for n in range(y.size):                      
        y[n] = b[0]*x[n] + state[0]
        updateStateLineUnrolled(state,a,b,x[n],y[n])              
    return y                                     
def updateStateLine(state,size,a,b,x,y):         
    for k in range(size):                        
        state[k-1] = (b[k]*x - a[k]*y) + state[k]
        renormalize(state[k-1])                
        return state    
def updateStateLineUnrolled(state,a,b,x,y):
    for k in range(len(n)):
        state[k-1] = b[k]*x - a[k]*y + state[k]
    for k in range(len(n)):
        state[k-1] = renormalize(state[k-1])
    return state
def IIR(b,a,x): #the iir filter is a translation of C++ version of Essentia 2.1-dev
    y = np.zeros(x.size)
    if type(a) != list:                  
        a = np.array([a])
    else:
        a = np.array(a)
    b = np.array(b)
    wanted_size = max(len(b), len(a))
    state = np.zeros(wanted_size)
    try:
        a /= a[0]
    except TypeError:
        a = a / a[0]
    b /= a[0]
    a[0] = 1.
    if len(b) == len(a):
        size = len(a)
        if size in range(2,17):
            filterABEqualSize(x,y,a,b, state)
        else:
            for n in range(len(y)):
                updateStateLine(state, state.size, a, b, x[n], y[n])
    elif b.size > a.size:
        for n in range(len(y)):
            y[n] = b[0] * x[n] + state[0]
            updateStateLine(state, len(a), a, b, x[n], y[n])
        for k in range(state.size):
            state[k-1] = b[k] * x[n] + state[k]
            renormalize(state[k-1])
    else:
        for i in range(len(y)):
            y[n] = b[0] * x[n] + state[0]
            for k in range(state.size):
                state[k-1] = (-a[k] * y[n]) + state[k]
                renormalize(state[k-1])
    return y

Usage = "python3 wfs.py soundfilename outputfilename"
def main():                                  
    if not len(sys.argv) == 3:                                        
        raise Exception(("Invalid ammount of input arguments", Usage))      
    try:
        prefilter, fs = read(#use a prefilter file)
                                                                            
        audio, fs = read(sys.argv[1]) #both audio and prefilter should have same fs

        audio = mono_stereo(audio)
                                            
        filtering = IIR(prefilter, 1, audio)
        filtering = normalize(filtering)

        xyz = [[0,1.5,3,6],[6,6,0,6]]  #by the moment these are the default configurations (thinking about 4 sources)

        interpolation = lagrange_interpolation(prefilter, xyz) #by know its only 2D, this script will run with a 3D field

        audio = delay(audio, 128)

        output = IIR(interpolation, 1, audio)
        output = normalize(output)

        write_file(sys.argv[2], fs, output)
    except Exception as e:
        logger.exception(e)
        exit(1) 

if __name__ == '__main__':                                  
    main()
