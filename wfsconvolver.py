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

def delay(audio, N, delay_N):  
    y_N = N + delay_N
    y = np.zeros(y_N)    
    for i in range(y.size):
        if (i < delay_N):
            y[i] = audio[i]
        elif (i >= delay_N and i < N):
            y[i] = audio[i] + audio[i - delay_N]
        else:
            y[i] = audio[i-delay_N]
    return y

prefilter, fs = read(prefilter_filename) 

audio, fs = read(filename) #both audio and prefilter should have same fs

filtering = lfilter(prefilter, 1, audio)

output = delay(result, audio.size, 1024)
