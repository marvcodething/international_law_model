# International Contract Analysis System - Simplified MVP

A streamlined contract analysis system using BERT models for US and Indian law with Claude integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Anthropic API key (optional, for enhanced analysis)

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd international_law_model

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.template .env
# Edit .env with your Anthropic API key
```

### Run Application
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## 📁 Project Structure

```
international_law_model/
├── app.py                  # Main Streamlit application
├── contract_models.py      # BERT models for US & Indian law
├── analysis_service.py     # GPT integration & file processing
├── requirements.txt        # Dependencies
├── .env.template          # Environment configuration template
└── README.md              # This file
```

## 🎯 Features

### Contract Analysis
- **Multi-format Support**: Upload PDF, DOCX, or paste text
- **Dual Jurisdiction**: Analyze under US and/or Indian law
- **Clause Classification**: Automatic identification of 12+ clause types
- **Risk Assessment**: AI-powered risk scoring and recommendations

### AI Models
- **US Contract BERT**: Based on nlpaueb/legal-bert-base-uncased
- **Indian Contract BERT**: Based on law-ai/InLegalBERT  
- **Claude Integration**: Enhanced risk assessment and comparisons

### Interactive Interface
- **Real-time Analysis**: Progress tracking and instant results
- **Visual Dashboard**: Charts and risk distribution
- **Clause Explorer**: Detailed examination of individual clauses
- **Comparison View**: Side-by-side jurisdiction analysis

## 📊 Clause Types Supported

### US Law (12 types)
- Termination, Payment, Liability, Confidentiality
- Intellectual Property, Governing Law, Dispute Resolution
- Force Majeure, Indemnification, Warranties, Deliverables, Term

### Indian Law (15 types)  
- All US types plus: Compliance, Registration, Stamp Duty

## 🔧 Configuration

### Environment Variables (.env)
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=1000
ANTHROPIC_TEMPERATURE=0.3
```

### Model Settings
- **GPU Support**: Automatically detected
- **Fallback Models**: DistilBERT if specialized models unavailable
- **Confidence Thresholds**: Adjustable per jurisdiction

## 🎮 Usage

1. **Upload Contract**: Drag & drop or paste contract text
2. **Select Jurisdiction**: US, Indian, or both
3. **Configure Options**: Risk assessment, comparison analysis
4. **Analyze**: Click "Analyze Contract" button
5. **Review Results**: Dashboard, clause details, risk assessment

## 📈 Analysis Output

### Clause Classification
- Clause type identification
- Confidence scores (0-1)
- Risk levels (High/Medium/Low)

### Risk Assessment  
- Overall contract risk
- Risk factor analysis
- Mitigation recommendations
- Jurisdiction-specific considerations

### Comparison Analysis
- Cross-jurisdiction differences
- Legal consideration highlights
- Optimization recommendations

## 🔨 Development

### Adding New Clause Types
1. Edit `contract_models.py`
2. Update `us_clause_types` or `indian_clause_types` lists
3. Retrain models with new data

### Customizing Risk Logic
1. Modify `_determine_risk_level()` in `contract_models.py`
2. Update risk assessment prompts in `analysis_service.py`

### Model Fine-tuning
```python
# Example: Load your fine-tuned models
model_path = "/path/to/your/contract-bert-model"
self.us_model = AutoModelForSequenceClassification.from_pretrained(model_path)
```

## 📋 Limitations

- **Demo Models**: Uses base legal BERT models (not contract-specific yet)
- **Clause Extraction**: Simple sentence splitting (can be enhanced)
- **File Processing**: Basic PDF/DOCX extraction
- **No Database**: Results not persisted between sessions

## 🚀 Future Enhancements

1. **Contract-specific BERT training** on labeled contract datasets
2. **Advanced clause extraction** using NLP techniques  
3. **Database integration** for analysis history
4. **API endpoints** for programmatic access
5. **Multi-language support** for Indian regional languages

## 📝 License

[Your License Here]

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes  
4. Test thoroughly
5. Submit pull request

---

**Time to MVP: 1-2 weeks** vs 14 weeks for full implementation!