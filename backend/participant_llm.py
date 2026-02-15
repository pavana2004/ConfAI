import json
import ollama

SYSTEM_PROMPT = """
Extract participant names from the message.

Rules:
- Output ONLY valid JSON
- Do not explain
- Return lowercase names
- If none found, return empty list

Format:
{ "participants": [] }
"""

def extract_participants_llm(message: str) -> list:
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )
        data = json.loads(response["message"]["content"])
        return data.get("participants", [])
    except:
        return []
