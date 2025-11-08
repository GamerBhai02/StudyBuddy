from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings
import logging
import os

logger = logging.getLogger(__name__)

def get_database_url():
    """
    Get database URL with fallback logic.
    Tries PostgreSQL first, falls back to SQLite if connection fails.
    """
    database_url = settings.DATABASE_URL
    
    # Detect database type
    is_postgresql = database_url.startswith('postgresql')
    is_sqlite = database_url.startswith('sqlite')
    
    if is_postgresql:
        logger.info("Detected PostgreSQL database configuration")
        # Try to connect to PostgreSQL
        try:
            test_engine = create_engine(database_url, pool_pre_ping=True)
            # Test connection
            with test_engine.connect() as conn:
                conn.execute("SELECT 1")
            logger.info("✓ PostgreSQL connection successful")
            test_engine.dispose()
            return database_url, {}
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed: {e}")
            logger.info("Falling back to SQLite database...")
            # Fall back to SQLite
            sqlite_path = os.path.join(os.getcwd(), "exam_prep_db.db")
            fallback_url = f"sqlite:///{sqlite_path}"
            logger.info(f"Using SQLite database at: {sqlite_path}")
            return fallback_url, {"check_same_thread": False}
    
    elif is_sqlite:
        logger.info(f"Using SQLite database: {database_url}")
        return database_url, {"check_same_thread": False}
    
    else:
        logger.warning(f"Unknown database type in URL: {database_url}")
        logger.info("Falling back to SQLite database...")
        sqlite_path = os.path.join(os.getcwd(), "exam_prep_db.db")
        fallback_url = f"sqlite:///{sqlite_path}"
        logger.info(f"Using SQLite database at: {sqlite_path}")
        return fallback_url, {"check_same_thread": False}

# Get appropriate database URL and connection arguments
database_url, connect_args = get_database_url()

# Create engine with appropriate configuration
engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_database():
    """
    Initialize database tables.
    Should be called from main.py on startup, not from route modules.
    """
    try:
        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")
        return False

def get_db():
    """Database session dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
