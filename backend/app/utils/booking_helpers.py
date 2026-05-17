from datetime import datetime, timedelta

AVAILABLE_TIME_SLOTS = [
    {"start": "11:00", "end": "12:00", "display": "11:00 AM - 12:00 PM"},
    {"start": "12:00", "end": "13:00", "display": "12:00 PM - 1:00 PM"},
    {"start": "13:00", "end": "14:00", "display": "1:00 PM - 2:00 PM"},
    {"start": "14:00", "end": "15:00", "display": "2:00 PM - 3:00 PM"},
    {"start": "15:00", "end": "16:00", "display": "3:00 PM - 4:00 PM"},
    {"start": "16:00", "end": "17:00", "display": "4:00 PM - 5:00 PM"},
    {"start": "17:00", "end": "18:00", "display": "5:00 PM - 6:00 PM"},
    {"start": "18:00", "end": "19:00", "display": "6:00 PM - 7:00 PM"},
]


async def generate_booking_ref(db_client) -> str:
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"SOV-{today_str}-"
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    result = db_client.table("bookings") \
        .select("id", count="exact") \
        .gte("created_at", today_start) \
        .like("booking_ref", f"{prefix}%") \
        .execute()

    count = result.count if result.count else 0
    return f"{prefix}{str(count + 1).zfill(4)}"


async def is_slot_available(db_client, date: datetime, time_slot: str) -> bool:
    date_str = date.strftime("%Y-%m-%d")
    result = db_client.table("bookings") \
        .select("id") \
        .eq("appointment_date", date_str) \
        .eq("time_slot", time_slot) \
        .in_("status", ["pending_payment", "confirmed", "checked_in", "in_progress"]) \
        .execute()

    return len(result.data) == 0


async def get_booked_slots(db_client, date: datetime) -> list:
    date_str = date.strftime("%Y-%m-%d")
    result = db_client.table("bookings") \
        .select("time_slot") \
        .eq("appointment_date", date_str) \
        .in_("status", ["pending_payment", "confirmed", "checked_in", "in_progress"]) \
        .execute()

    return [b["time_slot"] for b in result.data]


async def expire_unpaid_bookings(db_client):
    now = datetime.utcnow().isoformat()
    result = db_client.table("bookings") \
        .update({
            "status": "expired",
            "expired_at": now,
            "updated_at": now
        }) \
        .eq("status", "pending_payment") \
        .lt("payment_deadline", now) \
        .execute()

    return len(result.data) if result.data else 0
