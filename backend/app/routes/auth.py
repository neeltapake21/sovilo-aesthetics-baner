from datetime import timedelta, datetime
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Depends, Body, BackgroundTasks
from pydantic import BaseModel, EmailStr
import os
from pathlib import Path

from app.email import send_email
from app.db import get_collection
from app.models import UserCreate, UserInDB
from app.auth_utils import hash_password, verify_password, create_token, decode_token
from app.dependencies import get_current_user
from bson import ObjectId
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=201, response_model=Dict[str, Any])
async def register(payload: UserCreate = Body(...), background_tasks: BackgroundTasks = None):
    users = get_collection("users")
    existing = await users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(payload.password)
    doc = {
        "email": payload.email.lower(),
        "full_name": payload.full_name,
        "hashed_password": hashed,
        "is_email_verified": False,
        "two_factor_enabled": True,
        "failed_login_attempts": 0,
    }

    result = await users.insert_one(doc)
    user_id = str(result.inserted_id)

    # Create email verification token (short-lived)
    verify_token = create_token(user_id, token_type="verify", expires_delta=timedelta(hours=24))

    # queue email send (verification) using background task / SMTP
    frontend = os.getenv("FRONTEND_URL", "http://localhost:5173")
    verify_link = f"{frontend}/auth/verify?token={verify_token}"
    template_path = Path(__file__).parent.parent / "email_templates" / "verify_email.html"
    try:
        tpl = template_path.read_text()
        html_body = tpl.replace("{{verify_link}}", verify_link)
    except Exception:
        html_body = f"Please verify your email: {verify_link}"

    if background_tasks is not None:
        background_tasks.add_task(send_email, payload.email, "Verify your email", html_body)

    return {"message": "user_created", "user_id": user_id, "verify_token": verify_token}


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginPayload):
    users = get_collection("users")
    user_doc = await users.find_one({"email": payload.email.lower()})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = UserInDB(**user_doc)
    if not verify_password(payload.password, user.hashed_password):
        # increment failed attempts
        await users.update_one({"_id": user_doc["_id"]}, {"$inc": {"failed_login_attempts": 1}})
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_token(str(user_doc["_id"]), token_type="access")
    refresh = create_token(str(user_doc["_id"]), token_type="refresh")

    # store refresh token jti in DB for revocation/rotation
    try:
        payload_data = decode_token(refresh)
        jti = payload_data.get("jti")
        exp = payload_data.get("exp")
        refresh_col = get_collection("refresh_tokens")
        await refresh_col.insert_one({
            "jti": jti,
            "user_id": ObjectId(user_doc["_id"]),
            "revoked": False,
            "expires_at": datetime.utcfromtimestamp(exp),
            "created_at": datetime.utcnow(),
        })
    except Exception:
        pass

    return {"access_token": access, "refresh_token": refresh}


class RefreshPayload(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshPayload):
    try:
        data = decode_token(payload.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if data.get("typ") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    subject = data.get("sub")
    jti = data.get("jti")

    refresh_col = get_collection("refresh_tokens")
    token_doc = await refresh_col.find_one({"jti": jti})
    if not token_doc:
        raise HTTPException(status_code=401, detail="Refresh token not recognized")
    if token_doc.get("revoked"):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    # rotate: revoke old token
    await refresh_col.update_one({"jti": jti}, {"$set": {"revoked": True, "revoked_at": datetime.utcnow()}})

    # issue new tokens
    access = create_token(subject, token_type="access")
    refresh = create_token(subject, token_type="refresh")

    # store new refresh token record
    try:
        new_payload = decode_token(refresh)
        new_jti = new_payload.get("jti")
        new_exp = new_payload.get("exp")
        await refresh_col.insert_one({
            "jti": new_jti,
            "user_id": ObjectId(subject),
            "revoked": False,
            "expires_at": datetime.utcfromtimestamp(new_exp),
            "created_at": datetime.utcnow(),
        })
    except Exception:
        pass

    return {"access_token": access, "refresh_token": refresh}


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"id": current_user.get("id"), "email": current_user.get("email"), "full_name": current_user.get("full_name")}


class LogoutPayload(BaseModel):
    refresh_token: str


@router.post("/logout")
async def logout(payload: LogoutPayload = Body(...)):
    try:
        data = decode_token(payload.refresh_token)
    except Exception:
        # still return success to client
        return {"message": "logged_out"}

    jti = data.get("jti")
    exp = data.get("exp")
    refresh_col = get_collection("refresh_tokens")
    found = await refresh_col.find_one({"jti": jti})
    if found:
        await refresh_col.update_one({"jti": jti}, {"$set": {"revoked": True, "revoked_at": datetime.utcnow()}})
    else:
        await refresh_col.insert_one({"jti": jti, "user_id": None, "revoked": True, "expires_at": datetime.utcfromtimestamp(exp), "created_at": datetime.utcnow()})
    return {"message": "logged_out"}


class GooglePayload(BaseModel):
    id_token: str


@router.post("/google", response_model=TokenResponse)
async def google_auth(payload: GooglePayload):
    id_token_str = payload.id_token
    if not id_token_str:
        raise HTTPException(status_code=400, detail="Missing id_token")

    try:
        audience = os.getenv("GOOGLE_CLIENT_ID")
        idinfo = id_token.verify_oauth2_token(id_token_str, grequests.Request(), audience=audience)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")

    email = idinfo.get("email")
    name = idinfo.get("name") or ""

    if not email:
        raise HTTPException(status_code=400, detail="Google token did not contain email")

    users = get_collection("users")
    existing = await users.find_one({"email": email.lower()})
    if not existing:
        doc = {
            "email": email.lower(),
            "full_name": name,
            "hashed_password": None,
            "is_email_verified": True,
            "two_factor_enabled": False,
            "failed_login_attempts": 0,
        }
        result = await users.insert_one(doc)
        user_id = str(result.inserted_id)
    else:
        user_id = str(existing["_id"]) if isinstance(existing["_id"], ObjectId) else str(existing["_id"]) 

    access = create_token(user_id, token_type="access")
    refresh = create_token(user_id, token_type="refresh")

    # store refresh token jti
    try:
        payload_data = decode_token(refresh)
        jti = payload_data.get("jti")
        exp = payload_data.get("exp")
        refresh_col = get_collection("refresh_tokens")
        await refresh_col.insert_one({
            "jti": jti,
            "user_id": ObjectId(user_id),
            "revoked": False,
            "expires_at": datetime.utcfromtimestamp(exp),
            "created_at": datetime.utcnow(),
        })
    except Exception:
        pass

    return {"access_token": access, "refresh_token": refresh}
