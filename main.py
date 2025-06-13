import yaml
import os
import pyttsx3
from modules.asr_module import record_audio
from modules.response_gen import generate_response
import whisper

MAX_RETRIES = 3

def load_config():
    print("Loading config...")
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)

def transcribe_audio(filename):
    print("Transcribing audio using local Whisper model...")
    model = whisper.load_model("base")  # You can also try "medium"
    result = model.transcribe(filename, language="hi", task="transcribe")
    return result["text"]

def is_valid_transcript(text):
    return len(text.strip()) > 5 and any(char.isalpha() for char in text)

def get_fallback_response(attempt):
    fallback_responses = [
        "माफ़ कीजिए, आपकी बात समझ नहीं आई। कृपया फिर से बोलें।",
        "अब भी नहीं समझ पाया, कृपया स्पष्ट बोलें।",
        "कृपया थोड़ी देर बाद फिर से प्रयास करें।"
    ]
    return fallback_responses[min(attempt, len(fallback_responses) - 1)]

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    for voice in engine.getProperty('voices'):
        try:
            if "hi" in voice.languages[0].decode("utf-8") or "hindi" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        except:
            continue

    engine.say(text)
    engine.runAndWait()

def main():
    print("शिकायत प्रणाली शुरू हो रही है...\n")

    config = load_config()
    print("कॉन्फ़िग लोड हो गया ✅\n")

    for attempt in range(MAX_RETRIES):
        print("रिकॉर्डिंग शुरू...\n")
        record_audio("input.wav")
        print("रिकॉर्डिंग सेव हो गई ✅\n")

        user_text = transcribe_audio("input.wav")
        print("उपयोगकर्ता ने कहा:", user_text, "\n")

        if is_valid_transcript(user_text):
            bot_reply = generate_response(user_text)
            print("बॉट:", bot_reply)
            speak(bot_reply)
            break
        else:
            fallback = get_fallback_response(attempt)
            print("बॉट:", fallback)
            speak(fallback)
    else:
        final_msg = "सिस्टम को आपकी बात समझने में समस्या हो रही है। कृपया बाद में प्रयास करें।"
        print("\nबॉट:", final_msg)
        speak(final_msg)

if __name__ == "__main__":
    main()
