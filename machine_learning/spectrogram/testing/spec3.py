import matplotlib.pyplot as plt
import pywt
from scipy import signal
from scipy.io import wavfile
import numpy as np
import librosa


def plot_wavelet(time, signal, scales,
                 waveletname='mexh',
                 cmap='CMRmap',
                 title='Continuous Wavelet Transform',
                 ylabel='Frequency',
                 xlabel='Time'):
    dt = time[1] - time[0]
    [coefficients, frequencies] = pywt.cwt(signal, scales, waveletname, dt)
    power = (abs(coefficients)) ** 2
    period = 1. / frequencies
    levels = [0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]
    contourlevels = np.log2(levels)

    # plt.figure(figsize=(8, 8))
    # plt.gca().set_axis_off()
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # plt.margins(0, 0)
    # plt.contourf(time, np.log2(period), np.log2(power), contourlevels, extend='both', cmap=cmap)

    fig, ax = plt.subplots(figsize=(10, 10))
    # period = np.flipud(period)
    # power = np.flipud(power)
    ax.set_yscale('log')
    ax.contourf(time, np.log2(period), np.log2(power), 256, extend='both', cmap=cmap)

    ax.set_title(title, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_xlabel(xlabel, fontsize=18)

    plt.show()


file_name = 'sounds/snare/Acoustic Snare 01.wav'
y, sr = librosa.load(file_name, mono=True)

plot_wavelet(np.arange(0, len(y)), y, np.arange(0.5, 256))
