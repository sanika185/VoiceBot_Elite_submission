import sounddevice as sd
from scipy.io.wavfile import write
import noisereduce as nr
import numpy as np

def record_audio(config):
    fs = config['audio']['sample_rate']
    duration = config['audio']['duration']
    filename = config['audio']['filename']

    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Flatten and reduce noise
    recording = recording.flatten()
    reduced_noise = nr.reduce_noise(y=recording, sr=fs)

    write(filename, fs, reduced_noise.astype(np.int16))
    print(f"Recording saved as {filename}")
    return filename
