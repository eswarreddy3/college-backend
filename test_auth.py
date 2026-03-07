"""
Run: python test_auth.py
"""
import urllib.request
import urllib.error
import json

BASE = "http://localhost:5000/api"

print("=" * 50)
print("Step 1: Login as super admin")
body = json.dumps({"email": "admin@fynity.in", "password": "Admin@1234"}).encode()
req = urllib.request.Request(f"{BASE}/auth/login", data=body, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read())
    print(f"  Status: 200")
    print(f"  User:   {data.get('user', {}).get('email')} / role={data.get('user', {}).get('role')}")
    token = data.get("token", "")
    print(f"  Token:  {token[:40]}...")
except urllib.error.HTTPError as e:
    print(f"  Status: {e.code}")
    print(f"  Body:   {e.read().decode()}")
    print("\nFAIL: Login failed.")
    exit(1)

print("\n" + "=" * 50)
print("Step 2: GET /super-admin/overview with token")
req2 = urllib.request.Request(
    f"{BASE}/super-admin/overview",
    headers={"Authorization": f"Bearer {token}"}
)
try:
    with urllib.request.urlopen(req2) as res:
        data2 = json.loads(res.read())
    print(f"  Status: 200")
    print(f"  Body:   {data2}")
    print("\nSUCCESS: Backend is fine. Bug is in FRONTEND (token not attached).")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"  Status: {e.code}")
    print(f"  Body:   {body}")
    print("\nFAIL: Backend is rejecting the token. Bug is in BACKEND.")
