from datetime import datetime
from typing import Tuple

def format_amount_to_paise(amount_inr: float) -> int:
    """Convert INR amount to Paise."""
    return int(amount_inr * 100)

def get_current_ist_time() -> Tuple[datetime, str]:
    """Get current UTC datetime and formatted time string."""
    now = datetime.utcnow()
    # In a real app, you might want to convert to IST
    # For now, we'll use UTC and return a formatted time
    time_str = now.strftime("%H:%M:%S")
    return now, time_str

def validate_upi_id(vpa: str) -> bool:
    """Basic UPI ID validation."""
    if not vpa or "@" not in vpa:
        return False
    return True
