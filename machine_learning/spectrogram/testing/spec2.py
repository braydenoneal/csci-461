import matplotlib.pyplot as plt
# import pywt
from scipy import signal
from scipy.io import wavfile
import numpy as np
import librosa

file_name = 'snare1.wav'

plt.figure(figsize=(8, 8))
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

plt.figure(figsize=(8, 8))

sample_rate, samples = wavfile.read(f'{file_name}')
frequencies, times, spectrogram = signal.spectrogram(samples[:, 0], sample_rate, nperseg=64, nfft=4096)

plt.pcolormesh(times, frequencies, np.log(spectrogram), cmap='CMRmap')
plt.yscale('linear')
#
# y, sr = librosa.load(file_name, mono=True)
# print(y)
# nfft = 2048
# p = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=1, n_mels=nfft // 4, win_length=nfft // 2)
# librosa.display.specshow(librosa.power_to_db(p, ref=np.max), x_axis='s', y_axis='mel', cmap='CMRmap')

# y, sr = librosa.load(file_name, mono=True)
# print(y)
# cwtmatr = signal.cwt(y[:2500], signal.ricker, np.arange(1, 200))
# cwtmatr_yflip = np.flipud(cwtmatr)
# plt.imshow(cwtmatr_yflip, cmap='CMRmap', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

# y, sr = librosa.load(file_name, mono=True)
# coef, freqs = pywt.cwt(y, np.arange(1, 512, 2), 'gaus1')
# plt.matshow(coef)

# cwtmatr, freqs = pywt.cwt(y[:10_000], np.arange(1, 128), 'mexh')
# plt.imshow(cwtmatr, cmap='CMRmap', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

# plt.savefig(f'cwt_example.png')
plt.show()
