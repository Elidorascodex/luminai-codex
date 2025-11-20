#!/usr/bin/env python3
"""Cleaned test script for user anonymization endpoints.

This runs a small sequence of API checks against the backend at
http://localhost:8000. It is intentionally simple and uses only
the requests package so it remains flake8-friendly.
"""

from pathlib import Path
import sys
import requests

BASE_URL = "http://localhost:8000"


def _ensure_ok(resp):
    if resp.status_code != 200:
        print(f"❌ Failed: {resp.status_code} - {resp.text}")
        #!/usr/bin/env python3
        """Test script for user anonymization endpoints

        This is a compact and flake8-friendly test script that runs a simple
        sequence of HTTP checks against a local backend at http://localhost:8000.
        It is intended for manual developer use only.
        """

        import sys
        import requests

        BASE_URL = "http://localhost:8000"


        def _ensure_ok(resp):
            if resp.status_code != 200:
                print(f"❌ Failed: {resp.status_code} - {resp.text}")
                return False
            return True


        def test_create_profile():
            """Create a user profile and return the new user_id."""
            resp = requests.post(
                f"{BASE_URL}/api/user/profile",
                params={
                    "moniker": "TestStarGazer42",
                    "data_retention": "minimal",
                    "consent_analytics": False,
                },
                json={"age_band": "18-42", "region_band": "Eastern US"},
            )
            if not _ensure_ok(resp):
                return None
            return resp.json().get("user_id")


        def test_get_profile(user_id):
            resp = requests.get(f"{BASE_URL}/api/user/profile/{user_id}")
            return _ensure_ok(resp)


        def test_start_session(user_id):
            resp = requests.post(f"{BASE_URL}/api/user/session/start", params={"user_id": user_id})
            if not _ensure_ok(resp):
                return None
            return resp.json().get("session_id")


        def test_end_session(session_id):
            resp = requests.post(
                f"{BASE_URL}/api/user/session/end",
                params={"session_id": session_id, "summary": "Test session completed"},
            )
            return _ensure_ok(resp)


        def test_export_data(user_id):
            resp = requests.post(f"{BASE_URL}/api/user/export", params={"user_id": user_id})
            return _ensure_ok(resp)


        def test_delete_account(user_id):
            resp = requests.delete(
                f"{BASE_URL}/api/user/delete",
                json={"user_id": user_id, "confirmation_token": "I_CONFIRM_DELETE", "delete_all": True},
            )
            if not _ensure_ok(resp):
                return False
            # verify deletion
            verify = requests.get(f"{BASE_URL}/api/user/profile/{user_id}")
            return verify.status_code == 404


        def main():
            print("Running user anonymization smoke tests against backend")
            try:
                resp = requests.get(f"{BASE_URL}/docs")
                if resp.status_code != 200:
                    print(f"❌ Backend responded {resp.status_code}")
                    sys.exit(1)
            except requests.exceptions.ConnectionError:
                print(f"❌ Backend is not running at {BASE_URL}")
                print("Start with: cd backend && uvicorn main:app --reload")
                sys.exit(1)

            user_id = test_create_profile()
            if not user_id:
                sys.exit(1)
            if not test_get_profile(user_id):
                sys.exit(1)
            session_id = test_start_session(user_id)
            if not session_id:
                sys.exit(1)
            if not test_end_session(session_id):
                sys.exit(1)
            if not test_export_data(user_id):
                sys.exit(1)
            if not test_delete_account(user_id):
                sys.exit(1)
            print("✅ All tests passed")


        if __name__ == "__main__":
            main()

