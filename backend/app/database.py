from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:nixon_97.talat@localhost:3306/bgmi_ai'

# Create engine with echo=True for debugging
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def reset_database():
    """Reset the database by dropping and recreating all tables."""
    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("Database reset complete!")
    except Exception as e:
        print(f"Error resetting database: {e}")
        raise

def init_database():
    """Initialize the database by creating tables if they don't exist."""
    try:
        print("Creating tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        print("Database initialization complete!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Initialize database tables without resetting
init_database()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
