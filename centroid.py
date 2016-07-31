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

import numpy as np
from scipy.io.wavfile import read
from scipy.fftpack import *

fs, x = read("/pathtosound.wav") #audio should be mono

def spectral_centroid(x, samplerate=fs):
    magnitudes = np.abs(fft(x)) # magnitudes of positive frequencies
    length = len(x)
    freqs = np.abs(fftfreq(length, 1.0/samplerate))
    return (magnitudes*freqs) / magnitudes # return mean

print np.mean(spectral_centroid(x,fs))
