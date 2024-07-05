from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database connection setup
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL, echo=True)  # 'echo=True' for SQL output logs, remove in production

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@contextmanager
def session_manager():
    """Provide a transactional scope around a series of operations."""
    db_session = SessionLocal()
    try:
        yield db_session
        db_session.commit()  # Ensure any changes are committed if no errors occur
    except Exception as e:
        db_session.rollback()  # Roll back the transaction on error
        raise e
    finally:
        db_session.close()