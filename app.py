import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display

def plot_spectrograms(audio_file_1, audio_file_2):
    y1, sr1 = librosa.load(audio_file_1)
    y1_trimmed, _ = librosa.effects.trim(y1, top_db=40)

    y2, sr2 = librosa.load(audio_file_2)
    y2_trimmed, _ = librosa.effects.trim(y2, top_db=40)

    D1 = librosa.stft(y1_trimmed)
    D2 = librosa.stft(y2_trimmed)

    db_D1 = librosa.amplitude_to_db(np.abs(D1), ref=np.max)
    db_D2 = librosa.amplitude_to_db(np.abs(D2), ref=np.max)

    plt.figure(figsize=(14, 8))

    plt.subplot(2, 1, 1)
    librosa.display.specshow(db_D1, sr=sr1, x_axis='time', y_axis='log', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Power Spectrogram of First Audio File')

    plt.subplot(2, 1, 2)
    librosa.display.specshow(db_D2, sr=sr2, x_axis='time', y_axis='log', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Power Spectrogram of Second Audio File')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        plot_spectrograms(sys.argv[1], sys.argv[2])
    else:
        print("Please provide two audio file paths as arguments.")
