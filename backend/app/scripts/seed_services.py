"""Seed the services collection with the default SOVILO_SERVICES.
Run with: python -m app.scripts.seed_services
"""
import asyncio
from app.db import db

SOVILO_SERVICES = [
    {"serviceCode": "SKIN_001", "category": "Skin Derma", "name": "Hydrafacial", "basePrice": 300000, "durationMinutes": 60, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹3,000"},
    {"serviceCode": "SKIN_002", "category": "Skin Derma", "name": "Korean Glass Facial", "basePrice": 350000, "durationMinutes": 60, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹3,500"},
    {"serviceCode": "SKIN_003", "category": "Skin Derma", "name": "Carbon Facial", "basePrice": 250000, "durationMinutes": 30, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹2,500"},
    {"serviceCode": "SKIN_004", "category": "Skin Derma", "name": "Chemical Peel", "basePrice": 200000, "durationMinutes": 30, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹2,000"},
    {"serviceCode": "SKIN_005", "category": "Skin Derma", "name": "Microderma Abrasion", "basePrice": 200000, "durationMinutes": 45, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹2,000"},
    {"serviceCode": "SKIN_006", "category": "Skin Derma", "name": "Permanent Hair Reduction", "basePrice": 500000, "durationMinutes": 60, "sessionsRequired": 6, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹5,000"},
    {"serviceCode": "HAIR_001", "category": "Hair", "name": "PRP Hair Treatment", "basePrice": 600000, "durationMinutes": 90, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹6,000"},
    {"serviceCode": "HAIR_002", "category": "Hair", "name": "Hair Mask Laser", "basePrice": 250000, "durationMinutes": 45, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹2,500"},
    {"serviceCode": "HAIR_003", "category": "Hair", "name": "Micro Pigmentation", "basePrice": 800000, "durationMinutes": 120, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹8,000"},
    {"serviceCode": "WGHT_001", "category": "Weight", "name": "Cryo Lipolysis", "basePrice": 800000, "durationMinutes": 60, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹8,000"},
    {"serviceCode": "WGHT_002", "category": "Weight", "name": "Sono Lipolysis", "basePrice": 700000, "durationMinutes": 60, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹7,000"},
    {"serviceCode": "WGHT_003", "category": "Weight", "name": "Belly Gym (EMS)", "basePrice": 200000, "durationMinutes": 30, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹2,000"},
    {"serviceCode": "PAIN_001", "category": "Pain", "name": "Knee Pain Laser Therapy", "basePrice": 150000, "durationMinutes": 45, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹1,500"},
    {"serviceCode": "PAIN_002", "category": "Pain", "name": "Back Pain Laser Therapy", "basePrice": 150000, "durationMinutes": 45, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹1,500"},
    {"serviceCode": "REJV_001", "category": "Rejuvenation", "name": "Anti-Aging Treatment", "basePrice": 500000, "durationMinutes": 60, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹5,000"},
    {"serviceCode": "REJV_002", "category": "Rejuvenation", "name": "NAD+ Drip", "basePrice": 400000, "durationMinutes": 90, "isActive": True, "isOnlineBookable": True, "priceDisplay": "₹4,000"},
]

async def seed():
    existing = await db.services.count_documents({})
    if existing > 0:
        print(f"Services collection already has {existing} documents. Skipping seed.")
        return
    docs = []
    from datetime import datetime
    now = datetime.utcnow()
    for s in SOVILO_SERVICES:
        s["createdAt"] = now
        s["updatedAt"] = now
        docs.append(s)
    result = await db.services.insert_many(docs)
    print(f"Inserted {len(result.inserted_ids)} services")

if __name__ == "__main__":
    asyncio.run(seed())
