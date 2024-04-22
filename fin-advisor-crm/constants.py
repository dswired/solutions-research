from django.core.validators import RegexValidator

CHARACTER_MAX_LENGTH = 50
LARGE_CHARACTER_MAX_LENGTH = 200
MAX_DIGITS = 15
DECIMAL_PLACES = 5
ALPHANUMERIC = RegexValidator(
    r"^[0-9a-zA-Z_]*$", "Only alphanumeric characters are allowed."
)
ALPHABET = RegexValidator(r"[A-Za-z]*$", "Only alphabetic characters are allowed.")

CLIENT_TYPE_CHOICES = [
    ("INDIVIDUAL", "Individual"),
    ("CORPORATION", "Corporation"),
    ("TRUST", "Trust"),
    ("FOUNDATION", "Foundation"),
]

TRANSACTION_TYPE_CHOICES = [
    ("BUY", "buy"),
    ("SELL", "sell"),
    ("DEPOSIT", "deposit"),
    ("WITHDRAWAL", "withdrawal"),
    ("INSTRUMENT-CASHFLOW", "instrument-cashflow"),
]
