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
import numpy as np
from scipy.io.wavfile import read
import math

fs, data = read("/pathtosound.wav")

def dB(data=data):
    for i in data:
        return 20*np.log10(np.abs(np.max((np.fft.rfft(data[:2048])))))
    
print dB()

def dBlevel(dB=dB):
        return float(-120 + dB())

s = Server(audio="jack").boot()

a = SfPlayer("/pathtosound.wav")
gt = Gate(a, thresh=dBlevel()).mix(2).out()
    
s.gui(locals())
