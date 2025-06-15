import os
import httpx
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("[ERROR] OPENROUTER_API_KEY not found in .env")
else:
    print("[INFO] API key loaded successfully")

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://yourapp.com",  # Optional: Replace with your site if needed
    "X-Title": "VoiceBot Assistant"
}

def generate_response(question):
    try:
        question_in_hindi = GoogleTranslator(source='en', target='hi').translate(question)

        payload = {
            "model": "openchat/openchat-3.5-1210",  # You can try other models too
            "messages": [
                {"role": "system", "content": "तुम एक बैंकिंग ग्राहक सहायता सहायक हो जो हिंदी में उत्तर देता है।"},
                {"role": "user", "content": question_in_hindi}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }

        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        return "क्षमा करें, इस समय उत्तर देने में असमर्थ हूँ।"
