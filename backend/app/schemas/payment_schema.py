from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class CreateOrderRequest(BaseModel):
    bookingId: str

class VerifyPaymentRequest(BaseModel):
    bookingId: str
    razorpayOrderId: str
    razorpayPaymentId: str
    razorpaySignature: str

class PaymentTransactionSchema(BaseModel):
    bookingId: Optional[str] = None
    bookingRef: Optional[str] = None
    patientId: Optional[str] = None
    patientName: Optional[str] = None
    patientEmail: Optional[str] = None
    patientPhone: Optional[str] = None
    razorpayOrderId: str
    razorpayPaymentId: Optional[str] = None
    razorpaySignature: Optional[str] = None
    amount: int  # Paise
    amountINR: float
    currency: str = "INR"
    method: str = "upi"
    upiId: Optional[str] = None
    status: str = "created"  # created, captured, failed
    signatureVerified: bool = False
    webhookVerified: bool = False
    razorpayResponse: Optional[Dict[str, Any]] = None
    transactionDate: Optional[datetime] = None
    transactionTime: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    capturedAt: Optional[datetime] = None
