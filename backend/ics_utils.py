from datetime import datetime

def generate_ics(
    title: str,
    start_dt: datetime,
    end_dt: datetime,
    description: str,
    organizer_email: str | None = None
) -> str:
    organizer = organizer_email or "no-reply@confai.local"

    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ConfAI//Meeting Scheduler//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{int(datetime.now().timestamp())}@confai
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART;TZID=Asia/Kolkata:{start_dt.strftime('%Y%m%dT%H%M%S')}
DTEND;TZID=Asia/Kolkata:{end_dt.strftime('%Y%m%dT%H%M%S')}
SUMMARY:{title}
DESCRIPTION:{description}
ORGANIZER;CN=ConfAI:MAILTO:{organizer}
END:VEVENT
END:VCALENDAR
"""
