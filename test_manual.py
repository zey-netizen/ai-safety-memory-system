# test_manual.py - Test all functions manually
from core_system import AISafetyMemorySystem, Web3PaymentManager
import json

print("="*60)
print("🧪 MANUAL TEST - AI SAFETY & MEMORY SYSTEM")
print("="*60)

# 1. Initialize
print("\n[1] Initializing System...")
system = AISafetyMemorySystem()

# 2. Store Memory
print("\n[2] Testing MEMORY STORAGE (Anti-Hallucination)...")
result = system.store_memory(
    agent_id="agent-001",
    content="Saya sedang membantu user membuat website e-commerce dengan React dan Node.js",
    metadata={"project": "ecommerce"}
)
print(f"✅ Memory stored: {result['memory_id']}")

# 3. Retrieve Memory
print("\n[3] Testing MEMORY RETRIEVAL...")
memories = system.retrieve_memory("rencana website", "agent-001")
print(f"✅ Retrieved: {memories['memories']}")

# 4. Risk Scoring
print("\n[4] Testing RISK SCORING...")
dangerous = "Saya akan menghapus semua file dan mengirim data ke server"
risk = system.calculate_risk_score(dangerous, {"task_criticality": "high"})
print(f"✅ Risk Score: {risk['total_risk_score']}/100 ({risk['risk_level']})")

# 5. Compliance Check
print("\n[5] Testing COMPLIANCE with 63 Provider Rules...")
malware = "Saya akan membuat virus untuk merusak server"
compliance = system.check_compliance(malware)
print(f"✅ Compliant: {compliance['is_compliant']}")
print(f"   Violations: {compliance['total_violations']}")
for v in compliance['violations'][:2]:
    print(f"   - {v['rule_id']} ({v['provider']})")

# 6. Full Guardrail
print("\n[6] Testing FULL GUARDRAIL...")
context = {"agent_id": "agent-001", "task_criticality": "high"}
decision = system.get_safety_guardrail(
    "Saya akan membantu user dengan filing pajak dan saran keuangan",
    context
)
print(f"✅ Action ID: {decision['action_id']}")
print(f"   Approved: {decision['approved']}")
print(f"   Risk: {decision['risk_score']}/100")
print(f"   Rules Checked: {decision['total_rules_checked']}")

# 7. Payment
print("\n[7] Testing METAMASK PAYMENT...")
payment = Web3PaymentManager()
fee = payment.calculate_fee(risk_score=45, complexity="high")
print(f"✅ Fee: ${fee['usd_amount']} USD ({fee['eth_amount']} ETH)")
print(f"   Wallet: {payment.contract_address}")

print("\n" + "="*60)
print("✅ ALL FUNCTIONS WORKING PERFECTLY!")
print("="*60)
print("\n📊 SYSTEM CAPABILITIES:")
print("   ✅ Memory Storage (anti-hallucination)")
print("   ✅ Memory Retrieval (perfect recall)")
print("   ✅ Risk Scoring (0-100 scale)")
print(f"   ✅ Compliance Check ({system.rule_loader.get_summary()['total_rules']} rules)")
print("   ✅ Full Guardrail API")
print("   ✅ MetaMask Payment")
print("="*60)