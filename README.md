Sovilo's Aesthetics / Laser Clinic Website
==========================================

This repository contains a full-stack lead-generation website for **Sovilo's Aesthetics Baner / Laser Clinic** in Baner, Pune.

The stack is:

- Frontend: **React (Vite + TypeScript)**, **Tailwind CSS**, shadcn-style UI components, **React Router**, **React Hook Form**, **Zod**, **Framer Motion**, **Lucide React**
- Backend: **FastAPI**, **MongoDB**, **SMTP email** for appointment/contact notifications

## Project Structure

- `frontend/` – React single-page app (SPA)
- `backend/` – FastAPI API server with MongoDB integration
- `docs/google-sheet-apps-script.js` – Script to connect the contact form to a Google Sheet (customer database)

## Contact Form → Google Sheet (Customer Database)

The contact/appointment form can store submissions in a **Google Sheet** as your database of interested clients (skincare / consultation).

1. **Create or open a Google Sheet** (e.g. “Sovilo Appointments”).
2. **Add header row** (Row 1): `Timestamp` | `Name` | `Phone` | `Concern / Interest` | `Preferred Date` | `Source` | `Created At`
3. **Extensions → Apps Script**. Delete default code and paste the contents of `docs/google-sheet-apps-script.js`. Save.
4. **Deploy → New deployment → Web app**: Execute as **Me**, Who has access **Anyone**. Deploy and copy the **Web app URL** (ends with `/exec`).
5. In `frontend/src/pages/Contact.tsx`, set `GOOGLE_SHEET_WEBHOOK_URL` to that URL.
6. Submit the form on the site; a new row will appear in the sheet for each submission.

## Prerequisites

- Node.js 18+ and npm (or pnpm/yarn) installed
- Python 3.10+ installed
- MongoDB instance (local or cloud, e.g. MongoDB Atlas)

## Frontend Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Create a `.env` file in `frontend/`:

   ```bash
   cp .env.example .env
   ```

   Set:

   ```bash
   REACT_APP_BACKEND_URL=http://localhost:8000
   REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```

3. Run the dev server:

   ```bash
   npm run dev
   ```

## Backend Setup

1. Install dependencies:

   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   pip install -r requirements.txt
   ```

2. Create a `.env` file in `backend/`:

   ```bash
   cp .env.example .env
   ```

   Fill in:

   ```bash
   MONGO_URL=your_mongodb_url
   DB_NAME=sovilo_aesthetics
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   CLINIC_EMAIL=holisticclinicsbaner@gmail.com
   ```

3. Run the API:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Environment Variables Summary

### Frontend

- `REACT_APP_BACKEND_URL` – Base URL of the FastAPI backend
- `REACT_APP_GOOGLE_MAPS_API_KEY` – Google Maps Embed/JS API key

### Backend

- `MONGO_URL` – MongoDB connection string
- `DB_NAME` – Database name (e.g. `sovilo_aesthetics`)
- `SMTP_HOST` – SMTP server host (e.g. `smtp.gmail.com`)
- `SMTP_PORT` – SMTP port (e.g. `587`)
- `SMTP_USER` – SMTP username (e.g. Gmail address)
- `SMTP_PASSWORD` – SMTP app password
- `CLINIC_EMAIL` – Destination email for appointment/contact notifications

## Running the Full Stack

1. Start the backend API (port 8000 by default).
2. Start the frontend dev server (usually port 5173 with Vite).
3. Open the frontend in your browser and verify:
   - Home, Services, About, Contact/Booking pages load
   - Appointment form validates and submits to the backend
   - Contact info links (`tel:`, WhatsApp, email, Maps) work

## Production Notes

- Use a production-ready Node server or static host (e.g. Netlify, Vercel, S3+CloudFront) for the frontend.
- Use a proper ASGI server (e.g. `uvicorn` behind Nginx or a PaaS) for FastAPI.
- Configure HTTPS (TLS) for both frontend and backend.
- Add Google Analytics, sitemap, `robots.txt`, and schema markup as per the SEO section in the spec.


## Payment Integration (Razorpay UPI)

This project includes a Razorpay UPI integration (checkout popup flow) and server-side verification.

- Backend:
   - `app/utils/razorpay_client.py` — Razorpay SDK wrapper (order creation, signature & webhook verification, fetch payment details).
   - `app/routes/payments.py` — Endpoints: `/api/payment/create-order`, `/api/payment/verify`, `/api/payment/webhook`.
   - Run `python -m app.scripts.create_payment_indexes` to create indexes for the `payments` collection.

- Frontend:
   - `frontend/src/components/payment/PaymentPopup.tsx` — Popup component that opens Razorpay checkout configured for UPI (QR, apps, manual VPA entry). Use this component in your booking flow to open in-place (no redirect).
   - Environment: set `VITE_RAZORPAY_KEY_ID` in `frontend/.env`.

- Environment variables (examples in `backend/.env.example` and `frontend/.env.example`).

- Testing:
   - Use UPI test VPAs `success@razorpay` (succeeds) and `failure@razorpay` (fails).
   - Configure Razorpay webhook URL to `https://YOUR_DOMAIN/api/payment/webhook` and set `RAZORPAY_WEBHOOK_SECRET` in the backend env.

If you want, I can wire the popup into the existing booking form component and run the index-creation script now.

