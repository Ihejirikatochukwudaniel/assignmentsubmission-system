from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL environment variable is required')

# SQLite requires check_same_thread=False
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Try default DBAPI (psycopg2). If it's not available (DLL issues on Windows),
    # fall back to the pure-Python `pg8000` driver by rewriting the URL.
    try:
        # attempt to import psycopg2 to confirm availability
        import psycopg2  # type: ignore
        engine = create_engine(DATABASE_URL, future=True)
    except Exception:
        # Fallback to pg8000
        if DATABASE_URL.startswith('postgresql://'):
            pg8000_url = DATABASE_URL.replace('postgresql://', 'postgresql+pg8000://', 1)
            engine = create_engine(pg8000_url, future=True)
        else:
            # last resort: try creating engine with provided URL
            engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
