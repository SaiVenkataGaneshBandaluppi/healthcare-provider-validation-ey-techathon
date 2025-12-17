from datetime import datetime
import json

class ManagementAgent:
    """Agent 4: Workflow management and audit trail"""
    
    def __init__(self):
        pass
    
    def manage(self, provider: dict, validation_results: dict, enrichment_results: dict, qa_results: dict) -> dict:
        """
        Goal-driven workflow orchestration
        Manages audit trail and final decisions
        """
        print(f"Management Agent: Finalizing {provider.get('name', 'Unknown')}")
        
        management_results = {
            "agent": "management",
            "workflow_status": "completed",
            "audit_trail": [],
            "final_record": {},
            "decisions": []
        }
        
        # Decision 1: Create comprehensive audit trail
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "provider_npi": provider.get('npi'),
            "validation_status": validation_results.get("status"),
            "validation_confidence": validation_results.get("confidence"),
            "enrichments_applied": list(enrichment_results.get("enrichments", {}).keys()),
            "qa_status": qa_results.get("final_status"),
            "final_confidence": qa_results.get("final_confidence")
        }
        
        management_results["audit_trail"].append(audit_entry)
        management_results["decisions"].append("Audit trail created for compliance")
        
        # Decision 2: Compile final provider record
        final_record = {
            **provider,
            "specialty": enrichment_results.get("enrichments", {}).get("specialty", provider.get("specialty")),
            "standardized_address": enrichment_results.get("enrichments", {}).get("standardized_address"),
            "network_status": enrichment_results.get("enrichments", {}).get("network"),
            "validation_status": qa_results.get("final_status"),
            "confidence_score": round(qa_results.get("final_confidence", 0), 2),
            "processed_at": datetime.now().isoformat(),
            "audit_log": management_results["audit_trail"]
        }
        
        management_results["final_record"] = final_record
        
        # Decision 3: Determine next actions
        if qa_results.get("final_status") == "APPROVED":
            management_results["next_actions"] = ["Publish to directory", "Notify member services"]
            management_results["decisions"].append("GOAL-DRIVEN: Record approved for publication")
        elif qa_results.get("final_status") == "NEEDS_REVIEW":
            management_results["next_actions"] = ["Queue for human review", "Escalate to provider relations"]
            management_results["decisions"].append("GOAL-DRIVEN: Routing to manual review queue")
        else:
            management_results["next_actions"] = ["Archive", "Request provider to resubmit data"]
            management_results["decisions"].append("GOAL-DRIVEN: Record rejected, requesting resubmission")
        
        return management_results