import streamlit as st
import os
import sys

# Add the current directory to path so we can import agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.abnormality_agent import AbnormalityAgent
from agents.retriever_agent import RetrieverAgent
from agents.explanation_agent import ExplanationAgent
from agents.report_agent import ReportAgent

# Page Configuration
st.set_page_config(
    page_title="LabWise AI - Medical Awareness",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Academic & Premium" look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .status-high { color: #e74c3c; font-weight: bold; }
    .status-low { color: #e67e22; font-weight: bold; }
    .status-normal { color: #27ae60; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Application Title
st.markdown('<div class="main-header">🧬 LabWise AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Agentic RAG System for Medical Landscape Awareness & Orientation</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/microscope.png", width=100)
    st.title("Settings")
    st.info("This is an academic prototype designed to explain CBC (Complete Blood Count) results to patients in simplified Darija/Arabic.")
    st.warning("⚠️ **DISCLAIMER**: Not a diagnostic tool. Always consult a doctor.")
    
    st.markdown("---")
    st.write("**Architecture:**")
    st.caption("- Multi-Agent System")
    st.caption("- Local RAG (Medical Knowledge)")
    st.caption("- Rule-based + Template Analysis")

# Initialize Agents
@st.cache_resource
def load_agents():
    return {
        "abnormality": AbnormalityAgent(),
        "retriever": RetrieverAgent(),
        "explanation": ExplanationAgent(),
        "report": ReportAgent()
    }

agents = load_agents()

# Main Interface
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📝 Enter Lab Results")
    with st.container():
        gender = st.selectbox("Gender", ["Male", "Female"])
        hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=30.0, value=14.0, step=0.1)
        wbc = st.number_input("WBC (cells/mcL)", min_value=0, max_value=100000, value=6000, step=100)
        platelets = st.number_input("Platelets (/mcL)", min_value=0, max_value=1000000, value=250000, step=1000)
        
        analyze_btn = st.button("🔍 Analyze Results", use_container_width=True, type="primary")

with col2:
    if analyze_btn:
        with st.spinner("Agents are collaborating..."):
            # 1. Abnormality Analysis
            analysis = agents["abnormality"].analyze(gender, hb, wbc, platelets)
            
            # 2. Identify Abnormalities for RAG
            abnormal_keys = [k for k, v in analysis.items() if v["status"] != "Normal"]
            
            # 3. Retrieve Context
            if abnormal_keys:
                query_context = agents["retriever"].retrieve(abnormal_keys)
            else:
                query_context = "Values are within normal ranges. General health advice applies."
            
            # 4. Generate Explanation
            explanation = agents["explanation"].explain(analysis)
            
            # 5. Generate Report
            inputs = {"hb": hb, "wbc": wbc, "platelets": platelets}
            final_report = agents["report"].generate_report(gender, inputs, analysis, explanation, query_context)
            
            # --- Display Results ---
            st.success("Analysis Complete!")
            
            # Tabbed View
            tab1, tab2, tab3 = st.tabs(["📊 Analysis", "💬 Explanation (Darija)", "📄 Full Report"])
            
            with tab1:
                st.subheader("Medical Analysis")
                for param, result in analysis.items():
                    status_class = "status-normal"
                    if result["status"] == "High": status_class = "status-high"
                    if result["status"] == "Low": status_class = "status-low"
                    
                    st.markdown(f"""
                    <div class="card">
                        <b>{param.upper()}</b>: <span class="{status_class}">{result['status']}</span>
                        <br><i>Clinical Note: {result['severity']}</i>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                st.subheader("🤖 AI Explanation")
                st.info(explanation)
                
                st.subheader("📚 Medical Context (RAG)")
                with st.expander("Read Medical References"):
                    st.markdown(query_context)
            
            with tab3:
                st.subheader("Downloadable Report")
                st.text_area("Report Preview", final_report, height=300)
                st.download_button("📥 Download Report", final_report, file_name="labwise_report.txt")

    else:
        st.markdown("""
        ### 👋 Welcome to LabWise AI
        
        Please enter your CBC analysis values on the left to get started.
        
        **How it works:**
        1. **Abnormality Agent** checks your values against WHO standards.
        2. **Retriever Agent** fetches relevant medical data.
        3. **Explanation Agent** translates this into simple Darija for you.
        """)

# Footer / Social Vision
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #95a5a6; font-size: 0.9rem;">
    <b>Social Vision:</b> Helping patients reduce anxiety through understanding. <br>
    <i>University Evaluation Project | 2026</i>
</div>
""", unsafe_allow_html=True)
