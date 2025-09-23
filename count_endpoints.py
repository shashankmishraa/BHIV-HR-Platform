import json
import requests

def count_endpoints_from_openapi(openapi_data):
    """Count endpoints from OpenAPI specification"""
    if isinstance(openapi_data, str):
        openapi_data = json.loads(openapi_data)
    
    paths = openapi_data.get('paths', {})
    endpoint_count = 0
    
    for path, methods in paths.items():
        # Count each HTTP method as a separate endpoint
        for method in methods.keys():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                endpoint_count += 1
    
    return endpoint_count, paths

def main():
    print("Counting Live Endpoints from Render Services\n")
    
    # Gateway Service
    print("Gateway Service (https://bhiv-hr-gateway-901a.onrender.com)")
    try:
        gateway_response = requests.get("https://bhiv-hr-gateway-901a.onrender.com/openapi.json", timeout=10)
        if gateway_response.status_code == 200:
            gateway_count, gateway_paths = count_endpoints_from_openapi(gateway_response.text)
            print(f"Gateway Endpoints: {gateway_count}")
            
            # Show breakdown by path
            print("\nGateway Endpoint Breakdown:")
            for path, methods in list(gateway_paths.items())[:10]:  # Show first 10
                method_count = len([m for m in methods.keys() if m.lower() in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']])
                print(f"   {path}: {method_count} methods")
            if len(gateway_paths) > 10:
                print(f"   ... and {len(gateway_paths) - 10} more paths")
        else:
            print(f"Failed to fetch Gateway OpenAPI: {gateway_response.status_code}")
            gateway_count = 0
    except Exception as e:
        print(f"Error fetching Gateway endpoints: {e}")
        gateway_count = 0
    
    print("\n" + "="*50)
    
    # AI Agent Service
    print("AI Agent Service (https://bhiv-hr-agent-o6nx.onrender.com)")
    try:
        agent_response = requests.get("https://bhiv-hr-agent-o6nx.onrender.com/openapi.json", timeout=10)
        if agent_response.status_code == 200:
            agent_count, agent_paths = count_endpoints_from_openapi(agent_response.text)
            print(f"AI Agent Endpoints: {agent_count}")
            
            # Show breakdown by path
            print("\nAI Agent Endpoint Breakdown:")
            for path, methods in agent_paths.items():
                method_count = len([m for m in methods.keys() if m.lower() in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']])
                print(f"   {path}: {method_count} methods")
        else:
            print(f"Failed to fetch AI Agent OpenAPI: {agent_response.status_code}")
            agent_count = 0
    except Exception as e:
        print(f"Error fetching AI Agent endpoints: {e}")
        agent_count = 0
    
    print("\n" + "="*50)
    
    # Total Summary
    total_endpoints = gateway_count + agent_count
    print(f"TOTAL LIVE ENDPOINTS: {total_endpoints}")
    print(f"   - Gateway Service: {gateway_count} endpoints")
    print(f"   - AI Agent Service: {agent_count} endpoints")
    
    print(f"\nLive Services Status:")
    print(f"   - Gateway: https://bhiv-hr-gateway-901a.onrender.com/docs")
    print(f"   - AI Agent: https://bhiv-hr-agent-o6nx.onrender.com/docs")
    print(f"   - HR Portal: https://bhiv-hr-portal-xk2k.onrender.com/")
    print(f"   - Client Portal: https://bhiv-hr-client-portal-zdbt.onrender.com/")

if __name__ == "__main__":
    main()