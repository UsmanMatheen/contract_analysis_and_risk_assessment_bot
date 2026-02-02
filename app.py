"""Main Streamlit application for Contract Analysis Bot."""

import streamlit as st
import sys
from pathlib import Path
import uuid
from datetime import datetime
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_settings
from src.utils import setup_logging, get_logger
from src.audit import AuditLogger
from src.contract_analyzer import ContractAnalyzer
from src.risk_engine import RiskEngine
from src.template_manager import TemplateManager
from src.report_generator import ReportGenerator

# Initialize
setup_logging()
logger = get_logger()
settings = get_settings()
audit_logger = AuditLogger()

# Page configuration
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS
st.markdown("""
<style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 1.1rem;
        font-weight: 400;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 0.01em;
    }
    
    /* Professional Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
        letter-spacing: 0.02em;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border: none;
        padding: 0.65rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.2);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        box-shadow: 0 8px 12px -2px rgba(5, 150, 105, 0.3);
    }
    
    /* Risk Level Colors - Professional Palette */
    .risk-critical {
        color: #dc2626;
        font-weight: 600;
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        display: inline-block;
    }
    
    .risk-high {
        color: #ea580c;
        font-weight: 600;
        background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        display: inline-block;
    }
    
    .risk-medium {
        color: #d97706;
        font-weight: 600;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        display: inline-block;
    }
    
    .risk-low {
        color: #059669;
        font-weight: 600;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        display: inline-block;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1rem;
        color: #64748b;
        padding: 1rem 1.5rem;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
    }
    
    /* Alert Styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #e2e8f0;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #2563eb;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Text Area */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        font-family: 'Inter', monospace;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        border-radius: 8px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Professional Section Headers */
    h2, h3 {
        color: #1a1a2e;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    
    /* Professional Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None


def main():
    """Main application function."""
    
    # Professional Header
    st.markdown('<div class="main-header">Contract Analysis & Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enterprise-Grade Legal Intelligence Platform for SMEs</div>', unsafe_allow_html=True)
    
    # Professional Sidebar
    with st.sidebar:
        st.markdown("### Contract Analysis Platform")
        st.markdown("---")
        
        st.markdown("### Core Capabilities")
        st.markdown("""
        • Contract Type Classification
        • Intelligent Clause Analysis
        • Risk Assessment & Scoring
        • Terms Evaluation
        • Plain Language Insights
        • Professional Reports
        • Template Library
        """)
        
        st.markdown("---")
        
        # API Key validation
        if not settings.validate_api_keys():
            st.error("**API Configuration Required**\n\nPlease configure your API key in the .env file to enable analysis features.")
        else:
            st.success(f"**{settings.LLM_PROVIDER.upper()}** • Connected")
        
        st.markdown("---")
        st.markdown(f"**Version** {settings.APP_VERSION}")
        st.markdown(f"**Session** {st.session_state.session_id[:8]}")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Contract Analysis", "Template Library", "Analysis Reports", "Documentation"])
    
    with tab1:
        analyze_contract_tab()
    
    with tab2:
        templates_tab()
    
    with tab3:
        reports_tab()
    
    with tab4:
        about_tab()


def analyze_contract_tab():
    """Contract analysis tab."""
    
    st.header("Contract Analysis")
    
    # File upload
    st.subheader("Upload Contract Document")
    
    uploaded_file = st.file_uploader(
        "Select a contract file for analysis",
        type=settings.ALLOWED_EXTENSIONS,
        help=f"Supported formats: {', '.join(settings.ALLOWED_EXTENSIONS).upper()}"
    )
    
    if uploaded_file:
        # Validate file size
        file_size = len(uploaded_file.getvalue())
        max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        
        if file_size > max_size:
            st.error(f"File size ({file_size / (1024*1024):.2f} MB) exceeds maximum allowed ({settings.MAX_UPLOAD_SIZE_MB} MB)")
            return
        
        st.success(f"File uploaded: {uploaded_file.name} ({file_size / 1024:.2f} KB)")
        
        # Log upload
        audit_logger.log_contract_upload(
            filename=uploaded_file.name,
            file_size=file_size,
            file_type=uploaded_file.type,
            session_id=st.session_state.session_id
        )
        
        st.session_state.uploaded_file = uploaded_file
    
    # Analysis options
    st.subheader("Analysis Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "Document Language",
            options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi",
            index=0
        )
    
    with col2:
        analysis_type = st.selectbox(
            "Analysis Depth",
            options=["Full Analysis", "Quick Analysis"],
            index=0
        )
    
    # Analyze button
    if st.button("Begin Analysis", type="primary", disabled=not uploaded_file):
        analyze_contract(uploaded_file, language, analysis_type)
    
    # Display results
    if st.session_state.analysis_results:
        display_analysis_results(st.session_state.analysis_results)


def analyze_contract(uploaded_file, language, analysis_type):
    """Perform contract analysis."""
    
    try:
        with st.spinner("Analyzing contract... This may take a few minutes."):
            # Initialize analyzer
            analyzer = ContractAnalyzer()
            risk_engine = RiskEngine()
            
            # Log analysis request
            audit_logger.log_analysis_request(
                contract_type="Unknown",
                language=language,
                session_id=st.session_state.session_id
            )
            
            start_time = datetime.now()
            
            # Perform analysis
            if analysis_type == "Quick Analysis":
                # Quick analysis (classification + basic NLP)
                file_bytes = uploaded_file.getvalue()
                text_sample = file_bytes.decode('utf-8', errors='ignore')[:5000]
                results = analyzer.quick_analysis(text_sample)
            else:
                # Full analysis
                results = analyzer.analyze_contract(
                    file_bytes=uploaded_file.getvalue(),
                    filename=uploaded_file.name
                )
                
                # Add risk engine analysis
                if results['status'] == 'success':
                    nlp_analysis = results.get('nlp_analysis', {})
                    clauses = results.get('detailed_data', {}).get('all_clauses', [])
                    
                    # Get document text (simplified for risk engine)
                    doc_text = " ".join([c.get('text', '') for c in clauses[:20]])
                    
                    risk_analysis = risk_engine.assess_contract(doc_text, clauses)
                    results['risk_engine_analysis'] = risk_analysis
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Log completion
            if results['status'] == 'success':
                audit_logger.log_analysis_completion(
                    session_id=st.session_state.session_id,
                    analysis_results=results,
                    processing_time_seconds=processing_time
                )
                
                st.session_state.analysis_results = results
                st.success(f"Analysis completed in {processing_time:.2f} seconds")
                st.rerun()
            else:
                st.error(f"Analysis failed: {results.get('error_message', 'Unknown error')}")
    
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}\n{traceback.format_exc()}")
        st.error(f"An error occurred: {str(e)}")
        
        audit_logger.log_error(
            error_type="AnalysisError",
            error_message=str(e),
            session_id=st.session_state.session_id,
            stack_trace=traceback.format_exc()
        )


def display_analysis_results(results):
    """Display analysis results."""
    
    if results['status'] != 'success':
        st.error("Analysis was not successful")
        return
    
    st.markdown("---")
    st.header("Analysis Results")
    
    # Overview metrics
    st.subheader("Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        contract_type = results.get('contract_classification', {}).get('contract_type', 'Unknown')
        st.metric("Contract Type", contract_type)
    
    with col2:
        doc_info = results.get('document_info', {})
        st.metric("Word Count", doc_info.get('word_count', 0))
    
    with col3:
        nlp_analysis = results.get('nlp_analysis', {})
        st.metric("Clauses Analyzed", nlp_analysis.get('total_clauses', 0))
    
    with col4:
        risk_assessment = results.get('risk_assessment', {})
        risk_level = risk_assessment.get('overall_risk_level', 'Unknown')
        risk_class = f"risk-{risk_level.lower()}"
        st.markdown(f'<div class="metric-card"><div class="{risk_class}">Risk Level<br/>{risk_level}</div></div>', unsafe_allow_html=True)
    
    # Summary
    st.markdown("---")
    st.subheader("Contract Summary")
    
    summary = results.get('summary', {}).get('summary', '')
    if summary:
        st.write(summary)
    else:
        st.info("Summary not available")
    
    # Risk Assessment
    st.markdown("---")
    st.subheader("Risk Assessment")
    
    risk_assessment = results.get('risk_assessment', {})
    risk_score = risk_assessment.get('overall_risk_score', 0)
    risk_level = risk_assessment.get('overall_risk_level', 'Unknown')
    
    # Risk score gauge
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Overall Risk Score", f"{risk_score:.2f}")
        st.markdown(f"**Level:** <span class='risk-{risk_level.lower()}'>{risk_level}</span>", unsafe_allow_html=True)
    
    with col2:
        stats = risk_assessment.get('statistics', {})
        st.write("**Risk Breakdown:**")
        st.write(f"- Critical: {stats.get('critical_risks', 0)}")
        st.write(f"- High: {stats.get('high_risks', 0)}")
        st.write(f"- Medium: {stats.get('medium_risks', 0)}")
        st.write(f"- Low: {stats.get('low_risks', 0)}")
    
    # Identified Risks
    identified_risks = risk_assessment.get('identified_risks', [])
    if identified_risks:
        st.markdown("**Identified Risks:**")
        
        for i, risk in enumerate(identified_risks[:10], 1):
            with st.expander(f"{i}. {risk.get('category', 'Unknown').replace('_', ' ').title()} [{risk.get('severity', 'Unknown')}]"):
                st.write(f"**Description:** {risk.get('description', '')}")
                st.write(f"**Impact:** {risk.get('impact', '')}")
                st.write(f"**Recommendation:** {risk.get('recommendation', '')}")
                
                clause_text = risk.get('clause_text', '')
                if clause_text:
                    st.text_area("Related Clause:", clause_text, height=100, disabled=True)
    
    # Clause Analysis
    st.markdown("---")
    st.subheader("Clause Analysis")
    
    clause_analyses = results.get('clause_analyses', [])
    
    if clause_analyses:
        for i, clause_analysis in enumerate(clause_analyses[:10], 1):
            analysis = clause_analysis.get('analysis', {})
            
            with st.expander(f"Clause {i} - {clause_analysis.get('clause_type', 'General').title()}"):
                if isinstance(analysis, dict):
                    plain_lang = analysis.get('plain_language_explanation', '')
                    if plain_lang:
                        st.write("**Explanation:**", plain_lang)
                    
                    risk_level = analysis.get('risk_level', 'Unknown')
                    if risk_level != 'Unknown':
                        st.markdown(f"**Risk Level:** <span class='risk-{risk_level.lower()}'>{risk_level}</span>", unsafe_allow_html=True)
                else:
                    st.write(analysis)
    else:
        st.info("No detailed clause analysis available. This feature is available in Full Analysis mode.")
    
    # Recommendations
    st.markdown("---")
    st.subheader("Recommendations")
    
    recommendations = risk_assessment.get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            if "CRITICAL" in rec:
                st.error(rec)
            else:
                st.info(f"{i}. {rec}")
    
    # Export options
    st.markdown("---")
    st.subheader("Export Analysis Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate Full Report"):
            generate_pdf_report(results, report_type="full")
    
    with col2:
        if st.button("Generate Summary Report"):
            generate_pdf_report(results, report_type="summary")


def generate_pdf_report(results, report_type="full"):
    """Generate and download PDF report."""
    
    try:
        with st.spinner("Generating PDF report..."):
            report_gen = ReportGenerator()
            
            if report_type == "full":
                pdf_bytes = report_gen.generate_full_report(results)
                filename = f"contract_analysis_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            else:
                pdf_bytes = report_gen.generate_summary_report(results)
                filename = f"contract_analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Log export
            audit_logger.log_report_export(
                report_type=report_type,
                export_format="pdf",
                session_id=st.session_state.session_id
            )
            
            st.download_button(
                label=f"Download {report_type.title()} Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf"
            )
            
            st.success("Report generated successfully!")
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        st.error(f"Error generating report: {str(e)}")


def templates_tab():
    """Contract templates tab."""
    
    st.header("Professional Contract Templates")
    st.write("Access a curated library of SME-friendly contract templates designed for Indian businesses")
    
    try:
        template_manager = TemplateManager()
        templates = template_manager.list_templates()
        
        if not templates:
            st.info("No templates available")
            return
        
        # Display templates
        for template in templates:
            with st.expander(f"{template['title']}"):
                st.write(f"**Category:** {template['category']}")
                st.write(f"**Description:** {template['description']}")
                
                if st.button(f"View Template", key=f"view_{template['name']}"):
                    template_data = template_manager.get_template(template['name'])
                    st.text_area(
                        "Template Content:",
                        template_data['content'],
                        height=400,
                        disabled=True
                    )
                    
                    # Download button
                    st.download_button(
                        label="Download Template",
                        data=template_data['content'],
                        file_name=f"{template['name']}.txt",
                        mime="text/plain"
                    )
    
    except Exception as e:
        logger.error(f"Error loading templates: {str(e)}")
        st.error(f"Error loading templates: {str(e)}")


def reports_tab():
    """Reports and history tab."""
    
    st.header("Analysis Reports")
    
    if not st.session_state.analysis_results:
        st.info("No analysis results available. Please analyze a contract first to generate reports.")
        return
    
    st.write("Current session analysis results are available in the Contract Analysis tab.")
    st.write("Use the export functionality to download professional PDF reports.")
    
    # Show audit trail
    st.subheader("Session Activity Log")
    
    try:
        session_history = audit_logger.get_session_history(st.session_state.session_id)
        
        if session_history:
            for entry in session_history:
                with st.expander(f"{entry['activity_type']} - {entry['timestamp']}"):
                    st.json(entry)
        else:
            st.info("No activity logged in this session")
    
    except Exception as e:
        logger.error(f"Error loading session history: {str(e)}")
        st.error("Could not load session history")


def about_tab():
    """About tab."""
    
    st.header("About This Platform")
    
    st.markdown("""
    ### Platform Overview
    An enterprise-grade contract analysis platform powered by advanced AI, designed specifically 
    for small and medium businesses to understand complex legal agreements, identify risks, 
    and make informed decisions.
    
    ### Key Capabilities
    
    **Contract Intelligence**
    - Automated contract type classification
    - Deep clause-by-clause analysis
    - Plain language explanations
    - Multi-format document support
    
    **Risk Management**
    - Comprehensive risk assessment
    - Severity-based risk scoring
    - Pattern-based risk detection
    - Actionable mitigation strategies
    
    **Professional Outputs**
    - Executive summary reports
    - Detailed analysis documents
    - PDF export functionality
    - Audit trail maintenance
    
    ### Technology Stack
    - **AI Models:** GPT-4 / Claude 3
    - **NLP Engine:** spaCy
    - **Document Processing:** Multi-format parsers
    - **Infrastructure:** Streamlit
    
    ### Supported Contract Types
    - Employment Agreements
    - Vendor Contracts
    - Lease Agreements
    - Partnership Deeds
    - Service Contracts
    - Non-Disclosure Agreements
    - Consultancy Agreements
    - Purchase Orders
    
    ### Disclaimer
    **This platform provides AI-generated analysis for informational purposes only.**
    
    It is not a substitute for professional legal advice. Always consult with
    qualified legal counsel before making decisions based on this analysis.
    
    ### Security & Privacy
    - Secure document processing
    - No permanent data storage
    - Complete audit trails
    - Encrypted communications
    
    ---
    
    **Version:** {version}  
    **Environment:** {environment}  
    **AI Provider:** {provider}
    """.format(
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        provider=settings.LLM_PROVIDER.upper()
    ))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}\n{traceback.format_exc()}")
        st.error(f"An unexpected error occurred: {str(e)}")
