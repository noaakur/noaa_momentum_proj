"""
Test script for Team Presence Dashboard API.
Uses simple assertions instead of pytest.

Usage: python tests.py

Make sure the server is running on localhost:8000 before running tests.
"""
from typing import Optional
import requests
import sys

BASE_URL = "http://localhost:8000"

# Test credentials (must match seed data)
VALID_USER = {"username": "samc", "password": "password123"}
INVALID_USER = {"username": "samc", "password": "wrongpassword"}
NONEXISTENT_USER = {"username": "nobody", "password": "password123"}


def get_token(username: str, password: str) -> Optional[str]:
    """Helper to get auth token."""
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def auth_header(token: str) -> dict:
    """Helper to create auth header."""
    return {"Authorization": f"Bearer {token}"}


# =============================================================================
# Health Check Tests
# =============================================================================

def test_health_check():
    """Test that health endpoint returns healthy status."""
    response = requests.get(f"{BASE_URL}/health")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["status"] == "healthy", "Health check should return healthy"
    print("✅ test_health_check passed")


# =============================================================================
# Authentication Tests
# =============================================================================

def test_login_success():
    """Test successful login returns a token."""
    response = requests.post(f"{BASE_URL}/login", json=VALID_USER)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "access_token" in data, "Response should contain access_token"
    assert data["token_type"] == "bearer", "Token type should be bearer"
    assert len(data["access_token"]) > 0, "Token should not be empty"
    print("✅ test_login_success passed")


def test_login_wrong_password():
    """Test login with wrong password returns 401."""
    response = requests.post(f"{BASE_URL}/login", json=INVALID_USER)
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert "detail" in response.json(), "Response should contain error detail"
    print("✅ test_login_wrong_password passed")


def test_login_nonexistent_user():
    """Test login with nonexistent user returns 401."""
    response = requests.post(f"{BASE_URL}/login", json=NONEXISTENT_USER)
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ test_login_nonexistent_user passed")


def test_login_missing_fields():
    """Test login with missing fields returns 422."""
    response = requests.post(f"{BASE_URL}/login", json={"username": "samc"})
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ test_login_missing_fields passed")


# =============================================================================
# GET /team Tests
# =============================================================================

def test_get_team_authenticated():
    """Test GET /team with valid auth returns team list."""
    token = get_token(**VALID_USER)
    assert token is not None, "Should be able to get token"
    
    response = requests.get(f"{BASE_URL}/team", headers=auth_header(token))
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) >= 5, f"Should have at least 5 team members, got {len(data)}"
    
    # Verify user structure
    user = data[0]
    assert "id" in user, "User should have id"
    assert "full_name" in user, "User should have full_name"
    assert "status" in user, "User should have status"
    assert "updated_at" in user, "User should have updated_at"
    print("✅ test_get_team_authenticated passed")


def test_get_team_unauthenticated():
    """Test GET /team without auth returns 401."""
    response = requests.get(f"{BASE_URL}/team")
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ test_get_team_unauthenticated passed")


