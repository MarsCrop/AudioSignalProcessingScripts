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
import numpy as np
from smst.utils import audio, math
from essentia.standard import *

fs, data = audio.read_wav("/pathtosound.wav")

envelope = Envelope()

signal_envelope = envelope(data)

at = LogAttackTime()

attack_time = 10**(at(signal_envelope))

dboftrack = math.to_db_magnitudes(data)

attack_samples = dboftrack[:attack_time*fs]

# amplify attack without clipping the signal with a difference of 1 for output gain decrease
def amplify_attack(boost = float, output_gain_decrease = float):
     attack_db_level = dboftrack >= max(attack_samples)
     dboftrack[attack_db_level] += boost
     return (dboftrack - output_gain_decrease)

output = (10**(amplify_attack(boost = 0.6, output_gain_decrease = 1.6)*0.5))+data    
    
audio.write_wav(output,fs,"/pathtosound.wav")

