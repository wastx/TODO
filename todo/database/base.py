import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from todo.config import settings

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
db_path = os.path.join(BASE_DIR, 'todo', 'database', 'DB')
if not os.path.exists(db_path):
    os.makedirs(db_path)

Base = declarative_base()


def get_db():
    db_session_local = SessionLocal()
    try:
        yield db_session_local
    finally:
        db_session_local.close()


def choose_db(arg_db):
    engine = create_engine(settings.db_sqlite_url, connect_args={'check_same_thread': False}, echo=True)
    return engine


check_db = choose_db(settings.db_sqlite_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=check_db)
