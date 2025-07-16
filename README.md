# Contract Analysis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

Open-source legal contract analysis platform supporting multiple jurisdictions with AI-powered insights. Built for extensibility - easily add new countries, legal systems, and trained models.

## 🌟 Features

- **Multi-Jurisdiction Analysis**: Currently supports US and Indian legal frameworks
- **AI-Powered Classification**: BERT-based clause type identification and risk assessment
- **Interactive Chatbot**: Ask questions about contracts using Claude AI
- **Extensible Architecture**: Plugin system for adding new countries and models
- **Real-time Analysis**: Process PDF, DOCX, or text contracts instantly
- **Risk Assessment**: Automated risk scoring and recommendations
- **Comparative Analysis**: Side-by-side jurisdiction comparison

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Anthropic API key (optional, for AI chatbot features)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/contract-analysis-platform.git
cd contract-analysis-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env with your API keys
```

### Run the Application

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## 📁 Project Structure

```
contract-analysis-platform/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── .env.template            # Environment variables template
├── app.py                   # Main Streamlit application
├── contract_models.py       # BERT model implementations
├── analysis_service.py      # AI services and file processing
├── docs/                    # Documentation
│   ├── adding-countries.md  # Guide for adding new jurisdictions
│   ├── model-training.md    # Model training documentation
│   └── architecture.md      # System architecture guide
├── examples/                # Example implementations
│   ├── new_country_template/ # Template for new jurisdictions
│   └── custom_model_guide/   # Custom model integration guide
└── .github/                 # GitHub templates and workflows
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
```

## 🎯 Usage

### Basic Analysis

1. **Upload Contract**: Drag & drop PDF/DOCX or paste text
2. **Select Jurisdiction**: Choose US, Indian, or both
3. **Configure Options**: Enable risk assessment and comparison
4. **Analyze**: Click "Analyze Contract" and view results
5. **Explore**: Use the dashboard, clause explorer, and AI assistant

### AI Assistant

The integrated chatbot can answer questions about:
- Contract risks and implications
- Jurisdiction differences
- Specific clause analysis
- Legal recommendations

Example questions:
- "What are the highest risk clauses in this contract?"
- "How do US and Indian analyses differ for payment terms?"
- "Which jurisdiction is more favorable for termination?"

## 🛠️ Adding New Countries

The platform is designed for easy extension. To add a new jurisdiction:

### 1. Define Clause Types

Create jurisdiction-specific clause types:

```python
# In contract_models.py
self.germany_clause_types = [
    "Termination", "Payment", "Liability", "Data Protection",
    "Works Council", "Collective Bargaining", "Probation"
]
```

### 2. Add Model Configuration

```python
# Add German model loading
def load_german_model(self):
    self.german_tokenizer = AutoTokenizer.from_pretrained("german-legal-bert")
    self.german_model = AutoModelForSequenceClassification.from_pretrained(
        "german-legal-bert",
        num_labels=len(self.germany_clause_types)
    )
```

### 3. Update Classification Logic

```python
# Extend classify_clause method
if jurisdiction in ["germany", "all"]:
    results["germany"] = self._classify_with_model(
        text, self.german_model, self.german_tokenizer, self.germany_clause_types
    )
```

### 4. Update UI

Add the new jurisdiction to the Streamlit interface:

```python
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
```

See [docs/adding-countries.md](docs/adding-countries.md) for detailed implementation guide.

## 🤖 Model Training

### Supported Models

- **US**: `muhtasham/bert-tiny-finetuned-legal-contracts-longer`
- **India**: `law-ai/InLegalBERT`
- **Fallback**: `distilbert-base-uncased` (for any jurisdiction)

### Training Your Own Models

1. **Prepare Dataset**: Label contracts with clause types and jurisdictions
2. **Fine-tune BERT**: Use Hugging Face transformers
3. **Integrate Model**: Add to contract_models.py
4. **Test & Validate**: Ensure accuracy meets requirements

```python
# Example training script
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

See [docs/model-training.md](docs/model-training.md) for comprehensive training guide.

## 🔧 Configuration

### Environment Variables

```bash
# .env file
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=1500
ANTHROPIC_TEMPERATURE=0.3
```

### Model Configuration

