import requests
import re
from typing import Dict, Optional

class NPIValidator:
    """Validates provider data using NPPES NPI Registry API"""
    
    BASE_URL = "https://npiregistry.cms.hhs.gov/api/"
    
    @staticmethod
    def validate_npi(npi: str) -> Dict:
        """Validate NPI number against CMS registry"""
        try:
            # Clean NPI
            npi_clean = re.sub(r'\D', '', str(npi))
            
            if len(npi_clean) != 10:
                return {
                    "valid": False,
                    "error": "NPI must be 10 digits",
                    "npi": npi
                }
            
            # Call NPPES API
            params = {
                "number": npi_clean,
                "version": "2.1"
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("result_count", 0) > 0:
                    result = data["results"][0]
                    basic = result.get("basic", {})
                    
                    return {
                        "valid": True,
                        "npi": npi_clean,
                        "name": f"{basic.get('first_name', '')} {basic.get('last_name', '')}".strip(),
                        "credential": basic.get("credential", ""),
                        "status": basic.get("status", ""),
                        "data": result
                    }
                else:
                    return {
                        "valid": False,
                        "error": "NPI not found in registry",
                        "npi": npi_clean
                    }
            else:
                return {
                    "valid": False,
                    "error": f"API error: {response.status_code}",
                    "npi": npi_clean
                }
                
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}",
                "npi": npi
            }
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        phone_clean = re.sub(r'\D', '', str(phone))
        return len(phone_clean) == 10
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))