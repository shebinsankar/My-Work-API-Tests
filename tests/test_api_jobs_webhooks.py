import pytest


@pytest.mark.post
@pytest.mark.smoke
def test_create_job(base_url, api_session, job_payload):
    """Test job creation via POST request"""
    endpoint = f"{base_url}/posts"

    # Send POST request
    response = api_session.post(endpoint, json=job_payload)

    # Assert status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Parse response
    response_data = response.json()
    print("Response Data:", response_data)

    # Assert response contains ID
    assert "id" in response_data, "Response should contain 'id' field"
    assert response_data["id"] is not None, "ID should not be None"

    # Assert payload data is echoed back
    assert response_data.get("userId") == job_payload["userId"]
    assert response_data.get("action") == job_payload["action"]


@pytest.mark.post
def test_webhook_callback(base_url, api_session, webhook_url, job_payload):
    """Test creating a job and sending webhook callback with the job ID"""
    # Create job and get job ID
    endpoint = f"{base_url}/posts"
    job_response = api_session.post(endpoint, json=job_payload)

    assert job_response.status_code == 201, f"Job creation failed with status {job_response.status_code}"

    job_data = job_response.json()
    job_id = job_data.get("id")

    assert job_id is not None, "Job ID should not be None"
    print(f"Job created with ID: {job_id}")

    # Send webhook callback with the job ID and status
    callback_payload = {
        "jobId": job_id,
        "status": "completed"
    }

    # Send POST request to webhook
    response = api_session.post(webhook_url, json=callback_payload)

    # Assert webhook response status
    assert response.status_code in [200, 201], \
        f"Webhook POST failed with status {response.status_code}"

    print(
        f"Webhook callback sent successfully - Job {callback_payload['jobId']}: {callback_payload['status']}")
