import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename, config):
    duration = config["asr"]["duration"]
    sample_rate = config["asr"]["sample_rate"]
    channels = config["asr"]["channels"]

    print(f"🎤 {duration} सेकंड के लिए रिकॉर्ड हो रहा है...")

    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
        sd.wait()
        write(filename, sample_rate, audio)
        print("✅ रिकॉर्डिंग पूरी हो गई।\n")
    except Exception as e:
        print(f"[❌] रिकॉर्डिंग में त्रुटि: {e}")

