"""LLM handler for GPT-4 and Claude integration."""

import os
from typing import Dict, Any, Optional, List, Literal
from abc import ABC, abstractmethod
import openai
from anthropic import Anthropic

from config.settings import get_settings
from config.prompts import *
from src.utils import get_logger

logger = get_logger()


class BaseLLMHandler(ABC):
    """Abstract base class for LLM handlers."""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.3) -> str:
        """Generate text from prompt."""
        pass


class OpenAIHandler(BaseLLMHandler):
    """Handler for OpenAI GPT-4."""
    
    def __init__(self, api_key: str, model: str):
        """Initialize OpenAI handler."""
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"OpenAI handler initialized with model: {model}")
    
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.3) -> str:
        """Generate text using GPT-4."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert legal analyst specializing in contract review for Indian SMEs. Provide clear, actionable advice in plain business language."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise


class AnthropicHandler(BaseLLMHandler):
    """Handler for Anthropic Claude."""
    
    def __init__(self, api_key: str, model: str):
        """Initialize Anthropic handler."""
        self.client = Anthropic(api_key=api_key)
        self.model = model
        logger.info(f"Anthropic handler initialized with model: {model}")
    
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.3) -> str:
        """Generate text using Claude."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system="You are an expert legal analyst specializing in contract review for Indian SMEs. Provide clear, actionable advice in plain business language.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise


