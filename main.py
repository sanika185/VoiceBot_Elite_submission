import yaml
import whisper
from gtts import gTTS
from playsound import playsound
import os
import time

from modules.asr_module import record_audio
from modules.nlp_pipeline import categorize_query
from modules.response_gen import generate_response

# Load Whisper model
print("📢 Whisper मॉडल लोड हो रहा है...")
whisper_model = whisper.load_model("small")
print("✅ Whisper मॉडल लोड हो गया\n")

def load_config():
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[❌] config.yaml लोड करने में त्रुटि: {e}")
        return {}

def transcribe_audio(filename):
    try:
        result = whisper_model.transcribe(filename, language="hi", fp16=False)
        return result["text"].strip()
    except Exception as e:
        print(f"[❌] ट्रांसक्रिप्शन विफल: {e}")
        return ""

def speak(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")
    except Exception as e:
        print(f"[❌] बोलने में त्रुटि: {e}")

def main():
    config = load_config()
    if not config:
        return

    print("🤖 VoiceBot शुरू हो गया है। 'धन्यवाद' या 'thank you' कहकर बंद करें।\n")
    speak("नमस्ते! मैं Peer to Peer Lending VoiceBot हूँ। आप मुझसे पैसे उधार देने या लेने से जुड़े सवाल पूछ सकते हैं।")

    try:
        while True:
            print("\n🎙️ रिकॉर्डिंग शुरू...\n")
            record_audio("input.wav", config)

            print("📝 ट्रांसक्रिप्शन चल रहा है...\n")
            user_text = transcribe_audio("input.wav")

            if not user_text:
                reply = "माफ़ कीजिए, कुछ सुनाई नहीं दिया। कृपया दोबारा कहें।"
            elif "धन्यवाद" in user_text.lower() or "thank" in user_text.lower() or "stop" in user_text.lower():
                reply = "आपका दिन शुभ हो! धन्यवाद।"
                print("🤖 बॉट:", reply)
                speak(reply)
                break
            else:
                print("🙋‍♀️ यूज़र ने कहा:", user_text)
                intent = categorize_query(user_text)
                reply = generate_response(intent)

            print("🤖 बॉट:", reply)
            speak(reply)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 मैन्युअली बंद किया गया। धन्यवाद!")

if __name__ == "__main__":
    main()
