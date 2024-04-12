import librosa
import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy import signal

# file_name = 'sounds/snare1.wav'

# plt.figure(figsize=(10, 10))
# plt.gca().set_axis_off()
# plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
# plt.margins(0, 0)

# y, sr = librosa.load(f'{file_name}', mono=True)

# nfft = 2048
# ps = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=1, n_mels=nfft // 4, win_length=nfft // 2)
# librosa.display.specshow(librosa.power_to_db(ps, ref=np.max), x_axis='s', y_axis='mel', cmap='CMRmap')

# coefficient, frequency = pywt.cwt(y, np.arange(1, 500), 'gaus1', sampling_period=sr)
# coefficient = np.abs(coefficient[:-1, :-1])

# cwtmatr = signal.cwt(y[:2500], signal.ricker, np.arange(1, 200))
# cwtmatr_yflip = np.flipud(cwtmatr)
# plt.imshow(cwtmatr_yflip, cmap='CMRmap', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

# plt.savefig(f'images/{file_name[7:-4]}.png')
# plt.show()

import os

for subdir, dirs, files in os.walk('sounds'):
    for file in files:
        file_name = os.path.join(subdir, file)
        print(f'Computing {file_name}... ', end='')

        plt.figure(figsize=(10, 10))
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

        y, sr = librosa.load(file_name, mono=True)

        nfft = 2048
        p = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=1, n_mels=nfft // 4, win_length=nfft // 2)
        librosa.display.specshow(librosa.power_to_db(p, ref=np.max), x_axis='s', y_axis='mel', cmap='binary_r')

        plt.savefig(f'images/{file[:-4]}.png')
        plt.close()

        plt.figure(figsize=(10, 10))
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

        cwtmatr = signal.cwt(y[:2500], signal.ricker, np.arange(1, 200))
        cwtmatr_yflip = np.flipud(cwtmatr)
        plt.imshow(cwtmatr_yflip, cmap='binary_r', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

        plt.savefig(f'images/{file[:-4]}_cwt.png')
        plt.close()

        print('Done.')
