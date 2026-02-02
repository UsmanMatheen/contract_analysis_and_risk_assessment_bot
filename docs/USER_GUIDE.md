# 📖 User Guide

## Getting Started

### First Time Setup

1. **Access the Application**
   - Open your web browser
   - Navigate to the application URL
   - You'll see the main dashboard

2. **Check Configuration**
   - Look at the sidebar
   - Verify that "✓ OPENAI configured" or "✓ ANTHROPIC configured" appears
   - If you see an error, contact your administrator

## Using the Application

### Tab 1: Analyze Contract

#### Step 1: Upload Your Contract

1. Click on "Choose a contract file"
2. Select your contract file (PDF, DOCX, DOC, or TXT)
3. Maximum file size: 10 MB
4. Wait for the "✓ File uploaded" confirmation

**Supported Formats:**
- PDF (text-based - scanned PDFs may not work well)
- Microsoft Word (DOCX, DOC)
- Plain text (TXT)

#### Step 2: Configure Analysis Options

**Contract Language:**
- English (default)
- Hindi (experimental)

**Analysis Type:**
- **Full Analysis** (Recommended): Complete analysis with all features
  - Takes 2-5 minutes
  - Includes detailed clause analysis
  - Generates comprehensive risk assessment
  
- **Quick Analysis**: Fast overview
  - Takes 30-60 seconds
  - Basic classification and statistics
  - Good for initial review

#### Step 3: Start Analysis

1. Click "🔍 Analyze Contract" button
2. Wait for the analysis to complete
3. Progress will be shown on screen

#### Step 4: Review Results

The analysis results are organized into sections:

**Overview Metrics:**
- **Contract Type**: Classification (e.g., Employment Agreement, Service Contract)
- **Word Count**: Total words in the document
- **Clauses Analyzed**: Number of clauses identified
- **Risk Level**: Overall risk rating (Low/Medium/High/Critical)

**Contract Summary:**
- Plain-language summary of the contract
- Key terms and conditions
- Main obligations for both parties

**Risk Assessment:**
- Overall risk score (0.0 to 1.0)
- Breakdown by severity (Critical, High, Medium, Low)
- Detailed list of identified risks
- Each risk includes:
  - Category (e.g., penalty, indemnity, termination)
  - Severity level
  - Description of the risk
  - Business impact
  - Recommendation for mitigation

**Clause Analysis:**
- Individual analysis of key clauses
- Plain-language explanations
- Risk level for each clause
- Specific concerns and recommendations

**Recommendations:**
- Actionable advice for risk mitigation
- Compliance recommendations
- Negotiation points
- General best practices

#### Step 5: Export Report

Choose one of two report types:

**Full PDF Report:**
- Complete analysis with all details
- Professional formatting
- Suitable for legal review
- 10-20 pages typically

**Summary PDF:**
- Executive summary
- Key findings and recommendations
- 3-5 pages typically

### Tab 2: Templates

Access pre-built, SME-friendly contract templates:

**Available Templates:**
1. Employment Agreement
2. Service Contract
3. Non-Disclosure Agreement (NDA)
4. Consultancy Agreement
5. Vendor Contract

**How to Use Templates:**
1. Click on a template to expand
2. Review the template content
3. Click "View Template" to see full text
4. Click "⬇️ Download Template" to save
5. Customize the template for your needs
   - Replace [PLACEHOLDERS] with your information
   - Adjust terms as needed
   - Have a lawyer review before use

### Tab 3: Reports

View your current session's analysis results and activity log.

**Features:**
- Access current analysis results
- View session activity history
- Review all actions taken during your session

### Tab 4: About

Learn more about the application:
- Purpose and capabilities
- Technology stack
- Supported contract types
- Disclaimer and legal notes
- Privacy and security information

## Understanding Risk Levels

### Critical (0.8 - 1.0)
- **Meaning**: Extremely unfavorable terms that could result in severe consequences
- **Action**: Do NOT sign without legal counsel
- **Examples**:
  - Unlimited liability
  - Extremely harsh penalties
  - Complete IP rights transfer without compensation

### High (0.6 - 0.8)
- **Meaning**: Significantly unfavorable terms that pose substantial risk
- **Action**: Negotiate these terms before signing
- **Examples**:
  - Large indemnification clauses
  - Unilateral termination rights
  - Excessive penalties

### Medium (0.3 - 0.6)
- **Meaning**: Terms that may be unfavorable and should be reviewed
- **Action**: Consider negotiating or seek clarification
- **Examples**:
  - Reasonable non-compete clauses
  - Standard confidentiality terms
  - Moderate lock-in periods

