from groq import Groq
from utils.npi_api import NPIValidator
import os

class ValidationAgent:
    """Agent 1: Validates provider data against authoritative sources"""
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.npi_validator = NPIValidator()
        self.model = "llama-3.3-70b-versatile"
    
    def validate(self, provider: dict) -> dict:
        """
        Autonomously validates provider data
        Makes independent decisions about validation strategy
        """
        print(f"Validation Agent: Processing {provider.get('name', 'Unknown')}")
        
        validation_results = {
            "agent": "validation",
            "provider": provider,
            "validations": {},
            "confidence": 0.0,
            "decisions": []
        }
        
        # Decision 1: Validate NPI
        npi_result = self.npi_validator.validate_npi(provider.get('npi', ''))
        validation_results["validations"]["npi"] = npi_result
        
        if npi_result["valid"]:
            validation_results["decisions"].append("NPI validated against CMS registry")
            validation_results["confidence"] += 0.4
        else:
            validation_results["decisions"].append(f"NPI validation failed: {npi_result.get('error')}")
        
        # Decision 2: Validate phone format
        phone_valid = self.npi_validator.validate_phone(provider.get('phone', ''))
        validation_results["validations"]["phone"] = phone_valid
        
        if phone_valid:
            validation_results["decisions"].append("Phone format validated")
            validation_results["confidence"] += 0.3
        else:
            validation_results["decisions"].append("Phone format invalid - flagging for review")
        
        # Decision 3: Use LLM for intelligent validation
        llm_analysis = self._llm_validate(provider, validation_results)
        validation_results["llm_analysis"] = llm_analysis
        validation_results["confidence"] += 0.3 if "valid" in llm_analysis.lower() else 0.1
        
        # Autonomous decision: Pass or flag
        if validation_results["confidence"] >= 0.7:
            validation_results["status"] = "VALIDATED"
            validation_results["decisions"].append("AUTONOMOUS DECISION: High confidence - Auto-approved")
        elif validation_results["confidence"] >= 0.4:
            validation_results["status"] = "REVIEW"
            validation_results["decisions"].append("AUTONOMOUS DECISION: Medium confidence - Flagged for human review")
        else:
            validation_results["status"] = "REJECTED"
            validation_results["decisions"].append("AUTONOMOUS DECISION: Low confidence - Rejected")
        
        return validation_results
    
    def _llm_validate(self, provider: dict, current_results: dict) -> str:
        """Use LLM for intelligent validation analysis"""
        try:
            prompt = f"""You are a healthcare data validation expert. Analyze this provider record:

Provider: {provider.get('name')}
NPI: {provider.get('npi')} - {'Valid' if current_results['validations']['npi']['valid'] else 'Invalid'}
Phone: {provider.get('phone')} - {'Valid format' if current_results['validations']['phone'] else 'Invalid format'}
Address: {provider.get('address')}, {provider.get('city')}, {provider.get('state')}

Does this look like a legitimate healthcare provider record? Answer in 1-2 sentences."""

            completion = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"LLM analysis unavailable: {str(e)}"