"""Contract analyzer combining NLP and LLM capabilities."""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from src.document_parser import DocumentParser
from src.nlp_processor import NLPProcessor
from src.llm_handler import LLMHandler
from config.settings import get_settings
from src.utils import get_logger

logger = get_logger()


class ContractAnalyzer:
    """
    Main contract analyzer orchestrating NLP and LLM processing.
    
    Provides complete contract analysis including:
    - Document parsing
    - Contract classification
    - Clause extraction and analysis
    - Entity recognition
    - Risk assessment
    - Compliance checking
    """
    
    def __init__(self):
        """Initialize contract analyzer."""
        self.settings = get_settings()
        self.document_parser = DocumentParser()
        self.nlp_processor = NLPProcessor()
        self.llm_handler = LLMHandler()
        
        logger.info("ContractAnalyzer initialized")
    
    def analyze_contract(
        self,
        file_path: Optional[str] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform complete contract analysis.
        
        Args:
            file_path: Path to contract file
            file_bytes: Contract file bytes
            filename: Original filename
            
        Returns:
            Comprehensive analysis results
        """
        logger.info(f"Starting contract analysis: {filename or file_path}")
        
        start_time = datetime.now()
        
        try:
            # Step 1: Parse document
            logger.info("Step 1/6: Parsing document")
            parsed_doc = self.document_parser.parse(
                file_path=file_path,
                file_bytes=file_bytes,
                filename=filename
            )
            
            if not parsed_doc.is_valid:
                return self._create_error_response(
                    f"Document parsing failed: {parsed_doc.error_message}"
                )
            
            # Step 2: Classify contract type
            logger.info("Step 2/6: Classifying contract type")
            classification = self.llm_handler.classify_contract(parsed_doc.text)
            
            # Step 3: NLP processing
            logger.info("Step 3/6: Running NLP analysis")
            nlp_results = self.nlp_processor.process(parsed_doc.text)
            
            # Step 4: Analyze key clauses with LLM
            logger.info("Step 4/6: Analyzing clauses")
            clause_analyses = self._analyze_key_clauses(nlp_results['clauses'][:10])  # Top 10 clauses
            
            # Step 5: Risk assessment
            logger.info("Step 5/6: Assessing risks")
            risk_assessment = self.llm_handler.assess_risks(parsed_doc.text[:6000])
            
            # Step 6: Generate summary
            logger.info("Step 6/6: Generating summary")
            summary = self.llm_handler.generate_summary(parsed_doc.text)
            
            # Additional analyses
            unfavorable_terms = self.llm_handler.identify_unfavorable_terms(parsed_doc.text)
            compliance_check = self.llm_handler.check_compliance(parsed_doc.text[:5000])
            ambiguity_check = self.llm_handler.detect_ambiguity(parsed_doc.text[:5000])
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Compile results
            analysis_results = {
                'status': 'success',
                'analysis_id': f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': processing_time,
                
                # Document info
                'document_info': {
                    'filename': parsed_doc.metadata.get('filename'),
                    'file_type': parsed_doc.file_type,
                    'language': parsed_doc.language,
                    'word_count': parsed_doc.word_count,
                    'page_count': parsed_doc.page_count
                },
                
                # Classification
                'contract_classification': classification,
                
                # Summary
                'summary': summary,
                
                # NLP results
                'nlp_analysis': {
                    'total_clauses': nlp_results['statistics']['total_clauses'],
                    'obligations': nlp_results['statistics']['obligations'],
                    'rights': nlp_results['statistics']['rights'],
                    'prohibitions': nlp_results['statistics']['prohibitions'],
                    'entities': nlp_results['entities'],
                    'key_terms': nlp_results['key_terms']
                },
                
                # Clause analyses
                'clause_analyses': clause_analyses,
                
                # Risk assessment
                'risk_assessment': risk_assessment,
                
                # Unfavorable terms
                'unfavorable_terms': unfavorable_terms,
                
                # Compliance
                'compliance_check': compliance_check,
                
                # Ambiguity detection
                'ambiguity_check': ambiguity_check,
                
                # Full data
                'detailed_data': {
                    'all_clauses': nlp_results['clauses'],
                    'clause_classifications': nlp_results['clause_classifications']
                }
            }
            
            logger.info(f"Contract analysis completed in {processing_time:.2f}s")
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error during contract analysis: {str(e)}")
            return self._create_error_response(str(e))
    
    def _analyze_key_clauses(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze key clauses with LLM."""
        analyses = []
        
        for clause in clauses:
            # Focus on clauses with risk keywords
            if clause.get('keywords') or clause['word_count'] > 30:
                try:
                    analysis = self.llm_handler.analyze_clause(clause['text'])
                    analyses.append({
                        'clause_id': clause['id'],
                        'clause_type': clause['clause_type'],
                        'section_number': clause.get('section_number'),
                        'analysis': analysis
                    })
                except Exception as e:
                    logger.warning(f"Error analyzing clause {clause['id']}: {str(e)}")
                    continue
        
        return analyses
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            'status': 'error',
            'error_message': error_message,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_alternative_clauses(
        self,
        unfavorable_clauses: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Generate alternative clause suggestions.
        
        Args:
            unfavorable_clauses: List of unfavorable clauses with issues
            
        Returns:
            List of alternative clause suggestions
        """
        alternatives = []
        
        for item in unfavorable_clauses:
            clause = item.get('clause', '')
            issue = item.get('issue', '')
            
            if clause and issue:
                try:
                    suggestion = self.llm_handler.suggest_alternative_clause(clause, issue)
                    alternatives.append(suggestion)
                except Exception as e:
                    logger.warning(f"Error generating alternative: {str(e)}")
                    continue
        
        return alternatives
    
    def quick_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform quick analysis for preview.
        
        Args:
            text: Contract text
            
        Returns:
            Quick analysis results
        """
        logger.info("Performing quick analysis")
        
        try:
            # Quick classification
            classification = self.llm_handler.classify_contract(text[:2000])
            
            # Basic NLP
            nlp_results = self.nlp_processor.process(text[:3000])
            
            return {
                'status': 'success',
                'contract_type': classification['contract_type'],
                'clause_count': nlp_results['statistics']['total_clauses'],
                'key_terms': nlp_results['key_terms'][:10]
            }
            
        except Exception as e:
            logger.error(f"Error in quick analysis: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e)
            }
    
    def export_analysis(self, analysis_results: Dict[str, Any], format: str = 'json') -> str:
        """
        Export analysis results.
        
        Args:
            analysis_results: Analysis results dictionary
            format: Export format ('json' or 'text')
            
        Returns:
            Formatted export string
        """
        if format == 'json':
            return json.dumps(analysis_results, indent=2, ensure_ascii=False)
        elif format == 'text':
            return self._format_as_text(analysis_results)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _format_as_text(self, results: Dict[str, Any]) -> str:
        """Format results as readable text."""
        lines = []
        lines.append("=" * 80)
        lines.append("CONTRACT ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Document info
        doc_info = results.get('document_info', {})
        lines.append(f"Document: {doc_info.get('filename', 'Unknown')}")
        lines.append(f"Type: {doc_info.get('file_type', 'Unknown')}")
        lines.append(f"Language: {doc_info.get('language', 'Unknown')}")
        lines.append("")
        
        # Classification
        classification = results.get('contract_classification', {})
        lines.append(f"Contract Type: {classification.get('contract_type', 'Unknown')}")
        lines.append(f"Justification: {classification.get('justification', '')}")
        lines.append("")
        
        # Summary
        summary = results.get('summary', {})
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(summary.get('summary', ''))
        lines.append("")
        
        # Risk assessment
        risk = results.get('risk_assessment', {})
        lines.append("RISK ASSESSMENT")
        lines.append("-" * 80)
        lines.append(f"Identified Risks: {risk.get('risk_count', 0)}")
        lines.append("")
        
        return "\n".join(lines)
