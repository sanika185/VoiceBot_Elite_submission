import difflib

# Helper function to match approximate keywords in the text
def contains_approximate_keyword(text, keywords, cutoff=0.7):
    words = text.lower().split()
    for word in words:
        matches = difflib.get_close_matches(word, keywords, cutoff=cutoff)
        if matches:
            return True
    return False

def categorize_query(text):
    text = text.lower()

    # Define keyword sets
    keywords = {
        "Loan Awareness": ["loan", "p2p", "peer", "lend", "borrow", "उधार", "ऋण", "लोन", "पी2पी", "लेंड"],
        "Investor Awareness": ["निवेश", "investment", "investor", "return", "फायदा", "रिटर्न", "कमाई"],
        "Onboarding Help": ["register", "onboard", "signup", "kyc", "form", "रजिस्टर", "साइनअप", "प्रक्रिया", "कैसे", "शुरू"],
        "Security Concerns": ["safe", "secure", "data", "privacy", "सुरक्षा", "डाटा", "सेफ", "सिक्योर", "भरोसा"],
        "General P2P Info": ["p2p", "peer to peer", "पियर", "क्या है", "कैसे काम करता", "बता", "जानकारी"]
    }

    # Check for matches in order of specificity
    for intent, kw_list in keywords.items():
        if contains_approximate_keyword(text, kw_list):
            return intent

    return "Unclear"
