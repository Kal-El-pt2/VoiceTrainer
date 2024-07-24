import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import IPython.display as ipd

# Load the first audio file
audio_file_1 = 'C:/Users/arivw/PycharmProjects/HelloWorld/pythonProject/BR.wav'
y1, sr1 = librosa.load(audio_file_1)
y1_trimmed, _ = librosa.effects.trim(y1, top_db=40)

# Load the second audio file
audio_file_2 = 'C:/Users/arivw/PycharmProjects/HelloWorld/pythonProject/BR.wav'  # Update with the correct path
y2, sr2 = librosa.load(audio_file_2)
y2_trimmed, _ = librosa.effects.trim(y2, top_db=40)

# Compute the STFT of both audio files
D1 = librosa.stft(y1_trimmed)
D2 = librosa.stft(y2_trimmed)

# Convert to decibel scale
db_D1 = librosa.amplitude_to_db(np.abs(D1), ref=np.max)
db_D2 = librosa.amplitude_to_db(np.abs(D2), ref=np.max)

# Plot the spectrograms
plt.figure(figsize=(14, 8))

# Spectrogram of the first audio file
plt.subplot(2, 1, 1)
librosa.display.specshow(db_D1, sr=sr1, x_axis='time', y_axis='log', cmap='magma')
plt.colorbar(format='%+2.0f dB')
plt.title('Power Spectrogram of First Audio File')

# Spectrogram of the second audio file
plt.subplot(2, 1, 2)
librosa.display.specshow(db_D2, sr=sr2, x_axis='time', y_axis='log', cmap='magma')
plt.colorbar(format='%+2.0f dB')
plt.title('Power Spectrogram of Second Audio File')

plt.tight_layout()
plt.show()
