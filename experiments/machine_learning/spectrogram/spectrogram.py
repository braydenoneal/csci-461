import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import os

for subdir, dirs, files in os.walk('sounds'):
    for file in files:
        if file[-4:] == '.wav':
            file_name = os.path.join(subdir, file)
            print(f'Computing {file}... ', end='')

            plt.figure(figsize=(1, 1))
            plt.gca().set_axis_off()
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)

            y, sr = librosa.load(file_name, mono=True)

            nfft = 2048
            p = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=1, n_mels=nfft // 4,
                                               win_length=nfft // 2)
            librosa.display.specshow(librosa.power_to_db(p, ref=np.max), x_axis='s', y_axis='mel', cmap='binary_r')

            plt.savefig(f'images/{file_name[7:-4]}.png')
            plt.close()

            plt.figure(figsize=(1, 1))
            plt.gca().set_axis_off()
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)

            cwtmatr = signal.cwt(y[:2500], signal.ricker, np.arange(1, 200))
            cwtmatr_yflip = np.flipud(cwtmatr)
            plt.imshow(cwtmatr_yflip, cmap='binary_r', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

            plt.savefig(f'images_cwt/{file_name[7:-4]}.png')
            plt.close()

            print('Done.')
