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

from pyo import *
import math

class WFS():

    s = Server(audio='jack').boot()

    SIZE = 4095 #zero-padding

    theta = math.pi/2
     
    r = 1.75

    sinfo = sndinfo("/pathtosound.wav")
    
    sf = SfPlayer("/pathtosound.wav")

    mm = NewMatrix(SIZE, sinfo[0]/SIZE) #start creating the virtual source 
    fft = FFT(sf)
    alphasin = Sin(fft["imag"])
    omega = 2 * math.pi * alphasin
    alphacos = Cos(fft["imag"])
    betasin = Sin(fft["imag"], mul = 1./theta)
    x = r*alphasin*alphacos
    y = r*alphasin*betasin
    betacos = Cos(fft["imag"], mul = 1./theta)
    z = r*betacos #set some values for the pretty cool axis of the matrix
    c = MatrixPointer(mm, x, y, z,omega).out() #getting ready to point sources

    fieldreproduction = CvlVerb(sf, "/pathtoimpulse.wav",size=SIZE,bal=c,mul=1+PeakAmp(c)).out() #convolution with a wfs prefilter that works within the terms of the matrix

    sp = Scope([fieldreproduction])

    s.gui(locals())
