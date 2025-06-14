import difflib

# Helper function to check approximate matches of any keyword in the text
def contains_approximate_keyword(text, keywords, cutoff=0.7):
    words = text.split()
    for word in words:
        matches = difflib.get_close_matches(word, keywords, cutoff=cutoff)
        if matches:
            return True
    return False

def categorize_complaint(text):
    text = text.lower()

    # Keyword lists including common misspellings or phonetic variants
    water_keywords = ["पानी", "जल", "water", "leakage", "tank", "पानी", "पनी"]
    electricity_keywords = ["बिजली", "light", "power", "current", "electricity", "भिजली", "बिज़ली", "बिजलि", "भिज़ली", "बिजलीय"]
    road_keywords = ["road", "sadak", "गड्ढा", "गड्डा", "पॉथोल", "पॉठोल", "pothole", "खराब", "footpath"]
    garbage_keywords = ["कचरा", "garbage", "dustbin", "गंदगी", "सफाई", "गंडगी"]
    drainage_keywords = ["गटर", "नाली", "sewer", "पानी भरा", "blockage", "ब्लॉकेज"]
    street_light_keywords = ["street light", "pole", "bulb", "lamp", "स्ट्रीट लाइट", "बत्ती"]
    noise_pollution_keywords = ["शोर", "noise", "dj", "sound", "loudspeaker", "लाउडस्पीकर"]
    illegal_parking_keywords = ["parking", "गाड़ी", "कार", "blocked", "illegal", "पार्किंग"]
    animal_issue_keywords = ["dog", "कुत्ता", "cow", "गाय", "जानवर", "stray", "स्ट्रे"]

    # Check categories one by one with approximate matching
    if contains_approximate_keyword(text, water_keywords):
        return "Water Supply", None
    elif contains_approximate_keyword(text, electricity_keywords):
        return "Electricity", None
    elif contains_approximate_keyword(text, road_keywords):
        return "Road", None
    elif contains_approximate_keyword(text, garbage_keywords):
        return "Garbage", None
    elif contains_approximate_keyword(text, drainage_keywords):
        return "Drainage", None
    elif contains_approximate_keyword(text, street_light_keywords):
        return "Street Light", None
    elif contains_approximate_keyword(text, noise_pollution_keywords):
        return "Noise Pollution", None
    elif contains_approximate_keyword(text, illegal_parking_keywords):
        return "Illegal Parking", None
    elif contains_approximate_keyword(text, animal_issue_keywords):
        return "Animal Issue", None
    else:
        fallback_msg = "माफ कीजिए, यह शिकायत हमारी सेवाओं में नहीं आती है। कृपया पानी, बिजली, सड़क जैसी समस्या बताएं।"
        return "Other/Unclear", fallback_msg
