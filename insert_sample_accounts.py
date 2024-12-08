from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the backend directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.models import Account
from app.database import SQLALCHEMY_DATABASE_URL

# Create a new database session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_sample_accounts():
    db = SessionLocal()
    try:
        # Sample accounts to insert
        sample_accounts = [
            Account(level=1, rank='Bronze', skins='Skin1', price=100.0, description='Sample account 1', contact_info='contact1@example.com', approved=True),
            Account(level=2, rank='Silver', skins='Skin2', price=200.0, description='Sample account 2', contact_info='contact2@example.com', approved=True),
            Account(level=3, rank='Gold', skins='Skin3', price=300.0, description='Sample account 3', contact_info='contact3@example.com', approved=True)
        ]

        db.add_all(sample_accounts)
        db.commit()
        print('Sample accounts inserted successfully!')
    except Exception as e:
        print(f'Error inserting accounts: {e}')
    finally:
        db.close()

if __name__ == '__main__':
    insert_sample_accounts()
