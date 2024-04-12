import librosa
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np

file_name = 'snare1.wav'

sample_rate, samples = wavfile.read(f'{file_name}')
frequencies, times, spectrogram = signal.spectrogram(samples[:, 0], sample_rate, nperseg=64, nfft=4096)
# new_samples = np.pad(samples[:32_000, 0], (0, 32_000 - len(samples[:32_000, 0])), 'constant')
# frequencies, times, spectrogram = signal.spectrogram(new_samples, sample_rate, nperseg=256)

plt.figure(figsize=(12, 12))
# plt.set_cmap('binary_r')
# ps, ff, time, ima = plt.specgram(samples[:, 0], Fs=sample_rate, NFFT=4096, noverlap=0)
# plt.pcolormesh(times, frequencies, np.log(spectrogram), shading='flat')
# plt.pcolormesh(times, frequencies, np.log(spectrogram))
# plt.yscale('symlog')
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)
# plt.savefig(f'{file_name[:-4]}.png')
# plt.show()

y, sr = librosa.load('snare1.wav', duration=4)

# X = librosa.stft(y)
# Xdb = librosa.amplitude_to_db(abs(X))
# librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')

# ps = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=512, hop_length=1)
nfft = 2048
ps = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=1, n_mels=nfft // 4, win_length=nfft // 2)
ps_db = librosa.power_to_db(ps, ref=np.max)
librosa.display.specshow(ps_db, x_axis='s', y_axis='mel')

# plt.imshow(ps_db)
plt.show()
