import tkinter as tk
from tkinter import messagebox
import whisper
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import os
import csv

from modules.asr_module import record_audio
from categorize_complaint import categorize_complaint
import yaml

model = whisper.load_model("small")

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config()

def speak(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")
    except Exception as e:
        print(f"Error speaking: {e}")

def transcribe_audio(file):
    try:
        result = model.transcribe(file, language="hi", fp16=False)
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""

def log_complaint(complaint, location, category, reply, status):
    log_file = "complaint_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Complaint", "Location", "Category", "Bot Reply", "Status"])
        writer.writerow([timestamp, complaint, location, category, reply, status])

def process_complaint():
    status_label.config(text="🎙️ Recording...")
    root.update()
    try:
        record_audio("input.wav", config)
    except Exception as e:
        status_label.config(text="Recording failed.")
        messagebox.showerror("Error", str(e))
        return

    status_label.config(text="🧠 Transcribing...")
    root.update()
    user_text = transcribe_audio("input.wav")
    transcript_output.delete("1.0", tk.END)
    transcript_output.insert(tk.END, user_text)

    if len(user_text.strip()) < 5:
        msg = "कृपया स्पष्ट रूप से बोलें।"
        speak(msg)
        status_label.config(text="Fallback")
        return

    category, fallback = categorize_complaint(user_text.lower())
    if category == "Other/Unclear":
        speak(fallback)
        log_complaint(user_text, "NA", category, fallback, "Unclear")
        status_label.config(text="❌ Complaint unclear.")
        return

    location = location_entry.get().strip()
    if not location:
        speak("कृपया स्थान दर्ज करें।")
        status_label.config(text="Location missing.")
        return

    reply = f"आपकी शिकायत '{category}' श्रेणी में दर्ज की गई है। संबंधित विभाग को सूचित किया जाएगा।"
    speak(reply)
    log_complaint(user_text, location, category, reply, "Valid")
    status_label.config(text="✅ Complaint registered.")

# GUI setup
root = tk.Tk()
root.title("VoiceBot Complaint System")
root.geometry("600x400")
root.resizable(False, False)

tk.Label(root, text="🔊 Complaint Transcript:").pack(pady=5)
transcript_output = tk.Text(root, height=5, width=70)
transcript_output.pack(pady=5)

tk.Label(root, text="📍 Enter Location:").pack(pady=5)
location_entry = tk.Entry(root, width=40)
location_entry.pack()

tk.Button(root, text="🎤 Record Complaint", command=process_complaint, bg="#4CAF50", fg="white").pack(pady=15)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

tk.Label(root, text="📁 Complaints saved in complaint_log.csv").pack(pady=10)

root.mainloop()
