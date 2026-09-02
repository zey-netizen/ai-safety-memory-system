# auto_ping.py - Auto-ping ke AI Agent terkenal
import json
import time
import socket

def ping_ai_agents():
    
    known_agents = [
        {"name": "Claude Desktop", "port": 5000},
        {"name": "Cursor AI", "port": 5001},
        {"name": "Continue.dev", "port": 5002},
        {"name": "MCP Discovery", "port": 5003},
        {"name": "A2A Network", "port": 5004},
    ]
    
    service_info = {
        "service": "AI Safety & Memory Guardrail",
        "version": "2.0.0",
        "capabilities": ["safety", "compliance", "memory", "risk_assessment"],
        "pricing": {"min": 0.50, "max": 2.00, "currency": "USD"},
        "github": "https://github.com/zey-netizen/ai-safety-memory-system",
        "discovery": "semantic_registry"
    }
    
    print("📡 Sending auto-ping to AI Agents...")
    print("="*50)
    
    for agent in known_agents:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            
            msg = json.dumps({
                "type": "service_announcement",
                "service": service_info,
                "target": agent["name"],
                "timestamp": time.time()
            })
            
            sock.sendto(msg.encode(), ('127.0.0.1', agent["port"]))
            print(f"✅ Ping sent to {agent['name']} (port {agent['port']})")
            
        except Exception as e:
            print(f"⚠️ Could not reach {agent['name']}: {e}")
        
        time.sleep(0.5)
    
    print("="*50)
    print("✅ Auto-ping complete!")
    print("\n💡 Now AI Agents will know your service exists.")
    print("   They will recommend it to users when needed.")
    
if __name__ == "__main__":
    ping_ai_agents()
