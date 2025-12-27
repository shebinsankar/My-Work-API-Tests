import pytest
import requests
import uuid
from datetime import datetime


@pytest.fixture(scope="session")
def base_url():
    """Base URL"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_session():
    """Create a requests session for API calls"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    yield session
    session.close()


@pytest.fixture(scope="session")
def webhook_url():
    """Webhook URL for testing callbacks"""
    return "https://webhook.site/dffc9b13-9aa0-4da4-8475-cc1a8f0bcb6d"


@pytest.fixture
def job_payload():
    """Job payload for POST requests with unique identifier"""
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    return {
        "userId": 1,
        "action": "create_job",
        "testRunId": unique_id,  # Unique identifier
        "timestamp": timestamp
    }


@pytest.fixture
def unique_test_id():
    """Generate a unique test identifier for data isolation"""
    return str(uuid.uuid4())
