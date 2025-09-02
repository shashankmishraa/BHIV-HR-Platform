import requests

BASE_URL = "http://localhost:8000"
API_KEY = "myverysecureapikey123"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def check_headers():
    response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
    
    print("Response Status:", response.status_code)
    print("Response Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
    
    # Check for rate limiting headers specifically
    rate_headers = [h for h in response.headers.keys() if "ratelimit" in h.lower()]
    print(f"\nRate Limiting Headers Found: {rate_headers}")
    
    return rate_headers

if __name__ == "__main__":
    check_headers()