"""
Template for adding a new jurisdiction to the Contract Analysis Platform

Replace [COUNTRY] with your country name (e.g., "germany", "france", "canada")
Replace [FLAG] with appropriate flag emoji (e.g., "🇩🇪", "🇫🇷", "🇨🇦")
"""

# JURISDICTION CONFIGURATION TEMPLATE

# Basic Information
COUNTRY_CODE = "[COUNTRY]"  # e.g., "germany"
COUNTRY_NAME = "[COUNTRY] Legal System"  # e.g., "German Legal System"
COUNTRY_FLAG = "[FLAG]"  # e.g., "🇩🇪"

# Clause Types Specific to This Jurisdiction
CLAUSE_TYPES = [
    # Standard contract clauses (common across jurisdictions)
    "Termination",
    "Payment", 
    "Liability",
    "Confidentiality",
    "Intellectual Property",
    "Governing Law",
    "Dispute Resolution",
    "Force Majeure",
    "Indemnification",
    "Warranties",
    "Deliverables",
    "Term",
    
    # Add jurisdiction-specific clause types below
    "[COUNTRY]-Specific Clause 1",  # e.g., "Data Protection" for Germany
    "[COUNTRY]-Specific Clause 2",  # e.g., "Works Council" for Germany
    "[COUNTRY]-Specific Clause 3",  # e.g., "Collective Bargaining" for Germany
    
    # Add more as needed based on your legal system
]

# Model Configuration
MODEL_CONFIG = {
    # Primary model for this jurisdiction (if available)
    "primary_model": "[COUNTRY]-legal-bert",  # e.g., "german-legal-bert"
    
    # Fallback model if primary is not available
    "fallback_model": "distilbert-base-uncased",
    
    # Model source (huggingface model name or local path)
    "model_source": "your-org/[COUNTRY]-legal-bert",
    
    # Tokenizer (usually same as model)
    "tokenizer_source": "your-org/[COUNTRY]-legal-bert",
}

# Risk Factors Specific to This Jurisdiction
JURISDICTION_RISK_FACTORS = [
    "[COUNTRY] regulatory compliance",
    "[COUNTRY] tax obligations", 
    "[COUNTRY] employment law restrictions",
    "[COUNTRY] data protection requirements",
    "[COUNTRY] consumer protection laws",
    
    # Add more jurisdiction-specific risk factors
]

# Risk Level Mappings (customize based on local legal norms)
RISK_LEVEL_MAPPING = {
    "high": {
        "clause_types": ["Liability", "Termination", "[COUNTRY]-Specific Clause 1"],
        "confidence_threshold": 0.8
    },
    "medium": {
        "clause_types": ["Payment", "Intellectual Property", "Governing Law"],
        "confidence_threshold": 0.6
    },
    "low": {
        "clause_types": ["Confidentiality", "Warranties", "Deliverables"],
        "confidence_threshold": 0.4
    }
}

# Language Configuration
LANGUAGE_CONFIG = {
    "primary_language": "[LANGUAGE]",  # e.g., "german", "french"
    "language_code": "[LANG]",         # e.g., "de", "fr"
    "supports_multilingual": True,     # Set to False if only one language
    "fallback_language": "english"     # Fallback for translations
}

# Integration Configuration
INTEGRATION_CONFIG = {
    "ui_label": f"{COUNTRY_FLAG} {COUNTRY_NAME}",
    "short_code": COUNTRY_CODE,
    "enabled": True,  # Set to False to disable this jurisdiction
    "beta": True,     # Set to False once fully tested
}

# Sample Contract Patterns (for testing and validation)
SAMPLE_PATTERNS = {
    "contract_headers": [
        f"[COUNTRY] CONTRACT",
        f"{COUNTRY_NAME.upper()} AGREEMENT",
        # Add more patterns specific to your jurisdiction
    ],
    
    "common_phrases": [
        "according to [COUNTRY] law",
        "governed by [COUNTRY] legislation",
        # Add more common legal phrases
    ],
    
    "legal_terms": [
        # Add jurisdiction-specific legal terminology
        "[legal term 1]",
        "[legal term 2]",
        "[legal term 3]",
    ]
}