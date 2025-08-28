import httpx

# Test the API directly
API_BASE = "http://localhost:8000"
headers = {"X-API-KEY": "myverysecureapikey123"}

print("Testing API endpoints...")

# Test match endpoint
try:
    response = httpx.get(f"{API_BASE}/v1/match/1/top", headers=headers, timeout=10.0)
    print(f"Match endpoint status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")
        candidates = data.get("top_candidates", [])
        print(f"Number of candidates: {len(candidates)}")
        for i, candidate in enumerate(candidates, 1):
            print(f"  {i}. {candidate.get('name')} (Score: {candidate.get('score')})")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")