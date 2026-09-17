"""FastAPI Endpoints Automated Test Suite."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_and_readiness_endpoints():
    r_health = client.get("/api/v1/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "ok"

    r_ready = client.get("/api/v1/ready")
    assert r_ready.status_code == 200
    assert r_ready.json()["status"] == "ready"


def test_create_travel_plan_endpoint():
    payload = {
        "user_query": "Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000.",
    }
    response = client.post("/api/v1/travel/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["status"] in ["waiting_for_approval", "completed"]
    assert len(data["selected_agents"]) == 5
    assert data["is_demo"] is True

    # Test GET session details
    session_id = data["session_id"]
    r_get = client.get(f"/api/v1/travel/{session_id}")
    assert r_get.status_code == 200
    sess_data = r_get.json()
    assert sess_data["session_id"] == session_id
    assert sess_data["destination"] == "Dubai"


def test_approve_plan_endpoint():
    # 1. Create plan
    payload = {"user_query": "Plan a 5-day trip to Dubai"}
    r_create = client.post("/api/v1/travel/plan", json=payload)
    sess_id = r_create.json()["session_id"]

    # 2. Approve plan
    r_approve = client.post(f"/api/v1/travel/{sess_id}/approve", json={"feedback": "Looks great!"})
    assert r_approve.status_code == 200
    assert r_approve.json()["approval_status"] == "approved"


def test_edit_plan_endpoint():
    payload = {"user_query": "Plan a 5-day trip to Dubai"}
    r_create = client.post("/api/v1/travel/plan", json=payload)
    sess_id = r_create.json()["session_id"]

    r_edit = client.post(f"/api/v1/travel/{sess_id}/edit", json={"feedback": "Choose a beachfront resort."})
    assert r_edit.status_code == 200
    assert r_edit.json()["approval_status"] == "edited"


def test_reject_plan_endpoint():
    payload = {"user_query": "Plan a 5-day trip to Dubai"}
    r_create = client.post("/api/v1/travel/plan", json=payload)
    sess_id = r_create.json()["session_id"]

    r_reject = client.post(f"/api/v1/travel/{sess_id}/reject", json={"feedback": "Too expensive."})
    assert r_reject.status_code == 200
    assert r_reject.json()["approval_status"] == "rejected"