```python
# contract_models.py - Easy model swapping
US_MODEL = "muhtasham/bert-tiny-finetuned-legal-contracts-longer"
INDIAN_MODEL = "law-ai/InLegalBERT"
FALLBACK_MODEL = "distilbert-base-uncased"
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Quick Contributions

- 🐛 **Bug Reports**: Use GitHub issues with the bug template
- 💡 **Feature Requests**: Use GitHub issues with the feature template
- 📖 **Documentation**: Improve docs, add examples, fix typos
- 🌍 **New Jurisdictions**: Add support for new countries/legal systems

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Add** tests if applicable
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/contract-analysis-platform.git

# Create development environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If you create this

# Run tests
python -m pytest tests/

# Run the app locally
streamlit run app.py
```

### Code Standards

- **Comments**: Use `# FUNC:` for function descriptions, `# PARAM:` for parameters
- **Type Hints**: Add type annotations for better code clarity
- **Documentation**: Update relevant docs for new features
- **Testing**: Add tests for new functionality

## 📊 Supported Clause Types

### US Legal Framework (12 types)
- Termination, Payment, Liability, Confidentiality
- Intellectual Property, Governing Law, Dispute Resolution
- Force Majeure, Indemnification, Warranties, Deliverables, Term

### Indian Legal Framework (15 types)
- All US types plus: Compliance, Registration, Stamp Duty

### Adding New Types

```python
# Extend existing or create new jurisdiction clause types
self.new_jurisdiction_clause_types = [
    "Standard clauses...",
    "Jurisdiction-specific clause 1",
    "Jurisdiction-specific clause 2"
]
```

## 🔬 API Reference

### Core Classes

#### `ContractBERTAnalyzer`
Main analysis engine for contract processing.

```python
analyzer = ContractBERTAnalyzer()
analyzer.load_models()
result = analyzer.analyze_contract(text, jurisdiction="both")
```

#### `ContractAnalysisService`
File processing and AI integration service.

```python
service = ContractAnalysisService()
risk_assessment = service.generate_risk_assessment(clauses, "us")
comparison = service.compare_jurisdictions(us_data, indian_data)
chat_response = service.chat_about_contract(question, analysis_results)
```

### Key Methods

- `analyze_contract()`: Full contract analysis pipeline
- `classify_clause()`: Single clause classification
- `extract_clauses()`: Text parsing and clause extraction
- `generate_risk_assessment()`: Risk scoring and recommendations

## 📈 Roadmap

### Immediate (v1.1)
- [ ] Configuration-based jurisdiction management
- [ ] Plugin system for custom models
- [ ] Batch processing capability
- [ ] Export functionality (PDF, Excel)

### Short-term (v1.2-1.3)
- [ ] Database integration for analysis history
- [ ] REST API endpoints
- [ ] Advanced clause extraction (NLP-based)
- [ ] Multi-language support

### Long-term (v2.0+)
- [ ] Machine learning model marketplace
- [ ] Collaborative annotation platform
- [ ] Enterprise deployment options
- [ ] Integration with legal databases

## 🏆 Recognition

This project builds upon excellent work from:
- [Hugging Face](https://huggingface.co) - Transformer models and infrastructure
- [nlpaueb/legal-bert-base-uncased](https://huggingface.co/nlpaueb/legal-bert-base-uncased) - Legal BERT foundation
- [law-ai/InLegalBERT](https://huggingface.co/law-ai/InLegalBERT) - Indian legal language model
- [muhtasham/bert-tiny-finetuned-legal-contracts-longer](https://huggingface.co/muhtasham/bert-tiny-finetuned-legal-contracts-longer) - Contract-specific fine-tuning

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Community & Support

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community forum for questions and ideas
- **Documentation**: Comprehensive guides in the `docs/` directory
- **Examples**: Ready-to-use templates in `examples/`

## 🎉 Getting Started as a Contributor

1. **Star** this repository ⭐
2. **Read** the [contributing guidelines](CONTRIBUTING.md)
3. **Check** open issues for good first contributions
4. **Join** our community discussions
5. **Make** your first contribution!

---

**Built with ❤️ by the open-source community**

[Report Bug](https://github.com/yourusername/contract-analysis-platform/issues) • [Request Feature](https://github.com/yourusername/contract-analysis-platform/issues) • [Documentation](docs/) • [Examples](examples/)