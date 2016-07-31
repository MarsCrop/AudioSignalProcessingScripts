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
import os
from scipy import signal
from scipy.fftpack import ifft, fftshift
import math
from smst.models import dft, sine
from smst.utils import peaks, synth

def sine_multi(x, fs, ws, Ns, Bs, H, t, 
                            minSineDur=0.02, maxnSines=150, freqDevOffset=10, freqDevSlope=0.001):
    hsN = H/2
    pend = x.size
    pin = max([hsN] + [int(math.floor((w.size+1)/2)) for w in ws])
    x = np.append(np.zeros(pin),x)
    x = np.append(x,np.zeros(pin))

    def limit_tracks(tr):
        # limit number of tracks to maxnSines
        return np.resize(tr, min(maxnSines, tr.size))

    def pad_tracks(tr):
        tr_padded = np.zeros(maxnSines)
        tr_padded[:tfreq.size] = tr
        return tr_padded
    
    def dftAnal(p, w, N, B):
        hM1, hM2 = dft.half_window_sizes(w.size)
        x1 = x[p-hM1:p+hM2]
        fftbuffer = np.zeros(N)
        rw = w / sum(w)
        mX, pX = dft.from_audio(x1, rw, N)
        
        upperIndex = Bs.index(B)
        lower_bin = 1
        if upperIndex > 0:
            lower_bin = int(np.ceil(float(Bs[upperIndex-1]) * N / fs))
        upper_bin = int(np.ceil(float(B) * N / fs))
        
        ploc = peaks.find_peaks(mX, t)
        ploc = ploc[np.logical_and(ploc>lower_bin, ploc<=upper_bin)]
        iploc, ipmag, ipphase = peaks.interpolate_peaks(mX, pX, ploc)
        ipfreq = fs*iploc/float(N)

        return (ipfreq, ipmag, ipphase)

    tfreq = np.array([])
    # xtfreq, xtmag, xtphase
    xt = ([], [], [])

    while pin <= pend:
        #-----analysis-----
        pfs = np.array([])
        pms = np.array([])
        pps = np.array([])

        for i, w in enumerate(ws):
            pf, pm, pp = dftAnal(pin, w, Ns[i], Bs[i])
            pfs = np.concatenate((pfs, pf))
            pms = np.concatenate((pms, pm))
            pps = np.concatenate((pps, pp))
        
        track_frame = sine.track_sinusoids(pfs, pms, pps, tfreq, freqDevOffset, freqDevSlope)
        track_frame = [limit_tracks(tr_comp) for tr_comp in track_frame]
        tfreq = track_frame[0]

        for tr_comp, tracks in zip(track_frame, xt):
            tracks.append(pad_tracks(tr_comp))

    	xtfreq, xtmag, xtphase = [np.vstack(xt_comp) for xt_comp in xt]

        
        pin += H
        
    xtfreq = sine.clean_sinusoid_tracks(xtfreq, round(fs*minSineDur/H))  
    return xtfreq, xtmag, xtphase

def to_audio(tfreq, tmag, tphase, N, H, fs):
    """
    Synthesizes a sound using the sinusoidal model.

    :param tfreq: frequencies of sinusoids
    :param tmag: magnitudes of sinusoids
    :param tphase: phases of sinusoids
    :param N: synthesis FFT size
    :param H: hop size
    :param fs: sampling rate
    :returns: y: output array sound
    """

    hN = N / 2  # half of FFT size for synthesis
    L = tfreq.shape[0]  # number of frames
    pout = 0  # initialize output sound pointer
    ysize = H * (L + 3)  # output sound size
    y = np.zeros(ysize)  # initialize output array

    sw = sine.create_synth_window(N, H)

    lastytfreq = tfreq[0, :]  # initialize synthesis frequencies
    ytphase = 2 * np.pi * np.random.rand(tfreq.shape[1])  # initialize synthesis phases
    for l in range(L):  # iterate over all frames
        if tphase.size > 0:  # if no phases generate them
            ytphase = tphase[l, :]
        else:
            ytphase += (np.pi * (lastytfreq + tfreq[l, :]) / fs) * H  # propagate phases
        Y = synth.spectrum_for_sinusoids_py(tfreq[l, :], tmag[l, :], ytphase, N, fs)  # generate sines in the spectrum
        lastytfreq = tfreq[l, :]  # save frequency for phase propagation
        ytphase %= 2 * np.pi  # make phase inside 2*pi
        yw = np.real(fftshift(ifft(Y)))  # compute inverse FFT
        y[pout:pout + N] += sw * yw  # overlap-add and apply a synthesis window
        pout += H  # advance sound pointer
    y = np.delete(y, range(hN))  # delete half of first window
    y = np.delete(y, range(y.size - hN, y.size))  # delete half of the last window
    return y
