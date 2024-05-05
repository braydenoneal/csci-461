import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import librosa

FRAMES_PER_BUFFER = 1024 * 2
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000

device = pyaudio.PyAudio()

input('Press enter: ')

stream = device.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

seconds = 1
frames = []

for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

print('Done recording.')

stream.stop_stream()
stream.close()
device.terminate()

obj = wave.open('record.wav', 'wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(device.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b''.join(frames))
obj.close()

file = wave.open('record.wav', 'rb')

sample_freq = file.getframerate()
frames = file.getnframes()
signal_wave = file.readframes(-1)

file.close()

audio_array = np.frombuffer(signal_wave, dtype=np.float32)

plt.figure(figsize=(1, 1))
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

nfft = 2048
p = librosa.feature.melspectrogram(y=audio_array, sr=RATE, n_fft=nfft, hop_length=1, n_mels=nfft // 4,
                                   win_length=nfft // 2)
librosa.display.specshow(librosa.power_to_db(p, ref=np.max), x_axis='s', y_axis='mel', cmap='binary_r')

plt.savefig(f'record.png')
plt.close()
