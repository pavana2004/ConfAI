from datetime import datetime, timedelta
import re

def extract_date_time(message: str):
    msg = message.lower()
    now = datetime.now()

    date = None
    start_time = None
    end_time = None

    # ---------------------------
    # DATE PARSING
    # ---------------------------

    # ISO date: 2026-01-16
    iso_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", msg)
    if iso_match:
        date = iso_match.group(1)

    # today / tomorrow
    if "today" in msg:
        date = now.strftime("%Y-%m-%d")
    elif "tomorrow" in msg:
        date = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    # 16th january 2026
    natural_date = re.search(
        r"(\d{1,2})(st|nd|rd|th)?\s+"
        r"(january|february|march|april|may|june|"
        r"july|august|september|october|november|december)\s+(\d{4})",
        msg
    )
    if natural_date:
        day = int(natural_date.group(1))
        month_str = natural_date.group(3)
        year = int(natural_date.group(4))

        month_map = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }

        month = month_map[month_str]
        date = f"{year:04d}-{month:02d}-{day:02d}"

    # ---------------------------
    # TIME PARSING (24-hour FIRST)
    # ---------------------------

    # 24-hour range: 14:00 to 15:30
    range_24h = re.search(
        r"\b([01]\d|2[0-3]):([0-5]\d)\s*to\s*([01]\d|2[0-3]):([0-5]\d)\b",
        msg
    )
    if range_24h:
        start_time = f"{range_24h.group(1)}:{range_24h.group(2)}"
        end_time = f"{range_24h.group(3)}:{range_24h.group(4)}"
        return date, start_time, end_time

    # single 24-hour time: 14:00
    single_24h = re.search(r"\b([01]\d|2[0-3]):([0-5]\d)\b", msg)
    if single_24h:
        start_time = single_24h.group(0)

    # ---------------------------
    # TIME PARSING (am / pm)
    # ---------------------------

    def to_24h(h, m, mer):
        h = int(h)
        m = int(m) if m else 0
        if mer == "pm" and h != 12:
            h += 12
        if mer == "am" and h == 12:
            h = 0
        return f"{h:02d}:{m:02d}"

    # am/pm range: 2pm to 3:30pm
    range_ampm = re.search(
        r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*to\s*"
        r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)",
        msg
    )
    if range_ampm:
        start_time = to_24h(
            range_ampm.group(1),
            range_ampm.group(2),
            range_ampm.group(3)
        )
        end_time = to_24h(
            range_ampm.group(4),
            range_ampm.group(5),
            range_ampm.group(6)
        )
        return date, start_time, end_time

    # single am/pm: 2pm / 2:30pm
    single_ampm = re.search(
        r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)",
        msg
    )
    if single_ampm:
        start_time = to_24h(
            single_ampm.group(1),
            single_ampm.group(2),
            single_ampm.group(3)
        )

    return date, start_time, end_time
