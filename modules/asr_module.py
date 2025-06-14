import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename, config):
    fs = config['audio']['sample_rate']
    duration = config['audio']['duration']

    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    # ✅ Normalize audio to prevent low volume issues
    recording = np.int16(recording / np.max(np.abs(recording)) * 32767)

    write(filename, fs, recording)
    print(f"Recording saved as {filename}")


