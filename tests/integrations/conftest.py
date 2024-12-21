import pytest
from unittest.mock import MagicMock
from app.website.application import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Настройка для использования ин-мемори базы данных для тестов
TEST_DATABASE_URI = 'sqlite:///:memory:'


@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()
    mock_session.query = MagicMock()
    return mock_session


@pytest.fixture
def app():
    app = create_app()
    yield app
    with app.app_context():
        # выполнение кода после завершения теста, например очистка базы данных.
        pass


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(TEST_DATABASE_URI)
    yield engine
    engine.dispose()


@pytest.fixture(scope='session')
def session_factory(engine):
    Session = scoped_session(sessionmaker(bind=engine))
    yield Session
    Session.remove()


@pytest.fixture(scope='function')  # scope='function' означает, что фикстура создается для каждого теста
def db_session(session_factory, request):
    session = session_factory()
    yield session
    session.rollback()  # отменяем транзакции после каждого теста
    session.close()
