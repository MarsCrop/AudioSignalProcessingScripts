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

from essentia.standard import *
from smst.utils import audio

fs, x = audio.read_wav("/pathtosound.wav")

iir = IIR()
eq_loud = EqualLoudness()

signal_filtered = iir(x)
equal_loudness = eq_loud(signal_filtered)

audio.write_wav(equal_loudness,fs,"/pathtosound.wav")
