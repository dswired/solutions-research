import datetime


def time_greeting():
    now = datetime.datetime.now()
    if now.hour < 12:
        return "Good morning"
    elif 12 <= now.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
