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
from sine_multi import sine_multi, to_audio
from scipy.io.wavfile import read, write
from scipy import signal
from scipy.fftpack import ifft, fftshift
from smst.utils import math
from smst.models import sine
from smst.utils import audio
from essentia.standard import *


fs, x = audio.read_wav('/pathtosound.wav') 

Bs = [30,50,60,80,120,200,400,500,1000,2000,4000,6000,15600,16800,17000,18600,19800,22000]

Ns = [128,128,4096,4096,4096,4096,4096,4096,4096,4096,4096,2048,4096,4096,4096,4096,4096,4096]

ws = [signal.hamming(55),signal.hamming(55),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),signal.hamming(2047),np.hamming(257),np.hamming(257),np.hamming(127),np.hamming(57),np.hamming(55),np.hamming(53)]


def attack_and_release_time(signal):
	envelope = Envelope()

	signal_envelope = envelope(signal)

	at = LogAttackTime()

	attack_time = 10**(at(signal_envelope))
	release_time = (attack_time*10) #get some acceptable release time
	return attack_time, release_time

at, rel = attack_and_release_time(x)
 
bands = sine_multi(x=x, fs=fs, ws=ws[:11],Ns=Ns[:11],t=-78,Bs=Bs[:11],H=1024,minSineDur=.016, maxnSines=150, freqDevOffset=np.max(x)*0.0005, freqDevSlope=0.005)                                                    

freq = bands[0]
mag = bands[1]
phase = bands[2]

dB = 20 * np.log10(np.abs(mag/(np.sqrt(2))))
tlevel = 6
threshold = np.max(dB)-tlevel       
ratio = float(5/1) #ratio for decibels higher than the threshold, please consider that denominator is ratio expressed as a number, which means if you want to set the ratio to 3:1 or 3:2 ratio will be equal to 3/1 or 3/2
atcoef = -np.log(9)/(fs*at)
relcoef = -np.log(9)/(fs*rel)         
compute_gain = threshold+((dB[dB>threshold]-threshold)/ratio)
gain_modif=compute_gain-dB[dB>threshold]
smooth1 = (gain_modif*atcoef)+(threshold*(1-gain_modif))
dB[dB>threshold] = (gain_modif*relcoef)+(threshold*(1-relcoef))
dB[dB>threshold] = dB[dB>threshold]+(-(compute_gain*0.0005))

tmag = math.from_db_magnitudes(dB)

y = to_audio(tfreq=freq, tmag=-tmag, tphase=phase, N=4096, H=1024, fs=fs)

#filter

from scipy.signal import remez                 
lpf = remez(125, [50, 1000, 2000-250, 0.5*fs],[1, 0], Hz=fs)
from scipy.signal import freqz
w, h = freqz(lpf)
y = signal.lfilter(lpf, 1, y) 

#normalize
def normalize(level=int):
	maximum = np.max(np.abs(y)) / level
	return np.true_divide(y,maximum)
	
output = normalize(level=-1)

audio.write_wav(output,fs,'/pathtosound.wav')

