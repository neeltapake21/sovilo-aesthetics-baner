"""Create indexes for payments collection.

Run this once (or during deployment) to ensure proper indexes exist.
Example:
    python -m app.scripts.create_payment_indexes
"""
import asyncio
from app.db import db

async def main():
    print("Creating indexes for payments collection...")
    # payments collection name in this project is 'payments'
    await db.payments.create_index([("razorpayOrderId", 1)], unique=True)
    await db.payments.create_index([("bookingId", 1)])
    await db.payments.create_index([("patientId", 1)])
    await db.payments.create_index([("createdAt", -1)])
    await db.payments.create_index([("patientEmail", 1)])
    print("Indexes created.")

if __name__ == "__main__":
    asyncio.run(main())
