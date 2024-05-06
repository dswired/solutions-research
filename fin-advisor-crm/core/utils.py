def to_nullable_date(date: str) -> str:
    return date if date else None


def to_bool(val: str) -> bool:
    return val == "TRUE"
