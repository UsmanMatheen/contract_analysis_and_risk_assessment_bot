"""Report generator for PDF exports and summaries."""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import io

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.colors import HexColor

from config.settings import get_settings
from src.utils import get_logger

logger = get_logger()


class ReportGenerator:
    """
    Generate professional PDF reports for contract analysis.
    
    Features:
    - Comprehensive analysis reports
    - Risk assessment summaries
    - Clause-by-clause breakdowns
    - Professional formatting
    - Export for legal review
    """
    
    def __init__(self):
        """Initialize report generator."""
        self.settings = get_settings()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        logger.info("ReportGenerator initialized")
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#2c3e50'),
            spaceBefore=20,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=HexColor('#34495e'),
            spaceBefore=15,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Risk text styles
        for level in ['Critical', 'High', 'Medium', 'Low']:
            color_map = {
                'Critical': '#c0392b',
                'High': '#e67e22',
                'Medium': '#f39c12',
                'Low': '#27ae60'
            }
            
            self.styles.add(ParagraphStyle(
                name=f'Risk{level}',
                parent=self.styles['CustomBody'],
                textColor=HexColor(color_map[level]),
                fontName='Helvetica-Bold'
            ))
    
    def generate_full_report(
        self,
        analysis_results: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> bytes:
        """
        Generate complete analysis report.
        
        Args:
            analysis_results: Analysis results dictionary
            output_path: Optional path to save PDF
            
        Returns:
            PDF bytes
        """
        logger.info("Generating full analysis report")
        
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Title page
        story.extend(self._create_title_page(analysis_results))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        # Contract details
        story.extend(self._create_contract_details(analysis_results))
        
        # Risk assessment
        story.extend(self._create_risk_assessment(analysis_results))
        story.append(PageBreak())
        
        # Clause analysis
        story.extend(self._create_clause_analysis(analysis_results))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations(analysis_results))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        # Save to file if path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
            logger.info(f"Report saved to: {output_path}")
        
        logger.info("Full report generated successfully")
        return pdf_bytes
    
    def _create_title_page(self, results: Dict[str, Any]) -> list:
        """Create title page."""
        elements = []
        
        # Spacer
        elements.append(Spacer(1, 2 * inch))
        
        # Title
        title = Paragraph(
            "CONTRACT ANALYSIS REPORT",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Document info
        doc_info = results.get('document_info', {})
        filename = doc_info.get('filename', 'Unknown')
        
        info_text = f"<b>Document:</b> {filename}<br/>"
        info_text += f"<b>Analysis Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>"
        
        contract_type = results.get('contract_classification', {}).get('contract_type', 'Unknown')
        info_text += f"<b>Contract Type:</b> {contract_type}<br/>"
        
        risk_assessment = results.get('risk_assessment', {})
        risk_level = risk_assessment.get('overall_risk_level', 'Unknown')
        info_text += f"<b>Overall Risk Level:</b> {risk_level}"
        
        info_para = Paragraph(info_text, self.styles['CustomBody'])
        elements.append(info_para)
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Disclaimer
        disclaimer = Paragraph(
            "<i>This report is generated using AI-powered analysis and should be reviewed by qualified legal counsel before making any decisions.</i>",
            self.styles['CustomBody']
        )
        elements.append(disclaimer)
        
        return elements
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> list:
        """Create executive summary section."""
        elements = []
        
        # Section title
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Contract classification
        classification = results.get('contract_classification', {})
        contract_type = classification.get('contract_type', 'Unknown')
        justification = classification.get('justification', '')
        
        elements.append(Paragraph(f"<b>Contract Type:</b> {contract_type}", self.styles['CustomBody']))
        if justification:
            elements.append(Paragraph(justification, self.styles['CustomBody']))
        
        # Summary
        summary = results.get('summary', {}).get('summary', '')
        if summary:
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph("<b>Contract Summary:</b>", self.styles['SubsectionHeading']))
            elements.append(Paragraph(summary, self.styles['CustomBody']))
        
        # Key statistics
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph("<b>Key Statistics:</b>", self.styles['SubsectionHeading']))
        
        nlp_analysis = results.get('nlp_analysis', {})
        stats_data = [
            ['Metric', 'Value'],
            ['Total Clauses', str(nlp_analysis.get('total_clauses', 0))],
            ['Obligations', str(nlp_analysis.get('obligations', 0))],
            ['Rights', str(nlp_analysis.get('rights', 0))],
            ['Prohibitions', str(nlp_analysis.get('prohibitions', 0))],
        ]
        
        stats_table = Table(stats_data, colWidths=[3 * inch, 2 * inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        
        return elements
    
    def _create_contract_details(self, results: Dict[str, Any]) -> list:
        """Create contract details section."""
        elements = []
        
        elements.append(Paragraph("Contract Details", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Document information
        doc_info = results.get('document_info', {})
        
        details_data = [
            ['Property', 'Value'],
            ['Filename', doc_info.get('filename', 'N/A')],
            ['File Type', doc_info.get('file_type', 'N/A').upper()],
            ['Language', doc_info.get('language', 'N/A').upper()],
            ['Word Count', str(doc_info.get('word_count', 0))],
            ['Page Count', str(doc_info.get('page_count', 'N/A'))],
        ]
        
        details_table = Table(details_data, colWidths=[2.5 * inch, 3.5 * inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(details_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_risk_assessment(self, results: Dict[str, Any]) -> list:
        """Create risk assessment section."""
        elements = []
        
        elements.append(Paragraph("Risk Assessment", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.1 * inch))
        
        risk_assessment = results.get('risk_assessment', {})
        
        # Overall risk score
        overall_score = risk_assessment.get('overall_risk_score', 0)
        risk_level = risk_assessment.get('overall_risk_level', 'Unknown')
        
        risk_text = f"<b>Overall Risk Level:</b> {risk_level} ({overall_score:.2f})"
        elements.append(Paragraph(risk_text, self.styles[f'Risk{risk_level}' if risk_level in ['Critical', 'High', 'Medium', 'Low'] else 'CustomBody']))
        
        # Risk statistics
        stats = risk_assessment.get('statistics', {})
        if stats:
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph("<b>Risk Breakdown:</b>", self.styles['SubsectionHeading']))
            
            risk_stats_data = [
                ['Risk Level', 'Count'],
                ['Critical', str(stats.get('critical_risks', 0))],
                ['High', str(stats.get('high_risks', 0))],
                ['Medium', str(stats.get('medium_risks', 0))],
                ['Low', str(stats.get('low_risks', 0))],
            ]
            
            risk_table = Table(risk_stats_data, colWidths=[2.5 * inch, 1.5 * inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(risk_table)
        
        # Identified risks
        identified_risks = risk_assessment.get('identified_risks', [])
        if identified_risks:
            elements.append(Spacer(1, 0.3 * inch))
            elements.append(Paragraph("<b>Identified Risks:</b>", self.styles['SubsectionHeading']))
            
            for i, risk in enumerate(identified_risks[:10], 1):  # Top 10 risks
                risk_para = Paragraph(
                    f"<b>{i}. {risk.get('category', 'Unknown').replace('_', ' ').title()}</b> "
                    f"[{risk.get('severity', 'Unknown')}]<br/>"
                    f"{risk.get('description', '')}<br/>"
                    f"<i>Impact:</i> {risk.get('impact', '')}<br/>"
                    f"<i>Recommendation:</i> {risk.get('recommendation', '')}",
                    self.styles['CustomBody']
                )
                elements.append(risk_para)
                elements.append(Spacer(1, 0.1 * inch))
        
        return elements
    
    def _create_clause_analysis(self, results: Dict[str, Any]) -> list:
        """Create clause analysis section."""
        elements = []
        
        elements.append(Paragraph("Clause-by-Clause Analysis", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.1 * inch))
        
        clause_analyses = results.get('clause_analyses', [])
        
        if not clause_analyses:
            elements.append(Paragraph("No detailed clause analysis available.", self.styles['CustomBody']))
            return elements
        
        for i, clause_analysis in enumerate(clause_analyses[:15], 1):  # Top 15 clauses
            analysis = clause_analysis.get('analysis', {})
            
            # Clause heading
            clause_type = clause_analysis.get('clause_type', 'general').title()
            section = clause_analysis.get('section_number', f"#{i}")
            
            elements.append(Paragraph(
                f"<b>Clause {section}</b> [{clause_type}]",
                self.styles['SubsectionHeading']
            ))
            
            # Analysis
            if isinstance(analysis, dict):
                plain_lang = analysis.get('plain_language_explanation', '')
                if plain_lang:
                    elements.append(Paragraph(f"<b>Explanation:</b> {plain_lang}", self.styles['CustomBody']))
                
                risk_level = analysis.get('risk_level', 'Unknown')
                if risk_level != 'Unknown':
                    elements.append(Paragraph(
                        f"<b>Risk Level:</b> {risk_level}",
                        self.styles[f'Risk{risk_level}' if risk_level in ['Critical', 'High', 'Medium', 'Low'] else 'CustomBody']
                    ))
            
            elements.append(Spacer(1, 0.15 * inch))
        
        return elements
    
    def _create_recommendations(self, results: Dict[str, Any]) -> list:
        """Create recommendations section."""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Risk mitigation recommendations
        risk_assessment = results.get('risk_assessment', {})
        recommendations = risk_assessment.get('recommendations', [])
        
        if recommendations:
            elements.append(Paragraph("<b>Risk Mitigation:</b>", self.styles['SubsectionHeading']))
            
            for i, rec in enumerate(recommendations, 1):
                rec_para = Paragraph(f"{i}. {rec}", self.styles['CustomBody'])
                elements.append(rec_para)
            
            elements.append(Spacer(1, 0.2 * inch))
        
        # Compliance recommendations
        compliance = results.get('compliance_check', {})
        compliance_recs = compliance.get('recommendations', '')
        
        if compliance_recs:
            elements.append(Paragraph("<b>Compliance Recommendations:</b>", self.styles['SubsectionHeading']))
            elements.append(Paragraph(compliance_recs, self.styles['CustomBody']))
        
        # General advice
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("<b>General Advice:</b>", self.styles['SubsectionHeading']))
        
        advice = (
            "1. Review this report with qualified legal counsel before signing the contract.<br/>"
            "2. Negotiate unfavorable terms identified in the risk assessment.<br/>"
            "3. Ensure all parties understand their obligations and rights.<br/>"
            "4. Keep copies of all signed documents and correspondence.<br/>"
            "5. Monitor compliance with contract terms throughout the agreement period."
        )
        
        elements.append(Paragraph(advice, self.styles['CustomBody']))
        
        return elements
    
    def generate_summary_report(
        self,
        analysis_results: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> bytes:
        """
        Generate brief summary report.
        
        Args:
            analysis_results: Analysis results
            output_path: Optional save path
            
        Returns:
            PDF bytes
        """
        logger.info("Generating summary report")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        story = []
        story.extend(self._create_title_page(analysis_results))
        story.append(Spacer(1, 0.3 * inch))
        story.extend(self._create_executive_summary(analysis_results))
        story.append(Spacer(1, 0.2 * inch))
        story.extend(self._create_risk_assessment(analysis_results))
        
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
        
        return pdf_bytes
