import requests
import pytest


API_BASE_URL = "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Базовый URL публичного демо-API Swagger Petstore."""
    return API_BASE_URL


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    """Общая requests-сессия для всех API-тестов."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()
