import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

# Load the Whisper model (medium recommended for Hindi-English)
model = whisper.load_model("medium")

import sounddevice as sd
import scipy.io.wavfile as wav

def record_audio(filename, duration=5, fs=44100):
    print("🎤 बोलिए... (Speak now)")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        print("✅ रिकॉर्डिंग पूरी हो गई।")
        wav.write(filename, fs, recording)
    except Exception as e:
        print(f"[❌] रिकॉर्डिंग में त्रुटि: {e}")


def transcribe_audio():
    audio_path = record_audio()
    if not audio_path:
        return ""

    try:
        result = model.transcribe(audio_path, language="hi")  # You can use 'auto' for auto-detection
        os.remove(audio_path)  # Clean up temp file
        return result.get("text", "").strip()
    except Exception as e:
        print(f"[❌] ट्रांसक्रिप्शन में त्रुटि: {e}")
        return ""
