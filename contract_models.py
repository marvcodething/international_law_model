import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractBERTAnalyzer:
    """Contract analysis using BERT models for US and Indian law"""
    
    def __init__(self):
        self.us_model = None
        self.indian_model = None
        self.us_tokenizer = None
        self.indian_tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Contract clause types
        self.us_clause_types = [
            "Termination", "Payment", "Liability", "Confidentiality", 
            "Intellectual Property", "Governing Law", "Dispute Resolution",
            "Force Majeure", "Indemnification", "Warranties", "Deliverables", "Term"
        ]
        
        self.indian_clause_types = [
            "Termination", "Payment", "Liability", "Confidentiality",
            "Intellectual Property", "Governing Law", "Dispute Resolution", 
            "Force Majeure", "Indemnification", "Warranties", "Deliverables",
            "Term", "Compliance", "Registration", "Stamp Duty"
        ]
    
    def load_models(self):
        """Load pre-trained BERT models"""
        try:
            # US Legal BERT - Fine-tuned for contracts
            logger.info("Loading US Legal BERT model...")
            us_model_name = "muhtasham/bert-tiny-finetuned-legal-contracts-longer"
            self.us_tokenizer = AutoTokenizer.from_pretrained(us_model_name)
            self.us_model = AutoModelForSequenceClassification.from_pretrained(
                us_model_name,
                num_labels=len(self.us_clause_types)
            )
            self.us_model.to(self.device)
            
            # Indian Legal BERT
            logger.info("Loading Indian Legal BERT model...")
            self.indian_tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
            self.indian_model = AutoModelForSequenceClassification.from_pretrained(
                "law-ai/InLegalBERT",
                num_labels=len(self.indian_clause_types)
            )
            self.indian_model.to(self.device)
            
            logger.info("Models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            # Fallback to simpler models if specialized ones aren't available
            self._load_fallback_models()
    
    def _load_fallback_models(self):
        """Load fallback models if contract-specific ones aren't available"""
        logger.info("Loading fallback models...")
        model_name = "distilbert-base-uncased"
        
        self.us_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.us_model = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=len(self.us_clause_types)
        )
        
        self.indian_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.indian_model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(self.indian_clause_types)
        )
        
        self.us_model.to(self.device)
        self.indian_model.to(self.device)
    
    def classify_clause(self, text: str, jurisdiction: str = "both") -> Dict:
        """Classify a single clause"""
        results = {}
        
        if jurisdiction in ["us", "both"]:
            results["us"] = self._classify_with_model(
                text, self.us_model, self.us_tokenizer, self.us_clause_types
            )
        
        if jurisdiction in ["indian", "both"]:
            results["indian"] = self._classify_with_model(
                text, self.indian_model, self.indian_tokenizer, self.indian_clause_types
            )
        
        return results
    
    def _classify_with_model(self, text: str, model, tokenizer, clause_types: List[str]) -> Dict:
        """Internal classification with specific model"""
        try:
            # Tokenize input
            inputs = tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                padding=True, 
                max_length=512
            ).to(self.device)
            
            # Get model predictions
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get top prediction
            predicted_class_id = predictions.argmax().item()
            confidence = predictions[0][predicted_class_id].item()
            
            # Determine risk level based on clause type and confidence
            clause_type = clause_types[predicted_class_id]
            risk_level = self._determine_risk_level(clause_type, confidence)
            
            return {
                "clause_type": clause_type,
                "confidence": round(confidence, 3),
                "risk_level": risk_level,
                "all_scores": {
                    clause_types[i]: round(predictions[0][i].item(), 3) 
                    for i in range(len(clause_types))
                }
            }
            
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {
                "clause_type": "Unknown",
                "confidence": 0.0,
                "risk_level": "medium",
                "error": str(e)
            }
    
    def _determine_risk_level(self, clause_type: str, confidence: float) -> str:
        """Determine risk level based on clause type and confidence"""
        high_risk_clauses = ["Liability", "Indemnification", "Termination", "Governing Law"]
        medium_risk_clauses = ["Payment", "Intellectual Property", "Confidentiality"]
        
        if clause_type in high_risk_clauses:
            return "high" if confidence > 0.7 else "medium"
        elif clause_type in medium_risk_clauses:
            return "medium" if confidence > 0.6 else "low"
        else:
            return "low"
    
    def extract_clauses(self, contract_text: str) -> List[str]:
        """Enhanced clause extraction using multiple splitting strategies"""
        import re
        
        # First try splitting by paragraph breaks
        paragraphs = contract_text.split('\n\n')
        clauses = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip().replace('\n', ' ')
            
            # Skip very short or header-like content
            if (len(paragraph) > 50 and 
                not paragraph.lower().startswith(('whereas', 'this agreement', 'the parties', 'page ', 'exhibit'))) and \
                not re.match(r'^\d+[\.\)]\s*$', paragraph):  # Skip numbered sections without content
                
                # If paragraph is very long, try to split into sentences
                if len(paragraph) > 500:
                    sentences = re.split(r'\.(?=\s+[A-Z])', paragraph)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if len(sentence) > 50:
                            clauses.append(sentence + '.' if not sentence.endswith('.') else sentence)
                else:
                    clauses.append(paragraph)
        
        # If we didn't get enough clauses, fall back to sentence splitting
        if len(clauses) < 5:
            sentences = re.split(r'\.(?=\s+[A-Z])', contract_text)
            clauses = []
            for sentence in sentences:
                sentence = sentence.strip().replace('\n', ' ')
                if (len(sentence) > 50 and 
                    not sentence.lower().startswith(('whereas', 'this agreement', 'the parties'))):
                    clauses.append(sentence + '.' if not sentence.endswith('.') else sentence)
        
        return clauses
    
    def analyze_contract(self, contract_text: str, jurisdiction: str = "both") -> Dict:
        """Full contract analysis"""
        if not self.us_model or not self.indian_model:
            self.load_models()
        
        # Extract clauses
        clauses = self.extract_clauses(contract_text)
        
        # Analyze each clause
        clause_analyses = []
        for i, clause in enumerate(clauses):
            analysis = self.classify_clause(clause, jurisdiction)
            analysis["clause_id"] = i + 1
            analysis["text"] = clause[:200] + "..." if len(clause) > 200 else clause
            clause_analyses.append(analysis)
        
        # Generate summary statistics
        summary = self._generate_summary(clause_analyses, jurisdiction)
        
        return {
            "total_clauses": len(clauses),
            "clause_analyses": clause_analyses,
            "summary": summary
        }
    
    def _generate_summary(self, clause_analyses: List[Dict], jurisdiction: str) -> Dict:
        """Generate analysis summary"""
        summary = {}
        
        jurisdictions = ["us", "indian"] if jurisdiction == "both" else [jurisdiction]
        
        for juris in jurisdictions:
            if any(juris in analysis for analysis in clause_analyses):
                risk_counts = {"high": 0, "medium": 0, "low": 0}
                clause_type_counts = {}
                
                for analysis in clause_analyses:
                    if juris in analysis:
                        risk_level = analysis[juris]["risk_level"]
                        clause_type = analysis[juris]["clause_type"]
                        
                        risk_counts[risk_level] += 1
                        clause_type_counts[clause_type] = clause_type_counts.get(clause_type, 0) + 1
                
                summary[juris] = {
                    "risk_distribution": risk_counts,
                    "clause_types": clause_type_counts,
                    "overall_risk": self._calculate_overall_risk(risk_counts)
                }
        
        return summary
    
    def _calculate_overall_risk(self, risk_counts: Dict[str, int]) -> str:
        """Calculate overall contract risk"""
        total = sum(risk_counts.values())
        if total == 0:
            return "low"
        
        high_ratio = risk_counts["high"] / total
        medium_ratio = risk_counts["medium"] / total
        
        if high_ratio > 0.3:
            return "high"
        elif high_ratio > 0.1 or medium_ratio > 0.5:
            return "medium"
        else:
            return "low"