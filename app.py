"""Contract Analysis Platform - Main Streamlit Application

Open-source legal contract analysis system supporting multiple jurisdictions.
Contributors can easily add new countries and trained models.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import traceback
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.set_page_config(
    page_title="International Contract Analysis",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from contract_models import ContractBERTAnalyzer
    from analysis_service import ContractAnalysisService
    
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = ContractBERTAnalyzer()
        st.session_state.service = ContractAnalysisService()
        st.session_state.analysis_results = None
        st.session_state.models_loaded = False
        
except Exception as e:
    st.error(f"Error importing modules: {str(e)}")
    st.stop()

# FUNC: Main application entry point
def main():
    st.title("⚖️ International Contract Analysis Platform")
    st.markdown("### Open-source legal analysis for multiple jurisdictions")
    
    with st.sidebar:
        st.header("Configuration")
        
        jurisdiction = st.selectbox(
            "Select Jurisdiction(s)",
            ["both", "us", "indian"],
            format_func=lambda x: {
                "both": "🇺🇸🇮🇳 Both US & Indian",
                "us": "🇺🇸 US Only", 
                "indian": "🇮🇳 Indian Only"
            }[x]
        )
        
        st.subheader("Analysis Options")
        include_risk_assessment = st.checkbox("Include Risk Assessment", value=True)
        include_comparison = st.checkbox("Include Jurisdiction Comparison", value=True)
        
        st.subheader("Model Status")
        
        if hasattr(st.session_state, 'models_loaded') and st.session_state.models_loaded:
            st.success("✅ Models loaded")
        else:
            st.warning("⚠️ Models not loaded")
        
        if st.button("Load Models"):
            try:
                with st.spinner("Loading BERT models..."):
                    st.session_state.analyzer.load_models()
                    st.session_state.models_loaded = True
                st.success("Models loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load models: {str(e)}")
                st.info("The app will still work with fallback models.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Contract Analysis", "📊 Results Dashboard", "🔍 Clause Explorer", "💬 AI Assistant"])
    
    with tab1:
        contract_analysis_tab(jurisdiction, include_risk_assessment, include_comparison)
    
    with tab2:
        results_dashboard_tab()
    
    with tab3:
        clause_explorer_tab()
    
    with tab4:
        chatbot_tab()

# FUNC: Contract upload and analysis interface
def contract_analysis_tab(jurisdiction, include_risk_assessment, include_comparison):
    st.header("Contract Upload & Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload Contract Document",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    st.markdown("**Or paste contract text directly:**")
    contract_text = st.text_area(
        "Contract Text",
        height=200,
        placeholder="Paste your contract text here..."
    )
    
    if st.button("🔍 Analyze Contract", type="primary"):
        if uploaded_file is not None or contract_text.strip():
            analyze_contract(uploaded_file, contract_text, jurisdiction, include_risk_assessment, include_comparison)
        else:
            st.error("Please upload a file or enter contract text.")

# FUNC: Core contract analysis orchestration
# PARAM: uploaded_file - File object or None
# PARAM: contract_text - Raw text input
# PARAM: jurisdiction - Analysis scope (us/indian/both)
def analyze_contract(uploaded_file, contract_text, jurisdiction, include_risk_assessment, include_comparison):
    with st.spinner("Analyzing contract..."):
        try:
            if uploaded_file is not None:
                contract_text = st.session_state.service.extract_text_from_file(uploaded_file)
                st.success(f"✅ Extracted text from {uploaded_file.name}")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Extracting and classifying clauses...")
            progress_bar.progress(25)
            
            analysis_results = st.session_state.analyzer.analyze_contract(contract_text, jurisdiction)
            
            if include_risk_assessment:
                status_text.text("Generating risk assessment...")
                progress_bar.progress(50)
                
                risk_assessments = {}
                jurisdictions = ["us", "indian"] if jurisdiction == "both" else [jurisdiction]
                
                for juris in jurisdictions:
                    if juris in analysis_results["summary"]:
                        risk_assessments[juris] = st.session_state.service.generate_risk_assessment(
                            analysis_results["clause_analyses"], juris
                        )
                
                analysis_results["risk_assessments"] = risk_assessments
            
            if include_comparison and jurisdiction == "both":
                status_text.text("Comparing jurisdictions...")
                progress_bar.progress(75)
                
                us_summary = analysis_results["summary"].get("us", {})
                indian_summary = analysis_results["summary"].get("indian", {})
                
                comparison = st.session_state.service.compare_jurisdictions(us_summary, indian_summary)
                analysis_results["comparison"] = comparison
            
            progress_bar.progress(100)
            status_text.text("Analysis complete!")
            
            st.session_state.analysis_results = analysis_results
            display_analysis_results(analysis_results, jurisdiction)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# FUNC: Display comprehensive analysis results
def display_analysis_results(results, jurisdiction):
    st.success(f"✅ Analysis completed! Found {results['total_clauses']} clauses.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Clauses", results["total_clauses"])
    
    with col2:
        if "us" in results["summary"]:
            us_risk = results["summary"]["us"]["overall_risk"]
            st.metric("US Risk Level", us_risk.upper(), delta=None)
    
    with col3:
        if "indian" in results["summary"]:
            indian_risk = results["summary"]["indian"]["overall_risk"]
            st.metric("Indian Risk Level", indian_risk.upper(), delta=None)
    
    if len(results["summary"]) > 0:
        st.subheader("📊 Risk Distribution")
        display_risk_charts(results["summary"])
    
    st.subheader("📋 Clause Analysis Details")
    display_clause_table(results["clause_analyses"], jurisdiction)
    
    if "risk_assessments" in results:
        st.subheader("⚠️ Risk Assessment")
        display_risk_assessments(results["risk_assessments"])
    
    if "comparison" in results:
        st.subheader("🔍 Jurisdiction Comparison")
        st.text_area(
            "Comparative Analysis",
            results["comparison"]["detailed_comparison"],
            height=300
        )

# FUNC: Render risk distribution pie charts
def display_risk_charts(summary):
    fig = make_subplots(
        rows=1, cols=len(summary),
        specs=[[{"type": "pie"}] * len(summary)],
        subplot_titles=[f"{juris.upper()} Jurisdiction" for juris in summary.keys()]
    )
    
    colors = {"high": "#ff6b6b", "medium": "#ffd93d", "low": "#6bcf7f"}
    
    for i, (juris, data) in enumerate(summary.items()):
        risk_dist = data["risk_distribution"]
        
        fig.add_trace(
            go.Pie(
                labels=list(risk_dist.keys()),
                values=list(risk_dist.values()),
                name=juris.upper(),
                marker_colors=[colors[risk] for risk in risk_dist.keys()],
                showlegend=(i == 0)
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(height=400, title_text="Risk Distribution by Jurisdiction")
    st.plotly_chart(fig, use_container_width=True)

# FUNC: Render clause analysis data table with risk highlighting
def display_clause_table(clause_analyses, jurisdiction):
    table_data = []
    
    for analysis in clause_analyses:
        row = {
            "Clause ID": analysis["clause_id"],
            "Text Preview": analysis["text"][:200] + "..." if len(analysis["text"]) > 200 else analysis["text"]
        }
        
        if jurisdiction == "both":
            if "us" in analysis:
                row.update({
                    "US Type": analysis["us"]["clause_type"],
                    "US Risk": analysis["us"]["risk_level"],
                    "US Confidence": f"{analysis['us']['confidence']:.2f}"
                })
            if "indian" in analysis:
                row.update({
                    "Indian Type": analysis["indian"]["clause_type"],
                    "Indian Risk": analysis["indian"]["risk_level"],
                    "Indian Confidence": f"{analysis['indian']['confidence']:.2f}"
                })
        else:
            if jurisdiction in analysis:
                row.update({
                    "Clause Type": analysis[jurisdiction]["clause_type"],
                    "Risk Level": analysis[jurisdiction]["risk_level"],
                    "Confidence": f"{analysis[jurisdiction]['confidence']:.2f}"
                })
    
        table_data.append(row)
    
    df = pd.DataFrame(table_data)
    
    def highlight_risk(val):
        if isinstance(val, str):
            if "high" in val.lower():
                return "background-color: #ffebee"
            elif "medium" in val.lower():
                return "background-color: #fff8e1"
            elif "low" in val.lower():
                return "background-color: #e8f5e8"
        return ""
    
    styled_df = df.style.map(highlight_risk)
    st.dataframe(styled_df, use_container_width=True)

# FUNC: Display jurisdiction-specific risk assessments
def display_risk_assessments(risk_assessments):
    for juris, assessment in risk_assessments.items():
        with st.expander(f"{juris.upper()} Jurisdiction Risk Assessment"):
            st.markdown(assessment["detailed_assessment"])
            st.caption(f"Generated by: {assessment['generated_by']}")

# FUNC: Results dashboard with charts and metrics
def results_dashboard_tab():
    if st.session_state.analysis_results is None:
        st.info("👆 Please analyze a contract first to see the dashboard.")
        return
    
    results = st.session_state.analysis_results
    
    st.header("📊 Analysis Dashboard")
    
    if "summary" in results:
        for juris, summary in results["summary"].items():
            st.subheader(f"{juris.upper()} Jurisdiction - Clause Types")
            
            clause_types = summary.get("clause_types", {})
            if clause_types:
                df = pd.DataFrame(list(clause_types.items()), columns=["Clause Type", "Count"])
                
                fig = px.bar(
                    df, 
                    x="Clause Type", 
                    y="Count",
                    title=f"Clause Distribution - {juris.upper()}"
                )
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

# FUNC: Individual clause examination interface
def clause_explorer_tab():
    if st.session_state.analysis_results is None:
        st.info("👆 Please analyze a contract first to explore clauses.")
        return
    
    st.header("🔍 Clause Explorer")
    
    results = st.session_state.analysis_results
    clause_analyses = results["clause_analyses"]
    
    clause_options = [f"Clause {analysis['clause_id']}" for analysis in clause_analyses]
    selected_clause = st.selectbox("Select a clause to examine:", clause_options)
    
    if selected_clause:
        clause_id = int(selected_clause.split(" ")[1])
        clause_data = next(
            (analysis for analysis in clause_analyses if analysis["clause_id"] == clause_id),
            None
        )
        
        if clause_data:
            st.subheader(f"Clause {clause_id} Details")
            
            st.text_area("Full Clause Text", clause_data["text"], height=150)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "us" in clause_data:
                    st.markdown("**🇺🇸 US Analysis:**")
                    us_data = clause_data["us"]
                    st.write(f"**Type:** {us_data['clause_type']}")
                    st.write(f"**Risk:** {us_data['risk_level']}")
                    st.write(f"**Confidence:** {us_data['confidence']:.3f}")
            
            with col2:
                if "indian" in clause_data:
                    st.markdown("**🇮🇳 Indian Analysis:**")
                    indian_data = clause_data["indian"]
                    st.write(f"**Type:** {indian_data['clause_type']}")
                    st.write(f"**Risk:** {indian_data['risk_level']}")
                    st.write(f"**Confidence:** {indian_data['confidence']:.3f}")

# FUNC: AI chatbot interface for contract Q&A
def chatbot_tab():
    st.header("🤖 AI Legal Assistant")
    st.markdown("Ask questions about your contract analysis, jurisdiction differences, and legal implications.")
    
    if st.session_state.analysis_results is None:
        st.info("👆 Please analyze a contract first to enable the AI assistant.")
        st.markdown("""
        **What you can ask once a contract is analyzed:**
        - "What are the main risks in this contract?"
        - "How do the US and Indian analyses differ?"
        - "Which clauses need the most attention?"
        - "What are the payment terms and risks?"
        - "Are there any termination clauses I should be concerned about?"
        """)
        return
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
    
    user_question = st.chat_input("Ask me anything about your contract analysis...")
    
    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        with st.chat_message("user"):
            st.write(user_question)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                try:
                    response = st.session_state.service.chat_about_contract(
                        user_question, 
                        st.session_state.analysis_results
                    )
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    with st.sidebar:
        if st.session_state.analysis_results is not None:
            st.markdown("### 💡 Suggested Questions")
            
            suggested_questions = [
                "What are the highest risk clauses?",
                "How do US and Indian analyses differ?",
                "What payment terms should I be aware of?",
                "Are there any concerning termination clauses?",
                "What are the main compliance requirements?",
                "Which jurisdiction is more favorable?",
                "What liability issues should I consider?"
            ]
            
            for question in suggested_questions:
                if st.button(question, key=f"suggest_{hash(question)}"):
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    
                    try:
                        response = st.session_state.service.chat_about_contract(
                            question, 
                            st.session_state.analysis_results
                        )
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        st.rerun()
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                        st.rerun()
            
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()

if __name__ == "__main__":
    main()