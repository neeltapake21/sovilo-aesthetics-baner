from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth_utils import decode_token
from app.db import get_collection
from bson import ObjectId

auth_scheme = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing credentials")

    token = credentials.credentials
    try:
        data = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if data.get("typ") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = data.get("sub")
    users = get_collection("users")
    user_doc = await users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": str(user_doc.get("_id")), "email": user_doc.get("email"), "full_name": user_doc.get("full_name")}
