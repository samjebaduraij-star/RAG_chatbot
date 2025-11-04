# security.py
# Description: Basic authentication and token management
# Dependencies: fastapi, datetime, os
# Author: AI Generated Code
# Created: August 15, 2025

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from datetime import timedelta, datetime
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication token")
    # Optionally add expiry or session logic
    return True