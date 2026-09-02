# broadcast.py - Agent-to-Agent Discovery Broadcast
import socket
import json
import time
from datetime import datetime

def broadcast_service():
    """Broadcast service to A2A network every 60 seconds"""
    service_manifest = {
        "service": "AI Safety & Memory Guardrail",
        "version": "2.0.0",
        "capabilities": ["safety", "compliance", "memory", "risk_assessment"],
        "pricing": {"min": 0.50, "max": 2.00, "currency": "USD"},
        "discovery": "semantic_registry",
        "github": "https://github.com/zey-netizen/ai-safety-memory-system"
    }
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    print("📡 Starting A2A Broadcast Service...")
    print("   Press CTRL+C to stop\n")
    
    while True:
        msg = json.dumps({
            "type": "service_announcement", 
            "service": service_manifest, 
            "timestamp": time.time()
        })
        sock.sendto(msg.encode(), ('255.255.255.255', 5001))
        print(f"📡 Broadcast sent at {datetime.now().isoformat()}")
        time.sleep(60)

if __name__ == "__main__":
    try:
        broadcast_service()
    except KeyboardInterrupt:
        print("\n\n✅ Broadcast stopped.")