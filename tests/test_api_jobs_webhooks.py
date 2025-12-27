import pytest
import json
import time


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


@pytest.mark.post
def test_webhook_callback_and_verifiy(base_url, api_session, webhook_url, job_payload):
    """Test creating a job, sending webhook callback, and verifying the webhook received the correct payload."""
    # Create job and get job ID
    endpoint = f"{base_url}/posts"
    job_response = api_session.post(endpoint, json=job_payload)

    assert job_response.status_code == 201, f"Job creation failed with status {job_response.status_code}"

    job_data = job_response.json()
    job_id = job_data.get("id")

    assert job_id is not None, "Job ID should not be None"
    print(f"Job created with ID: {job_id}")

    # Extract webhook token from URL
    webhook_token = webhook_url.split('/')[-1]
    print(f"Using webhook token: {webhook_token}")

    # Send webhook callback with the job ID and status
    callback_payload = {
        "jobId": job_id,
        "status": "completed",
        "timestamp": time.time(),
        "message": "Job processing completed successfully"
    }

    webhook_response = api_session.post(webhook_url, json=callback_payload)

    # Assert webhook POST succeeded
    assert webhook_response.status_code in [200, 201], \
        f"Webhook POST failed with status {webhook_response.status_code}"

    print(
        f"Webhook callback sent - Job {callback_payload['jobId']}: {callback_payload['status']}")

    # Wait briefly for webhook.site to process the request
    time.sleep(2)  # To Do - try removing this sleep later

    # Fetch the last received request from webhook.site API
    webhook_api_url = f"https://webhook.site/token/{webhook_token}/requests?sorting=newest"

    fetch_response = api_session.get(webhook_api_url)

    assert fetch_response.status_code == 200, f"Failed to fetch webhook data with status {fetch_response.status_code}"

    webhook_data = fetch_response.json()
    print("Successfully fetched webhook data")

    # Verify that requests were received
    assert "data" in webhook_data, "Webhook response should contain 'data' field"
    assert len(webhook_data["data"]) > 0, "No requests received by webhook"

    # Get the most recent request
    latest_request = webhook_data["data"][0]
    print(
        f"Found latest webhook request at: {latest_request.get('created_at')}")

    # Parse and verify the received payload
    received_content = latest_request.get("content", "{}")

    # The content might be a string, so parse it if needed
    if isinstance(received_content, str):
        received_payload = json.loads(received_content)
    else:
        received_payload = received_content

    print(f"Received payload: {received_payload}")

    # Assert the received payload matches what we sent
    assert received_payload.get("jobId") == callback_payload["jobId"], \
        f"Job ID mismatch: expected {callback_payload['jobId']}, got {received_payload.get('jobId')}"

    assert received_payload.get("status") == callback_payload["status"], \
        f"Status mismatch: expected {callback_payload['status']}, got {received_payload.get('status')}"

    assert "timestamp" in received_payload, "Timestamp should be present in received payload"
    assert "message" in received_payload, "Message should be present in received payload"

    print("Payload verification successful - All fields match!")
    print(f"  - Job ID: {received_payload['jobId']}")
    print(f"  - Status: {received_payload['status']}")
    print(f"  - Message: {received_payload['message']}")
