# Adding New Countries/Jurisdictions

This guide walks you through adding support for a new legal jurisdiction to the Contract Analysis Platform.

## Overview

The platform is designed with extensibility in mind. Adding a new country involves:

1. **Defining jurisdiction-specific clause types**
2. **Configuring or training legal models**
3. **Updating the analysis pipeline**
4. **Modifying the user interface**
5. **Testing and validation**

## Step-by-Step Implementation

### 1. Define Clause Types

Each jurisdiction has specific legal clause types that are relevant to that legal system.

```python
# In contract_models.py, add your jurisdiction's clause types
self.germany_clause_types = [
    "Termination", "Payment", "Liability", "Confidentiality",
    "Data Protection",      # GDPR-specific
    "Works Council",        # German labor law
    "Collective Bargaining", # German employment
    "Probation Period",     # German employment
    "Vacation Entitlement", # German employment
    "Sick Leave",          # German social security
    "Social Insurance",     # German welfare system
    "Corporate Law",        # German business law
    "Tax Obligations"       # German tax law
]
```

### 2. Model Integration

#### Option A: Use Existing Legal BERT Model

```python
def load_german_model(self):
    \"\"\"Load German legal BERT model\"\"\"
    logger.info("Loading German Legal BERT model...")
    
    # Use a German legal model if available
    german_model_name = "german-legal-bert-model"  # Replace with actual model
    
    self.german_tokenizer = AutoTokenizer.from_pretrained(german_model_name)
    self.german_model = AutoModelForSequenceClassification.from_pretrained(
        german_model_name,
        num_labels=len(self.germany_clause_types)
    )
    self.german_model.to(self.device)
```

#### Option B: Fine-tune Your Own Model

```python
# training_script.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer

# Load base German BERT
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-german-cased")
model = AutoModelForSequenceClassification.from_pretrained(
    "dbmdz/bert-base-german-cased",
    num_labels=len(german_clause_types)
)

# Fine-tune on labeled German contract data
# ... training code ...
```

### 3. Update Analysis Pipeline

#### Extend the ContractBERTAnalyzer class:

```python
def __init__(self):
    # ... existing code ...
    
    # Add German model attributes
    self.german_model = None
    self.german_tokenizer = None
    
    # Add German clause types
    self.germany_clause_types = [
        # ... clause types from step 1 ...
    ]

def load_models(self):
    try:
        # ... existing US and Indian model loading ...
        
        # Add German model loading
        self.load_german_model()
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        self._load_fallback_models()

def classify_clause(self, text: str, jurisdiction: str = "all") -> Dict:
    results = {}
    
    # ... existing US and Indian classification ...
    
    # Add German classification
    if jurisdiction in ["germany", "all"]:
        if self.german_model and self.german_tokenizer:
            results["germany"] = self._classify_with_model(
                text, self.german_model, self.german_tokenizer, self.germany_clause_types
            )
    
    return results
```

### 4. Update User Interface

#### Modify app.py to include the new jurisdiction:

```python
# Update jurisdiction selector
jurisdiction = st.selectbox(
    "Select Jurisdiction(s)",
    ["all", "us", "indian", "germany"],  # Add new option
    format_func=lambda x: {
        "all": "🌍 All Jurisdictions",
        "us": "🇺🇸 United States", 
        "indian": "🇮🇳 India",
        "germany": "🇩🇪 Germany"  # Add new mapping
    }[x]
)

# Update results display
def display_analysis_results(results, jurisdiction):
    # ... existing code ...
    
    # Add German metrics
    with col4:  # Add new column
        if "germany" in results["summary"]:
            german_risk = results["summary"]["germany"]["overall_risk"]
            st.metric("German Risk Level", german_risk.upper(), delta=None)

# Update clause table
def display_clause_table(clause_analyses, jurisdiction):
    # ... existing code ...
    
    if jurisdiction == "all":
        # Add German columns
        if "germany" in analysis:
            row.update({
                "German Type": analysis["germany"]["clause_type"],
                "German Risk": analysis["germany"]["risk_level"],
                "German Confidence": f"{analysis['germany']['confidence']:.2f}"
            })
```

### 5. Risk Assessment Integration

```python
# In analysis_service.py
def generate_risk_assessment(self, clause_analyses: List[Dict], jurisdiction: str) -> Dict:
    # ... existing logic ...
    
    # Add German-specific risk factors
    if jurisdiction == "germany":
        # German-specific risk considerations
        german_risk_factors = [
            "Data protection compliance (GDPR)",
            "Works council notification requirements", 
            "Collective bargaining agreement compliance",
            "German labor law restrictions",
            "Tax withholding obligations"
        ]
        
        # Include in risk assessment
        # ... implementation ...
```

### 6. Testing Your Implementation

