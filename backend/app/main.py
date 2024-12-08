from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import timedelta, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
import uvicorn
import logging

from app.database import engine, Base, get_db
from app.models import Account
from app.security import (
    authenticate_admin,
    create_access_token,
    get_current_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="BGMI Market",
    description="A platform for buying and selling BGMI accounts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

# Pydantic models
class AccountBase(BaseModel):
    level: int
    rank: str
    skins: str
    price: float
    description: str
    contact_info: str

class AccountCreate(AccountBase):
    pass

class AccountResponse(BaseModel):
    id: int
    level: int
    rank: str
    skins: str
    price: float
    description: str
    contact_info: str
    created_at: datetime
    approved: bool

    class Config:
        orm_mode = True

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to BGMI Market API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Public endpoints
@app.get("/accounts", response_model=List[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    try:
        accounts = db.query(Account).filter(Account.approved == True).all()
        return [
            {
                "id": acc.id,
                "level": acc.level,
                "rank": acc.rank,
                "skins": acc.skins,
                "price": acc.price,
                "description": acc.description,
                "contact_info": acc.contact_info,
                "created_at": acc.created_at,
                "approved": acc.approved
            }
            for acc in accounts
        ]
    except Exception as e:
        print(f"Error in list_accounts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/accounts", response_model=AccountResponse)
async def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    try:
        print(f"DEBUG: Creating new account with data: {account_data}")
        
        # Validate required fields
        if not account_data.level or account_data.level < 1:
            raise HTTPException(status_code=400, detail="Invalid account level")
            
        if not account_data.rank:
            raise HTTPException(status_code=400, detail="Rank is required")
            
        if not account_data.price or account_data.price < 0:
            raise HTTPException(status_code=400, detail="Invalid price")
            
        if not account_data.contact_info:
            raise HTTPException(status_code=400, detail="Contact information is required")
            
        # Create account
        account = Account(
            level=account_data.level,
            rank=account_data.rank,
            skins=account_data.skins,
            price=account_data.price,
            description=account_data.description,
            contact_info=account_data.contact_info,
            approved=False
        )
        
        # Add to database
        db.add(account)
        db.commit()
        db.refresh(account)
        
        print(f"DEBUG: Successfully created account with ID: {account.id}")
        return account
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        print(f"ERROR: Failed to create account - {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create account: {str(e)}"
        )

# Admin endpoints
@app.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_admin(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/admin/accounts", response_model=List[AccountResponse])
async def list_all_accounts(db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    try:
        print(f"DEBUG: Admin {current_admin} requesting all accounts")
        accounts = db.query(Account).all()
        print(f"DEBUG: Found {len(accounts)} accounts")
        
        # Convert accounts to dict for debugging
        accounts_data = []
        for account in accounts:
            try:
                account_dict = {
                    "id": account.id,
                    "level": account.level,
                    "rank": account.rank,
                    "skins": account.skins,
                    "price": account.price,
                    "description": account.description,
                    "contact_info": account.contact_info,
                    "created_at": account.created_at,
                    "approved": account.approved
                }
                accounts_data.append(account_dict)
            except Exception as e:
                print(f"ERROR: Failed to convert account {account.id} - {str(e)}")
                continue
        
        print(f"DEBUG: Account data: {accounts_data}")
        return accounts
    except Exception as e:
        print(f"ERROR: Failed to fetch accounts - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch accounts: {str(e)}"
        )

@app.post("/admin/accounts/{account_id}/approve")
async def approve_account(account_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    try:
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        account.approved = True
        db.commit()
        return {"message": "Account approved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/accounts/{account_id}")
async def delete_account(account_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    try:
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        db.delete(account)
        db.commit()
        return {"message": "Account deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000)
