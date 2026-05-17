from datetime import datetime
import json


async def log_activity(db, patient_id: str, patient_email: str, event_category: str, event_type: str, event_label: str = "", metadata: dict = None, page: str = "", device: str = ""):
    try:
        doc = {
            "patient_id": str(patient_id) if patient_id else None,
            "patient_email": patient_email,
            "event_category": event_category,
            "event_type": event_type,
            "event_label": event_label,
            "metadata": json.dumps(metadata or {}),
            "page": page,
            "device": device,
            "created_at": datetime.utcnow().isoformat(),
        }
        db.table("activities").insert(doc).execute()
    except Exception:
        # Logging should never break primary flow
        return
