"""Main NLP processor for contract text analysis."""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import spacy
from spacy.language import Language
import nltk
from nltk.tokenize import sent_tokenize

from config.settings import get_settings
from src.utils import get_logger

logger = get_logger()


@dataclass
class Clause:
    """Represents a contract clause."""
    
    id: str
    text: str
    clause_type: str  # obligation, right, prohibition, general
    section_number: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    entities: Dict[str, List[str]] = field(default_factory=dict)
    sentence_count: int = 0
    word_count: int = 0


@dataclass
class LegalEntity:
    """Represents a legal entity extracted from contract."""
    
    entity_type: str  # PARTY, DATE, MONEY, JURISDICTION, OBLIGATION, etc.
    text: str
    context: str
    confidence: float = 1.0


class NLPProcessor:
    """
    NLP processor for contract text analysis.
    
    Features:
    - Clause extraction and classification
    - Named Entity Recognition (NER)
    - Obligation/Right/Prohibition detection
    - Keyword extraction
    - Sentence segmentation
    """
    
    def __init__(self):
        """Initialize NLP processor."""
        self.settings = get_settings()
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_lg")
            logger.info("Loaded spaCy model: en_core_web_lg")
        except OSError:
            logger.warning("en_core_web_lg not found, using en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Add custom pipeline components
        self._setup_custom_components()
        
        # Download NLTK data if needed
        self._ensure_nltk_data()
        
        # Legal keywords
        self.obligation_keywords = {
            'shall', 'must', 'will', 'required to', 'obligated to',
            'agrees to', 'undertakes to', 'covenant', 'bound to'
        }
        
        self.right_keywords = {
            'may', 'entitled to', 'right to', 'permitted to',
            'authorized to', 'can', 'allowed to', 'privilege'
        }
        
        self.prohibition_keywords = {
            'shall not', 'must not', 'may not', 'prohibited from',
            'forbidden to', 'restricted from', 'cannot', 'will not'
        }
        
        # Risk-related keywords
        self.risk_keywords = {
            'penalty', 'liquidated damages', 'indemnify', 'indemnification',
            'liability', 'terminate', 'termination', 'breach', 'default',
            'force majeure', 'arbitration', 'jurisdiction', 'non-compete',
            'confidential', 'intellectual property', 'warranty', 'guarantee'
        }
        
        logger.info("NLPProcessor initialized")
    
    def _setup_custom_components(self):
        """Setup custom spaCy pipeline components."""
        # Add sentence segmentation rules for legal text
        if not self.nlp.has_pipe("sentencizer"):
            sentencizer = self.nlp.add_pipe("sentencizer")
    
    def _ensure_nltk_data(self):
        """Ensure required NLTK data is downloaded."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            logger.info("Downloading NLTK stopwords")
            nltk.download('stopwords', quiet=True)
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        Process contract text with full NLP pipeline.
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary with all NLP analysis results
        """
        logger.info("Processing contract text with NLP pipeline")
        
        # Extract clauses
        clauses = self.extract_clauses(text)
        logger.info(f"Extracted {len(clauses)} clauses")
        
        # Extract entities
        entities = self.extract_entities(text)
        logger.info(f"Extracted {len(entities)} entities")
        
        # Detect obligations, rights, prohibitions
        clause_classifications = self.classify_clauses(clauses)
        
        # Extract key terms
        key_terms = self.extract_key_terms(text)
        
        return {
            'clauses': [self._clause_to_dict(c) for c in clauses],
            'entities': self._group_entities(entities),
            'clause_classifications': clause_classifications,
            'key_terms': key_terms,
            'statistics': {
                'total_clauses': len(clauses),
                'total_entities': len(entities),
                'obligations': len([c for c in clauses if c.clause_type == 'obligation']),
                'rights': len([c for c in clauses if c.clause_type == 'right']),
                'prohibitions': len([c for c in clauses if c.clause_type == 'prohibition']),
            }
        }
    
    def extract_clauses(self, text: str) -> List[Clause]:
        """
        Extract clauses from contract text.
        
        Args:
            text: Contract text
            
        Returns:
            List of Clause objects
        """
        clauses = []
        
        # Strategy 1: Split by numbered sections (1., 2., etc.)
        section_pattern = r'(?:^|\n)(\d+\.(?:\d+\.)*)\s*([A-Z][^\n]+)'
        sections = re.split(section_pattern, text, flags=re.MULTILINE)
        
        if len(sections) > 3:  # Found numbered sections
            for i in range(1, len(sections), 3):
                if i + 2 <= len(sections):
                    section_num = sections[i].strip()
                    title = sections[i + 1].strip()
                    content = sections[i + 2].strip() if i + 2 < len(sections) else ""
                    
                    clause_text = f"{title}\n{content}".strip()
                    if clause_text:
                        clause = self._create_clause(
                            clause_id=f"clause_{len(clauses) + 1}",
                            text=clause_text,
                            section_number=section_num
                        )
                        clauses.append(clause)
        else:
            # Strategy 2: Split by paragraphs
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs, 1):
                para = para.strip()
                if para and len(para) > 50:  # Minimum clause length
                    clause = self._create_clause(
                        clause_id=f"clause_{i}",
                        text=para
                    )
                    clauses.append(clause)
        
        return clauses
    
    def _create_clause(
        self,
        clause_id: str,
        text: str,
        section_number: Optional[str] = None
    ) -> Clause:
        """Create a Clause object with analysis."""
        # Determine clause type
        clause_type = self._determine_clause_type(text)
        
        # Extract keywords
        keywords = self._extract_keywords_from_text(text)
        
        # Count sentences and words
        sentences = sent_tokenize(text)
        words = text.split()
        
        return Clause(
            id=clause_id,
            text=text,
            clause_type=clause_type,
            section_number=section_number,
            keywords=keywords,
            sentence_count=len(sentences),
            word_count=len(words)
        )
    
    def _determine_clause_type(self, text: str) -> str:
        """Determine if clause is obligation, right, prohibition, or general."""
        text_lower = text.lower()
        
        # Check for prohibitions first (more specific)
        for keyword in self.prohibition_keywords:
            if keyword in text_lower:
                return 'prohibition'
        
        # Check for obligations
        for keyword in self.obligation_keywords:
            if keyword in text_lower:
                return 'obligation'
        
        # Check for rights
        for keyword in self.right_keywords:
            if keyword in text_lower:
                return 'right'
        
        return 'general'
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        keywords = []
        text_lower = text.lower()
        
        # Check for risk keywords
        for keyword in self.risk_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords
    
    def extract_entities(self, text: str) -> List[LegalEntity]:
        """
        Extract named entities from contract.
        
        Args:
            text: Contract text
            
        Returns:
            List of LegalEntity objects
        """
        entities = []
        
        # Process with spaCy
        doc = self.nlp(text[:1000000])  # Limit to 1M chars for memory
        
        for ent in doc.ents:
            # Map spaCy entity types to legal entity types
            entity_type = self._map_entity_type(ent.label_)
            
            # Get context (surrounding text)
            start = max(0, ent.start_char - 50)
            end = min(len(text), ent.end_char + 50)
            context = text[start:end]
            
            legal_entity = LegalEntity(
                entity_type=entity_type,
                text=ent.text,
                context=context
            )
            entities.append(legal_entity)
        
        # Extract custom legal entities
        custom_entities = self._extract_custom_entities(text)
        entities.extend(custom_entities)
        
        return entities
    
    def _map_entity_type(self, spacy_label: str) -> str:
        """Map spaCy entity labels to legal entity types."""
        mapping = {
            'PERSON': 'PARTY',
            'ORG': 'PARTY',
            'DATE': 'DATE',
            'MONEY': 'MONEY',
            'GPE': 'JURISDICTION',
            'LAW': 'LAW_REFERENCE',
            'CARDINAL': 'NUMBER',
            'PERCENT': 'PERCENTAGE',
            'TIME': 'TIME_PERIOD'
        }
        return mapping.get(spacy_label, spacy_label)
    
    def _extract_custom_entities(self, text: str) -> List[LegalEntity]:
        """Extract custom legal entities using patterns."""
        entities = []
        
        # Extract amounts (INR)
        amount_pattern = r'(?:INR|Rs\.?|₹)\s*[\d,]+(?:\.\d{2})?'
        for match in re.finditer(amount_pattern, text):
            entities.append(LegalEntity(
                entity_type='MONEY',
                text=match.group(),
                context=text[max(0, match.start()-30):match.end()+30]
            ))
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entities.append(LegalEntity(
                entity_type='EMAIL',
                text=match.group(),
                context=text[max(0, match.start()-30):match.end()+30]
            ))
        
        # Extract notice periods
        notice_pattern = r'\d+\s*(?:days?|months?|years?)\s*(?:notice|prior notice)'
        for match in re.finditer(notice_pattern, text, re.IGNORECASE):
            entities.append(LegalEntity(
                entity_type='NOTICE_PERIOD',
                text=match.group(),
                context=text[max(0, match.start()-30):match.end()+30]
            ))
        
        return entities
    
    def classify_clauses(self, clauses: List[Clause]) -> Dict[str, List[str]]:
        """
        Classify clauses by type.
        
        Args:
            clauses: List of Clause objects
            
        Returns:
            Dictionary mapping clause types to clause IDs
        """
        classification = {
            'obligations': [],
            'rights': [],
            'prohibitions': [],
            'general': []
        }
        
        for clause in clauses:
            if clause.clause_type == 'obligation':
                classification['obligations'].append(clause.id)
            elif clause.clause_type == 'right':
                classification['rights'].append(clause.id)
            elif clause.clause_type == 'prohibition':
                classification['prohibitions'].append(clause.id)
            else:
                classification['general'].append(clause.id)
        
        return classification
    
    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms from contract.
        
        Args:
            text: Contract text
            
        Returns:
            List of key terms
        """
        doc = self.nlp(text[:100000])  # Limit for performance
        
        # Extract noun phrases
        key_terms = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) >= 2:  # Multi-word terms
                key_terms.append(chunk.text)
        
        # Deduplicate and sort by frequency
        from collections import Counter
        term_counts = Counter(key_terms)
        top_terms = [term for term, count in term_counts.most_common(20)]
        
        return top_terms
    
    def _clause_to_dict(self, clause: Clause) -> Dict[str, Any]:
        """Convert Clause object to dictionary."""
        return {
            'id': clause.id,
            'text': clause.text,
            'clause_type': clause.clause_type,
            'section_number': clause.section_number,
            'keywords': clause.keywords,
            'entities': clause.entities,
            'sentence_count': clause.sentence_count,
            'word_count': clause.word_count
        }
    
    def _group_entities(self, entities: List[LegalEntity]) -> Dict[str, List[Dict[str, Any]]]:
        """Group entities by type."""
        grouped = {}
        
        for entity in entities:
            if entity.entity_type not in grouped:
                grouped[entity.entity_type] = []
            
            grouped[entity.entity_type].append({
                'text': entity.text,
                'context': entity.context,
                'confidence': entity.confidence
            })
        
        return grouped
