import requests
from fastapi import HTTPException, status, Header
from typing import Optional
from config import settings
from schemas import ValidatedUser


def validate_token_with_auth_service(authorization: Optional[str] = Header(None)) -> ValidatedUser:
    """Dependency to validate token with Auth Service"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    # validate token with auth service
    try:
        response = requests.post(
            f"{settings.AUTH_SERVICE_URL}/validate-token",
            json={"token": token},
            timeout=5
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user_data = response.json()
        return ValidatedUser(**user_data)
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth service unavailable: {str(e)}"
        )


def require_admin(current_user: ValidatedUser) -> ValidatedUser:
    """
    Dependency to check if user has admin role
    Design Pattern: Dependency Injection with role-based access control
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
