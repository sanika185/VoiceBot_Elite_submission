def classify_department(text):
    text = text.lower()
    if "पानी" in text or "जल" in text:
        return "Water Department"
    elif "कचरा" in text or "गंदगी" in text:
        return "Sanitation Department"
    elif "सड़क" in text or "गड्ढा" in text:
        return "Road Maintenance"
    elif "बिजली" in text or "लाइट" in text:
        return "Electricity Department"
    else:
        return None

def check_location(text):
    return any(word in text for word in ["में", "पास", "निकट", "स्थान", "इलाका"])

