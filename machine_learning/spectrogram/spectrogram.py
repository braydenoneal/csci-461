import librosa
import matplotlib.pyplot as plt
import numpy as np

file_name = 'snare1.wav'

plt.figure(figsize=(2, 2))
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

y, sr = librosa.load(f'{file_name}', duration=4, mono=True)

nfft = 2048
ps = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=1, n_mels=nfft // 4, win_length=nfft // 2)

librosa.display.specshow(librosa.power_to_db(ps, ref=np.max), x_axis='s', y_axis='mel')
# plt.savefig(f'{file_name[:-4]}.png')
plt.show()
