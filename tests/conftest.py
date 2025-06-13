import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_orm.models import Base

@pytest.fixture(scope="function")
def session():
    """
    Фикстура для создания чистой сессии базы данных для каждого теста.
    Использует SQLite в памяти.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db_session = SessionLocal()
    
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(engine) 