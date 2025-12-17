from groq import Groq
import os

class QAAgent:
    """Agent 3: Quality assurance and cross-validation"""
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
    
    def quality_check(self, provider: dict, validation_results: dict, enrichment_results: dict) -> dict:
        """
        Self-correcting quality assurance
        Identifies inconsistencies and makes corrections
        """
        print(f"QA Agent: Cross-validating {provider.get('name', 'Unknown')}")
        
        qa_results = {
            "agent": "qa",
            "checks": {},
            "corrections": [],
            "final_confidence": 0.0,
            "decisions": []
        }
        
        # Check 1: Cross-validate name consistency
        original_name = provider.get('name', '')
        npi_name = validation_results.get("validations", {}).get("npi", {}).get("name", '')
        
        if npi_name and original_name:
            name_match = self._compare_names(original_name, npi_name)
            qa_results["checks"]["name_consistency"] = name_match
            
            if not name_match:
                qa_results["corrections"].append(f"Name mismatch detected: '{original_name}' vs '{npi_name}'")
                qa_results["decisions"].append("🔧 SELF-CORRECTION: Flagging name inconsistency")
            else:
                qa_results["decisions"].append("Name consistency verified")
        
        # Check 2: Validate enrichment quality
        specialty = enrichment_results.get("enrichments", {}).get("specialty", "")
        if specialty and specialty != "General Practice":
            qa_results["checks"]["specialty_confidence"] = "high"
            qa_results["decisions"].append(f"Specialty '{specialty}' appears valid")
        else:
            qa_results["checks"]["specialty_confidence"] = "low"
            qa_results["decisions"].append("Specialty confidence low - may need verification")
        
        # Check 3: Overall confidence calculation
        validation_conf = validation_results.get("confidence", 0)
        enrichment_quality = 0.9 if qa_results["checks"].get("specialty_confidence") == "high" else 0.6
        consistency_score = 1.0 if qa_results["checks"].get("name_consistency", True) else 0.5
        
        qa_results["final_confidence"] = (validation_conf * 0.5) + (enrichment_quality * 0.3) + (consistency_score * 0.2)
        
        # Autonomous decision on final status
        if qa_results["final_confidence"] >= 0.85:
            qa_results["final_status"] = "APPROVED"
            qa_results["decisions"].append("AUTONOMOUS DECISION: High quality - Approved")
        elif qa_results["final_confidence"] >= 0.6:
            qa_results["final_status"] = "NEEDS_REVIEW"
            qa_results["decisions"].append("AUTONOMOUS DECISION: Quality check - Needs review")
        else:
            qa_results["final_status"] = "REJECTED"
            qa_results["decisions"].append("AUTONOMOUS DECISION: Quality too low - Rejected")
        
        return qa_results
    
    def _compare_names(self, name1: str, name2: str) -> bool:
        """Simple name comparison"""
        n1 = name1.lower().replace('.', '').replace(',', '')
        n2 = name2.lower().replace('.', '').replace(',', '')
        
        # Check if major parts match
        n1_parts = set(n1.split())
        n2_parts = set(n2.split())
        
        overlap = len(n1_parts & n2_parts)
        return overlap >= 2  # At least 2 name parts match