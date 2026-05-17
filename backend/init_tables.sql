-- Supabase SQL Schema for Sovilo Aesthetics
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor → New Query)

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    hashed_password TEXT,
    is_email_verified BOOLEAN DEFAULT FALSE,
    two_factor_enabled BOOLEAN DEFAULT TRUE,
    otp_code TEXT,
    otp_expires_at TIMESTAMPTZ,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- REFRESH TOKENS
-- ============================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    jti TEXT UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- SERVICES (clinic service catalog)
-- ============================================
CREATE TABLE IF NOT EXISTS services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    service_code TEXT,
    category TEXT,
    base_price INT DEFAULT 0,         -- in paise (100 = ₹1)
    duration_minutes INT DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    is_online_bookable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed a default consultation service
INSERT INTO services (name, service_code, category, base_price, duration_minutes)
VALUES ('General Consultation', 'CONS-001', 'Consultation', 100, 30)
ON CONFLICT DO NOTHING;

-- ============================================
-- BOOKINGS
-- ============================================
CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_ref TEXT UNIQUE NOT NULL,
    patient_id UUID REFERENCES users(id) ON DELETE SET NULL,
    patient_name TEXT,
    patient_email TEXT,
    patient_phone TEXT,
    service_id UUID REFERENCES services(id),
    service_code TEXT,
    service_name TEXT,
    service_category TEXT,
    appointment_date DATE,
    appointment_date_string TEXT,
    time_slot TEXT DEFAULT 'TBD',
    duration_minutes INT DEFAULT 30,
    status TEXT DEFAULT 'pending_payment',
    original_price INT DEFAULT 0,
    discount_amount INT DEFAULT 0,
    final_price INT DEFAULT 0,
    currency TEXT DEFAULT 'INR',
    price_display_inr TEXT,
    payment_deadline TIMESTAMPTZ,
    patient_notes TEXT,
    concerns TEXT,
    first_visit BOOLEAN DEFAULT TRUE,
    referral_source TEXT DEFAULT 'website',
    confirmation_email_sent BOOLEAN DEFAULT FALSE,
    reminder_email_sent BOOLEAN DEFAULT FALSE,
    booking_source TEXT DEFAULT 'website',
    razorpay_order_id TEXT,
    confirmed_at TIMESTAMPTZ,
    expired_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- PAYMENT TRANSACTIONS
-- ============================================
CREATE TABLE IF NOT EXISTS payment_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id UUID REFERENCES bookings(id) ON DELETE CASCADE,
    booking_ref TEXT,
    patient_id UUID REFERENCES users(id) ON DELETE SET NULL,
    patient_name TEXT,
    patient_email TEXT,
    patient_phone TEXT,
    razorpay_order_id TEXT,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT,
    amount INT DEFAULT 0,
    amount_inr NUMERIC(10,2),
    currency TEXT DEFAULT 'INR',
    method TEXT DEFAULT 'upi',
    status TEXT DEFAULT 'created',
    upi_id TEXT,
    transaction_date TIMESTAMPTZ,
    transaction_time TEXT,
    signature_verified BOOLEAN DEFAULT FALSE,
    webhook_verified BOOLEAN DEFAULT FALSE,
    razorpay_response JSONB,
    captured_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- ACTIVITIES (audit log)
-- ============================================
CREATE TABLE IF NOT EXISTS activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id TEXT,
    patient_email TEXT,
    event_category TEXT,
    event_type TEXT,
    event_label TEXT,
    metadata JSONB DEFAULT '{}',
    page TEXT,
    device TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- PATIENTS (for bookings.py get_current_patient)
-- ============================================
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT,
    email TEXT,
    phone_number TEXT,
    account_status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
