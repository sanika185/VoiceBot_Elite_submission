import os
import httpx
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load OpenRouter API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Setup HTTP headers for OpenRouter
headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost",  # Required by OpenRouter (use your own domain or localhost)
    "X-Title": "VoiceBot Elite"          # Any title
}

# Translation functions
def translate_to_hindi(text):
    try:
        return GoogleTranslator(source='en', target='hi').translate(text)
    except Exception as e:
        print(f"[Translation Error - EN→HI] {e}")
        return text

def translate_to_english(text):
    try:
        return GoogleTranslator(source='hi', target='en').translate(text)
    except Exception as e:
        print(f"[Translation Error - HI→EN] {e}")
        return text

# Chat function using OpenRouter
def generate_response(question):
    try:
        question_in_hindi = translate_to_hindi(question)

        messages = [
            {"role": "system", "content": "तुम एक बैंकिंग ग्राहक सहायता सहायक हो जो हिंदी में उत्तर देता है।"},
            {"role": "user", "content": question_in_hindi}
        ]

        payload = {
            "model": "openrouter/openai/gpt-3.5-turbo",  # You can change model here if needed
            "messages": messages,
            "temperature": 0.7
        }

        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30.0
        )

        result = response.json()

        return result['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        return "क्षमा करें, इस समय उत्तर देने में असमर्थ हूँ।"
