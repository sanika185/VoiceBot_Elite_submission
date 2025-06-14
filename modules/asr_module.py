import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename, config):
    fs = config['audio']['sample_rate']
    duration = config['audio']['duration']

    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print(f"Recording saved as {filename}")

