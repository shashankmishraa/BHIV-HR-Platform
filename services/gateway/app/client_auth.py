"""
Simple client authentication module
"""

def authenticate_client(client_id: str, access_code: str):
    """Simple client authentication - returns client data if valid"""
    # Simple hardcoded authentication for demo
    if client_id == "1" and access_code == "google123":
        return {
            "client_id": 1,
            "client_name": "Google Inc"
        }
    return None

def create_client_token(client_id: int, client_name: str):
    """Create a simple token for client"""
    return f"client_token_{client_id}_{client_name}"

def verify_client_token(token: str = None):
    """Verify client token - simple implementation"""
    if token and token.startswith("client_token_"):
        parts = token.split("_")
        if len(parts) >= 3:
            return {
                "client_id": int(parts[2]),
                "client_name": "_".join(parts[3:])
            }
    return None