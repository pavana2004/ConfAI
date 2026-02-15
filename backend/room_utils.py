KNOWN_ROOMS = [
    "conference room a",
    "conference room b",
    "huddle room 1",
    "huddle room 2",
    "big brain",
    
]

def extract_room_name(message: str):
    msg = message.lower()
    for room in KNOWN_ROOMS:
        if room in msg:
            return room.title()
    return None
