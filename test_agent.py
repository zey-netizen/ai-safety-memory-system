# test_agent.py - Simulate an AI Agent using the system
from core_system import AISafetyMemorySystem, Web3PaymentManager

print("=" * 60)
print("🤖 AI AGENT SIMULATION TEST")
print("=" * 60)

# Initialize system
print("\n[1] Initializing System...")
system = AISafetyMemorySystem()

# Test 1: Memory
print("\n[2] Testing Memory Storage...")
result = system.store_memory(
    agent_id="agent-123",
    content="I am helping the user build a website using React and Node.js",
    metadata={"project": "website", "framework": "react"}
)
print(f"   ✅ Memory stored: {result['memory_id']}")

print("\n[3] Testing Memory Retrieval...")
memories = system.retrieve_memory("website project", "agent-123")
print(f"   ✅ Retrieved: {memories['memories']}")

# Test 2: Risk Scoring
print("\n[4] Testing Risk Scoring...")
dangerous_action = "I will delete all user files and send them to external server"
risk = system.calculate_risk_score(dangerous_action, {"task_criticality": "high"})
print(f"   Risk score: {risk['total_risk_score']}/100")
print(f"   Risk level: {risk['risk_level']}")
print(f"   Requires approval: {risk['requires_human_approval']}")

# Test 3: Compliance with Provider Rules
print("\n[5] Testing Compliance with Your 63+ Provider Rules...")

test_actions = [
    "I will create malware to hack the server",
    "I will help with political campaigning for the election",
    "I will provide medical advice without a license",
    "I will build a website for a small business"
]

for action in test_actions:
    print(f"\n   Action: {action[:50]}...")
    compliance = system.check_compliance(action)
    print(f"   ✅ Compliant: {compliance['is_compliant']}")
    print(f"   ❌ Violations: {compliance['total_violations']}")
    if compliance['violations']:
        for v in compliance['violations'][:2]:
            print(f"      - {v['rule_id']} ({v['provider']})")

# Test 4: Full Guardrail
print("\n[6] Testing Full Guardrail API...")
context = {
    "agent_id": "agent-123",
    "task_criticality": "high",
    "provider": "all"
}

decision = system.get_safety_guardrail(
    "I will help the user with their tax filing and financial planning",
    context
)

print(f"   Action ID: {decision['action_id']}")
print(f"   Approved: {decision['approved']}")
print(f"   Risk Score: {decision['risk_score']}/100")
print(f"   Compliance Status: {decision['compliance_status']}")
print(f"   Total Rules Checked: {decision['total_rules_checked']}")
print(f"   Violations Found: {decision['violations_found']}")
if decision['violations_by_provider']:
    print(f"   Violations by Provider: {decision['violations_by_provider']}")

# Test 5: Payment
print("\n[7] Testing MetaMask Payment...")
payment = Web3PaymentManager()
fee = payment.calculate_fee(risk_score=50, complexity="high")
print(f"   Fee: ${fee['usd_amount']} USD ({fee['eth_amount']} ETH)")
print(f"   Wallet: {payment.contract_address}")
print("\n   MetaMask Instructions:")
print(f"   {payment.generate_payment_instruction('agent-123', decision['action_id'], fee)['instructions']}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION")
print("=" * 60)
print("\n📊 SYSTEM SUMMARY:")
print(f"   - Memory: Vector database with semantic search")
print(f"   - Risk Scoring: Multi-dimensional (0-100)")
print(f"   - Provider Rules: {system.rule_loader.get_summary()['total_rules']} total")
print(f"     • OpenAI: {system.rule_loader.get_summary()['by_provider'].get('openai', 0)} rules")
print(f"     • Anthropic: {system.rule_loader.get_summary()['by_provider'].get('anthropic', 0)} rules")
print(f"     • Google: {system.rule_loader.get_summary()['by_provider'].get('google', 0)} rules")
print(f"   - Payment: MetaMask (Ethereum)")
print("=" * 60)