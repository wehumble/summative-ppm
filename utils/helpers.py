from dateutil import parser
from datetime import date

def parse_date(date_str: str) -> str:
    """
    Parse a date string into ISO format (YYYY-MM-DD).
    Raises ValueError if parsing fails.
    """
    try:
        dt = parser.parse(date_str)
        return dt.date().isoformat()
    except Exception:
        raise ValueError(f"Invalid date format: '{date_str}'. Please use a valid date.")

def validate_email(email: str) -> str:
    """Simple email validation. Returns email if valid, raises ValueError otherwise."""
    if "@" not in email or "." not in email:
        raise ValueError(f"Invalid email address: '{email}'")
    return email