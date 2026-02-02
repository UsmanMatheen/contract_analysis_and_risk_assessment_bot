"""Template manager for standardized contract templates."""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from config.settings import get_settings
from src.llm_handler import LLMHandler
from src.utils import get_logger

logger = get_logger()


class TemplateManager:
    """
    Manages standardized SME-friendly contract templates.
    
    Features:
    - Pre-built template library
    - Custom template generation
    - Template customization
    - Variable substitution
    """
    
    def __init__(self):
        """Initialize template manager."""
        self.settings = get_settings()
        self.templates_dir = self.settings.TEMPLATES_DIR
        self.llm_handler = None  # Lazy load
        
        # Create templates directory if not exists
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize default templates
        self._initialize_default_templates()
        
        logger.info("TemplateManager initialized")
    
    def _initialize_default_templates(self):
        """Initialize default contract templates."""
        default_templates = {
            'employment_agreement': self._get_employment_template(),
            'service_contract': self._get_service_template(),
            'nda': self._get_nda_template(),
            'consultancy_agreement': self._get_consultancy_template(),
            'vendor_contract': self._get_vendor_template()
        }
        
        for template_name, template_content in default_templates.items():
            template_file = self.templates_dir / f"{template_name}.json"
            if not template_file.exists():
                self._save_template(template_name, template_content)
                logger.info(f"Created default template: {template_name}")
    
    def get_template(self, template_name: str) -> Dict[str, Any]:
        """
        Get template by name.
        
        Args:
            template_name: Template identifier
            
        Returns:
            Template dictionary
        """
        template_file = self.templates_dir / f"{template_name}.json"
        
        if not template_file.exists():
            raise ValueError(f"Template not found: {template_name}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_templates(self) -> List[Dict[str, str]]:
        """
        List all available templates.
        
        Returns:
            List of template metadata
        """
        templates = []
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template = json.load(f)
                    templates.append({
                        'name': template_file.stem,
                        'title': template.get('title', template_file.stem),
                        'description': template.get('description', ''),
                        'category': template.get('category', 'General')
                    })
            except Exception as e:
                logger.warning(f"Error loading template {template_file}: {str(e)}")
                continue
        
        return templates
    
    def generate_contract(
        self,
        template_name: str,
        variables: Dict[str, str]
    ) -> str:
        """
        Generate contract from template with variables.
        
        Args:
            template_name: Template to use
            variables: Dictionary of variable values
            
        Returns:
            Generated contract text
        """
        template = self.get_template(template_name)
        contract_text = template['content']
        
        # Substitute variables
        for var_name, var_value in variables.items():
            placeholder = f"[{var_name.upper()}]"
            contract_text = contract_text.replace(placeholder, var_value)
        
        return contract_text
    
    def _save_template(self, template_name: str, template_data: Dict[str, Any]):
        """Save template to file."""
        template_file = self.templates_dir / f"{template_name}.json"
        
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
    
    def _get_employment_template(self) -> Dict[str, Any]:
        """Get employment agreement template."""
        return {
            'title': 'Employment Agreement',
            'description': 'Standard employment agreement for Indian companies',
            'category': 'Employment',
            'variables': [
                'COMPANY_NAME', 'EMPLOYEE_NAME', 'POSITION', 'START_DATE',
                'SALARY', 'LOCATION', 'NOTICE_PERIOD'
            ],
            'content': '''EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into on [START_DATE] between:

[COMPANY_NAME], a company registered under the Companies Act, 2013 ("Employer")
AND
[EMPLOYEE_NAME], residing at [LOCATION] ("Employee")

1. POSITION AND DUTIES
The Employee is appointed as [POSITION] and shall perform duties as reasonably assigned by the Employer.

2. COMPENSATION
The Employee shall receive a gross salary of INR [SALARY] per annum, payable monthly on the last working day of each month.

3. TERM AND TERMINATION
3.1 This Agreement shall commence on [START_DATE] and continue until terminated by either party.
3.2 Either party may terminate with [NOTICE_PERIOD] days written notice.
3.3 The Employer may terminate immediately for cause including misconduct or breach of duties.

4. WORKING HOURS
The Employee shall work standard business hours with flexibility as required by the position.

5. LEAVE ENTITLEMENT
The Employee is entitled to leave as per company policy and applicable labor laws.

6. CONFIDENTIALITY
The Employee shall maintain confidentiality of all proprietary information during and after employment.

7. INTELLECTUAL PROPERTY
All work products created during employment shall be the property of the Employer.

8. NON-COMPETE
The Employee agrees not to engage in competing business for [6] months post-termination within [50] km radius.

9. GOVERNING LAW
This Agreement shall be governed by the laws of India. Disputes shall be resolved through arbitration in [LOCATION].

IN WITNESS WHEREOF, the parties have executed this Agreement.

_____________________          _____________________
[COMPANY_NAME]                 [EMPLOYEE_NAME]
Authorized Signatory           Employee

Date: [START_DATE]
'''
        }
    
    def _get_service_template(self) -> Dict[str, Any]:
        """Get service contract template."""
        return {
            'title': 'Service Contract',
            'description': 'General service agreement for service providers',
            'category': 'Services',
            'variables': [
                'CLIENT_NAME', 'SERVICE_PROVIDER_NAME', 'SERVICE_DESCRIPTION',
                'CONTRACT_VALUE', 'START_DATE', 'END_DATE', 'PAYMENT_TERMS'
            ],
            'content': '''SERVICE AGREEMENT

This Service Agreement ("Agreement") is made on [START_DATE] between:

[CLIENT_NAME] ("Client")
AND
[SERVICE_PROVIDER_NAME] ("Service Provider")

1. SERVICES
The Service Provider shall provide the following services: [SERVICE_DESCRIPTION]

2. TERM
This Agreement shall be effective from [START_DATE] to [END_DATE].

3. COMPENSATION
3.1 The Client shall pay INR [CONTRACT_VALUE] for the services.
3.2 Payment terms: [PAYMENT_TERMS]

4. DELIVERABLES
The Service Provider shall deliver all agreed deliverables within the specified timelines.

5. TERMINATION
Either party may terminate with 30 days written notice. Early termination requires payment for work completed.

6. CONFIDENTIALITY
Both parties shall maintain confidentiality of proprietary information.

7. LIMITATION OF LIABILITY
Liability is limited to the contract value. Neither party liable for consequential damages.

8. DISPUTE RESOLUTION
Disputes shall be resolved through arbitration under Indian Arbitration and Conciliation Act, 1996.

IN WITNESS WHEREOF:

_____________________          _____________________
[CLIENT_NAME]                  [SERVICE_PROVIDER_NAME]
'''
        }
    
    def _get_nda_template(self) -> Dict[str, Any]:
        """Get NDA template."""
        return {
            'title': 'Non-Disclosure Agreement (NDA)',
            'description': 'Mutual non-disclosure agreement',
            'category': 'Confidentiality',
            'variables': [
                'PARTY1_NAME', 'PARTY2_NAME', 'PURPOSE', 'DURATION', 'DATE'
            ],
            'content': '''NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is made on [DATE] between:

[PARTY1_NAME] ("Disclosing Party")
AND
[PARTY2_NAME] ("Receiving Party")

1. PURPOSE
The parties wish to explore [PURPOSE] and will share confidential information.

2. CONFIDENTIAL INFORMATION
Includes all technical, business, and financial information disclosed by either party.

3. OBLIGATIONS
3.1 The Receiving Party shall maintain confidentiality and not disclose to third parties.
3.2 Information shall be used solely for the stated purpose.
3.3 Reasonable measures shall be taken to protect confidential information.

4. EXCLUSIONS
This Agreement does not apply to information that:
a) Is publicly available
b) Was known before disclosure
c) Is independently developed
d) Is required to be disclosed by law

5. TERM
This Agreement shall remain in effect for [DURATION] years from the date of signing.

6. RETURN OF INFORMATION
Upon request, all confidential materials shall be returned or destroyed.

7. GOVERNING LAW
This Agreement is governed by the laws of India.

_____________________          _____________________
[PARTY1_NAME]                  [PARTY2_NAME]
'''
        }
    
    def _get_consultancy_template(self) -> Dict[str, Any]:
        """Get consultancy agreement template."""
        return {
            'title': 'Consultancy Agreement',
            'description': 'Independent consultant engagement agreement',
            'category': 'Consultancy',
            'variables': [
                'COMPANY_NAME', 'CONSULTANT_NAME', 'SCOPE', 'FEES',
                'START_DATE', 'END_DATE', 'PAYMENT_SCHEDULE'
            ],
            'content': '''CONSULTANCY AGREEMENT

Agreement made on [START_DATE] between:

[COMPANY_NAME] ("Company")
AND
[CONSULTANT_NAME] ("Consultant")

1. SCOPE OF WORK
The Consultant shall provide the following services: [SCOPE]

2. TERM
From [START_DATE] to [END_DATE], renewable by mutual agreement.

3. COMPENSATION
3.1 Fees: INR [FEES]
3.2 Payment Schedule: [PAYMENT_SCHEDULE]
3.3 Reimbursement of pre-approved expenses with receipts.

4. INDEPENDENT CONTRACTOR
The Consultant is an independent contractor, not an employee.

5. DELIVERABLES AND TIMELINE
The Consultant shall deliver work as per agreed timeline and quality standards.

6. CONFIDENTIALITY
All company information shall be kept confidential.

7. INTELLECTUAL PROPERTY
Work products shall belong to the Company unless otherwise agreed.

8. TERMINATION
Either party may terminate with 15 days notice.

9. INDEMNIFICATION
Each party indemnifies the other for breaches of their obligations.

10. GOVERNING LAW
This Agreement is governed by Indian law.

_____________________          _____________________
[COMPANY_NAME]                 [CONSULTANT_NAME]
'''
        }
    
    def _get_vendor_template(self) -> Dict[str, Any]:
        """Get vendor contract template."""
        return {
            'title': 'Vendor Contract',
            'description': 'Purchase and supply agreement',
            'category': 'Procurement',
            'variables': [
                'BUYER_NAME', 'VENDOR_NAME', 'PRODUCTS', 'QUANTITY',
                'PRICE', 'DELIVERY_DATE', 'PAYMENT_TERMS'
            ],
            'content': '''VENDOR SUPPLY AGREEMENT

Agreement dated [DELIVERY_DATE] between:

[BUYER_NAME] ("Buyer")
AND
[VENDOR_NAME] ("Vendor")

1. PRODUCTS
The Vendor shall supply: [PRODUCTS]
Quantity: [QUANTITY]

2. PRICE
Total Price: INR [PRICE]
Payment Terms: [PAYMENT_TERMS]

3. DELIVERY
Delivery Date: [DELIVERY_DATE]
Delivery Location: As specified by Buyer

4. QUALITY STANDARDS
Products shall meet specified quality standards and be fit for purpose.

5. INSPECTION AND ACCEPTANCE
Buyer may inspect within 7 days. Defective products shall be replaced at Vendor's cost.

6. WARRANTY
Vendor warrants products are free from defects for 90 days from delivery.

7. LIABILITY
Vendor liable for defective products. Liability capped at contract value.

8. TERMINATION
Either party may terminate for material breach with 15 days notice.

9. FORCE MAJEURE
Neither party liable for delays due to force majeure events.

10. DISPUTE RESOLUTION
Disputes resolved through arbitration in India.

_____________________          _____________________
[BUYER_NAME]                   [VENDOR_NAME]
'''
        }
