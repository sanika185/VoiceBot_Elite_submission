import openai

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"  # Replace this or use an environment variable

def generate_response(text):
    prompt = f"""
    उपयोगकर्ता ने यह कहा: "{text}"
    कृपया समस्या को समझकर हिंदी में एक उपयुक्त उत्तर दें। उत्तर स्पष्ट, सहायक और सीधे मुद्दे पर होना चाहिए।
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "आप एक सहायक हिंदी ग्राहक सेवा सहायक हैं।"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"उत्तर प्राप्त करने में त्रुटि हुई: {str(e)}"

