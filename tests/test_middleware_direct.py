#!/usr/bin/env python3
"""
Direct test of HTTP method handling middleware
Tests the middleware implementation directly without external services
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import time
import threading
from datetime import datetime

# Create test FastAPI app with our middleware
app = FastAPI(title="HTTP Method Test App", version="1.0.0")

# HTTP Method Handler Middleware (MUST be first)
@app.middleware("http")
async def http_method_handler(request: Request, call_next):
    """Handle HTTP methods including HEAD and OPTIONS requests"""
    method = request.method
    path = request.url.path
    
    print(f"Middleware processing: {method} {path}")
    
    # Handle HEAD requests by converting to GET and removing body
    if method == "HEAD":
        # Create new request with GET method
        get_request = Request(
            scope={
                **request.scope,
                "method": "GET"
            }
        )
        response = await call_next(get_request)
        # Remove body content for HEAD response but keep headers
        return Response(
            content="",
            status_code=response.status_code,
            headers=response.headers,
            media_type=response.media_type
        )
    
    # Handle OPTIONS requests for CORS preflight
    elif method == "OPTIONS":
        return Response(
            content="",
            status_code=200,
            headers={
                "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "86400"
            }
        )
    
    # Handle unsupported methods
    elif method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return PlainTextResponse(
            content=f"Method {method} not allowed. Supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS",
            status_code=405,
            headers={
                "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"
            }
        )
    
    return await call_next(request)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

# Test endpoints
@app.get("/")
@app.head("/")
def read_root():
    return {"message": "Test API", "methods_supported": ["GET", "HEAD", "OPTIONS"]}

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/test")
@app.head("/test")
@app.options("/test")
def test_endpoint():
    return {"test": "success", "methods": ["GET", "HEAD", "OPTIONS"]}

def run_test_server():
    """Run test server in background"""
    uvicorn.run(app, host="127.0.0.1", port=8888, log_level="error")

def test_middleware():
    """Test the middleware implementation"""
    print("HTTP Method Middleware Direct Test")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Start test server in background
    server_thread = threading.Thread(target=run_test_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    base_url = "http://127.0.0.1:8888"
    
    # Test cases
    test_cases = [
        ("GET /", "GET", f"{base_url}/"),
        ("HEAD /", "HEAD", f"{base_url}/"),
        ("OPTIONS /", "OPTIONS", f"{base_url}/"),
        ("GET /health", "GET", f"{base_url}/health"),
        ("HEAD /health", "HEAD", f"{base_url}/health"),
        ("OPTIONS /health", "OPTIONS", f"{base_url}/health"),
        ("GET /test", "GET", f"{base_url}/test"),
        ("HEAD /test", "HEAD", f"{base_url}/test"),
        ("OPTIONS /test", "OPTIONS", f"{base_url}/test"),
        ("TRACE / (unsupported)", "TRACE", f"{base_url}/"),
    ]
    
    results = {}
    
    for test_name, method, url in test_cases:
        try:
            if method == "GET":
                response = requests.get(url, timeout=2)
            elif method == "HEAD":
                response = requests.head(url, timeout=2)
            elif method == "OPTIONS":
                response = requests.options(url, timeout=2)
            elif method == "TRACE":
                response = requests.request("TRACE", url, timeout=2)
            
            status = response.status_code
            
            if method in ["GET"] and status == 200:
                results[test_name] = "PASSED"
                print(f"  {test_name}: PASSED (200)")
            elif method == "HEAD" and status == 200:
                if len(response.content) == 0:
                    results[test_name] = "PASSED"
                    print(f"  {test_name}: PASSED (200, no body)")
                else:
                    results[test_name] = "FAILED"
                    print(f"  {test_name}: FAILED (200, has body: {len(response.content)} bytes)")
            elif method == "OPTIONS" and status == 200:
                if 'Allow' in response.headers:
                    results[test_name] = "PASSED"
                    print(f"  {test_name}: PASSED (200, Allow: {response.headers['Allow']})")
                else:
                    results[test_name] = "FAILED"
                    print(f"  {test_name}: FAILED (200, no Allow header)")
            elif method == "TRACE" and status == 405:
                results[test_name] = "PASSED"
                print(f"  {test_name}: PASSED (405 - correctly rejected)")
            else:
                results[test_name] = "FAILED"
                print(f"  {test_name}: FAILED (Status: {status})")
                
        except Exception as e:
            results[test_name] = "ERROR"
            print(f"  {test_name}: ERROR - {str(e)}")
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result == "PASSED")
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    if passed == total:
        print("\nSUCCESS: All middleware tests passed!")
        print("The HTTP method handling middleware is working correctly.")
    else:
        print(f"\nPARTIAL: {passed}/{total} tests passed")
        print("Some middleware functionality may need adjustment.")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_middleware()