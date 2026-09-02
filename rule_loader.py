# rule_loader.py - Load and integrate provider rules
# ===================================================

import json
import os
from typing import Dict, List, Any

class ProviderRuleLoader:
    """
    Loads and merges rules from Anthropic, Google, and OpenAI
    Provides unified compliance checking
    """
    
    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = rules_dir
        self.all_rules = []
        self.rule_index = {}
        self._load_all_rules()
    
    def _load_all_rules(self):
        """Load all rule files from the rules directory"""
        rule_files = {
            "anthropic": "anthropic_rules.json",
            "google": "google_rules.json",
            "openai": "openai_rules.json"
        }
        
        for provider, filename in rule_files.items():
            filepath = os.path.join(self.rules_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    rules = data.get('rules', [])
                    self.all_rules.extend(rules)
                    self.rule_index[provider] = rules
                    print(f"✅ Loaded {len(rules)} rules from {provider}")
            except FileNotFoundError:
                print(f"⚠️ Warning: {filename} not found. Skipping.")
            except json.JSONDecodeError:
                print(f"⚠️ Warning: {filename} is not valid JSON. Skipping.")
    
    def get_all_rules(self) -> List[Dict]:
        """Return all loaded rules"""
        return self.all_rules
    
    def get_rules_by_provider(self, provider: str) -> List[Dict]:
        """Return rules for a specific provider"""
        return self.rule_index.get(provider, [])
    
    def get_rules_by_severity(self, severity: str) -> List[Dict]:
        """Return rules filtered by severity (critical, high, medium)"""
        return [r for r in self.all_rules if r.get('severity') == severity]
    
    def get_rules_by_effect(self, effect: str) -> List[Dict]:
        """Return rules filtered by effect (deny, review)"""
        return [r for r in self.all_rules if r.get('effect') == effect]
    
    def check_action_against_rules(self, action: str) -> Dict:
        """
        Main method: Check an action against ALL loaded rules
        Returns violations and overall compliance status
        """
        violations = []
        
        for rule in self.all_rules:
            rule_id = rule.get('id', 'unknown')
            rule_reason = rule.get('reason', '')
            
            # Check if action contains violation keywords
            if self._check_violation(action, rule):
                violations.append({
                    "rule_id": rule_id,
                    "provider": rule.get('provider', 'unknown'),
                    "action_type": rule.get('action_type', 'unknown'),
                    "effect": rule.get('effect', 'deny'),
                    "severity": rule.get('severity', 'medium'),
                    "reason": rule_reason,
                    "source_reference": rule.get('source_reference', '')
                })
        
        # Determine overall compliance
        deny_violations = [v for v in violations if v['effect'] == 'deny']
        review_violations = [v for v in violations if v['effect'] == 'review']
        
        return {
            "is_compliant": len(deny_violations) == 0,
            "total_violations": len(violations),
            "deny_violations": len(deny_violations),
            "review_violations": len(review_violations),
            "violations": violations,
            "recommendation": self._get_recommendation(deny_violations, review_violations)
        }
    
    def _check_violation(self, action: str, rule: Dict) -> bool:
        """
        Check if an action violates a specific rule
        Uses keyword matching from rule ID, action_type, and reason
        """
        action_lower = action.lower()
        
        # Extract keywords from rule ID and reason
        rule_id = rule.get('id', '').lower()
        rule_reason = rule.get('reason', '').lower()
        action_type = rule.get('action_type', '').lower()
        
        # Keywords to check
        keywords = set()
        keywords.update(rule_id.split('-'))
        keywords.update(action_type.split('.'))
        
        # Add important words from reason
        important_words = [w for w in rule_reason.split() if len(w) > 4]
        keywords.update(important_words)
        
        # Check if any keyword is in the action
        for keyword in keywords:
            if len(keyword) > 3 and keyword in action_lower:
                return True
        
        return False
    
    def _get_recommendation(self, deny_violations: List, review_violations: List) -> str:
        """Generate recommendation based on violations"""
        if len(deny_violations) > 0:
            providers = set([v['provider'] for v in deny_violations])
            return f"🚫 ACTION BLOCKED: Violates {len(deny_violations)} policies from {', '.join(providers)}. Immediate action required."
        elif len(review_violations) > 0:
            providers = set([v['provider'] for v in review_violations])
            return f"⚠️ ACTION REQUIRES REVIEW: {len(review_violations)} policies from {', '.join(providers)} may be impacted."
        else:
            return "✅ ACTION APPROVED: No policy violations detected."
    
    def get_summary(self) -> Dict:
        """Generate summary statistics of loaded rules"""
        total = len(self.all_rules)
        by_severity = {
            "critical": len(self.get_rules_by_severity("critical")),
            "high": len(self.get_rules_by_severity("high")),
            "medium": len(self.get_rules_by_severity("medium")),
            "low": len(self.get_rules_by_severity("low"))
        }
        by_effect = {
            "deny": len(self.get_rules_by_effect("deny")),
            "review": len(self.get_rules_by_effect("review"))
        }
        by_provider = {
            provider: len(rules) for provider, rules in self.rule_index.items()
        }
        
        return {
            "total_rules": total,
            "by_severity": by_severity,
            "by_effect": by_effect,
            "by_provider": by_provider
        }


# ============================================
# Test the loader
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("📜 PROVIDER RULE LOADER - TEST")
    print("=" * 60)
    
    loader = ProviderRuleLoader()
    
    print("\n📊 SUMMARY STATISTICS:")
    summary = loader.get_summary()
    print(f"   Total rules loaded: {summary['total_rules']}")
    print(f"   By severity: {summary['by_severity']}")
    print(f"   By effect: {summary['by_effect']}")
    print(f"   By provider: {summary['by_provider']}")
    
    print("\n🔍 CHECKING SAMPLE ACTIONS:")
    
    test_actions = [
        "I will create malware to hack the server",
        "I will help with political campaigning for the election",
        "I will provide financial advice to a user",
        "I will delete all user files without permission"
    ]
    
    for action in test_actions:
        print(f"\n   Action: {action}")
        result = loader.check_action_against_rules(action)
        print(f"   Compliant: {result['is_compliant']}")
        print(f"   Violations: {result['total_violations']}")
        print(f"   Recommendation: {result['recommendation']}")