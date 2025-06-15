def infer_context(user_input, intent):
    user_input = user_input.lower()

    if intent == "Loan Awareness" and any(word in user_input for word in ["yes", "want", "interested", "apply", "please"]):
        return "interested"

    if intent == "Investor Awareness" and any(word in user_input for word in ["invest", "return", "profit", "interested"]):
        return "interested"

    if intent == "Complaint / Help" and any(word in user_input for word in ["error", "problem", "issue", "not working"]):
        return "problem_reported"

    if intent == "Security Concerns" and any(word in user_input for word in ["safe", "secure", "privacy", "data", "worried"]):
        return "worried"

    if intent == "Onboarding Help" and any(word in user_input for word in ["register", "sign up", "start", "how to start"]):
        return "interested"

    if intent == "General P2P Info" and any(word in user_input for word in ["how", "process", "steps", "explain"]):
        return "interested"

    return None