#### Create test cases:

```python
# tests/test_german_jurisdiction.py
import pytest
from contract_models import ContractBERTAnalyzer

def test_german_clause_classification():
    analyzer = ContractBERTAnalyzer()
    analyzer.load_models()
    
    # Test German contract clause
    german_clause = "Der Arbeitnehmer verpflichtet sich zur Verschwiegenheit..."
    result = analyzer.classify_clause(german_clause, "germany")
    
    assert "germany" in result
    assert result["germany"]["clause_type"] in analyzer.germany_clause_types
    assert 0 <= result["germany"]["confidence"] <= 1

def test_german_contract_analysis():
    analyzer = ContractBERTAnalyzer()
    
    # Test full German contract
    german_contract = \"\"\"
    ARBEITSVERTRAG
    
    Zwischen der Firma ... und Herrn/Frau ...
    wird folgender Arbeitsvertrag geschlossen:
    
    § 1 Beginn und Dauer des Arbeitsverhältnisses
    Das Arbeitsverhältnis beginnt am ...
    \"\"\"
    
    result = analyzer.analyze_contract(german_contract, "germany")
    
    assert "germany" in result["summary"]
    assert result["total_clauses"] > 0
```

### 7. Documentation Updates

#### Update relevant documentation:

1. **README.md**: Add Germany to supported jurisdictions
2. **This file**: Add your jurisdiction as an example
3. **Model documentation**: Describe the German model used
4. **Risk assessment**: Document German-specific risk factors

### 8. Configuration Management

#### Add jurisdiction configuration:

```python
# config/jurisdictions.json (future enhancement)
{
    "germany": {
        "name": "Germany",
        "flag": "🇩🇪",
        "model": "german-legal-bert",
        "clause_types": [
            "Termination", "Payment", "Liability", "Data Protection",
            "Works Council", "Collective Bargaining", "Probation Period"
        ],
        "risk_factors": [
            "GDPR compliance", "Labor law restrictions", "Tax obligations"
        ]
    }
}
```

## Model Training Guide

### Data Collection

1. **Gather German Contracts**: Collect representative German legal contracts
2. **Annotation**: Label clauses with German clause types
3. **Quality Control**: Ensure consistent labeling by legal experts
4. **Data Splitting**: Create train/validation/test sets

### Training Process

```python
# german_model_training.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
import torch

# Load German BERT base model
model_name = "dbmdz/bert-base-german-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(german_clause_types)
)

# Prepare datasets
train_dataset = ContractDataset(train_texts, train_labels, tokenizer)
eval_dataset = ContractDataset(eval_texts, eval_labels, tokenizer)

# Training arguments
training_args = TrainingArguments(
    output_dir='./german-contract-bert',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    evaluation_strategy="steps",
    eval_steps=500,
    save_steps=1000,
    save_total_limit=2,
)

# Train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()

# Save the fine-tuned model
trainer.save_model("./german-contract-bert-final")
tokenizer.save_pretrained("./german-contract-bert-final")
```

## Best Practices

### 1. Legal Expertise
- **Collaborate with German legal experts** for clause type definitions
- **Validate risk assessment logic** with German attorneys
- **Consider local legal nuances** and terminology

### 2. Model Performance
- **Achieve >85% accuracy** on validation set before deployment
- **Test on diverse contract types** (employment, commercial, etc.)
- **Monitor performance** and retrain as needed

### 3. Code Quality
- **Follow existing code patterns** for consistency
- **Add comprehensive tests** for new functionality
- **Update documentation** for all changes
- **Use proper error handling** and logging

### 4. User Experience
- **Provide clear jurisdiction labeling** in UI
- **Include German-specific help text** and examples
- **Offer German language interface** (future enhancement)

## Common Challenges & Solutions

### Challenge: Limited Training Data
**Solution**: Start with multilingual legal BERT models and fine-tune incrementally as more data becomes available.

### Challenge: Legal Terminology Variations
**Solution**: Include synonym mapping and consider multiple valid clause type classifications.

### Challenge: Model Performance
**Solution**: Use ensemble methods or hybrid approaches combining rule-based and ML classification.

### Challenge: Integration Complexity
**Solution**: Follow the established patterns and extend gradually, testing each component individually.

## Community Contribution

When contributing a new jurisdiction:

1. **Open a GitHub issue** first to discuss the implementation
2. **Follow the development workflow** outlined in the main README
3. **Include comprehensive tests** and documentation
4. **Provide sample contracts** (anonymized) for validation
5. **Consider maintenance commitment** for ongoing model updates

## Support

For questions about adding new jurisdictions:
- Open a GitHub discussion
- Check existing jurisdiction implementations for patterns
- Reach out to the community for legal expertise
- Review the architecture documentation for technical details