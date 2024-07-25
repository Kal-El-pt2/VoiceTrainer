import pyaudio
import wave
import keyboard
import threading

class Recorder:
    def __init__(self):
        self._recording = False
        self._stop_event = threading.Event()

    def _listen_for_stop(self):
        while not self._stop_event.is_set():
            if keyboard.is_pressed('s'):
                self._stop_event.set()
                print("Stopping recording...")

    def start_recording(self):
        self._recording = True
        self._stop_event.clear()
        stop_thread = threading.Thread(target=self._listen_for_stop)
        stop_thread.start()

        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        try:
            while not self._stop_event.is_set():
                data = stream.read(1024)
                frames.append(data)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

        output_file = "myrecording.wav"
        with wave.open(output_file, "wb") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))

        print(output_file)  # Print only the filename

if __name__ == "__main__":
    try:
        print("Recording started. Press 's' to stop.")  # Moved outside the recording function to separate concerns
        recorder = Recorder()
        recorder.start_recording()
    except KeyboardInterrupt:
        print("\nRecording stopped manually.")
