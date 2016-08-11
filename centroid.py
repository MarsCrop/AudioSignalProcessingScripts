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
from smst.utils import audio
from scipy.fftpack import *
from pyo import *

fs, x = audio.read_wav("/pathtosound.wav") #audio should be mono

def spectral_centroid(x, samplerate=fs):
    magnitudes = np.abs(fft(x)) # magnitudes of positive frequencies
    length = len(x)
    freqs = np.abs(fftfreq(length, 1.0/samplerate))
    return np.mean((magnitudes*freqs) / magnitudes) # return mean

freq = int(spectral_centroid(x,fs))

s = Server(audio="jack").boot()

eq = EQ(SfPlayer("/pathtosound.wav"), freq = freq, boost = 6).out()
s.gui(locals())
