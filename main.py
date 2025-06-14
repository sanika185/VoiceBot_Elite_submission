import yaml
import os
import whisper
import csv
from datetime import datetime
from gtts import gTTS
from playsound import playsound
import time
import sqlite3
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv  # Add dotenv import

from modules.asr_module import record_audio
from modules.response_gen import generate_response
from categorize_complaint import categorize_complaint
from modules.mailer import send_email

MAX_RETRIES = 3

# Load environment variables from .env
load_dotenv()

# Get sensitive info from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Whisper मॉडल लोड हो रहा है...")
whisper_model = whisper.load_model("small")
print("Whisper मॉडल लोड हो गया ✅")

def load_config():
    print("Loading config...")
    with open("config/config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def transcribe_audio(filename):
    print("Transcribing audio using local Whisper model...")
    try:
        result = whisper_model.transcribe(filename, language="hi", fp16=False)
        print("DEBUG - Whisper raw result:", result)
        return result["text"].strip()
    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return ""

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
    print(f"[DEBUG] Bot will speak: {text}")
    try:
        tts = gTTS(text=text, lang='hi')
        filename = "voice_output.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"[ERROR] Speaking failed: {e}")

def is_location_present(text):
    common_locations = ["nashik", "pune", "mumbai", "kolhapur", "delhi"]
    return any(loc.lower() in text.lower() for loc in common_locations)

def ask_for_location(config):
    speak("कृपया स्थान बताएं जहाँ यह समस्या हो रही है।")
    print("स्थान रिकॉर्ड किया जा रहा है...")
    record_audio("location.wav", config)
    print("स्थान रिकॉर्ड हो गया ✅")
    location_text = transcribe_audio("location.wav")
    print("स्थान:", location_text)
    return location_text if location_text else "अज्ञात स्थान"

def log_complaint(complaint, location, bot_reply, status, category="NA"):
    log_file = "complaint_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Complaint", "Location", "Category", "Bot Reply", "Status"])
        writer.writerow([timestamp, complaint, location, category, bot_reply, status])

# Main CLI Logic
def main():
    print("शिकायत प्रणाली शुरू हो रही है...\n")
    config = load_config()
    print("कॉन्फ़िग लोड हो गया ✅\n")

    for attempt in range(MAX_RETRIES):
        print("रिकॉर्डिंग शुरू...\n")
        try:
            record_audio("input.wav", config)
            print("रिकॉर्डिंग सेव हो गई ✅\n")
        except Exception as e:
            print(f"[ERROR] रिकॉर्डिंग में समस्या: {e}")
            speak("रिकॉर्डिंग में समस्या आ गई है। कृपया पुनः प्रयास करें।")
            continue

        user_text = transcribe_audio("input.wav")
        print("उपयोगकर्ता ने कहा:", user_text, "\n")

        if is_valid_transcript(user_text):
            user_text_norm = user_text.lower().strip()
            category, fallback = categorize_complaint(user_text_norm)

            if category == "Other/Unclear":
                print("बॉट:", fallback)
                speak(fallback)
                log_complaint(user_text, "NA", fallback, "Unclear", category)
                break

            if not is_location_present(user_text):
                location = ask_for_location(config)
            else:
                location = "उल्लेखित"

            bot_reply = f"आपकी शिकायत '{category}' श्रेणी में दर्ज की गई है। संबंधित विभाग को सूचित किया जाएगा।"
            print("बॉट:", bot_reply)
            speak(bot_reply)
            log_complaint(user_text, location, bot_reply, "Valid", category)

            # ✅ Send email notification securely using env variables
            subject = "नई शिकायत प्राप्त हुई"
            body = f"""नई शिकायत दर्ज की गई है:
शिकायत: {user_text}
स्थान: {location}
श्रेणी: {category}
बॉट जवाब: {bot_reply}
"""
            to_email = "sanikagadade641@gmail.com"

            # Use EMAIL_USER and EMAIL_PASS loaded from .env
            send_email(to_email, subject, body, "setuvani0@gmail.com", "tffrkmibpycxvntl")  # ✅ works, but not secure


            break
        else:
            fallback = get_fallback_response(attempt)
            print("बॉट:", fallback)
            speak(fallback)
            log_complaint(user_text, "NA", fallback, "Fallback")

    else:
        final_msg = "सिस्टम को आपकी बात समझने में समस्या हो रही है। कृपया बाद में प्रयास करें।"
        print("\nबॉट:", final_msg)
        speak(final_msg)
        log_complaint("असमर्थ ट्रांसक्रिप्ट", "NA", final_msg, "Failed")

# GUI Wrapper
def gui_main():
    root = tk.Tk()
    root.title("🎤 शिकायत दर्ज करें - Civic Voicebot")
    root.geometry("720x480")

    log_area = scrolledtext.ScrolledText(root, width=85, height=25, font=("Arial", 10))
    log_area.pack(padx=10, pady=10)

    def run_and_log():
        log_area.insert(tk.END, "🔄 प्रक्रिया शुरू हो रही है...\n")
        log_area.update()
        main()
        log_area.insert(tk.END, "✅ प्रक्रिया पूरी हो गई!\n\n")
        log_area.see(tk.END)

    record_button = tk.Button(root, text="🎤 रिकॉर्ड करके शिकायत दर्ज करें", font=("Arial", 14), command=run_and_log)
    record_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui_main()

