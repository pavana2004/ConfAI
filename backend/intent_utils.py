import re

def infer_intent_from_text(message: str):
    msg = message.lower()

    # explicit offline signals
    if re.search(r"\bconference room\b", msg) or re.search(r"\bmeeting room\b", msg):
        return "book_offline_meeting"

    # explicit online signals (whole words only)
    if re.search(r"\bonline\b", msg):
        return "book_online_meeting"

    if re.search(r"\bzoom\b", msg):
        return "book_online_meeting"

    if re.search(r"\bgoogle meet\b", msg):
        return "book_online_meeting"

    if re.search(r"\bteams\b", msg):
        return "book_online_meeting"

    # direct answers
    if msg.strip() == "online":
        return "book_online_meeting"

    if msg.strip() == "offline":
        return "book_offline_meeting"

    return "unknown"
