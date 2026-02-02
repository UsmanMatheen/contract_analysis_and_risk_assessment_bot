"""LLM prompt templates for contract analysis."""

# Contract Classification Prompt
CONTRACT_CLASSIFICATION_PROMPT = """You are a legal contract classification expert. Analyze the following contract text and classify it into one of these categories:

Categories:
1. Employment Agreement
2. Vendor Contract
3. Lease Agreement
4. Partnership Deed
5. Service Contract
6. Non-Disclosure Agreement
7. Consultancy Agreement
8. Purchase Order

Contract Text:
{contract_text}

Respond with ONLY the category name and a brief justification (2-3 sentences).

Format:
Category: [Category Name]
Justification: [Brief explanation]
"""

# Clause Analysis Prompt
CLAUSE_ANALYSIS_PROMPT = """You are a legal expert analyzing contract clauses for small business owners. Analyze the following clause and provide:

1. Plain-language explanation (simple business English)
2. Key obligations or rights
3. Potential risks or concerns
4. Risk level (Low/Medium/High/Critical)

Clause:
{clause_text}

Provide clear, actionable insights suitable for non-lawyers.
"""

# Risk Assessment Prompt
RISK_ASSESSMENT_PROMPT = """You are a contract risk assessment specialist. Analyze the following contract section for potential risks relevant to Indian SMEs.

Focus on:
- Penalty clauses
- Indemnity obligations
- Unilateral termination rights
- Unfavorable payment terms
- Jurisdiction and arbitration issues
- IP transfer or non-compete restrictions
- Auto-renewal or lock-in periods
- Liability limitations
- Compliance with Indian Contract Act

Contract Section:
{contract_section}

For each identified risk:
1. Risk Category
2. Risk Level (Low/Medium/High/Critical)
3. Specific Concern
4. Business Impact
5. Recommended Action

Be specific and actionable.
"""

# Unfavorable Terms Detection Prompt
UNFAVORABLE_TERMS_PROMPT = """You are reviewing a contract on behalf of a small/medium Indian business. Identify any terms that are potentially unfavorable or one-sided.

Look for:
- Excessive penalties or liquidated damages
- Unlimited liability or indemnification
- One-sided termination clauses
- Unreasonable payment terms
- Overly restrictive non-compete
- Automatic renewal without easy exit
- Unfavorable jurisdiction clauses
- Broad IP assignment
- Weak confidentiality protections

Contract Text:
{contract_text}

For each unfavorable term:
1. Clause excerpt
2. Why it's unfavorable
3. Potential impact
4. Suggested alternative or negotiation point
"""

# Alternative Clause Suggestion Prompt
ALTERNATIVE_CLAUSE_PROMPT = """You are a contract drafting expert. The following clause has been identified as potentially unfavorable. Suggest a more balanced alternative that protects both parties' interests.

Original Clause:
{original_clause}

Identified Issue:
{issue}

Provide:
1. Improved alternative clause (complete text)
2. Explanation of improvements
3. Key protections added for the reviewing party
"""

# Contract Summary Prompt
CONTRACT_SUMMARY_PROMPT = """You are creating a plain-language summary of a legal contract for a small business owner. Summarize the following contract in simple business English.

Include:
1. Contract Type
2. Parties Involved
3. Key Terms (duration, payment, deliverables)
4. Main Obligations (both parties)
5. Important Rights
6. Termination Conditions
7. Notable Restrictions or Limitations
8. Governing Law and Jurisdiction

Contract Text:
{contract_text}

Keep the summary clear, concise, and focused on business implications. Avoid legal jargon.
"""

# Named Entity Extraction Prompt
NER_EXTRACTION_PROMPT = """Extract the following information from the contract:

1. Parties: All party names, roles (e.g., "Employer", "Vendor")
2. Dates: Effective date, termination date, key milestones
3. Financial Terms: Amounts, payment schedules, penalties
4. Locations: Jurisdiction, governing law, place of arbitration
5. Deliverables: Products, services, or obligations
6. Timelines: Duration, deadlines, notice periods
7. IP/Assets: Intellectual property, confidential information

Contract Text:
{contract_text}

Format as structured data with clear labels.
"""

# Compliance Check Prompt
COMPLIANCE_CHECK_PROMPT = """Review the following contract for compliance with common Indian legal standards and business practices.

Check for:
1. Compliance with Indian Contract Act, 1872 principles
2. Reasonable notice periods
3. Fair termination clauses
4. Proper jurisdiction clauses (Indian courts/arbitration)
5. Payment terms aligned with business norms
6. Reasonable liability limitations
7. Clear definition of force majeure
8. Proper confidentiality provisions

Contract Section:
{contract_section}

Identify:
1. Compliant aspects
2. Potential compliance concerns
3. Missing standard protections
4. Recommendations for improvement
"""

# Ambiguity Detection Prompt
AMBIGUITY_DETECTION_PROMPT = """You are a legal language analyst. Review the following contract text for ambiguous, vague, or unclear language that could lead to disputes.

Look for:
- Undefined terms
- Vague timeframes ("reasonable time", "promptly")
- Unclear obligations ("best efforts" vs. "commercially reasonable efforts")
- Undefined financial terms
- Unclear scope of work
- Ambiguous conditions or triggers

Contract Text:
{contract_text}

For each ambiguity:
1. Ambiguous phrase/clause
2. Why it's unclear
3. Potential interpretation issues
4. Suggested clarification
"""

# Multilingual Translation Prompt (Hindi to English)
HINDI_TRANSLATION_PROMPT = """Translate the following Hindi contract text to English, maintaining legal terminology and structure.

Hindi Text:
{hindi_text}

Provide accurate legal translation suitable for contract analysis.
"""

# Risk Mitigation Strategy Prompt
RISK_MITIGATION_PROMPT = """Based on the identified risks in this contract, provide practical risk mitigation strategies for a small/medium Indian business.

Identified Risks:
{identified_risks}

For each risk, suggest:
1. Immediate actions (before signing)
2. Negotiation points
3. Alternative contract terms
4. Protective measures during execution
5. Monitoring and compliance steps

Be practical and actionable for SME owners.
"""

# Template Generation Prompt
TEMPLATE_GENERATION_PROMPT = """Create a balanced, SME-friendly template for a {contract_type} suitable for Indian businesses.

Include:
1. Essential clauses
2. Fair terms for both parties
3. Clear language (minimal jargon)
4. Compliance with Indian laws
5. Reasonable protections
6. Standard termination provisions
7. Dispute resolution mechanism

Provide a complete template with [PLACEHOLDER] markers for customization.
"""
