import asyncio
import traceback

async def main():
    try:
        import sys
        sys.path.insert(0, r"c:\Sovilo\backend")
        from dotenv import load_dotenv
        load_dotenv(r"c:\Sovilo\backend\.env")
        
        import motor.motor_asyncio
        import os
        
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGODB_DB", "sovilo")
        
        print(f"Connecting to: {uri}, db: {db_name}")
        
        client = motor.motor_asyncio.AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        # Test connection
        await client.admin.command('ping')
        print("MongoDB connection: OK")
        
        # Test generate_booking_ref
        from app.utils.booking_helpers import generate_booking_ref
        ref = await generate_booking_ref(db)
        print(f"generate_booking_ref: {ref}")
        
        # Test insert
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        booking = {
            "bookingRef": ref,
            "patientId": None,
            "patientName": "Test",
            "patientPhone": "1234567891",
            "serviceId": "consultation",
            "serviceCode": "CONS-001",
            "serviceName": "General Consultation",
            "serviceCategory": "Consultation",
            "appointmentDate": datetime(2026, 1, 30),
            "appointmentDateString": "30 January 2026",
            "timeSlot": "TBD",
            "durationMinutes": 30,
            "status": "pending_payment",
            "originalPrice": 300000,
            "discountAmount": 0,
            "finalPrice": 300000,
            "currency": "INR",
            "priceDisplayINR": "₹3,000",
            "paymentDeadline": now + timedelta(minutes=60),
            "concerns": "kh",
            "bookingSource": "contact_form",
            "createdAt": now,
            "updatedAt": now,
        }
        result = await db.bookings.insert_one(booking)
        print(f"Insert OK, id: {result.inserted_id}")
        
        # Clean up test doc
        await db.bookings.delete_one({"_id": result.inserted_id})
        print("Cleanup done. All tests passed!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()

asyncio.run(main())
