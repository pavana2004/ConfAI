
# # SYSTEM_PROMPT = """
# # You are an assistant that extracts structured meeting booking information.

# # Rules:
# # - Output ONLY valid JSON
# # - Do not explain anything
# # - Do not guess missing values
# # - If information is missing, set the field to null
# # - Dates must be in YYYY-MM-DD
# # - Times must be in 24-hour HH:MM format
# # - Participants must be a list of lowercase names

# # Supported intents:
# # - book_offline_meeting
# # - book_online_meeting
# # """
# import json
# import ollama

# SYSTEM_PROMPT = """
# You are an assistant that classifies meeting booking intent.

# Output ONLY valid JSON.

# Possible intents:
# - book_offline_meeting
# - book_online_meeting
# - unknown

# Do not extract dates, times, room names, or participants.
# Only classify intent.
# """

# def call_llm(message: str) -> dict:
#     try:
#         response = ollama.chat(
#             model="phi3:mini",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": message}
#             ]
#         )

#         return json.loads(response["message"]["content"])

#     except Exception as e:
#         print("LOCAL LLM FAILED:", e)
#         return { "intent": "unknown" }




# SYSTEM_PROMPT = """
# You are an assistant that extracts structured meeting booking information.

# Rules:
# - Output ONLY valid JSON
# - Do not explain anything
# - Do not guess missing values
# - If information is missing, set the field to null
# - Dates must be in YYYY-MM-DD
# - Times must be in 24-hour HH:MM format
# - Participants must be a list of lowercase names

# Supported intents:
# - book_offline_meeting
# - book_online_meeting
# """
import json
import ollama

SYSTEM_PROMPT = """
You are an assistant that classifies meeting booking intent.

Output ONLY valid JSON.
You are a strict JSON API.

You MUST reply with valid JSON only.
NO explanations.
NO markdown.
NO text outside JSON.

If unsure, respond with:
{"intent":"unknown"}

Possible intents:
- book_offline_meeting
- book_online_meeting
- unknown

Do not extract dates, times, room names, or participants.
Only classify intent.
"""

def call_llm(message: str) -> dict:
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        # return json.loads(response["message"]["content"])
        content = response["message"]["content"].strip()

        if not content:
            raise ValueError("Empty response from LLM")

        # Try to extract JSON block only
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError(f"Invalid JSON from LLM: {content}")

        return json.loads(content[start:end])

    except Exception as e:
        print("LOCAL LLM FAILED:", e)
        return { "intent": "unknown" }
