"""Integration test script for the complete system."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.contract_analyzer import ContractAnalyzer
from src.risk_engine import RiskEngine
from src.template_manager import TemplateManager
from src.report_generator import ReportGenerator
from src.utils import setup_logging, get_logger

# Setup
setup_logging()
logger = get_logger()


def test_full_workflow():
    """Test complete analysis workflow."""
    
    print("\n" + "="*80)
    print("INTEGRATION TEST: Full Workflow")
    print("="*80 + "\n")
    
    # Sample contract text
    sample_contract = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement is entered into on January 1, 2026,
    between ABC Technologies Private Limited ("Employer") and John Doe ("Employee").
    
    1. POSITION AND DUTIES
    The Employee shall serve as Software Engineer and perform all duties assigned.
    
    2. COMPENSATION
    The Employee shall receive INR 10,00,000 per annum, payable monthly.
    
    3. TERM AND TERMINATION
    This Agreement shall commence on January 1, 2026. Either party may terminate
    with 30 days written notice. The Employer may terminate immediately for cause.
    
    4. CONFIDENTIALITY
    The Employee shall maintain strict confidentiality of all proprietary information
    during and after employment for a period of 5 years.
    
    5. NON-COMPETE
    The Employee agrees not to engage in any competing business for 12 months
    after termination within a 50 km radius of the Employer's offices.
    
    6. INTELLECTUAL PROPERTY
    All work products, inventions, and intellectual property created during
    employment shall be the sole property of the Employer.
    
    7. INDEMNIFICATION
    The Employee shall indemnify and hold harmless the Employer from any claims
    arising from the Employee's actions or negligence.
    
    8. GOVERNING LAW
    This Agreement shall be governed by the laws of India. Disputes shall be
    resolved through arbitration in Mumbai.
    """
    
    try:
        # Step 1: Initialize components
        print("Step 1: Initializing components...")
        analyzer = ContractAnalyzer()
        risk_engine = RiskEngine()
        print("✓ Components initialized\n")
        
        # Step 2: Analyze contract
        print("Step 2: Analyzing contract...")
        results = analyzer.analyze_contract(
            file_bytes=sample_contract.encode('utf-8'),
            filename="test_employment_contract.txt"
        )
        
        if results['status'] != 'success':
            print(f"✗ Analysis failed: {results.get('error_message')}")
            return False
        
        print("✓ Contract analyzed successfully\n")
        
        # Step 3: Display results
        print("Step 3: Analysis Results")
        print("-" * 80)
        
        # Classification
        classification = results.get('contract_classification', {})
        print(f"Contract Type: {classification.get('contract_type', 'Unknown')}")
        print(f"Justification: {classification.get('justification', '')}\n")
        
        # NLP stats
        nlp = results.get('nlp_analysis', {})
        print(f"Total Clauses: {nlp.get('total_clauses', 0)}")
        print(f"Obligations: {nlp.get('obligations', 0)}")
        print(f"Rights: {nlp.get('rights', 0)}")
        print(f"Prohibitions: {nlp.get('prohibitions', 0)}\n")
        
        # Risk assessment
        risk = results.get('risk_assessment', {})
        print(f"Overall Risk Score: {risk.get('overall_risk_score', 0):.2f}")
        print(f"Risk Level: {risk.get('overall_risk_level', 'Unknown')}")
        print(f"Identified Risks: {risk.get('risk_count', 0)}\n")
        
        # Step 4: Test risk engine
        print("Step 4: Testing Risk Engine...")
        clauses = results.get('detailed_data', {}).get('all_clauses', [])
        risk_analysis = risk_engine.assess_contract(sample_contract, clauses)
        
        print(f"Risk Engine Score: {risk_analysis['overall_risk_score']:.2f}")
        print(f"Risk Engine Level: {risk_analysis['overall_risk_level']}")
        print(f"High Risk Clauses: {len(risk_analysis['high_risk_clauses'])}\n")
        
        # Step 5: Test report generation
        print("Step 5: Testing Report Generation...")
        report_gen = ReportGenerator()
        
        # Generate summary report
        pdf_bytes = report_gen.generate_summary_report(results)
        print(f"✓ Generated PDF report: {len(pdf_bytes)} bytes\n")
        
        # Step 6: Test template manager
        print("Step 6: Testing Template Manager...")
        template_mgr = TemplateManager()
        
        templates = template_mgr.list_templates()
        print(f"✓ Available templates: {len(templates)}")
        for t in templates:
            print(f"  - {t['title']}")
        print()
        
        # Generate contract from template
        if templates:
            generated = template_mgr.generate_contract(
                template_name=templates[0]['name'],
                variables={
                    'COMPANY_NAME': 'Test Company',
                    'EMPLOYEE_NAME': 'Jane Smith',
                    'POSITION': 'Developer',
                    'START_DATE': '2026-03-01',
                    'SALARY': '800,000',
                    'LOCATION': 'Bangalore',
                    'NOTICE_PERIOD': '30'
                }
            )
            print(f"✓ Generated contract: {len(generated)} characters\n")
        
        print("="*80)
        print("ALL TESTS PASSED ✓")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling."""
    
    print("\n" + "="*80)
    print("INTEGRATION TEST: Error Handling")
    print("="*80 + "\n")
    
    analyzer = ContractAnalyzer()
    
    # Test 1: Invalid file
    print("Test 1: Invalid file...")
    result = analyzer.analyze_contract(
        file_bytes=b"",
        filename="empty.txt"
    )
    
    if not result.get('is_valid', True) or result.get('status') == 'error':
        print("✓ Correctly handled empty file\n")
    else:
        print("✗ Failed to detect empty file\n")
    
    # Test 2: Very short text
    print("Test 2: Very short text...")
    result = analyzer.quick_analysis("Hello")
    
    if result.get('status') in ['success', 'error']:
        print("✓ Handled short text\n")
    else:
        print("✗ Failed on short text\n")
    
    print("="*80)
    print("Error Handling Tests Complete")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("\nContract Analysis Bot - Integration Tests\n")
    
    # Run tests
    success = test_full_workflow()
    test_error_handling()
    
    if success:
        print("\n✓ All integration tests passed successfully!\n")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed\n")
        sys.exit(1)
