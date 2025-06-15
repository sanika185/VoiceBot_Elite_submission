import yaml
import whisper
from gtts import gTTS
from playsound import playsound
import os
import time
from deep_translator import GoogleTranslator
from difflib import get_close_matches

from modules.asr_module import record_audio
from modules.nlp_pipeline import categorize_query
from modules.response_gen import generate_response

# Load Whisper model
print("📢 Whisper मॉडल लोड हो रहा है...")
model = whisper.load_model("medium")
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
        result = model.transcribe(filename, language='hi')
        transcript = result.get("text", "").strip()
        if transcript:
            return transcript
        else:
            print("⚠️ ट्रांसक्रिप्शन खाली है।")
            return ""
    except Exception as e:
        print(f"[❌] ट्रांसक्रिप्शन विफल: {e}")
        return ""

def clean_transcript(text):
    keywords = [
        "लोन कैसे लें", "ब्याज दरें", "क्या यह सुरक्षित है", "loan", "interest",
        "safe", "platform safe", "प्लेटफॉर्म सुरक्षित है", "निवेश", "register", "समस्या"
    ]
    matches = get_close_matches(text.lower(), keywords, n=1, cutoff=0.6)
    return matches[0] if matches else text

def speak(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")
    except Exception as e:
        print(f"[❌] बोलने में त्रुटि: {e}")

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"[❌] अनुवाद में त्रुटि: {e}")
        return text

def main():
    config = load_config()
    if not config:
        return

    duration = config.get("recording", {}).get("duration", 5)

    print("🤖 VoiceBot शुरू हो गया है। 'धन्यवाद' या 'thank you' कहकर बंद करें।\n")
    speak("नमस्ते! मैं पीयर टू पीयर लेंडिंग वॉइसबॉट हूँ। आप मुझसे पैसे उधार देने या लेने से जुड़े सवाल पूछ सकते हैं। उदाहरण के लिए पूछिए – लोन कैसे लें? या प्लेटफॉर्म सुरक्षित है?")

    try:
        while True:
            print("\n🎙️ रिकॉर्डिंग शुरू...\n")
            record_audio("input.wav", duration)
            print("📝 ट्रांसक्रिप्शन चल रहा है...\n")

            user_text = transcribe_audio("input.wav")
            if not user_text:
                reply = "माफ़ कीजिए, कुछ सुनाई नहीं दिया। कृपया फिर से बोलिए।"
            elif any(word in user_text.lower() for word in ["धन्यवाद", "thank", "stop", "बंद"]):
                reply = "आपका दिन शुभ हो! धन्यवाद।"
                print("🤖 बॉट:", reply)
                speak(reply)
                break
            else:
                print("🙋‍♀️ यूज़र ने कहा:", user_text)
                cleaned_text = clean_transcript(user_text)

                # Only translate if it seems necessary (basic English detection)
                needs_translation = not any(char.isalpha() and char.isascii() for char in cleaned_text)
                translated_text = translate_to_english(cleaned_text) if needs_translation else cleaned_text
                print("🌐 अनुवादित:", translated_text)

                intent = categorize_query(translated_text)
                reply = generate_response(intent)

            print("🤖 बॉट:", reply)
            speak(reply)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 मैन्युअली बंद किया गया। धन्यवाद!")

if __name__ == "__main__":
    main()
