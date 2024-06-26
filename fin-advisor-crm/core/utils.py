import datetime


def to_nullable_date(date: str) -> str:
    return date if date else None


def to_bool(val: str) -> bool:
    return val == "TRUE"


def get_current_time_greeting():
    now = datetime.datetime.now()
    if now.hour < 12:
        return "Good morning"
    elif 12 <= now.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