class LLMHandler:
    """
    Main LLM handler supporting both GPT-4 and Claude.
    
    Features:
    - Contract classification
    - Clause analysis
    - Risk assessment
    - Unfavorable terms detection
    - Alternative clause suggestions
    - Contract summaries
    - Named entity extraction
    - Compliance checking
    """
    
    def __init__(self):
        """Initialize LLM handler."""
        self.settings = get_settings()
        
        # Validate API keys
        if not self.settings.validate_api_keys():
            raise ValueError(
                f"API key not configured for provider: {self.settings.LLM_PROVIDER}. "
                "Please set the appropriate API key in .env file."
            )
        
        # Initialize appropriate handler
        if self.settings.LLM_PROVIDER == "openai":
            self.handler = OpenAIHandler(
                api_key=self.settings.OPENAI_API_KEY,
                model=self.settings.OPENAI_MODEL
            )
        elif self.settings.LLM_PROVIDER == "anthropic":
            self.handler = AnthropicHandler(
                api_key=self.settings.ANTHROPIC_API_KEY,
                model=self.settings.ANTHROPIC_MODEL
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.settings.LLM_PROVIDER}")
        
        logger.info(f"LLMHandler initialized with provider: {self.settings.LLM_PROVIDER}")
    
    def classify_contract(self, contract_text: str) -> Dict[str, Any]:
        """
        Classify contract type.
        
        Args:
            contract_text: Contract text (first 3000 chars used)
            
        Returns:
            Dictionary with contract_type and justification
        """
        logger.info("Classifying contract type")
        
        # Use first 3000 characters for classification
        text_sample = contract_text[:3000]
        
        prompt = CONTRACT_CLASSIFICATION_PROMPT.format(contract_text=text_sample)
        
        try:
            response = self.handler.generate(prompt, max_tokens=500, temperature=0.2)
            
            # Parse response
            contract_type = "Unknown"
            justification = ""
            
            for line in response.split('\n'):
                if line.startswith('Category:'):
                    contract_type = line.replace('Category:', '').strip()
                elif line.startswith('Justification:'):
                    justification = line.replace('Justification:', '').strip()
            
            logger.info(f"Contract classified as: {contract_type}")
            
            return {
                'contract_type': contract_type,
                'justification': justification,
                'confidence': 'high' if contract_type in self.settings.CONTRACT_TYPES else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error classifying contract: {str(e)}")
            return {
                'contract_type': 'Unknown',
                'justification': f'Error: {str(e)}',
                'confidence': 'low'
            }
    
    def analyze_clause(self, clause_text: str) -> Dict[str, Any]:
        """
        Analyze individual clause.
        
        Args:
            clause_text: Clause text
            
        Returns:
            Dictionary with analysis results
        """
        logger.debug(f"Analyzing clause: {clause_text[:100]}...")
        
        prompt = CLAUSE_ANALYSIS_PROMPT.format(clause_text=clause_text)
        
        try:
            response = self.handler.generate(prompt, max_tokens=800, temperature=0.3)
            
            return {
                'clause_text': clause_text,
                'analysis': response,
                'plain_language_explanation': self._extract_section(response, 'explanation'),
                'key_points': self._extract_section(response, 'obligations'),
                'risks': self._extract_section(response, 'risks'),
                'risk_level': self._extract_risk_level(response)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing clause: {str(e)}")
            return {
                'clause_text': clause_text,
                'analysis': f'Error: {str(e)}',
                'risk_level': 'unknown'
            }
    
    def assess_risks(self, contract_section: str) -> Dict[str, Any]:
        """
        Assess risks in contract section.
        
        Args:
            contract_section: Contract text section
            
        Returns:
            Dictionary with risk assessment
        """
        logger.info("Assessing contract risks")
        
        prompt = RISK_ASSESSMENT_PROMPT.format(contract_section=contract_section)
        
        try:
            response = self.handler.generate(prompt, max_tokens=1500, temperature=0.3)
            
            # Parse risks from response
            risks = self._parse_risk_response(response)
            
            return {
                'risks': risks,
                'risk_count': len(risks),
                'overall_assessment': response
            }
            
        except Exception as e:
            logger.error(f"Error assessing risks: {str(e)}")
            return {
                'risks': [],
                'risk_count': 0,
                'overall_assessment': f'Error: {str(e)}'
            }
    
    def identify_unfavorable_terms(self, contract_text: str) -> Dict[str, Any]:
        """
        Identify unfavorable terms in contract.
        
        Args:
            contract_text: Full contract text
            
        Returns:
            Dictionary with unfavorable terms
        """
        logger.info("Identifying unfavorable terms")
        
        prompt = UNFAVORABLE_TERMS_PROMPT.format(contract_text=contract_text[:5000])
        
        try:
            response = self.handler.generate(prompt, max_tokens=2000, temperature=0.3)
            
            unfavorable_terms = self._parse_unfavorable_terms(response)
            
            return {
                'unfavorable_terms': unfavorable_terms,
                'term_count': len(unfavorable_terms),
                'detailed_analysis': response
            }
            
        except Exception as e:
            logger.error(f"Error identifying unfavorable terms: {str(e)}")
            return {
                'unfavorable_terms': [],
                'term_count': 0,
                'detailed_analysis': f'Error: {str(e)}'
            }
    
    def suggest_alternative_clause(self, original_clause: str, issue: str) -> Dict[str, Any]:
        """
        Suggest alternative clause wording.
        
        Args:
            original_clause: Original clause text
            issue: Identified issue with clause
            
        Returns:
            Dictionary with alternative clause suggestion
        """
        logger.info("Generating alternative clause suggestion")
        
        prompt = ALTERNATIVE_CLAUSE_PROMPT.format(
            original_clause=original_clause,
            issue=issue
        )
        
        try:
            response = self.handler.generate(prompt, max_tokens=1000, temperature=0.4)
            
            return {
                'original_clause': original_clause,
                'issue': issue,
                'suggested_alternative': response,
                'improvements': self._extract_section(response, 'improvements')
            }
            
        except Exception as e:
            logger.error(f"Error suggesting alternative: {str(e)}")
            return {
                'original_clause': original_clause,
                'issue': issue,
                'suggested_alternative': f'Error: {str(e)}'
            }
    
    def generate_summary(self, contract_text: str) -> Dict[str, Any]:
        """
        Generate plain-language contract summary.
        
        Args:
            contract_text: Full contract text
            
        Returns:
            Dictionary with contract summary
        """
        logger.info("Generating contract summary")
        
        prompt = CONTRACT_SUMMARY_PROMPT.format(contract_text=contract_text[:8000])
        
        try:
            response = self.handler.generate(prompt, max_tokens=1500, temperature=0.3)
            
            return {
                'summary': response,
                'key_sections': self._extract_key_sections(response)
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return {
                'summary': f'Error: {str(e)}',
                'key_sections': {}
            }
    
    def extract_named_entities(self, contract_text: str) -> Dict[str, Any]:
        """
        Extract named entities using LLM.
        
        Args:
            contract_text: Contract text
            
        Returns:
            Dictionary with extracted entities
        """
        logger.info("Extracting named entities with LLM")
        
        prompt = NER_EXTRACTION_PROMPT.format(contract_text=contract_text[:5000])
        
        try:
            response = self.handler.generate(prompt, max_tokens=1200, temperature=0.2)
            
            return {
                'entities': self._parse_entities(response),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {
                'entities': {},
                'raw_response': f'Error: {str(e)}'
            }
    
    def check_compliance(self, contract_section: str) -> Dict[str, Any]:
        """
        Check compliance with Indian legal standards.
        
        Args:
            contract_section: Contract section to check
            
        Returns:
            Dictionary with compliance analysis
        """
        logger.info("Checking contract compliance")
        
        prompt = COMPLIANCE_CHECK_PROMPT.format(contract_section=contract_section)
        
        try:
            response = self.handler.generate(prompt, max_tokens=1200, temperature=0.3)
            
            return {
                'compliance_analysis': response,
                'compliant_aspects': self._extract_section(response, 'compliant'),
                'concerns': self._extract_section(response, 'concerns'),
                'recommendations': self._extract_section(response, 'recommendations')
            }
            
        except Exception as e:
            logger.error(f"Error checking compliance: {str(e)}")
            return {
                'compliance_analysis': f'Error: {str(e)}',
                'concerns': []
            }
    
    def detect_ambiguity(self, contract_text: str) -> Dict[str, Any]:
        """
        Detect ambiguous language in contract.
        
        Args:
            contract_text: Contract text
            
        Returns:
            Dictionary with ambiguity detection results
        """
        logger.info("Detecting ambiguous language")
        
        prompt = AMBIGUITY_DETECTION_PROMPT.format(contract_text=contract_text[:5000])
        
        try:
            response = self.handler.generate(prompt, max_tokens=1500, temperature=0.3)
            
            ambiguities = self._parse_ambiguities(response)
            
            return {
                'ambiguities': ambiguities,
                'ambiguity_count': len(ambiguities),
                'detailed_analysis': response
            }
            
        except Exception as e:
            logger.error(f"Error detecting ambiguity: {str(e)}")
            return {
                'ambiguities': [],
                'ambiguity_count': 0,
                'detailed_analysis': f'Error: {str(e)}'
            }
    
    # Helper methods
    
    def _extract_section(self, text: str, section_keyword: str) -> str:
        """Extract specific section from response."""
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_keyword.lower() in line.lower():
                in_section = True
                section_lines.append(line)
            elif in_section:
                if line.strip() and not line[0].isalpha():
                    section_lines.append(line)
                elif line.strip() and line[0].isupper() and ':' in line:
                    break
                else:
                    section_lines.append(line)
        
        return '\n'.join(section_lines).strip()
    
    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from response."""
        text_lower = text.lower()
        if 'critical' in text_lower:
            return 'Critical'
        elif 'high' in text_lower:
            return 'High'
        elif 'medium' in text_lower:
            return 'Medium'
        elif 'low' in text_lower:
            return 'Low'
        return 'Unknown'
    
    def _parse_risk_response(self, response: str) -> List[Dict[str, str]]:
        """Parse risk assessment response."""
        risks = []
        # Simple parsing - can be enhanced
        lines = response.split('\n')
        current_risk = {}
        
        for line in lines:
            if 'category:' in line.lower():
                if current_risk:
                    risks.append(current_risk)
                current_risk = {'category': line.split(':', 1)[1].strip()}
            elif 'level:' in line.lower():
                current_risk['level'] = line.split(':', 1)[1].strip()
            elif 'concern:' in line.lower():
                current_risk['concern'] = line.split(':', 1)[1].strip()
        
        if current_risk:
            risks.append(current_risk)
        
        return risks
    
    def _parse_unfavorable_terms(self, response: str) -> List[Dict[str, str]]:
        """Parse unfavorable terms response."""
        terms = []
        # Simple parsing
        sections = response.split('\n\n')
        for section in sections:
            if section.strip():
                terms.append({'description': section.strip()})
        return terms
    
    def _extract_key_sections(self, summary: str) -> Dict[str, str]:
        """Extract key sections from summary."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in summary.split('\n'):
            if line.strip() and ':' in line and line[0].isdigit():
                if current_section:
                    sections[current_section] = ' '.join(current_content)
                current_section = line.strip()
                current_content = []
            elif line.strip():
                current_content.append(line.strip())
        
        if current_section:
            sections[current_section] = ' '.join(current_content)
        
        return sections
    
    def _parse_entities(self, response: str) -> Dict[str, List[str]]:
        """Parse entities from response."""
        entities = {}
        current_type = None
        
        for line in response.split('\n'):
            if ':' in line and line[0].isdigit():
                parts = line.split(':', 1)
                current_type = parts[0].strip().split('.', 1)[1].strip()
                entities[current_type] = []
            elif line.strip() and current_type:
                entities[current_type].append(line.strip())
        
        return entities
    
    def _parse_ambiguities(self, response: str) -> List[Dict[str, str]]:
        """Parse ambiguities from response."""
        ambiguities = []
        sections = response.split('\n\n')
        
        for section in sections:
            if section.strip() and ('ambiguous' in section.lower() or 'unclear' in section.lower()):
                ambiguities.append({'description': section.strip()})
        
        return ambiguities
