"""
Initialize database with default user
Run this once: python init_db.py
"""
from app.config.database import SessionLocal, engine, Base
from app.models.models import User
import sys

def init_database():
    print("Initializing database...")
    
    try:
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created")
    except Exception as e:
        print(f"⚠ Warning: Could not create tables: {e}")
        print("  This is normal if the database already exists or if using SQLite")
    
    # Create default user
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.id == 1).first()
        if existing_user:
            print(f"✓ Default user already exists: {existing_user.email}")
        else:
            user = User(
                id=1,
                email="student@studybuddy.com",
                name="Default Student"
            )
            db.add(user)
            db.commit()
            print(f"✓ Created default user: {user.email}")
        
        # Count existing data
        user_count = db.query(User).count()
        print(f"\n✓ Database initialized successfully")
        print(f"   Total users: {user_count}")
        
    except Exception as e:
        print(f"⚠ Warning: {e}")
        print("  Database may already be initialized or there may be a connection issue")
        db.rollback()
        # Don't exit with error, let the application try to continue
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
