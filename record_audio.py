import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename, config):
    fs = config['audio']['sample_rate']
    duration = config['audio']['duration']

    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Check for silence
    max_volume = np.max(np.abs(recording))
    print(f"DEBUG - Max volume: {max_volume}")
    if max_volume < 500:
        print("⚠️ Warning: Very low or no audio detected! Please speak louder or check your mic.")

    write(filename, fs, recording)
    print(f"Recording saved as {filename}")
