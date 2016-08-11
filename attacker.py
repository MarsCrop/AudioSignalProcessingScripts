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

from scipy.fftpack import *
import math
import numpy as np
from smst.utils import audio

#TODO: debug distortion

fs, data = audio.read_wav("/pathtosound.wav")

time = (len(data)/fs)

at = math.exp(-1/(time*fs))

print at

seconds = np.array_split(data,time/at)

def rms(array):
    for i in array:
        rms = lambda: np.sqrt(np.mean(np.square(np.abs(fft(array)))))
        return rms()
        break

def dB(rms):
        dB = 10 * np.log10(np.abs(rms(array=seconds[0])/seconds[0]))
        return np.max(dB[dB<120])
        
dBofrms = dB(rms)
        
def dBoftrack():
    for i in seconds[:]: 
        dBoftrack = 20 * np.log10(np.abs(data))
        return dBoftrack

dBoftrack = dBoftrack()

def amplifyAttack():
     a1 = dBoftrack <= dBofrms
     dBoftrack[a1] *= 6
     return np.int16(dBoftrack)

output = amplifyAttack()+data    
    
audio.write_wav(output,fs,"/pathtosound.wav")
