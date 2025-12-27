# API Test Automation - Job Creation & Webhook Callback Tests

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

**Run all tests**:
```powershell
pytest
```

An HTML report (`report.html`) is automatically generated after each test run.

### Fixtures (conftest.py)

- `base_url`: Public API endpoint (jsonplaceholder.typicode.com)
- `api_session`: Configured requests session
- `webhook_url`: webhook.site endpoint for callbacks
- `job_payload`: Default job creation payload

**Note**: Update the `webhook_url` fixture in `conftest.py` with your own webhook.site URL for testing.

## Project Structure

```
tests/                              # Test files
  test_api_jobs_webhooks.py         # Job and webhook tests
conftest.py                         # Pytest fixtures
pytest.ini                          # Pytest configuration
requirements.txt                    # Dependencies
report.html                         # Generated test report
```

## Dependencies

- pytest - Testing framework
- requests - HTTP client library
- pytest-html - HTML report generation


## 1. CI & Longevity: If this test suite had to run in CI for years, what would you change in your design to keep it stable and fast?

1. Use small mock server to simulate the job API and webhook callbacks so the tests are fully under control(Mock server, Flask).
2. Separate or group tests which are fast tests and integration tests.
3. Make tests independent - reduce dependency on previous tests.
4. Avoid sleeping in the code - instead use poll timeouts and add wait conditions.
5. Fail the suite fast when core tests fail. Separate flaky tests.
6. Add more logging/reports features for easy debug of failures.
7. No hard coded variables and secrets - use vault, configuration per stage/environment.
8. Use unique data per test, avoid shared file systems and no rely on execution order.


## 2. Observability & Debugging: If the webhook sometimes never arrived in CI but worked locally, how would you debug and stabilize it?

1. Logging - Add timestamps and full HTTP headers/bodies to logs for each webhook POST.
2. Improve retry logics.
3. Check on the network restrictions and firewalls blocks.
4. Poll webhook api's multiple times to record the delays.
5. Use fallback verification methods.
6. Setup failure alerts, use dashboards provided or use monitoring tools such as Grafana.


## 3. Data & Isolation: How would you ensure test data isolation in a shared environment?

1. Maintain isolated staging/test environments. Generate test data at test setup instead of reusing shared records.
2. Tear down data - Delete the test data after execution using cleanup jobs
3. Use unique identifiers and run identifiers for each test run to avoid data collisions
4. Avoid cross-test dependencies: No test should rely on data produced by another test.
5. Use transaction-rollback tests by running each test inside its own database transaction and rolling it back at the end so all test data is automatically discarded.
6. Use test containers for data isolations.
7. Ensure tests don't rely on shared state or global resources that could conflict.