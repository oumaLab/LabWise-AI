import streamlit as st
import sys
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LabWise AI - Medical Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMPORTS ---
# Ensure we can import from the root directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.abnormality_agent import AbnormalityAgent
    from agents.retriever_agent import RetrieverAgent
    from agents.explanation_agent import ExplanationAgent
    from agents.report_agent import ReportAgent
except ImportError as e:
    st.error(f"Error importing agents: {e}. Please ensure 'agents' directory exists and contains valid modules.")
    st.stop()

# --- CSS STYLING ---
st.markdown("""
<style>
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 2.5rem;
        color: #0E1117;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #f0f2f6;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .status-High { background-color: #ffcccc; color: #990000; }
    .status-Low { background-color: #fff4cc; color: #996600; }
    .status-Normal { background-color: #ccffcc; color: #006600; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">🧬 LabWise AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Agentic RAG System for Medical Landscape Awareness</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    st.info(
        "**LabWise AI** is an academic prototype designed to explain laboratory results "
        "to patients in simplified **Moroccan Darija / Arabic**."
    )
    
    st.warning("⚠️ **DISCLAIMER:** This tool is for educational purposes only. It is NOT a diagnostic tool. Consult a doctor.")
    
    st.markdown("---")
    st.markdown("#### Architecture")
    st.markdown("- **Agents:** Multi-agent Logic")
    st.markdown("- **RAG:** Local Medical Context")
    st.markdown("- **Language:** Darija + Medical Arabic")

# --- INITIALIZATION ---
@st.cache_resource
def load_agents():
    """Initializes and caches the agents to prevent reloading on every interaction."""
    return {
        "abnormality": AbnormalityAgent(),
        "retriever": RetrieverAgent(knowledge_base_path="data/medical_context.txt"),
        "explanation": ExplanationAgent(),
        "report": ReportAgent()
    }

try:
    agents = load_agents()
except Exception as e:
    st.error(f"Failed to initialize agents: {e}")
    st.stop()

# --- MAIN INTERFACE ---
col_input, col_results = st.columns([1, 2], gap="large")

with col_input:
    st.markdown("### 📝 Patient Data")
    st.markdown("Enter the values from your CBC laboratory report.")
    
    with st.container(border=True):
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        st.markdown("---")
        hb = st.number_input("Hemoglobin (Hb) [g/dL]", min_value=0.0, max_value=25.0, value=14.0, step=0.1, help="Oxygen-carrying protein.")
        wbc = st.number_input("WBC (Leukocytes) [/mcL]", min_value=0, max_value=50000, value=6000, step=100, help="White Blood Cells count.")
        platelets = st.number_input("Platelets [/mcL]", min_value=0, max_value=1000000, value=250000, step=1000, help="Clotting cells.")

    btn_analyze = st.button("🔍 Analyze Results", type="primary", use_container_width=True)

with col_results:
    if btn_analyze:
        with st.spinner("🤖 LabWise Agents are analyzing..."):
            try:
                # 1. Abnormality Agent
                analysis = agents["abnormality"].analyze(gender, hb, wbc, platelets)
                
                # 2. Retriever Agent
                # Filter only abnormal keys for retrieval
                abnormal_keys = [k for k, v in analysis.items() if v["status"] != "Normal"]
                if abnormal_keys:
                    context = agents["retriever"].retrieve(abnormal_keys)
                else:
                    context = "Resultat kolchi normal. Hamdollah."

                # 3. Explanation Agent
                explanation = agents["explanation"].explain(analysis)

                # 4. Report Agent
                inputs = {"hb": hb, "wbc": wbc, "platelets": platelets}
                final_report = agents["report"].generate_report(gender, inputs, analysis, explanation, context)

                # --- DISPLAY ---
                st.balloons()
                
                # Summary Tabs
                tab_analysis, tab_explanation, tab_report = st.tabs(["📊 Medical Analysis", "💬 Simplified Explanation", "📥 Download Report"])

                with tab_analysis:
                    st.success("Analysis Complete")
                    for param, result in analysis.items():
                        status = result['status']
                        severity = result['severity']
                        color_class = f"status-{status}"
                        
                        st.markdown(f"""
                        <div class="card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h4 style="margin:0;">{param.upper()}</h4>
                                <span class="status-badge {color_class}">{status}</span>
                            </div>
                            <p style="margin-top:10px; color:#555;"><i>Clinical Indication: {severity}</i></p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_explanation:
                    st.info("💡 **Explanation in Darija / Arabic**")
                    st.markdown(f"<div style='background-color:#f0f8ff; padding:15px; border-radius:10px; border-left: 5px solid #3498db;'>{explanation}</div>", unsafe_allow_html=True)
                    
                    with st.expander("📚 Show Medical Reference Context (RAG)"):
                        st.markdown(context)

                with tab_report:
                    st.markdown("### Generated Report")
                    st.text_area("Report Preview", final_report, height=350)
                    st.download_button(
                        label="📄 Download Report as Text",
                        data=final_report,
                        file_name=f"LabWise_Report_{gender}_{hb}_{wbc}.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    
    else:
        st.markdown(
            """
            <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; text-align: center; color: #6c757d;">
                <h3>👋 Welcome!</h3>
                <p>Please enter your data on the left to start the analysis.</p>
                <p style="font-size: 0.8rem;"><i>LabWise AI ensures your data is processed locally within the session.</i></p>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #bdc3c7; font-size: 0.8rem;">
        LabWise AI v1.0 | Academic Prototype | Streamlit Cloud Ready <br>
        Developed for Health Awareness
    </div>
    """,
    unsafe_allow_html=True
)
