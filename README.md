# API Test Automation

REST API testing with pytest.

## Setup

1. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Run Tests

```powershell
pytest
```

An HTML report (`report.html`) is automatically generated after each test run.

## Project Structure

```
tests/              # Test files
conftest.py         # Pytest fixtures
pytest.ini          # Pytest configuration
requirements.txt    # Dependencies
```

## Dependencies

- pytest
- requests  
- pytest-html