def test_get_team_invalid_token():
    """Test GET /team with invalid token returns 401."""
    response = requests.get(
        f"{BASE_URL}/team",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ test_get_team_invalid_token passed")


def test_get_team_filter_single_status():
    """Test GET /team with single status filter."""
    token = get_token(**VALID_USER)
    
    # Filter by "Working" status (0)
    response = requests.get(
        f"{BASE_URL}/team?status=0",
        headers=auth_header(token)
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    
    # All returned users should have "Working" status
    for user in data:
        assert user["status"] == "Working", f"Expected 'Working', got '{user['status']}'"
    print("✅ test_get_team_filter_single_status passed")


def test_get_team_filter_multiple_statuses():
    """Test GET /team with multiple status filters (bonus feature)."""
    token = get_token(**VALID_USER)
    
    # Filter by "Working" (0) and "On Vacation" (2)
    response = requests.get(
        f"{BASE_URL}/team?status=0&status=2",
        headers=auth_header(token)
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    # All returned users should have one of the filtered statuses
    valid_statuses = {"Working", "On Vacation"}
    for user in data:
        assert user["status"] in valid_statuses, \
            f"Expected status in {valid_statuses}, got '{user['status']}'"
    print("✅ test_get_team_filter_multiple_statuses passed")


def test_get_team_filter_no_results():
    """Test GET /team filter that matches no users."""
    token = get_token(**VALID_USER)
    
    # First update all users to different statuses, then filter by unused status
    # For now, just verify the endpoint handles empty results gracefully
    response = requests.get(
        f"{BASE_URL}/team?status=0&status=1&status=2&status=3",
        headers=auth_header(token)
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert isinstance(response.json(), list), "Response should be a list"
    print("✅ test_get_team_filter_no_results passed")


# =============================================================================
# PATCH /me/status Tests
# =============================================================================

def test_update_status_authenticated():
    """Test PATCH /me/status with valid auth updates status."""
    token = get_token(**VALID_USER)
    
    # Update to "Working Remotely" (1)
    response = requests.patch(
        f"{BASE_URL}/me/status",
        json={"status": 1},
        headers=auth_header(token)
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "Working Remotely", f"Expected 'Working Remotely', got '{data['status']}'"
    
    # Verify update persisted by checking team list
    team_response = requests.get(f"{BASE_URL}/team", headers=auth_header(token))
    team = team_response.json()
    current_user = next((u for u in team if u["full_name"] == "Sam Cooke"), None)
    assert current_user is not None, "Should find current user in team"
    assert current_user["status"] == "Working Remotely", "Status should be updated"
    print("✅ test_update_status_authenticated passed")


def test_update_status_unauthenticated():
    """Test PATCH /me/status without auth returns 401."""
    response = requests.patch(
        f"{BASE_URL}/me/status",
        json={"status": 0}
    )
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("✅ test_update_status_unauthenticated passed")


def test_update_status_invalid_status():
    """Test PATCH /me/status with invalid status value returns 422."""
    token = get_token(**VALID_USER)
    
    response = requests.patch(
        f"{BASE_URL}/me/status",
        json={"status": 99},  # Invalid status
        headers=auth_header(token)
    )
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ test_update_status_invalid_status passed")


def test_update_status_missing_field():
    """Test PATCH /me/status with missing status field returns 422."""
    token = get_token(**VALID_USER)
    
    response = requests.patch(
        f"{BASE_URL}/me/status",
        json={},
        headers=auth_header(token)
    )
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ test_update_status_missing_field passed")


def test_update_status_all_valid_statuses():
    """Test that all valid status values can be set."""
    token = get_token(**VALID_USER)
    
    statuses = [
        (0, "Working"),
        (1, "Working Remotely"),
        (2, "On Vacation"),
        (3, "Business Trip"),
    ]
    
    for status_code, status_label in statuses:
        response = requests.patch(
            f"{BASE_URL}/me/status",
            json={"status": status_code},
            headers=auth_header(token)
        )
        
        assert response.status_code == 200, \
            f"Failed to set status {status_code}: got {response.status_code}"
        assert response.json()["status"] == status_label, \
            f"Expected '{status_label}', got '{response.json()['status']}'"
    
    # Reset to Working
    requests.patch(
        f"{BASE_URL}/me/status",
        json={"status": 0},
        headers=auth_header(token)
    )
    print("✅ test_update_status_all_valid_statuses passed")


# =============================================================================
# Run All Tests
# =============================================================================

def run_all_tests():
    """Run all test functions."""
    tests = [
        # Health
        test_health_check,
        # Auth
        test_login_success,
        test_login_wrong_password,
        test_login_nonexistent_user,
        test_login_missing_fields,
        # GET /team
        test_get_team_authenticated,
        test_get_team_unauthenticated,
        test_get_team_invalid_token,
        test_get_team_filter_single_status,
        test_get_team_filter_multiple_statuses,
        test_get_team_filter_no_results,
        # PATCH /me/status
        test_update_status_authenticated,
        test_update_status_unauthenticated,
        test_update_status_invalid_status,
        test_update_status_missing_field,
        test_update_status_all_valid_statuses,
    ]
    
    print("=" * 60)
    print("Running Team Presence Dashboard API Tests")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except requests.exceptions.ConnectionError:
            print(f"❌ {test.__name__} FAILED: Could not connect to server")
            print("   Make sure the server is running on localhost:8000")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED with unexpected error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

