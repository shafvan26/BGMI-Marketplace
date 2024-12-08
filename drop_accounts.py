from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the backend directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.models import Account
from app.database import SQLALCHEMY_DATABASE_URL, Base

# Create a new database session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def drop_all_accounts():
    db = SessionLocal()
    try:
        print("Dropping all accounts...")
        # Delete all records from the accounts table
        db.query(Account).delete()
        db.commit()
        print("All accounts have been deleted successfully!")
        
        # Show current count of accounts
        count = db.query(Account).count()
        print(f"Current number of accounts in database: {count}")
    except Exception as e:
        print(f"Error dropping accounts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    drop_all_accounts()
