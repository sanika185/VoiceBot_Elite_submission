# modules/response_gen.py

def generate_response(user_text):
    user_text = user_text.lower()

    if "पानी" in user_text:
        return "आपकी पानी से जुड़ी शिकायत दर्ज कर ली गई है।"
    elif "बिजली" in user_text or "लाइट" in user_text:
        return "बिजली विभाग को आपकी शिकायत भेज दी गई है।"
    elif "सड़क" in user_text or "गड्ढे" in user_text:
        return "सड़क से संबंधित शिकायत रिकॉर्ड हो गई है।"
    elif "सफाई" in user_text or "कचरा" in user_text:
        return "स्वच्छता विभाग को सूचना दे दी गई है।"
    elif "आवारा कुत्ते" in user_text or "जानवर" in user_text:
        return "नगर पालिका को पशु नियंत्रण की सूचना दी गई है।"
    else:
        return "आपकी शिकायत को रिकॉर्ड कर लिया गया है। संबंधित विभाग को सूचित किया जाएगा।"
