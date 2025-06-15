import difflib
import re

# Normalize and tokenize text
def preprocess_text(text):
    text = text.lower()
    return re.findall(r'\w+', text)

# Approximate phrase or word matching
def contains_approximate_keyword(text, keywords, cutoff=0.7):
    words = preprocess_text(text)
    text_joined = " ".join(words)

    for keyword in keywords:
        # Check exact keyword match in full string (e.g. "create account")
        if keyword in text_joined:
            return True

        # Also check approximate matches word-by-word
        for word in words:
            matches = difflib.get_close_matches(word, [keyword], cutoff=cutoff)
            if matches:
                return True

    return False

def best_matching_intent(text, keywords, cutoff=0.6):
    words = preprocess_text(text)
    intent_scores = {}

    for intent, kw_list in keywords.items():
        score = 0
        for keyword in kw_list:
            for word in words:
                if difflib.SequenceMatcher(None, word, keyword).ratio() >= cutoff:
                    score += 1
        intent_scores[intent] = score

    # Return the intent with highest score if any matches
    top_intent = max(intent_scores, key=intent_scores.get)
    return top_intent if intent_scores[top_intent] > 0 else "Unclear"

# Main categorization logic
def categorize_query(text):
    text = text.lower()

    # Bilingual + Hinglish keywords
    keywords = {
        "Loan Awareness": [
            "loan", "p2p", "peer", "lend", "borrow", "interest", "emi",
            "उधार", "ऋण", "लोन", "कर्ज", "ब्याज", "क़िस्त", "installment"
        ],
        "Investor Awareness": [
            "investment", "invest", "return", "roi", "profit", "gain", "fund", "risk",
            "निवेश", "रिटर्न", "फायदा", "कमाई", "ब्याज", "फंड", "जोखिम", "investment kaise kare"
        ],
        "Onboarding Help": [
            "register", "signup", "create account", "start", "begin", "kyc", "upload", 
            "रजिस्टर", "साइनअप", "खाता", "शुरू", "केवाईसी", "जोड़ें", "फॉर्म", "कैसे शुरू करें"
        ],
        "Security Concerns": [
            "safe", "secure", "risk", "trust", "authentic", "data", "privacy", "security",
            "सुरक्षित", "सेफ", "भरोसा", "सिक्योर", "जोखिम", "गोपनीयता", "डेटा"
        ],
        "General P2P Info": [
            "p2p", "peer to peer", "platform", "explain", "details", "what is", "overview",
            "क्या है", "कैसे काम करता", "प्लेटफार्म", "जानकारी", "बताओ", "explain karo", "p2p ka matlab"
        ],
        "Complaint / Help": [
            "issue", "problem", "help", "support", "not working", "error", "complaint", "crash",
            "समस्या", "मदद", "समाधान", "शिकायत", "गलती", "nahi chal raha", "app band hai"
        ]
    }

    # Try exact or close match first
    for intent, kw_list in keywords.items():
        if contains_approximate_keyword(text, kw_list):
            return intent

    # If nothing matches well, try guessing based on closest phrases
    return best_matching_intent(text, keywords)

