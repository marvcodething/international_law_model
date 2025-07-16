# Contract Analysis Platform

Open-source legal contract analysis platform supporting multiple jurisdictions with AI-powered insights. Built for extensibility—easily add new countries, legal systems, and trained models.

## Features

- Multi-jurisdiction contract analysis (US and Indian legal frameworks supported)
- AI-powered clause classification and risk assessment
- Interactive chatbot for contract questions (Claude AI)
- Extensible architecture for adding new countries and models
- Real-time analysis of PDF, DOCX, or text contracts
- Automated risk scoring and recommendations
- Comparative analysis between jurisdictions

## Quick Start

### Prerequisites
- Python 3.11 or higher
- (Optional) Anthropic API key for AI chatbot features

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/contract-analysis-platform.git
cd contract-analysis-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env with your API keys if needed
```

### Running the Application

#### Option 1: Standard Python Setup
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

#### Option 2: Docker (Recommended)
```bash
# Using Docker Compose (easiest)
docker-compose up

# Or build and run manually
docker build -t contract-analysis-platform .
docker run -p 8501:8501 contract-analysis-platform
```
Open http://localhost:8501 in your browser.

### Docker Deployment

The application is fully containerized for easy deployment:

```bash
# Quick start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

#### Environment Variables for Docker
Create a `.env` file for API keys:
```bash
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## Usage

1. Upload a contract (PDF, DOCX, or text)
2. Select jurisdiction (US, Indian, or both)
3. Configure options (risk assessment, comparison)
4. Click "Analyze Contract" to view results
5. Use the dashboard, clause explorer, and AI assistant as needed

## Extending the Platform

To add a new jurisdiction:
1. Define clause types in `contract_models.py`
2. Add model configuration and loading logic
3. Update classification logic
4. Update the Streamlit UI to include the new jurisdiction

See `docs/adding-countries.md` for details.

## Model Training

- US model: `muhtasham/bert-tiny-finetuned-legal-contracts-longer`
- Indian model: `law-ai/InLegalBERT`
- Fallback: `distilbert-base-uncased`

To train your own model, prepare a labeled dataset, fine-tune a BERT model, and integrate it in `contract_models.py`.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push your branch
5. Open a Pull Request

See the `docs/` directory for more information on extending and developing the platform.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
