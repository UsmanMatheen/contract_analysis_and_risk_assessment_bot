"""Risk assessment engine for contract analysis."""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import re

from config.settings import get_settings
from src.utils import get_logger

logger = get_logger()


@dataclass
class RiskItem:
    """Represents an identified risk."""
    
    risk_id: str
    category: str
    severity: str  # Low, Medium, High, Critical
    score: float  # 0.0 to 1.0
    description: str
    clause_text: str
    impact: str
    recommendation: str


class RiskEngine:
    """
    Risk assessment engine for contract analysis.
    
    Features:
    - Pattern-based risk detection
    - Risk scoring and categorization
    - Composite risk calculation
    - Risk mitigation recommendations
    """
    
    def __init__(self):
        """Initialize risk engine."""
        self.settings = get_settings()
        
        # Define risk patterns
        self.risk_patterns = self._define_risk_patterns()
        
        logger.info("RiskEngine initialized")
    
    def _define_risk_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Define risk detection patterns."""
        return {
            'penalty': [
                {
                    'pattern': r'liquidated\s+damages?|penalty|penali[zs]e',
                    'keywords': ['liquidated damages', 'penalty', 'fine'],
                    'severity': 'High',
                    'base_score': 0.7
                }
            ],
            'indemnity': [
                {
                    'pattern': r'indemni(?:fy|fication|ty)|hold\s+harmless|defend\s+against',
                    'keywords': ['indemnify', 'indemnification', 'hold harmless'],
                    'severity': 'High',
                    'base_score': 0.75
                }
            ],
            'termination': [
                {
                    'pattern': r'terminat(?:e|ion)\s+(?:immediately|without\s+(?:notice|cause))|unilateral\s+termination',
                    'keywords': ['terminate without notice', 'immediate termination', 'unilateral'],
                    'severity': 'High',
                    'base_score': 0.7
                },
                {
                    'pattern': r'auto(?:matic(?:ally)?)?[- ]renew',
                    'keywords': ['auto-renew', 'automatic renewal'],
                    'severity': 'Medium',
                    'base_score': 0.5
                }
            ],
            'liability': [
                {
                    'pattern': r'unlimited\s+liability|no\s+limitation\s+on\s+liability',
                    'keywords': ['unlimited liability'],
                    'severity': 'Critical',
                    'base_score': 0.9
                },
                {
                    'pattern': r'consequential\s+damages|punitive\s+damages',
                    'keywords': ['consequential damages', 'punitive damages'],
                    'severity': 'High',
                    'base_score': 0.7
                }
            ],
            'non_compete': [
                {
                    'pattern': r'non[- ]compete|non[- ]competition|restrictive\s+covenant',
                    'keywords': ['non-compete', 'non-competition'],
                    'severity': 'Medium',
                    'base_score': 0.6
                }
            ],
            'ip_transfer': [
                {
                    'pattern': r'transfer\s+(?:all|any)\s+(?:intellectual\s+property|ip)|assign\s+(?:all|any)\s+rights',
                    'keywords': ['IP transfer', 'assign all rights', 'transfer IP'],
                    'severity': 'High',
                    'base_score': 0.7
                }
            ],
            'jurisdiction': [
                {
                    'pattern': r'exclusive\s+jurisdiction|courts?\s+of\s+(?!india|delhi|mumbai|bangalore)',
                    'keywords': ['exclusive jurisdiction', 'foreign courts'],
                    'severity': 'Medium',
                    'base_score': 0.55
                }
            ],
            'payment': [
                {
                    'pattern': r'payment\s+in\s+advance|upfront\s+payment|(?:100|full)\s*%\s+advance',
                    'keywords': ['advance payment', 'upfront payment'],
                    'severity': 'Medium',
                    'base_score': 0.5
                },
                {
                    'pattern': r'no\s+refund|non[- ]refundable',
                    'keywords': ['non-refundable', 'no refund'],
                    'severity': 'Medium',
                    'base_score': 0.55
                }
            ],
            'confidentiality': [
                {
                    'pattern': r'perpetual\s+confidentiality|confidential(?:ity)?\s+forever',
                    'keywords': ['perpetual confidentiality', 'forever'],
                    'severity': 'Medium',
                    'base_score': 0.5
                }
            ],
            'lock_in': [
                {
                    'pattern': r'(?:minimum|lock[- ]in)\s+(?:period|term)\s+(?:of\s+)?(?:\d+)\s+(?:year|month)',
                    'keywords': ['lock-in period', 'minimum term'],
                    'severity': 'Medium',
                    'base_score': 0.5
                }
            ]
        }
    
    def assess_contract(self, contract_text: str, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess overall contract risk.
        
        Args:
            contract_text: Full contract text
            clauses: List of extracted clauses
            
        Returns:
            Comprehensive risk assessment
        """
        logger.info("Assessing contract risks")
        
        # Detect risks
        identified_risks = self._detect_risks(contract_text, clauses)
        
        # Calculate clause-level scores
        clause_scores = self._calculate_clause_scores(clauses, identified_risks)
        
        # Calculate overall risk score
        overall_score = self._calculate_overall_score(identified_risks, clause_scores)
        
        # Categorize risks
        risk_by_category = self._categorize_risks(identified_risks)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(identified_risks)
        
        return {
            'overall_risk_score': overall_score,
            'overall_risk_level': self.settings.get_risk_level(overall_score),
            'identified_risks': [self._risk_to_dict(r) for r in identified_risks],
            'risk_count': len(identified_risks),
            'risks_by_category': risk_by_category,
            'risks_by_severity': self._group_by_severity(identified_risks),
            'clause_risk_scores': clause_scores,
            'high_risk_clauses': self._get_high_risk_clauses(clause_scores),
            'recommendations': recommendations,
            'statistics': {
                'critical_risks': len([r for r in identified_risks if r.severity == 'Critical']),
                'high_risks': len([r for r in identified_risks if r.severity == 'High']),
                'medium_risks': len([r for r in identified_risks if r.severity == 'Medium']),
                'low_risks': len([r for r in identified_risks if r.severity == 'Low'])
            }
        }
    
    def _detect_risks(self, contract_text: str, clauses: List[Dict[str, Any]]) -> List[RiskItem]:
        """Detect risks using pattern matching."""
        risks = []
        risk_id_counter = 1
        
        for category, patterns in self.risk_patterns.items():
            for pattern_def in patterns:
                pattern = pattern_def['pattern']
                
                # Search in full text
                for match in re.finditer(pattern, contract_text, re.IGNORECASE):
                    # Extract context
                    start = max(0, match.start() - 100)
                    end = min(len(contract_text), match.end() + 100)
                    context = contract_text[start:end]
                    
                    # Find matching clause
                    matching_clause = self._find_matching_clause(context, clauses)
                    
                    # Create risk item
                    risk = RiskItem(
                        risk_id=f"risk_{risk_id_counter}",
                        category=category,
                        severity=pattern_def['severity'],
                        score=pattern_def['base_score'],
                        description=f"Detected {category.replace('_', ' ')} risk",
                        clause_text=matching_clause or context,
                        impact=self._get_impact_description(category),
                        recommendation=self._get_recommendation(category)
                    )
                    
                    risks.append(risk)
                    risk_id_counter += 1
        
        logger.info(f"Detected {len(risks)} risks across {len(set(r.category for r in risks))} categories")
        
        return risks
    
    def _find_matching_clause(self, context: str, clauses: List[Dict[str, Any]]) -> str:
        """Find clause that matches the context."""
        for clause in clauses:
            clause_text = clause.get('text', '')
            if context in clause_text or clause_text in context:
                return clause_text
        return ""
    
    def _calculate_clause_scores(
        self,
        clauses: List[Dict[str, Any]],
        risks: List[RiskItem]
    ) -> Dict[str, float]:
        """Calculate risk scores for each clause."""
        clause_scores = {}
        
        for clause in clauses:
            clause_id = clause.get('id', '')
            clause_text = clause.get('text', '')
            
            # Find risks affecting this clause
            clause_risks = [
                r for r in risks
                if r.clause_text and (r.clause_text in clause_text or clause_text in r.clause_text)
            ]
            
            if clause_risks:
                # Average risk score
                score = sum(r.score for r in clause_risks) / len(clause_risks)
            else:
                # Base score from clause type
                score = self._get_base_clause_score(clause)
            
            clause_scores[clause_id] = min(score, 1.0)
        
        return clause_scores
    
    def _get_base_clause_score(self, clause: Dict[str, Any]) -> float:
        """Get base risk score for clause based on type."""
        clause_type = clause.get('clause_type', 'general')
        keywords = clause.get('keywords', [])
        
        # Base scores
        scores = {
            'obligation': 0.3,
            'prohibition': 0.4,
            'right': 0.1,
            'general': 0.2
        }
        
        base_score = scores.get(clause_type, 0.2)
        
        # Increase if risk keywords present
        if keywords:
            base_score += 0.1 * len(keywords)
        
        return min(base_score, 1.0)
    
    def _calculate_overall_score(
        self,
        risks: List[RiskItem],
        clause_scores: Dict[str, float]
    ) -> float:
        """Calculate overall contract risk score."""
        if not risks and not clause_scores:
            return 0.2  # Base risk
        
        # Weight by severity
        severity_weights = {
            'Critical': 1.0,
            'High': 0.75,
            'Medium': 0.5,
            'Low': 0.25
        }
        
        if risks:
            weighted_risk_score = sum(
                r.score * severity_weights.get(r.severity, 0.5)
                for r in risks
            ) / len(risks)
        else:
            weighted_risk_score = 0.2
        
        if clause_scores:
            avg_clause_score = sum(clause_scores.values()) / len(clause_scores)
        else:
            avg_clause_score = 0.2
        
        # Combine scores (70% from detected risks, 30% from clauses)
        overall = (weighted_risk_score * 0.7) + (avg_clause_score * 0.3)
        
        return round(overall, 3)
    
    def _categorize_risks(self, risks: List[RiskItem]) -> Dict[str, List[Dict[str, Any]]]:
        """Group risks by category."""
        categorized = {}
        
        for risk in risks:
            if risk.category not in categorized:
                categorized[risk.category] = []
            
            categorized[risk.category].append(self._risk_to_dict(risk))
        
        return categorized
    
    def _group_by_severity(self, risks: List[RiskItem]) -> Dict[str, int]:
        """Group risks by severity level."""
        return {
            'Critical': len([r for r in risks if r.severity == 'Critical']),
            'High': len([r for r in risks if r.severity == 'High']),
            'Medium': len([r for r in risks if r.severity == 'Medium']),
            'Low': len([r for r in risks if r.severity == 'Low'])
        }
    
    def _get_high_risk_clauses(self, clause_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Get clauses with high risk scores."""
        high_risk = []
        
        for clause_id, score in clause_scores.items():
            risk_level = self.settings.get_risk_level(score)
            if risk_level in ['High', 'Critical']:
                high_risk.append({
                    'clause_id': clause_id,
                    'risk_score': score,
                    'risk_level': risk_level
                })
        
        return sorted(high_risk, key=lambda x: x['risk_score'], reverse=True)
    
    def _generate_recommendations(self, risks: List[RiskItem]) -> List[str]:
        """Generate risk mitigation recommendations."""
        recommendations = []
        
        # Group by category
        categories = set(r.category for r in risks)
        
        for category in categories:
            category_risks = [r for r in risks if r.category == category]
            highest_severity = max(category_risks, key=lambda r: r.score).severity
            
            rec = f"Review and negotiate {category.replace('_', ' ')} clauses ({len(category_risks)} identified, highest severity: {highest_severity})"
            recommendations.append(rec)
        
        # Add general recommendations
        if any(r.severity == 'Critical' for r in risks):
            recommendations.insert(0, "⚠️ CRITICAL: Seek legal counsel before signing this contract")
        
        return recommendations
    
    def _get_impact_description(self, category: str) -> str:
        """Get impact description for risk category."""
        impacts = {
            'penalty': 'Financial penalties may be imposed for contract breaches',
            'indemnity': 'You may be liable for third-party claims and damages',
            'termination': 'Contract may be terminated unfavorably',
            'liability': 'High exposure to legal and financial liability',
            'non_compete': 'Business activities may be restricted post-contract',
            'ip_transfer': 'Loss of intellectual property rights',
            'jurisdiction': 'Legal disputes may need to be handled in unfavorable jurisdiction',
            'payment': 'Financial risk from payment terms',
            'confidentiality': 'Long-term confidentiality obligations',
            'lock_in': 'Extended commitment with limited exit options'
        }
        return impacts.get(category, 'Potential business risk')
    
    def _get_recommendation(self, category: str) -> str:
        """Get recommendation for risk category."""
        recommendations = {
            'penalty': 'Negotiate cap on penalties and ensure they are reasonable',
            'indemnity': 'Limit indemnification to direct damages and reasonable scope',
            'termination': 'Negotiate notice period and add mutual termination rights',
            'liability': 'Add liability caps and exclude consequential damages',
            'non_compete': 'Limit scope, duration, and geographical area',
            'ip_transfer': 'Retain rights to pre-existing IP and limit transfer scope',
            'jurisdiction': 'Negotiate for Indian courts and arbitration',
            'payment': 'Negotiate milestone-based payments or escrow arrangements',
            'confidentiality': 'Limit duration and scope of confidentiality',
            'lock_in': 'Negotiate shorter terms or early exit options'
        }
        return recommendations.get(category, 'Review with legal counsel')
    
    def _risk_to_dict(self, risk: RiskItem) -> Dict[str, Any]:
        """Convert RiskItem to dictionary."""
        return {
            'risk_id': risk.risk_id,
            'category': risk.category,
            'severity': risk.severity,
            'score': risk.score,
            'description': risk.description,
            'clause_text': risk.clause_text[:200] + '...' if len(risk.clause_text) > 200 else risk.clause_text,
            'impact': risk.impact,
            'recommendation': risk.recommendation
        }
