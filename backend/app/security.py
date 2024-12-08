from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "nixon")  # Using the secret key from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Admin credentials (from .env)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "shafvann")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # For simplicity, direct comparison since we're not hashing in this demo
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    return password  # No hashing for demo

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_admin(username: str, password: str) -> bool:
    """Authenticate admin credentials."""
    try:
        # Load environment variables again to ensure they're fresh
        load_dotenv()
        
        # Get admin credentials from environment
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if not admin_username or not admin_password:
            print("ERROR: Admin credentials not found in environment variables")
            return False
            
        # Compare credentials
        username_match = username == admin_username
        password_match = password == admin_password
        
        print(f"DEBUG: Authentication attempt for user: {username}")
        print(f"DEBUG: Username match: {username_match}")
        print(f"DEBUG: Password match: {password_match}")
        
        return username_match and password_match
        
    except Exception as e:
        print(f"ERROR: Authentication error - {str(e)}")
        return False

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Load environment variables again to ensure they're fresh
        load_dotenv()
        admin_username = os.getenv("ADMIN_USERNAME")
        
        if not admin_username:
            print("ERROR: Admin username not found in environment variables")
            raise credentials_exception
            
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            print("ERROR: Username not found in token")
            raise credentials_exception
            
        if username != admin_username:
            print(f"ERROR: Token username ({username}) does not match admin username ({admin_username})")
            raise credentials_exception
            
        print(f"DEBUG: Successfully validated token for user: {username}")
        return username
        
    except JWTError as e:
        print(f"ERROR: JWT validation error - {str(e)}")
        raise credentials_exception
    except Exception as e:
        print(f"ERROR: Unexpected error in token validation - {str(e)}")
        raise credentials_exception
