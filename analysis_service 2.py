import openai
import os
from typing import Dict, List
import logging
from dotenv import load_dotenv
import PyPDF2
import docx
import io

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractAnalysisService:
    """Service for contract analysis and risk assessment"""
    
    def __init__(self):
        # Initialize OpenAI client
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        
        if not openai.api_key:
            logger.warning("OpenAI API key not found. GPT analysis will be disabled.")
    
    def extract_text_from_file(self, uploaded_file) -> str:
        """Extract text from uploaded file (PDF, DOCX, or TXT)"""
        try:
            file_type = uploaded_file.type
            
            if file_type == "application/pdf":
                return self._extract_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self._extract_from_docx(uploaded_file)
            elif file_type == "text/plain":
                return str(uploaded_file.read(), "utf-8")
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Error extracting text from file: {e}")
            raise
    
    def _extract_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def generate_risk_assessment(self, clause_analyses: List[Dict], jurisdiction: str) -> Dict:
        """Generate detailed risk assessment using GPT-4"""
        if not openai.api_key:
            return self._generate_simple_risk_assessment(clause_analyses, jurisdiction)
        
        try:
            # Prepare clause summary for GPT
            clause_summary = self._prepare_clause_summary(clause_analyses, jurisdiction)
            
            prompt = self._create_risk_assessment_prompt(clause_summary, jurisdiction)
            
            response = openai.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are an expert legal analyst specializing in contract risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            risk_assessment = response.choices[0].message.content
            
            return {
                "detailed_assessment": risk_assessment,
                "generated_by": "GPT-4",
                "jurisdiction": jurisdiction
            }
            
        except Exception as e:
            logger.error(f"Error generating GPT risk assessment: {e}")
            return self._generate_simple_risk_assessment(clause_analyses, jurisdiction)
    
    def _prepare_clause_summary(self, clause_analyses: List[Dict], jurisdiction: str) -> str:
        """Prepare a summary of clause analyses for GPT"""
        summary_lines = []
        
        for analysis in clause_analyses:
            if jurisdiction in analysis:
                clause_data = analysis[jurisdiction]
                summary_lines.append(
                    f"Clause {analysis['clause_id']}: {clause_data['clause_type']} "
                    f"(Risk: {clause_data['risk_level']}, Confidence: {clause_data['confidence']})"
                )
        
        return "\n".join(summary_lines)
    
    def _create_risk_assessment_prompt(self, clause_summary: str, jurisdiction: str) -> str:
        """Create prompt for GPT risk assessment"""
        jurisdiction_context = {
            "us": "US federal and state contract law, including UCC provisions",
            "indian": "Indian Contract Act 1872 and relevant commercial law"
        }
        
        context = jurisdiction_context.get(jurisdiction, "general contract law")
        
        return f"""
        Analyze the following contract clauses under {context}:

        {clause_summary}

        Provide a comprehensive risk assessment including:
        1. Overall risk level (High/Medium/Low) and justification
        2. Top 3 risk factors and mitigation strategies
        3. Key clauses that need attention
        4. Recommendations for contract improvement
        5. Potential legal issues specific to {jurisdiction.upper()} jurisdiction

        Keep the assessment concise but thorough, focusing on actionable insights.
        """
    
    def _generate_simple_risk_assessment(self, clause_analyses: List[Dict], jurisdiction: str) -> Dict:
        """Generate simple risk assessment without GPT"""
        risk_counts = {"high": 0, "medium": 0, "low": 0}
        high_risk_clauses = []
        
        for analysis in clause_analyses:
            if jurisdiction in analysis:
                risk_level = analysis[jurisdiction]["risk_level"]
                risk_counts[risk_level] += 1
                
                if risk_level == "high":
                    high_risk_clauses.append({
                        "clause_id": analysis["clause_id"],
                        "type": analysis[jurisdiction]["clause_type"],
                        "text": analysis["text"][:100] + "..."
                    })
        
        total_clauses = sum(risk_counts.values())
        overall_risk = "low"
        
        if risk_counts["high"] > total_clauses * 0.3:
            overall_risk = "high"
        elif risk_counts["high"] > 0 or risk_counts["medium"] > total_clauses * 0.5:
            overall_risk = "medium"
        
        assessment = f"""
        Risk Assessment Summary for {jurisdiction.upper()} jurisdiction:
        
        Overall Risk Level: {overall_risk.upper()}
        
        Risk Distribution:
        - High Risk: {risk_counts['high']} clauses
        - Medium Risk: {risk_counts['medium']} clauses  
        - Low Risk: {risk_counts['low']} clauses
        
        High Risk Clauses Requiring Attention:
        """
        
        for clause in high_risk_clauses[:3]:  # Top 3 high-risk clauses
            assessment += f"\n- Clause {clause['clause_id']} ({clause['type']}): {clause['text']}"
        
        return {
            "detailed_assessment": assessment,
            "generated_by": "Rule-based analysis",
            "jurisdiction": jurisdiction
        }
    
    def compare_jurisdictions(self, us_analysis: Dict, indian_analysis: Dict) -> Dict:
        """Compare contract analysis between US and Indian jurisdictions"""
        if not openai.api_key:
            return self._generate_simple_comparison(us_analysis, indian_analysis)
        
        try:
            comparison_prompt = self._create_comparison_prompt(us_analysis, indian_analysis)
            
            response = openai.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are an expert in comparative contract law between US and Indian jurisdictions."},
                    {"role": "user", "content": comparison_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            comparison = response.choices[0].message.content
            
            return {
                "detailed_comparison": comparison,
                "generated_by": "GPT-4"
            }
            
        except Exception as e:
            logger.error(f"Error generating jurisdiction comparison: {e}")
            return self._generate_simple_comparison(us_analysis, indian_analysis)
    
    def _create_comparison_prompt(self, us_analysis: Dict, indian_analysis: Dict) -> str:
        """Create prompt for jurisdiction comparison"""
        return f"""
        Compare this contract analysis between US and Indian jurisdictions:
        
        US Analysis Summary:
        - Overall Risk: {us_analysis.get('overall_risk', 'Unknown')}
        - Risk Distribution: {us_analysis.get('risk_distribution', {})}
        - Key Clause Types: {list(us_analysis.get('clause_types', {}).keys())[:5]}
        
        Indian Analysis Summary:
        - Overall Risk: {indian_analysis.get('overall_risk', 'Unknown')}
        - Risk Distribution: {indian_analysis.get('risk_distribution', {})}
        - Key Clause Types: {list(indian_analysis.get('clause_types', {}).keys())[:5]}
        
        Provide a comparative analysis including:
        1. Key differences in risk assessment between jurisdictions
        2. Jurisdiction-specific legal considerations
        3. Clauses that may need modification for each jurisdiction
        4. Recommendations for cross-border contract optimization
        5. Potential conflicts or issues when operating across both jurisdictions
        """
    
    def _generate_simple_comparison(self, us_analysis: Dict, indian_analysis: Dict) -> Dict:
        """Generate simple comparison without GPT"""
        us_risk = us_analysis.get('overall_risk', 'unknown')
        indian_risk = indian_analysis.get('overall_risk', 'unknown')
        
        comparison = f"""
        Jurisdiction Comparison Summary:
        
        Risk Level Comparison:
        - US Jurisdiction: {us_risk.upper()} risk
        - Indian Jurisdiction: {indian_risk.upper()} risk
        
        Key Observations:
        """
        
        if us_risk != indian_risk:
            comparison += f"\n- Risk levels differ: US shows {us_risk} risk while Indian shows {indian_risk} risk"
            comparison += "\n- This suggests jurisdiction-specific legal considerations affect risk assessment"
        else:
            comparison += f"\n- Both jurisdictions show similar {us_risk} risk levels"
            comparison += "\n- Contract terms appear relatively consistent across jurisdictions"
        
        us_clauses = set(us_analysis.get('clause_types', {}).keys())
        indian_clauses = set(indian_analysis.get('clause_types', {}).keys())
        
        unique_us = us_clauses - indian_clauses
        unique_indian = indian_clauses - us_clauses
        
        if unique_us:
            comparison += f"\n- US-specific considerations: {', '.join(list(unique_us)[:3])}"
        
        if unique_indian:
            comparison += f"\n- Indian-specific considerations: {', '.join(list(unique_indian)[:3])}"
        
        return {
            "detailed_comparison": comparison,
            "generated_by": "Rule-based comparison"
        }