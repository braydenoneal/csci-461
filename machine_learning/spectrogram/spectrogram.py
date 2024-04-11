import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np

file_name = 'snare1.wav'

sample_rate, samples = wavfile.read(f'{file_name}')
frequencies, times, spectrogram = signal.spectrogram(samples[:, 0], sample_rate, nperseg=64, nfft=4096)
# new_samples = np.pad(samples[:32_000, 0], (0, 32_000 - len(samples[:32_000, 0])), 'constant')
# frequencies, times, spectrogram = signal.spectrogram(new_samples, sample_rate, nperseg=256)

plt.figure(figsize=(8, 8))
# plt.pcolormesh(times, frequencies, np.log(spectrogram), cmap='CMRmap')
plt.pcolormesh(times, frequencies, np.log(spectrogram), cmap='binary_r')
plt.yscale('linear')
# plt.gca().set_axis_off()
# plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
# plt.margins(0, 0)
# plt.savefig(f'{file_name[:-4]}.png')
plt.show()
