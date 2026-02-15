import ollama

SYSTEM_PROMPT = """
You are a meeting assistant.

Your job is ONLY to ask short, natural follow-up questions.

Rules:
- Ask in plain English
- Ask only what is missing
- One sentence maximum
- No creativity
- No examples
- No extra instructions
- No meta commentary
- No formatting
- Do not explain yourself
"""

QUESTION_MAP = {
    "participants": "Who should be included?",
    "end time": "When should it end?",
    "start time": "When should it start?",
    "date": "Which day should this be?",
    "room name": "Which room should I book?",
    "meeting type": "Should this be online or in person?"
}

def ask_missing_fields(missing_fields: list[str]) -> str:
    # deterministic fallback (IMPORTANT)
    if len(missing_fields) == 1:
        return QUESTION_MAP.get(missing_fields[0], "Can you clarify that?")

    # controlled LLM usage for multiple fields
    prompt = (
        "Ask a single short question to get this information: "
        + ", ".join(missing_fields)
    )

    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()