### Low (0.0 - 0.3)
- **Meaning**: Standard terms with minimal risk
- **Action**: Review for understanding, generally acceptable
- **Examples**:
  - Standard notice periods
  - Reasonable payment terms
  - Fair jurisdiction clauses

## Common Risk Categories

### 1. Penalty Clauses
- Financial penalties for breach
- Liquidated damages
- **Watch for**: Excessive or unreasonable amounts

### 2. Indemnity Clauses
- Obligation to compensate for third-party claims
- **Watch for**: Unlimited scope or unreasonable coverage

### 3. Termination Terms
- Conditions for ending the contract
- **Watch for**: Unilateral termination, no notice period

### 4. Liability Limitations
- Caps on damages and liability
- **Watch for**: Unlimited liability, one-sided limitations

### 5. Non-Compete Clauses
- Restrictions on business activities
- **Watch for**: Overly broad scope, long duration, large geographical area

### 6. IP Transfer
- Transfer of intellectual property rights
- **Watch for**: Broad assignments, no compensation

### 7. Jurisdiction
- Where disputes will be resolved
- **Watch for**: Foreign jurisdictions, unfamiliar legal systems

### 8. Payment Terms
- How and when payment is made
- **Watch for**: Full advance payment, no milestones, no refunds

### 9. Confidentiality
- Obligations to keep information secret
- **Watch for**: Perpetual terms, overly broad definitions

### 10. Lock-in Periods
- Minimum commitment duration
- **Watch for**: Long periods, no early exit, automatic renewal

## Best Practices

### Before Analysis
1. ✅ Ensure you have a clean, readable document
2. ✅ Check file size is under 10 MB
3. ✅ Have the complete contract (not just excerpts)

### During Analysis
1. ✅ Select the correct language
2. ✅ Choose "Full Analysis" for important contracts
3. ✅ Wait for complete results (don't interrupt)

### After Analysis
1. ✅ Read the entire analysis carefully
2. ✅ Pay special attention to Critical and High risks
3. ✅ Download and save the PDF report
4. ✅ Share results with your legal advisor
5. ✅ Use recommendations as negotiation points

### Important Notes
- ⚠️ **Not Legal Advice**: This tool provides analysis, not legal counsel
- ⚠️ **Always Consult Lawyers**: Have qualified legal counsel review important contracts
- ⚠️ **Verify Information**: Double-check all extracted information
- ⚠️ **Context Matters**: AI may not understand your specific business context

## Troubleshooting

### Problem: Analysis Takes Too Long
- **Cause**: Large document or server load
- **Solution**: Wait patiently, or try Quick Analysis first

### Problem: Analysis Failed
- **Causes**:
  - File format not supported
  - Corrupted file
  - File too large
  - Server error
- **Solutions**:
  - Convert to supported format
  - Try a different file
  - Reduce file size
  - Contact administrator

### Problem: Poor Quality Results
- **Causes**:
  - Scanned PDF (image-based)
  - Poor document quality
  - Unusual formatting
- **Solutions**:
  - Use text-based PDF
  - Clean up document formatting
  - Try DOCX format instead

### Problem: Can't Download Report
- **Cause**: Browser blocking download
- **Solution**: Check browser settings, allow downloads

## Privacy and Security

### What We Do
- ✅ Analyze your contract using AI
- ✅ Generate analysis reports
- ✅ Log activity for troubleshooting
- ✅ Protect your data

### What We DON'T Do
- ❌ Store your contracts permanently
- ❌ Share your data with third parties
- ❌ Use your contracts to train AI models
- ❌ Keep copies after your session ends

### Your Responsibilities
- Ensure you have right to upload the contract
- Don't upload highly confidential documents to public instances
- Review privacy policy of your deployment

## Getting Help

### If You Need Assistance
1. Check this user guide first
2. Review the "About" tab for basic information
3. Contact your system administrator
4. For technical issues, provide:
   - What you were trying to do
   - What error message you saw
   - When the problem occurred

## Tips for Best Results

1. **Use Clean Documents**: Well-formatted contracts produce better results
2. **Full Analysis for Important Contracts**: Don't skip the detailed analysis
3. **Read Everything**: Don't rely solely on risk scores
4. **Negotiate**: Use identified risks as negotiation leverage
5. **Get Legal Review**: Always have important contracts reviewed by a lawyer
6. **Keep Reports**: Save PDF reports for your records
7. **Update Regularly**: Check if newer versions of the tool are available

---

**Happy Analyzing! Make informed decisions with AI-powered insights.**
